# Talk outline

Working structure for the presentation. Edit freely — this is for thinking, not for LaTeX.

---

## 1. Motivation

**Core question:** Can the foundation model paradigm — so successful in NLP and vision — work for heterogeneous scientific data?

- Astronomy is data-rich but modality-fragmented: images, spectra, scalars, all from different instruments
- Cross-survey science today requires bespoke pipelines per task
- A single pretrained encoder could unlock many tasks at once

**Goal:** establish why this is hard and why it matters, before introducing AION as the answer.

---

## 2. Data

- 5 surveys: Legacy Survey, HSC, SDSS, DESI, Gaia
- ~200M observations spanning stars, galaxies, quasars
- Key challenge: heterogeneous noise models, different resolutions, missing modalities per object
- Cross-matching strategy ties objects across surveys

**Possible angle:** emphasise the *scale and diversity* — this is what makes the problem interesting and what makes a unified model non-trivial.

---

## 3. Architecture

### 3a. Tokenisation
- Modality-specific tokenisers trained independently and then frozen
- Image tokeniser: VQ-VAE style, per-survey to handle different PSFs/bands
- Spectrum tokeniser: 1D conv encoder, handles variable wavelength grids
- Scalar tokeniser: learned embeddings per measurement

**Key point:** tokenisation homogenises wildly different data into a common token space.

### 3b. Multimodal masked modelling
- Tokens from all modalities concatenated with modality/survey embeddings
- Standard transformer, BERT-style masked prediction
- Modality-level masking encourages cross-modal transfer

---

## 4. Model family

- Three scales: 300M, 700M, 3.1B parameters
- Consistent scaling behaviour (lower eval loss with more params)
- All released open-source

---

## 5. Results

### Out-of-the-box (frozen encoder + lightweight head)
- Photometric redshift — images, spectra, scalars
- Stellar metallicity ([Fe/H])
- Galaxy morphology (GZ10 classification)
- Similarity retrieval

### Embedding / emergent capabilities
- HSC image prediction from DESI spectra (cross-modal transfer)
- Spectral super-resolution
- GZ3D segmentation
- Rare object detection

**Possible angle:** lead with the most striking result (cross-modal transfer?) to show the model has learned something genuinely physical.

---

## 6. Conclusion

- AION-1 shows the foundation model paradigm can work for heterogeneous scientific data
- A single frozen encoder is competitive across a broad task suite
- Blueprint for multimodal scientific foundation models beyond astronomy
- Open questions: more modalities (radio, X-ray, time series), fine-tuning in low-data regimes
