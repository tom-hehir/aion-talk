#!/usr/bin/env bash
# fetch-url.sh — download an arbitrary resource from a URL.
#
# Usage:
#   scripts/fetch-url.sh <url> <output-path>
#
# Example:
#   scripts/fetch-url.sh https://example.com/figure.png resources/images/figure.png

set -euo pipefail

URL="${1:?Usage: $0 <url> <output-path>}"
OUTPUT="${2:?Usage: $0 <url> <output-path>}"

mkdir -p "$(dirname "$OUTPUT")"
curl -fL "$URL" -o "$OUTPUT"
echo "Done → ${OUTPUT}"
