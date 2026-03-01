# Presentation Plan: AION-1

## 1. Title Slide
- Title, speaker, affiliation, date
- Link to AION-1 paper (arXiv:2510.17960)

## 2. Team
- Acknowledge all authors on the paper
- Photo collage from GitHub profiles (Polymathic AI team)

## 3. Motivation: Status Quo in Astronomical ML
- Previous ML in astronomy: task-specific and data-specific models
- Illustrate with examples overlapping AION's downstream tasks:
  - Anomaly detection
  - Parameter estimation
  - Morphology classification
  - (Generation — optional)
- Contrast with approaches using strong physical priors / inductive bias
- Mention Bayesian statistical frameworks as an alternative paradigm

## 4. Prior Foundation Model Efforts in Astronomy
Group into three broad categories:
1. **Supervised pre-training** on large, complex label sets
2. **Contrastive learning**
   - Single-modality (e.g. Stein et al.)
   - Multi-modal (e.g. AstroCLIP, AstroM³)
3. **Generative** (e.g. AstroPT)

## 5. Introducing AION-1
- First large-scale, multi-modal, multi-survey, generative foundation model for astronomy

## 6. Data (§3, Figure 2)
- 5 surveys: Legacy Survey, HSC, SDSS, DESI, Gaia
- ~200M observations of stars, galaxies, quasars
- Shout-out to the Multimodal Universe (MMU) as the data source (paper, repo, HuggingFace)

## 7. Architecture & Objective (§4–5, Figure 1)
### 7a. Overview (Figure 1)
- Note the error in Figure 1: it incorrectly implies physical parameters are used to predict
  "blue 2 and 7" tokens, which are actually received as input

### 7b. Modality-Specific Tokenisation
- Quantisation schemes: LFQ, FSQ, binning (for scalars)
- Tokeniser architectures: name only (fancy CNNs); no detail on subsampled linear projection
- Training objective: proper negative log-likelihood
  - Spectrum also uses cross-entropy on the mask prediction (likelihood-based, but no
    principled way to weight against flux likelihood)

### 7c. AION Transformer
- Encoder–decoder transformer setup
- Modality and positional encodings

### 7d. Objective Function
- Masked token modelling over discrete tokens
- Why discretisation (quantisation) is necessary

## 8. Model Training & Variants (§6, Figure 6)
- Training setup
- Model sizes: 300M, 700M, 3.1B parameters

## 9. Downstream Tasks

### 9.1 Out-of-the-Box Capabilities (§7.1)
- Generation scheme: iterative masked decoding (reference MaskGIT figure)
- **Redshift estimation** (§7.1.1): conditioned on various subsets of modalities
- **Spectral super-resolution** (§7.1.2): Gaia → DESI spectra

### 9.2 Embedding-Based Downstream Tasks (§7.2)
- Method: freeze encoder, finetune a lightweight prediction head; pool embeddings where appropriate
- **Galaxy parameter estimation** (§7.2.1, Table 1)
- **Galaxy morphology classification** (§7.2.2, Table 2)
- **Galaxy image segmentation** (§7.2.3, Figure 9) — show IoU definition (equation on slide, not explained)
- **Stellar parameter estimation** (§7.2.4, Tables 3–4)
- **Low-data regime / scaling** (§7.2.5, Figure 10) — note two advantages: low-data performance and faster data saturation

### 9.3 Rare Object Detection (§7.3)
- Dataset summary (Table 5)
- Method: cosine-similarity–based retrieval
- nDCG equations on slide (not explained)
- Retrieval results (Figure 11)

### 9.4 Emergent Transfer Properties (§7.4)
- **HSC image → DESI spectrum** (§7.4.1, Figure 12)
- **Cross-survey morphology** (§7.4.2, Table 6): predict morphology from HSC embeddings using
  a head trained on Legacy Survey embeddings

## 10. Future Work
- Replace quantised tokens with continuous tokens
- Better decoder: current decoder does not produce a correct/proper distribution over tokens
  given the encoder embedding; candidates: autoregressive modelling, diffusion models, or
  drop decoding entirely with a JEPA objective
- Better pooling: mean pooling is suboptimal — consider self-supervised discriminative
  finetuning for summary embeddings
- Community adoption:
  - Integration into survey pipelines (ML-inferred data products)
  - Highlight best use-cases: embeddings for parameter estimation and similarity retrieval
  - Generation not recommended for practical use yet

## 11. Conclusions (§8)
- Integrates multiple modalities across multiple surveys
- Achieves or surpasses state-of-the-art on diverse downstream tasks
- Excels in the low-data regime
- Enables zero-shot semantic retrieval
- Enables cross-survey transfer learning
- Addresses the need for a flexible, scalable, community-shareable framework
- A potential template for foundation models in other scientific domains

## 12. Resources
- **Multimodal Universe**: paper, repo, HuggingFace
- **AION-1**: repo (github.com/PolymathicAI/AION), HuggingFace
- **Paper**: conference proceedings and arXiv (arXiv:2510.17960)

---

## Extra / Backup Slides
- Original VQ-VAE quantisation method (background reference)
