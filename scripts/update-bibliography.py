#!/usr/bin/env python3
"""Generate presentation-bibliography.bib from notes/*.yaml paper lists.

For papers with an `arxiv` field, fetches BibTeX from the arXiv API and
renames the key to the one specified in the YAML.  For papers with a
`bibtex` field, uses that verbatim.  Journal metadata in the YAML
(journal, journal-url, doi) is merged into the entry.
"""

import re
import sys
import time
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
NOTES_DIR = ROOT / "notes"
BIB_OUT = ROOT / "presentation" / "bibliography" / "presentation-bibliography.bib"

ARXIV_BIBTEX_URL = "https://arxiv.org/bibtex/{}"


def fetch_arxiv_bibtex(arxiv_id: str) -> str:
    url = ARXIV_BIBTEX_URL.format(arxiv_id)
    req = urllib.request.Request(url, headers={"User-Agent": "aion-talk-bibgen/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode()


def rekey(bibtex: str, new_key: str) -> str:
    """Replace the BibTeX entry key with new_key."""
    return re.sub(r"(@\w+\{)\s*[^,]+,", rf"\g<1>{new_key},", bibtex, count=1)


def inject_journal(bibtex: str, paper: dict) -> str:
    """Upgrade @misc → @article and inject journal/doi fields if provided."""
    journal = paper.get("journal")
    journal_url = paper.get("journal-url")
    doi = paper.get("doi")

    if not journal:
        return bibtex

    # Upgrade entry type
    bibtex = re.sub(r"@misc\{", "@article{", bibtex, flags=re.IGNORECASE)

    # Extract year and volume/pages from "MNRAS 511 (2022)" style strings
    extra_fields = []
    m = re.match(r"(.+?)\s+(\d+)(?:\s*\((\d{4})\))?", journal)
    if m:
        journal_name = m.group(1).strip()
        volume = m.group(2)
        year_from_journal = m.group(3)
        extra_fields.append(f'  journal = {{{journal_name}}},')
        extra_fields.append(f'  volume  = {{{volume}}},')
        if year_from_journal:
            # Replace or confirm year field
            bibtex = re.sub(r"\byear\s*=\s*\{[^}]*\}", f"year    = {{{year_from_journal}}}", bibtex)
    else:
        extra_fields.append(f'  journal = {{{journal}}},')

    if doi:
        extra_fields.append(f'  doi     = {{{doi}}},')
    if journal_url and not doi:
        # Store url if no DOI
        extra_fields.append(f'  url     = {{{journal_url}}},')

    if extra_fields:
        insert = "\n".join(extra_fields) + "\n"
        bibtex = re.sub(r"(eprint\s*=\s*\{[^}]+\},)", r"\1\n" + insert, bibtex)

    return bibtex


def papers_from_yaml(path: Path) -> list[tuple[str, dict]]:
    """Return [(category_name, paper_dict), ...] preserving order."""
    with open(path) as f:
        data = yaml.safe_load(f)
    result = []
    for category, papers in data.items():
        if not isinstance(papers, list):
            continue
        for paper in papers:
            result.append((category, paper))
    return result


def main() -> None:
    yaml_files = sorted(NOTES_DIR.glob("*.yaml"))
    if not yaml_files:
        print("No YAML files found in notes/")
        sys.exit(1)

    all_entries: list[str] = []
    seen_keys: set[str] = set()

    for yaml_file in yaml_files:
        all_entries.append(f"% {'─' * 74}")
        all_entries.append(f"% {yaml_file.stem}")
        all_entries.append(f"% {'─' * 74}\n")

        for category, paper in papers_from_yaml(yaml_file):
            key = paper["key"]
            if key in seen_keys:
                print(f"  skip  {key} (duplicate)")
                continue
            seen_keys.add(key)

            # Use inline bibtex if provided
            if "bibtex" in paper:
                entry = paper["bibtex"].strip()
                entry = rekey(entry, key)
                all_entries.append(entry + "\n")
                print(f"  inline {key}")
                continue

            arxiv_id = paper.get("arxiv")
            if not arxiv_id:
                print(f"  WARN  {key}: no arxiv id and no bibtex field — skipping")
                continue

            print(f"  fetch  {key} (arXiv:{arxiv_id})")
            try:
                bibtex = fetch_arxiv_bibtex(arxiv_id)
                time.sleep(0.5)  # be polite to arXiv
            except Exception as e:
                print(f"  ERROR  {key}: {e}")
                continue

            bibtex = rekey(bibtex, key)
            bibtex = inject_journal(bibtex, paper)
            all_entries.append(bibtex.strip() + "\n")

    BIB_OUT.write_text("\n".join(all_entries) + "\n")
    print(f"\nWrote {len(seen_keys)} entries to {BIB_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
