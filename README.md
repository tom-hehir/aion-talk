# aion-talk

Beamer presentation of the AION-1 paper:
> *AION-1: Omnimodal Foundation Model for Astronomical Sciences.* [arXiv:2510.17960](https://arxiv.org/abs/2510.17960)

## Talk Abstract

Modern astronomical surveys produce vast, heterogeneous datasets spanning multiband photometric images, spectroscopy, and rich metadata. While machine learning methods have achieved impressive results within individual modalities, most models remain specialised and task-specific, making it difficult to reuse them across surveys and scientific problems. In this talk, I will present AION-1, the first family of large-scale (up to 3.1B parameters) multimodal foundation models designed for the astronomical sciences.

AION-1 employs modality-specific tokenizers to convert diverse inputs—images, spectra, and scalar properties—into a common representation space, where a transformer learns joint structure across modalities via masked-token modeling. We pretrain on over 200 million stars, galaxies, and quasars from five major surveys: Legacy Survey, HSC, SDSS, DESI, and Gaia, homogenising the treatment of observations with unique instrument signatures.

AION-1 achieves state-of-the-art performance across a broad suite of downstream tasks, including physical property estimation, morphology classification, similarity search, image segmentation, and spectral super-resolution, with minimal task-specific finetuning. I will discuss its effectiveness in low-data regimes and its capacity to learn survey-agnostic universal representations. As a fully open-source framework, AION-1 provides a scalable blueprint for building multimodal foundation models capable of integrating heterogeneous observations across the physical sciences. All code, data, and weights are publicly available.

## Repository layout

```text
aion-talk/
├── presentation/
│   ├── presentation.tex        # LaTeX source
│   └── build/                  # gitignored — transient build artefacts (make + IDE)
├── notes/                      # planning — outline and ideas in markdown
├── scripts/
│   ├── fetch-arxiv-paper.sh    # download arXiv PDF + source, write info.md
│   └── fetch-url.sh            # download an arbitrary resource from a URL
├── resources/                  # gitignored — populate with make fetch before building
│   ├── aion-1-paper/           # AION-1 paper (required for build)
│   │   ├── paper.pdf
│   │   ├── info.md             # metadata and BibTeX citation
│   │   └── source/             # extracted arXiv source; figures used in talk
│   └── papers/<arxiv-id>/      # other referenced papers (ad hoc)
├── presentation.pdf            # gitignored during iteration; committed at milestones
└── Makefile
```

## Setup

On a fresh clone:

```sh
uv sync       # create .venv and install Python dependencies
make fetch    # fetch all resources declared in resources.yaml
```

To add resources, edit `resources.yaml` and re-run `make fetch`. Resources can also be fetched ad hoc:

```sh
scripts/fetch-arxiv-paper.sh https://arxiv.org/abs/2501.00001 resources/papers/2501.00001
scripts/fetch-url.sh https://example.com/figure.png resources/images/figure.png
```

## Building

```sh
make          # → presentation/build/presentation.pdf
make clean    # remove aux files
make mrproper # remove presentation/build/ entirely
```

Requires TeX Live 2025 with the `moloch` beamer theme and Fira Sans fonts. Builds with LuaLaTeX via `latexmk`.

### VS Code

A `.vscode/settings.json` is included that configures LaTeX Workshop to use LuaLaTeX and output to `presentation/build/`, matching the `make` build.

## Milestone workflow

Snapshot the slides before a talk:

```sh
make release                       # copies presentation/build/presentation.pdf → presentation.pdf
git add -f presentation.pdf
git commit -m "slides: <occasion>"
git tag -a <occasion> -m "<notes>"
```

Optionally snapshot resources at the same time:

```sh
git add -f resources/              # or selectively: git add -f resources/aion-1-paper/
```

Retrieve from a past milestone:

```sh
git show <tag>:presentation.pdf > recovered.pdf
git checkout <tag> -- resources/
```
