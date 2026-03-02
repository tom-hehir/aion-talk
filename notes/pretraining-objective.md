# Pre-training objective: simple explanation

## What is being learned?

AION-1 learns to predict the discrete token IDs of masked tokens given the token IDs of observed tokens. This is standard **masked token modelling** (cross-entropy over a vocabulary of token IDs), generalised to work across multiple modalities simultaneously.

## Loss

Negative log-likelihood of the correct token IDs:

```
L(θ) = −Σᵢ log p_θ(x_i^tgt | x^obs)
```

`p_θ` is a categorical distribution (softmax) over the codebook vocabulary for each output position. There is one output head per modality (each with its own vocabulary size).

## How inputs and outputs are selected (the masking strategy)

**Input budget: 256 tokens.**

1. Pick one modality uniformly at random as the "primary" modality.
2. Uniformly sample a number of tokens `n` from that modality.
3. Fill the remaining `256 − n` slots by sampling tokens uniformly from all other modalities.

**Output budget: 128 tokens.**

1. Pick one modality at random (can differ from the input primary).
2. Sample a number of tokens from that modality using a **Beta distribution skewed toward zero** (so the model usually predicts few tokens from that modality — this mirrors the distribution at inference time).
3. Fill the remaining output slots by sampling uniformly from other modalities.

## Key points

- Input and output tokens come from **different disjoint subsets** of the full token pool.
- The model learns both **intra-modal** (predict spectrum tokens from other spectrum tokens) and **cross-modal** (predict spectrum tokens from image tokens) relationships in every batch.
- The Beta skew on the output budget means the model trains on many examples where it predicts a small number of output tokens per modality. This mirrors ROAR inference, where at each step only a fraction of remaining tokens are revealed.
- The Dirichlet sampling used in the original 4M paper was found to produce mostly-empty batches when modalities have very different lengths, so AION uses this simpler budget-based strategy instead.
