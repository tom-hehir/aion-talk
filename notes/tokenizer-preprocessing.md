# Tokenizer preprocessing details

Each tokenizer does survey-specific preprocessing before the autoencoder sees the data.

---

## Image tokenizer

1. **Band stacking.** All distinct survey bands are treated as separate channels. HSC (g,r,i,z,y) and Legacy Survey (g,r,i,z) are separate channels even when they share a filter name, giving a fixed 9-channel tensor. Missing bands for a given object are zero-filled; a binary mask `m_c` records which bands are present.

2. **Zero-point normalisation.** HSC is rescaled to the Legacy Survey zero-point of 22.5 mag (`s = 10^((ZP−22.5)/2.5)`) and pixel scales are equalised. This improves training stability but isn't strictly necessary since bands are already separated.

3. **arcsinh normalisation.** Applied to handle the high dynamic range of astronomical images. Inverted before computing the autoencoding loss.

4. **Subsampled linear projection.** The 9-channel image is projected to ≈6C = 54 channels via a learnable `W ∈ ℝ^{C×54}`. A scale factor `α(m_c)` keeps the feature norm invariant to missing bands. The projection is inverted after decoding. This disentangles survey-specific channel information before the ResNet sees it.

5. **Autoencoder.** MagViT-style ResNet (no transformer blocks), 2 downsampling blocks (factor-16 reduction), latent `24×24×512` → compressed to `d=4` → FSQ (codebook 2^12 = 4096, levels `{8,5,5,5}`). ~50M parameters.

---

## Spectrum tokenizer

1. **Median normalisation.** Compute a robust median flux `f̃` (ignoring masked pixels). This is range-compressed with `log₁₀` and tokenised separately as a scalar (codebook 1024) — it captures the overall brightness scale.

2. **Flux + inverse-std stacking.** Flux `f` and inverse standard deviation `istd` are both normalised by `f̃` and stacked into a 2-channel array `x ∈ ℝ^{B×2×L}`.

3. **Interpolation onto a fixed wavelength grid.** Both DESI and SDSS spectra are linearly interpolated onto a shared 8704-point grid covering 3500–10462.4 Å at 0.8 Å spacing. This removes survey-specific wavelength and dispersion differences.

4. **Autoencoder.** 4-stage ConvNeXt V2 backbone (initial 4×4 conv + LayerNorm, then three 2×2 downsampling stages). Compresses to `273×512`, then down to 10 dims for the quantizer (matching 2^10 codebook). LFQ quantiser (1024 codes). Three training losses: flux NLL (inverse-variance weighted), mask BCE, LFQ commitment loss (β=0.25).

---

## Scalar tokenizer

For scalars with large dynamic range (e.g. fluxes, radii), a `log₁₀` or `arcsinh` transform is applied first. Then:

1. **CDF normalisation.** Tabulate the empirical CDF `F_x` on the training set (via reservoir sampling, ~10^6 samples). Map each value to a standard normal variate: `z_i = Φ⁻¹(F_x(x_i))`.

2. **Fixed-codebook quantisation.** Centroids are placed at K=1024 equally spaced normal quantiles: `c_k = Φ⁻¹((k − ½)/K)`. No parameters learned, no loss required.

3. **Reconstruction.** `x̂_i = F_x⁻¹(Φ(c_i))`. Error is below typical measurement uncertainties for K=1024.

**Scalars tokenised per survey:**
- Legacy Survey: g,r,i,z fluxes; WISE W1–W4; E(B−V); ellipticity e₁,e₂; half-light radius R_eff
- HSC: g,r,i,z,y fluxes; shape tensor components
- SDSS & DESI: pipeline redshift z
- Gaia: 110 BP/RP coefficients, parallax, ra, dec, G, BP, RP fluxes
