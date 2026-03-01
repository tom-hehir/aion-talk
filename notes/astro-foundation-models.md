# Astro Foundation Models

Foundation model efforts in astronomy, grouped by approach.
BibTeX keys match `presentation/bibliography/presentation-bibliography.bib`.
To fetch arXiv source for a paper (e.g. to reuse figures), add it to `arxiv-papers-source` in `resources.yaml`.

---

## Supervised Pre-training

### `walmsley2023zoobot` — Zoobot galaxy morphology library
- [JOSS 8:85 (2023)](https://joss.theoj.org/papers/10.21105/joss.05312) — no arXiv
- Open-source adaptable deep learning library for galaxy morphology, designed for transfer learning to new morphology tasks.

### `walmsley2024scalinglaws` — Scaling laws for galaxy images
- [arXiv:2404.02973](https://arxiv.org/abs/2404.02973)
- First systematic study of supervised scaling laws for galaxy images using 840k Galaxy Zoo images.

---

## Contrastive Learning

### `hayat2021selfsupervised` — Contrastive SSL on SDSS photometry
- [arXiv:2012.13083](https://arxiv.org/abs/2012.13083) | [ApJL 911 (2021)](https://iopscience.iop.org/article/10.3847/2041-8213/abf2c7)
- Contrastive self-supervised learning on SDSS multi-band galaxy photometry; outperforms supervised baselines with 2–4× fewer labels.

### `parker2024astroclip` — AstroCLIP cross-modal foundation model
- [arXiv:2310.03024](https://arxiv.org/abs/2310.03024) | [MNRAS 531 (2024)](https://academic.oup.com/mnras/article/531/4/4990/7697182)
- Cross-modal foundation model aligning DESI galaxy images and spectra in a shared latent space via contrastive learning.

### `rizhko2024astromm` — AstroM³ trimodal self-supervised model
- [arXiv:2411.08842](https://arxiv.org/abs/2411.08842) | [AJ (2025)](https://iopscience.iop.org/article/10.3847/1538-3881/adcbad)
- First trimodal CLIP-style self-supervised model in astronomy, jointly embedding time-series photometry, spectra, and metadata.

---

## Generative / Autoregressive

### `smith2024astropt` — AstroPT scaling for galaxy images
- [arXiv:2405.14930](https://arxiv.org/abs/2405.14930) | [ICML 2024](https://icml.cc/virtual/2024/36761)
- Autoregressive transformer pretrained on 8.6M DESI Legacy Survey galaxy images; scaling from 1M to 2.1B parameters.

### `zhang2024maven` — Maven supernova foundation model
- [arXiv:2408.16829](https://arxiv.org/abs/2408.16829) | [NeurIPS 2024](https://neurips.cc/virtual/2024/102928)
- First foundation model for supernova science, pretraining on 500k synthetic light curves and spectra then fine-tuning on ZTF.

### `leung2023stellar` — Transformer foundation model for stars
- [arXiv:2308.10944](https://arxiv.org/abs/2308.10944) | [MNRAS 527 (2023)](https://academic.oup.com/mnras/article/527/1/1494/7291945)
- Self-supervised transformer trained on multi-survey stellar data; performs both discriminative and generative downstream tasks.
