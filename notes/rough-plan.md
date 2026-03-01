# Rough plan for presentation

Below is a rough plan for the presentation. I will want to add to it, trim it,
or make refinements as I go, but this is the starting point.

- opening slide:
  - title
  - speaker
  - affiliation
  - date
  - link to AION-1 paper
- shout-out to the team on the paper / polymathic. List all authors, perhaps
grab photos from github accounts and make a collage.
- status quo: how machine learning was used previously in astronomy, i.e.
task-specific and data-specific models. Provide multiple examples of previous
works which overlap in the tasks we use AION for e.g. anomaly detection,
parameter estimation, morphology classification, and perhaps generation (not
sure we need to cover generation). Also maybe include an example with very
strong physical priors and inductive bias (very different to the foundation
model approach), and maybe something with a Bayesian statistical framework
baked in.
- discuss previous foundation model or foundation-model-like efforts in
astronomy and group them into 3 broad categories: supervised pre-training on
a large number of complicated labels, contrastive learning (single modality like
Stein et al, multimodal like AstroCLIP and AstroM^3), generative (like AstroPT).
- introduce AION-1 as the first large-scale, multimodal / multi-survey,
generative foundation model for astronomy.
- present the data AION is trained on (section 3 and figure 2) and give
shout-out to the multimodal universe (MMU) from which the data is sourced.
- explain AION's architecture / objective:
  - overview (figure 1)
    - note that there is a mistake in the figure (it does not really make sense
    to be predicting the "blue 2 and 7" tokens from physical parameters as they
    are received as input)
  - modality-specific tokenization
    - introduce quantization schemes: LFQ, FSQ, binning (for scalars)
    - summarize the tokenizer architectures and quantization schemes
      - don't go into too much detail on architectures -- just name the model
      and explain that they are basically fancy CNNs. Don't explain the
      subsampled linear projection in any detail. Do mention that we use the
      proper negative log likelihood to train the codecs (note that spectrum
      also does the cross-entropy on predicting the mask -- which is still
      a likelihood-based objective, but no a-priori way to combine with the
      flux likelihood contribution).
  - AION architecture:
    - transformer encoder / decoder setup
    - modality and positional encoding
  - explain how we quantize the tokens and why this is necessary
  - explain the objective function
- explain model training and variants (section 6 and figure 6)
- present downstream task results from the paper (probably all of them should be
included as slides but we can skip some during the talk to avoid making it too
long):
  - 7.1: "out-of-the-box capabilities"
    - introduce generation scheme in section 7.1. (refer to figure from MaskGIT
    paper).
    - 7.1.1: redshift estimation (conditioned on various subsets of modalities)
    - 7.1.2: spectral super-resolution (gaia spectra to desi spectra)
  - 7.2: using AION's embeddings
    - introduce concept of finetuning a light prediction head on top of
    embeddings from frozen AION encoder (and pooling where appropriate)
    - 7.2.1: galaxy parameter estimation (table 1)
    - 7.2.2: galaxy morphology classification (table 2)
    - 7.2.3: galaxy image segmentation (figure 9)
      - show definition of IoU (won't go through the equation but good to show) 
    - 7.2.4: stellar parameter estimation (table 3 and table 4)
    - 7.2.5: performance in low-data regime (scaling results in figure 10)
    briefly include on the slide the two advantages mentioned in the paper
    ("low-data performance" and "faster data saturation")
  - 7.3: "rare object detection"
    - summary of datasets (table 5)
    - introduce method (cosine similarity based retrieval)
    - include equations for nDCG (won't go through these but good to show)
    - retrieval results (figure 11)
  - 7.4: "emergent transfer properties":
    - 7.4.1: HSC image to DESI spectrum (figure 12)
    - 7.4.2: predicting morphology from HSC embeddings with head trained on
    legacy survey embeddings (table 6)
- next steps and future work:
  - replacing quantized tokens with continuous tokens
  - decoder does not produce a good (correct? proper?) distribution over tokens
  conditional on the encoder embedding. We can look to other objectives to
  address this e.g. autoregressive modeling, or diffusion models. Or if we don't
  want to decode, use a JEPA and save the cost of decoding entirely.
  - mean pooling is not ideal -- do some self-supervised discriminative
  finetuning for making better "summary embeddings"
  - encouraging adoption by the community:
    - including in survey pipelines (ML inferred data products?)
    - highlight best use-cases: using the model as an embedder for e.g.
    parameter estimation or similarity-based retrieval. Don't recommend
    generation.
- conclusions:
  - points from the paper's conclusion in section 8:
    - integrates multiple modalities
    - achieves / surpasses state-of-the-art performance on diverse downstream
    tasks
    - excels in low-data regime
    - enables zero-shot semantic retrieval
    - enables transfer learning
  - how we address the need for a more flexible / scalable framework which can
  be shared by the community
  - could be an example for other scientific domains beyond astronomy
- point to our work:
  - Multimodal Universe for data (paper, repo, and huggingface)
  - AION-1 (repo and huggingface)
  - paper (conference and arxiv)
- extra slides:
  - original method of quantization from VQ-VAE
