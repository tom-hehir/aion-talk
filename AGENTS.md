# AGENTS.md

Instructions for AI agents working in this repository. See [README.md](README.md) for setup, build, and workflow commands.

## Project

Beamer presentation of the AION-1 paper (arXiv:2510.17960), presented by Tom Hehir at the Institute of Astronomy, University of Cambridge.

## LaTeX conventions

- Edit only `presentation/presentation.tex`
- Theme: `\usetheme{moloch}` — option macro is `\molochset{}` (**not** `\metroset`)
- Valid `progressbar` values: `none`, `head`, `frametitle`, `foot`
- The `numbering` moloch option is deprecated; use `\setbeamertemplate{frame numbering}[fraction]`
- Figures resolved via `\graphicspath{{../resources/aion-1-paper/source/figures/}}`
- Engine is LuaLaTeX — fontspec and Fira Sans are available

## Paper summary (AION-1)

- **Data**: 5 surveys — Legacy Survey, HSC, SDSS, DESI, Gaia (~200M observations of stars, galaxies, quasars)
- **Architecture**: two-stage — modality-specific VQ-VAE tokenisers → shared transformer with masked token modelling
- **Model sizes**: 300M, 700M, 3.1B parameters
- **Downstream tasks**: photo-z, stellar [Fe/H], galaxy morphology (GZ10), similarity retrieval, segmentation (GZ3D), spectral super-resolution
- **Code**: [github.com/PolymathicAI/AION](https://github.com/PolymathicAI/AION/)

## Presentation structure

Motivation → Data → Architecture (Tokenisation, Multimodal Masked Modelling) → Model Family → Downstream Tasks → Conclusion
