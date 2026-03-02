# CLAUDE.md

See [AGENTS.md](AGENTS.md) for project context and [README.md](README.md) for workflows.

## Gotchas

- Moloch option macro is `\molochset{}` — `\metroset` (from predecessor Metropolis) will error
- `git mv` won't work on untracked files — use regular `mv` then `git add`
- **Always add downloaded resources to `resources.yaml`** — both images (`images:` section) and papers (`arxiv-papers-source:` section) — so `make fetch` reproduces them on a fresh clone. Download the file first, then add the entry.
