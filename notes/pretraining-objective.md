# Pre-training objective: simple explanation

## What is being learned?

AION-1 learns to predict the discrete token IDs of masked tokens given the token IDs of observed tokens. This is standard **masked token modelling** (cross-entropy over a vocabulary of token IDs), generalised to work across multiple modalities simultaneously.

## Loss and equation derivation

The slide shows a three-line derivation:

```
L(θ) = −H(f, p_θ)
      = −E_{(x^targ, x^cond) ~ f} [ log p_θ(x^targ | x^cond) ]
      ≃ −Σᵢ log p_θ(x_i^targ | x_i^cond)
```

**Line 1: cross-entropy framing.**
`H(f, p_θ)` is the cross-entropy between `f` and the model distribution `p_θ`. Minimising `L(θ)` is equivalent to minimising the KL divergence `KL(f || p_θ)` (since the entropy of `f` is constant w.r.t. θ).

**What is `f`?**
`f` is the **sampling distribution over (x^targ, x^cond) pairs** induced by the masking strategy. It is not the data distribution itself — it is the joint distribution over how tokens are split into conditioning (observed) and target (masked) subsets. Each draw from `f` produces one training example: a random conditioning set and a disjoint random target set, drawn according to the input/output budget rules (primary modality + fill, Beta skew on outputs). `f` is never computed explicitly; we only ever sample from it.

Crucially, `f` is **not uniform over all possible token subsets**. The masking strategy imposes a specific frequency distribution: the primary-modality selection and the Beta skew on output count mean some tokens and modality combinations appear as training targets far more often than others. This matters because the model is optimised to be good at exactly the tasks that `f` makes frequent — the choice of `f` directly shapes model capabilities. Training under this non-uniform `f` (rather than uniform masking) is a deliberate design decision: the Beta skew on outputs mirrors the ROAR inference distribution, so the model is trained on the same kind of prediction tasks it will face at test time.

**Line 2: expectation form.**
Writing out the definition of cross-entropy makes the role of `f` explicit: we take the expected negative log-likelihood of the correct token IDs under the sampling distribution `f`.

**Line 3: Monte Carlo approximation.**
Since we cannot compute the expectation analytically, we replace it with an empirical sum over `N` training examples (token positions in the batch). This is the standard stochastic gradient approximation.

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
