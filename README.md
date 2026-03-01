# aion-talk

Beamer presentation of the AION-1 paper:
> *AION-1: Omnimodal Foundation Model for Astronomical Sciences.* [arXiv:2510.17960](https://arxiv.org/abs/2510.17960)

## Repository layout

```
aion-talk/
├── presentation/       # LaTeX source
│   └── presentation.tex
├── paper/
│   ├── aion-1-paper.pdf
│   └── source/         # arXiv LaTeX source (figures reused in talk)
├── build/              # gitignored — transient build artefacts
├── presentation.pdf    # gitignored during iteration; committed at milestones
└── Makefile
```

## Building

```sh
make          # produces build/presentation.pdf
make clean    # remove aux files
make mrproper # remove entire build/ directory
```

Requires a TeX Live installation with the `moloch` beamer theme and Fira Sans fonts (included in TeX Live 2025). The build uses LuaLaTeX via `latexmk`.

## Milestone workflow

When you want to snapshot the current slides (e.g. before a talk):

```sh
make release                          # copies build/presentation.pdf → presentation.pdf
git add -f presentation.pdf
git commit -m "slides: <occasion>"
git tag -a <occasion> -m "<notes>"    # e.g. git tag -a group-meeting-2026-03 -m "..."
```

To retrieve the PDF from a past milestone:

```sh
git show <tag>:presentation.pdf > recovered.pdf
```
