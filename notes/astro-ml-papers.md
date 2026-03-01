# Astro ML Papers — task-specific models

Papers illustrating the pre-foundation-model paradigm: one model per task/survey.
BibTeX keys match `presentation/bibliography/presentation-bibliography.bib`.
To fetch arXiv source for a paper (e.g. to reuse figures), add it to `arxiv-papers-source` in `resources.yaml`.

---

## Anomaly Detection

### `storeyfisher2021anomaly` — GAN anomaly detection in HSC
- [arXiv:2105.02434](https://arxiv.org/abs/2105.02434) | [MNRAS 508 (2021)](https://academic.oup.com/mnras/article/508/2/2946/6369368)
- Wasserstein GAN pipeline applied to ~1M HSC galaxy images, recovering mergers, tidal features, and rare systems.

---

## Parameter Estimation

### `alsing2020speculator` — SPECULATOR SED emulator
- [arXiv:1911.11778](https://arxiv.org/abs/1911.11778) | [ApJS (2020)](https://iopscience.iop.org/article/10.3847/1538-4365/ab917f)
- PCA + neural network emulator of stellar population synthesis models; 10³–10⁴× speed-up for SED fitting.

### `hahn2023provabgs` — PROVABGS probabilistic SED fitting
- [arXiv:2306.06318](https://arxiv.org/abs/2306.06318) | [ApJ (2024)](https://iopscience.iop.org/article/10.3847/1538-4357/ad19c8)
- Probabilistic stellar mass function for DESI BGS galaxies using hierarchical Bayesian SED inference.

### `jespersen2022mangrove` — Mangrove: galaxies from merger trees
- [arXiv:2210.13473](https://arxiv.org/abs/2210.13473) | [ApJ (2022)](https://iopscience.iop.org/article/10.3847/1538-4357/ac9b18)
- Graph neural network emulator mapping dark matter merger trees to galaxy properties, 10,000× faster than semi-analytic models.

### `spuriomancini2022cosmopower` — CosmoPower cosmological emulator
- [arXiv:2106.03846](https://arxiv.org/abs/2106.03846) | [MNRAS 511 (2022)](https://academic.oup.com/mnras/article/511/2/1771/6505144)
- Neural emulators for matter and CMB power spectra; up to 10⁴× speed-up for Bayesian cosmological inference.

### `korber2023pinion` — PINION reionization emulator
- [arXiv:2208.13803](https://arxiv.org/abs/2208.13803) | [MNRAS (2023)](https://academic.oup.com/mnras/article/521/1/902/7059216)
- Physics-informed neural network emulator for 4D hydrogen reionization history from N-body density fields.

### `luciesmith2019halos` — Interpretable ML for halo formation
- [arXiv:1906.06339](https://arxiv.org/abs/1906.06339) | [MNRAS 490 (2019)](https://academic.oup.com/mnras/article/490/1/331/5570617)
- Interpretable ML framework mapping initial conditions to halo masses; finds tidal shear adds no significant predictive power over density alone.

### `kane2025europium` — Europium abundances from GALAH
- [arXiv:2512.02125](https://arxiv.org/abs/2512.02125) | [MNRAS (2025)](https://academic.oup.com/mnras/advance-article/doi/10.1093/mnras/stag209/8444584)
- CNN label-transfer catalogue of europium abundances for ~119,000 GALAH DR4 stars.

---

## Morphology Classification

### `dieleman2015galaxymorphology` — CNN galaxy morphology (Galaxy Zoo)
- [arXiv:1503.07077](https://arxiv.org/abs/1503.07077) | [MNRAS 450 (2015)](https://academic.oup.com/mnras/article/450/2/1441/979677)
- Rotation-invariant CNN for Galaxy Zoo morphology; near-perfect accuracy on high-agreement images.

---

## Spectroscopy

### `melchior2023spender` — SPENDER galaxy spectra autoencoder
- [arXiv:2211.07890](https://arxiv.org/abs/2211.07890) | [AJ (2023)](https://iopscience.iop.org/article/10.3847/1538-3881/ace0ff)
- Convolutional autoencoder for encoding, reconstructing, and super-resolving galaxy spectra at arbitrary redshift.

### `cheng2022lya` — CNN for Lyα forest
- [arXiv:2209.02142](https://arxiv.org/abs/2209.02142) | [MNRAS (2022)](https://academic.oup.com/mnras/article/517/1/755/6702734)
- CNN trained on simulated spectra to identify low-column-density Lyman-α absorbers in quasar spectra.

---

## Lensing

### `metcalf2019lensfinding` — Strong lens finding challenge
- [arXiv:1802.03609](https://arxiv.org/abs/1802.03609) | [A&A 625 (2019)](https://www.aanda.org/articles/aa/full_html/2019/05/aa32797-18/aa32797-18.html)
- Benchmark of CNN and other classifiers for strong gravitational lens finding at survey scale.
