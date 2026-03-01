#!/usr/bin/env python3
"""Fetch all resources declared in resources.yaml."""

import subprocess
import sys
from pathlib import Path

import yaml
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

ROOT = Path(__file__).parent.parent
RESOURCES_DIR = ROOT / "resources"
PAPERS_DIR = RESOURCES_DIR / "papers"


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main() -> None:
    with open(ROOT / "resources.yaml") as f:
        config = yaml.safe_load(f)

    # ── arXiv papers (source always fetched) ──────────────────────────────────
    for identifier, url in (config.get("arxiv-papers") or {}).items():
        out_dir = PAPERS_DIR / identifier
        if (out_dir / "source").exists():
            print(f"  skip  {identifier} (already fetched)")
            continue
        print(f"  fetch {identifier}")
        run(["scripts/fetch-arxiv-paper.sh", url, f"resources/papers/{identifier}"])

    # ── arXiv papers with source (opt-in) ─────────────────────────────────────
    for identifier, url in (config.get("arxiv-papers-source") or {}).items():
        out_dir = PAPERS_DIR / identifier
        if (out_dir / "source").exists():
            print(f"  skip  {identifier} (already fetched)")
            continue
        print(f"  fetch {identifier}")
        run(["scripts/fetch-arxiv-paper.sh", url, f"resources/papers/{identifier}"])

    # ── images ────────────────────────────────────────────────────────────────
    for identifier, url in (config.get("images") or {}).items():
        out_path = RESOURCES_DIR / "images" / identifier
        if out_path.exists():
            print(f"  skip  {identifier} (already fetched)")
            continue
        print(f"  fetch {identifier}")
        run(["scripts/fetch-url.sh", url, f"resources/images/{identifier}"])
        if out_path.suffix == ".svg":
            pdf_path = out_path.with_suffix(".pdf")
            drawing = svg2rlg(str(out_path))
            renderPDF.drawToFile(drawing, str(pdf_path))
            print(f"  conv  {identifier} → {pdf_path.name}")


if __name__ == "__main__":
    main()
