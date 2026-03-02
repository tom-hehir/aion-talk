#!/usr/bin/env python3
"""Render labeled LaTeX tables from paper sources into cached PDFs.

Usage:
  uv run scripts/render-tables.py
  uv run scripts/render-tables.py --paper aion-1-paper
  uv run scripts/render-tables.py --label tab:model-size
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
DEFAULT_CONFIG = ROOT / "tables.yaml"
DEFAULT_OUT_ROOT = ROOT / "resources" / "rendered" / "tables"

ALLOWED_ENVS = {"table", "table*", "subtable", "subfigure", "wraptable", "longtable", "figure", "figure*"}


def sanitize_label(label: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", label)


def load_config(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing config: {path}")
    with open(path) as f:
        return yaml.safe_load(f) or {}


def find_docclass_and_preamble(lines: list[str]) -> tuple[str, list[str]]:
    docclass_idx = None
    begin_doc_idx = None
    for i, line in enumerate(lines):
        if docclass_idx is None and r"\documentclass" in line:
            docclass_idx = i
        if r"\begin{document}" in line:
            begin_doc_idx = i
            break
    if docclass_idx is None or begin_doc_idx is None:
        raise ValueError("Could not locate \\documentclass or \\begin{document}.")
    docclass_line = lines[docclass_idx]
    preamble_lines = lines[docclass_idx + 1 : begin_doc_idx]
    return docclass_line, preamble_lines


def parse_env_ranges(lines: list[str]) -> list[tuple[str, int, int]]:
    env_stack: list[tuple[str, int]] = []
    ranges: list[tuple[str, int, int]] = []
    pattern = re.compile(r"\\(begin|end)\{([^}]+)\}")

    for i, line in enumerate(lines):
        for match in pattern.finditer(line):
            kind, env = match.group(1), match.group(2)
            if kind == "begin":
                env_stack.append((env, i))
            else:
                if not env_stack:
                    continue
                # Pop the most recent matching env if possible.
                idx = next((j for j in range(len(env_stack) - 1, -1, -1) if env_stack[j][0] == env), None)
                if idx is None:
                    continue
                start_env, start_idx = env_stack.pop(idx)
                if start_env == env:
                    ranges.append((env, start_idx, i))
    return ranges


def select_env_block(lines: list[str], label: str) -> tuple[str, list[str]]:
    label_token = f"\\label{{{label}}}"
    label_idx = next((i for i, line in enumerate(lines) if label_token in line), None)
    if label_idx is None:
        raise ValueError(f"Label not found: {label}")

    ranges = parse_env_ranges(lines)
    candidates = [
        (env, start, end)
        for env, start, end in ranges
        if env in ALLOWED_ENVS and start <= label_idx <= end
    ]
    if not candidates:
        raise ValueError(f"No table-like environment found for label {label}.")

    env, start, end = min(candidates, key=lambda t: t[2] - t[1])
    return env, lines[start : end + 1]


def build_wrapper(docclass_line: str, preamble_lines: list[str], env: str, table_lines: list[str]) -> str:
    has_preview = any("preview" in line and "usepackage" in line for line in preamble_lines)
    preview_lines = []
    if not has_preview:
        preview_lines.append(r"\usepackage[active,tightpage]{preview}")
    preview_lines.extend(
        [
            r"\PreviewEnvironment{table}",
            r"\PreviewEnvironment{table*}",
            r"\PreviewEnvironment{subtable}",
            r"\PreviewEnvironment{subfigure}",
            r"\PreviewEnvironment{wraptable}",
            r"\PreviewEnvironment{longtable}",
            r"\PreviewEnvironment{figure}",
            r"\PreviewEnvironment{figure*}",
        ]
    )

    body_lines = table_lines
    if env in {"table", "table*", "wraptable"}:
        begin_token = f"\\begin{{{env}}}"
        end_token = f"\\end{{{env}}}"
        stripped = [line for line in table_lines if begin_token not in line and end_token not in line]
        stripped = [line.replace("\\caption{", "\\captionof{table}{") for line in stripped]
        body_lines = [r"\begin{preview}", *stripped, r"\end{preview}"]
    elif env in {"subtable", "subfigure"}:
        begin_token = f"\\begin{{{env}}}"
        end_token = f"\\end{{{env}}}"
        stripped = [line for line in table_lines if begin_token not in line and end_token not in line]
        body_lines = [r"\begin{preview}", *stripped, r"\end{preview}"]
    elif env in {"figure", "figure*"}:
        begin_token = f"\\begin{{{env}}}"
        end_token = f"\\end{{{env}}}"
        stripped = [line for line in table_lines if begin_token not in line and end_token not in line]
        # \caption requires a float wrapper; use \captionof{figure} since we stripped it
        stripped = [line.replace("\\caption{", "\\captionof{figure}{") for line in stripped]
        # Replace sub-float environments with minipage so subcaption doesn't complain
        # about being outside a float
        processed = []
        for line in stripped:
            line = re.sub(r"\\begin\{subfigure\}(\[[^\]]*\])?\{([^}]*)\}", r"\\begin{minipage}{\2}", line)
            line = re.sub(r"\\end\{subfigure\}", r"\\end{minipage}", line)
            line = re.sub(r"\\begin\{subtable\}(\[[^\]]*\])?\{([^}]*)\}", r"\\begin{minipage}{\2}", line)
            line = re.sub(r"\\end\{subtable\}", r"\\end{minipage}", line)
            processed.append(line)
        body_lines = [r"\begin{preview}", *processed, r"\end{preview}"]

    wrapper_lines = [
        "% auto-generated by scripts/render-tables.py",
        docclass_line,
        *preamble_lines,
        *preview_lines,
        r"\begin{document}",
        *body_lines,
        r"\bibliographystyle{plainnat}",
        r"\bibliography{mmoma.bib}",
        r"\end{document}",
    ]
    return "\n".join(wrapper_lines) + "\n"


def compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def render_table(source: Path, label: str, out_dir: Path) -> None:
    lines = source.read_text().splitlines()
    docclass_line, preamble_lines = find_docclass_and_preamble(lines)
    env, table_lines = select_env_block(lines, label)
    wrapper = build_wrapper(docclass_line, preamble_lines, env, table_lines)

    safe_label = sanitize_label(label)
    out_dir.mkdir(parents=True, exist_ok=True)
    tex_path = out_dir / f"{safe_label}.tex"
    pdf_path = out_dir / f"{safe_label}.pdf"
    hash_path = out_dir / f"{safe_label}.sha256"

    new_hash = compute_hash(wrapper)
    if pdf_path.exists() and hash_path.exists():
        if hash_path.read_text().strip() == new_hash:
            print(f"  skip  {label} (cached)")
            return

    tex_path.write_text(wrapper)

    env = os.environ.copy()
    paper_dir = str(source.parent)
    tex_paths = f"{paper_dir}:{paper_dir}/assets:"
    env["TEXINPUTS"] = tex_paths + env.get("TEXINPUTS", "")
    env["TEXFONTS"] = tex_paths + env.get("TEXFONTS", "")
    env["TTFONTS"] = tex_paths + env.get("TTFONTS", "")
    env["OPENTYPEFONTS"] = tex_paths + env.get("OPENTYPEFONTS", "")
    env["BIBINPUTS"] = paper_dir + ":" + env.get("BIBINPUTS", "")

    def run_pdflatex() -> None:
        cmd = [
            "pdflatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-output-directory",
            str(out_dir),
            str(tex_path),
        ]
        result = subprocess.run(cmd, cwd=out_dir, env=env)
        if result.returncode != 0:
            raise RuntimeError(f"pdflatex failed for {label}")

    run_pdflatex()

    # Run bibtex to resolve \cite{} commands, then recompile.
    aux_path = out_dir / f"{safe_label}.aux"
    if aux_path.exists() and r"\bibdata" in aux_path.read_text():
        subprocess.run(["bibtex", safe_label], cwd=out_dir, env=env)
        run_pdflatex()
        run_pdflatex()

    if not pdf_path.exists():
        raise RuntimeError(f"Expected PDF not produced: {pdf_path}")

    hash_path.write_text(new_hash)
    print(f"  render {label} → {pdf_path.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--paper", action="append", default=[])
    parser.add_argument("--label", action="append", default=[])
    args = parser.parse_args()

    config = load_config(args.config)
    papers = config.get("papers") or {}
    if not papers:
        print("No papers configured in tables.yaml.")
        return

    for paper_key, spec in papers.items():
        if args.paper and paper_key not in args.paper:
            continue
        source = ROOT / spec["source"]
        labels = spec.get("labels") or []
        if args.label:
            labels = [lbl for lbl in labels if lbl in args.label]
        if not labels:
            continue
        if not source.exists():
            raise FileNotFoundError(f"Missing source: {source}")

        print(f"Paper: {paper_key}")
        out_dir = DEFAULT_OUT_ROOT / paper_key
        for label in labels:
            render_table(source, label, out_dir)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover - CLI guard
        print(f"ERROR: {exc}")
        sys.exit(1)
