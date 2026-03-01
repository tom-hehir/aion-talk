# Astro Foundation Models

Foundation model efforts in astronomy, grouped by approach.
BibTeX keys match `presentation/bibliography/presentation-bibliography.bib`.
To fetch arXiv source for a paper (e.g. to reuse figures), add it to `arxiv-papers` in `resources.yaml`.

---

## Supervised Pre-training

### `walmsley2023zoobot` — Zoobot galaxy morphology library
- **JOSS** 8:85 (2023) — no arXiv
- Open-source adaptable deep learning library for galaxy morphology, designed for transfer learning to new morphology tasks.

### `walmsley2024scalinglaws` — Scaling laws for galaxy images
- **arXiv:** 2404.02973 (2024)
- First systematic study of supervised scaling laws for galaxy images using 840k Galaxy Zoo images.

---

## Contrastive Learning

### `hayat2021selfsupervised` — Contrastive SSL on SDSS photometry
- **arXiv:** 2012.13083 | **ApJL** 911 (2021)
- Contrastive self-supervised learning on SDSS multi-band galaxy photometry; outperforms supervised baselines with 2–4× fewer labels.

### `parker2024astroclip` — AstroCLIP cross-modal foundation model
- **arXiv:** 2310.03024 | **MNRAS** 531 (2024)
- Cross-modal foundation model aligning DESI galaxy images and spectra in a shared latent space via contrastive learning.

### `rizhko2024astromm` — AstroM³ trimodal self-supervised model
- **arXiv:** 2411.08842 | **AJ** (2025)
- First trimodal CLIP-style self-supervised model in astronomy, jointly embedding time-series photometry, spectra, and metadata.

---

## Generative / Autoregressive

### `smith2024astropt` — AstroPT scaling for galaxy images
- **arXiv:** 2405.14930 | **ICML 2024**
- Autoregressive transformer pretrained on 8.6M DESI Legacy Survey galaxy images; scaling from 1M to 2.1B parameters.

### `zhang2024maven` — Maven supernova foundation model
- **arXiv:** 2408.16829 | **NeurIPS 2024**
- First foundation model for supernova science, pretraining on 500k synthetic light curves and spectra then fine-tuning on ZTF.

### `leung2023stellar` — Transformer foundation model for stars
- **arXiv:** 2308.10944 | **MNRAS** 527 (2023)
- Self-supervised transformer trained on multi-survey stellar data; performs both discriminative and generative downstream tasks.
