# ROAR inference sampling: simple explanation

ROAR (Random Order AutoRegressive) is the generation scheme used at inference time. It was introduced in 4M and adopted by AION-1.

## The basic idea

Given some observed tokens `x^in` (the conditioning information), you want to sample the unknown query tokens `x^qry`. ROAR does this **iteratively**: in each step it reveals and samples a fraction of the still-unknown tokens, conditioning on everything revealed so far. The fraction decreases geometrically, so the number of steps is O(log |Q|) rather than O(|Q|).

## Step by step

At each iteration `t`, given the current set of unknown query indices `Q_t`:

1. **Shuffle.** Draw a random permutation of `Q_t`.
2. **Pick a subset.** Take the first `ρ_t = ⌊r^t |Q_t|⌋` indices from that permutation. Call this set `S_t`. (With `r ∈ (0,1)`, this is a geometrically shrinking fraction of remaining tokens.)
3. **Sample.** Draw each token in `S_t` from the model: `x_j ~ p_θ(· | x^in ∪ previously-sampled)`.
4. **Commit.** Move those tokens from unknown to known: add them to `x^in`, remove from `Q`.

Repeat until `Q` is empty.

## Can sampled tokens be resampled?

**No.** Once a token is sampled in step 3 and promoted to `x^in` in step 4, it is permanently removed from `Q`. It will never be revisited or resampled, regardless of how confident the model was.

This is different from **MaskGIT**, which uses confidence scores to decide which tokens to remask: at each step MaskGIT samples all unknown tokens, keeps the highest-confidence ones, and masks the rest back for the next round. ROAR makes no such distinction — it samples a random subset, not a confidence-filtered subset, and those sampled tokens are final.

**Implication:** the ordering in which tokens are revealed is random (step 1 is a random permutation), so the model sees a wide variety of reveal orders during training and generalises to arbitrary conditioning sets.

## Limitation

Because each token is sampled independently from `p_θ(x_j | x^in)` (the model factorises the joint), multi-token correlations may be underrepresented. The samples are plausible but are **not guaranteed to be well-calibrated joint posteriors** over sequences of many tokens. This is why the paper recommends using AION-1 primarily as an embedding model rather than relying on posterior draws for scientific analysis.
