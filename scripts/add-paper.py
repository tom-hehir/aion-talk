#!/usr/bin/env python3
"""Add a paper entry to a notes YAML file from an arXiv URL/ID.

Usage:
    uv run scripts/add-paper.py <arxiv-url-or-id> [journal-url]

Fetches arXiv metadata, proposes a key, then appends the entry to a
chosen YAML file.  Add journal / description fields manually afterwards.
"""

import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).parent.parent
NOTES_DIR = ROOT / "notes"

ARXIV_API_URL = "https://export.arxiv.org/api/query?id_list={}"
ARXIV_NS = "http://www.w3.org/2005/Atom"

TITLE_STOPWORDS = {
    "a", "an", "the", "of", "for", "in", "on", "at", "to", "and", "or",
    "with", "via", "from", "using", "based", "towards", "toward",
    "deep", "neural", "network", "networks", "learning", "model", "models",
    "data", "large", "new", "fast", "self",
}


def parse_arxiv_id(s: str) -> str:
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([^\s/?#]+)", s, re.IGNORECASE)
    return m.group(1) if m else s.strip()


def fetch_arxiv_metadata(arxiv_id: str) -> dict:
    url = ARXIV_API_URL.format(arxiv_id)
    req = urllib.request.Request(url, headers={"User-Agent": "aion-talk-addpaper/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        xml_bytes = resp.read()

    root = ET.fromstring(xml_bytes)
    ns = {"a": ARXIV_NS}
    entry = root.find("a:entry", ns)
    if entry is None:
        raise ValueError(f"No arXiv entry found for id={arxiv_id!r}")

    title = re.sub(r"\s+", " ", entry.find("a:title", ns).text.strip())
    authors = [el.find("a:name", ns).text.strip() for el in entry.findall("a:author", ns)]
    year = entry.find("a:published", ns).text[:4]

    return {"title": title, "authors": authors, "year": year}


def suggest_key(meta: dict) -> str:
    last_name = re.sub(r"[^a-z]", "", meta["authors"][0].split()[-1].lower())
    words = re.findall(r"[a-z]{4,}", meta["title"].lower())
    keyword = next((w for w in words if w not in TITLE_STOPWORDS), words[0] if words else "paper")
    return f"{last_name}{meta['year']}{keyword}"


def prompt(question: str, default: str = "") -> str:
    display = f" [{default}]" if default else ""
    answer = input(f"{question}{display}: ").strip()
    return answer if answer else default


def prompt_choice(heading: str, options: list[str]) -> str:
    print(f"\n{heading}")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        raw = input("> ").strip()
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except ValueError:
            pass
        print(f"  Enter a number between 1 and {len(options)}.")


def append_entry(path: Path, entry: dict) -> None:
    """Append entry as a top-level list item at the end of the file."""
    with open(path) as f:
        content = f.read()

    lines = [""]
    lines.append(f"- key: {entry['key']}")
    lines.append(f"  arxiv: \"{entry['arxiv']}\"")
    if entry.get("journal-url"):
        lines.append(f"  journal-url: {entry['journal-url']}")
    snippet = "\n".join(lines) + "\n"

    with open(path, "w") as f:
        f.write(content.rstrip("\n") + "\n" + snippet)


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in {"-h", "--help"}:
        print(__doc__)
        sys.exit(0 if args else 1)

    arxiv_id = parse_arxiv_id(args[0])
    journal_url = args[1] if len(args) > 1 else None

    print(f"Fetching arXiv:{arxiv_id} …")
    meta = fetch_arxiv_metadata(arxiv_id)

    authors_display = ", ".join(meta["authors"][:3])
    if len(meta["authors"]) > 3:
        authors_display += " et al."
    print(f"\n  Title:   {meta['title']}")
    print(f"  Authors: {authors_display}")
    print(f"  Year:    {meta['year']}")

    key = prompt("\nkey", suggest_key(meta))

    yaml_files = sorted(NOTES_DIR.glob("*.yaml"))
    chosen_name = prompt_choice("Which YAML file?", [f.name for f in yaml_files])
    chosen_path = NOTES_DIR / chosen_name

    entry = {"key": key, "arxiv": arxiv_id}
    if journal_url:
        entry["journal-url"] = journal_url

    append_entry(chosen_path, entry)
    print(f"\nAdded '{key}' to {chosen_name}")
    if not journal_url:
        print("  Tip: add journal / journal-url fields manually once published.")


if __name__ == "__main__":
    main()
