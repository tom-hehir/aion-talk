#!/usr/bin/env bash
# fetch-paper.sh — download PDF and LaTeX source for an arXiv paper,
#                  and write an info.md with metadata and citation.
#
# Usage:
#   scripts/fetch-paper.sh <arxiv-id-or-url> <output-dir>
#
# Examples:
#   scripts/fetch-paper.sh 2510.17960 resources/aion-1-paper
#   scripts/fetch-paper.sh https://arxiv.org/abs/2510.17960 resources/papers/2510.17960

set -euo pipefail

INPUT="${1:?Usage: $0 <arxiv-id-or-url> <output-dir>}"
OUT_DIR="${2:?Usage: $0 <arxiv-id-or-url> <output-dir>}"

# Accept either a bare ID ("2510.17960") or a full arXiv URL
ARXIV_ID="${INPUT##*/}"

mkdir -p "$OUT_DIR"

# ── metadata ──────────────────────────────────────────────────────────────────
echo "Fetching metadata for ${ARXIV_ID}..."
API_XML=$(mktemp)
curl -fsSL "https://export.arxiv.org/api/query?id_list=${ARXIV_ID}" > "$API_XML"

python3 - "$API_XML" "$OUT_DIR" "$ARXIV_ID" <<'PYEOF'
import sys
import xml.etree.ElementTree as ET

xml_file, out_dir, arxiv_id = sys.argv[1], sys.argv[2], sys.argv[3]

tree = ET.parse(xml_file)
root = tree.getroot()

ns = {
    'atom':  'http://www.w3.org/2005/Atom',
    'arxiv': 'http://arxiv.org/schemas/atom',
}

entry     = root.find('atom:entry', ns)
title     = ' '.join(entry.find('atom:title', ns).text.split())
published = entry.find('atom:published', ns).text[:10]
authors   = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]
abstract  = ' '.join(entry.find('atom:summary', ns).text.split())
arxiv_url = f"https://arxiv.org/abs/{arxiv_id}"

cat_el    = entry.find('arxiv:primary_category', ns)
primary_class = cat_el.attrib.get('term', '') if cat_el is not None else ''

year           = published[:4]
first_surname  = authors[0].split()[-1].lower() if authors else 'unknown'
bibtex_key     = f"{first_surname}{year}"
author_bibtex  = ' and\n               '.join(authors)

info = f"""\
# {title}

- **arXiv**: {arxiv_url}
- **Published**: {published}
- **Authors**: {', '.join(authors)}

## Abstract

{abstract}

## Citation

```bibtex
@misc{{{bibtex_key},
  title         = {{{{{title}}}}},
  author        = {{{author_bibtex}}},
  year          = {{{year}}},
  eprint        = {{{arxiv_id}}},
  archivePrefix = {{arXiv}},
  primaryClass  = {{{primary_class}}},
  url           = {{{arxiv_url}}},
}}
```
"""

with open(f"{out_dir}/info.md", "w") as f:
    f.write(info)

print(f"  title:   {title}")
print(f"  authors: {', '.join(authors[:3])}{'...' if len(authors) > 3 else ''}")
print(f"  date:    {published}")
PYEOF

rm "$API_XML"

# ── PDF ───────────────────────────────────────────────────────────────────────
echo "Fetching PDF for ${ARXIV_ID}..."
curl -fL "https://arxiv.org/pdf/${ARXIV_ID}" -o "${OUT_DIR}/paper.pdf"

# ── Source ────────────────────────────────────────────────────────────────────
echo "Fetching source for ${ARXIV_ID}..."
ARCHIVE="${OUT_DIR}/_source_archive"
curl -fL "https://arxiv.org/e-print/${ARXIV_ID}" -o "$ARCHIVE"

echo "Extracting source..."
mkdir -p "${OUT_DIR}/source"

# arXiv serves either a .tar.gz (most papers) or a gzipped single .tex file
if tar -xzf "$ARCHIVE" -C "${OUT_DIR}/source" 2>/dev/null; then
    :
elif tar -xf "$ARCHIVE" -C "${OUT_DIR}/source" 2>/dev/null; then
    :
else
    gunzip -c "$ARCHIVE" > "${OUT_DIR}/source/main.tex"
fi

rm "$ARCHIVE"
echo "Done → ${OUT_DIR}"
