#!/usr/bin/env python3
"""Fetch team profile photos declared in presentation/team.yaml.

For each author, the image source is resolved in priority order:
  1. `photo` field (local path or URL) — if set, used directly
  2. `github` field — fetches https://github.com/<handle>.png
  3. Neither set — skipped with a warning

Photos are saved to resources/team-photos/<slug>.png. A sidecar
<slug>.source file records the source used; if it matches the current
config the photo is skipped, otherwise it is re-fetched.
"""

import urllib.request
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
TEAM_YAML = ROOT / "presentation" / "team.yaml"
OUT_DIR = ROOT / "resources" / "team-photos"


def name_to_slug(name: str) -> str:
    return name.lower().replace(" ", "-")


def fetch(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(dest, "wb") as f:
        shutil.copyfileobj(resp, f)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(TEAM_YAML) as f:
        config = yaml.safe_load(f)

    errors = []
    for author in config["authors"]:
        name = author["name"]
        slug = name_to_slug(name)
        dest = OUT_DIR / f"{slug}.png"
        source_file = OUT_DIR / f"{slug}.source"

        photo = author.get("photo") or ""
        github = author.get("github") or ""

        # Determine the current source key (what takes precedence)
        if photo:
            current_source = f"photo:{photo}"
        elif github:
            current_source = f"github:{github}"
        else:
            print(f"  SKIP  {name}: no github handle or photo set", file=sys.stderr)
            errors.append(name)
            continue

        # Skip if cached file exists and was fetched from the same source
        if dest.exists() and source_file.exists():
            if source_file.read_text().strip() == current_source:
                print(f"  skip  {name}")
                continue

        # Fetch or copy
        if photo:
            if photo.startswith("http://") or photo.startswith("https://"):
                print(f"  fetch {name}  (photo URL)")
                fetch(photo, dest)
            else:
                src = ROOT / photo
                if not src.exists():
                    print(f"  ERROR {name}: local photo not found: {src}", file=sys.stderr)
                    errors.append(name)
                    continue
                print(f"  copy  {name}  (local photo)")
                shutil.copy(src, dest)
        else:
            url = f"https://github.com/{github}.png?size=200"
            print(f"  fetch {name}  (github.com/{github})")
            fetch(url, dest)

        source_file.write_text(current_source)

    if errors:
        print(f"\nWarning: {len(errors)} author(s) have no photo source: {', '.join(errors)}", file=sys.stderr)


if __name__ == "__main__":
    main()
