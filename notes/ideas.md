# Ideas and open questions

Rougher thinking — things to consider, angles to explore, decisions not yet made.

---

## Narrative / framing

- What's the one-sentence take-home? Draft: *"A single model, trained on 200M heterogeneous astronomical observations, learns representations that transfer across tasks and modalities — without any task-specific pretraining."*
- Who is the audience? Adjust depth of ML vs. astronomy background accordingly.
- Should the talk lead with a striking result (e.g. cross-modal transfer) and work backwards, rather than following the paper's linear structure?

## Things to emphasise / de-emphasise

- The tokenisation design feels underappreciated — it's what makes the whole thing tractable. Worth a dedicated beat.
- The model family / scaling section could be brief unless there's a specific point to make about scale.
- The downstream results section is long in the paper — which subset is most compelling for a talk?

## Figures to prioritise

- `aion.png` — the main overview figure, probably slide 2
- `hsc_from_desi.png` — cross-modal transfer, visually striking
- `eval_loss.png` — scaling behaviour
- `redshift_image.png` / `redshift_photometry.png` — bread-and-butter downstream result
- `spectrum_superresolution.pdf` — another visually compelling emergent capability

## Open questions

- How long is this talk? (The current skeleton is ~20 content slides — could be 20 min or 45 min depending on depth.)
- Is there a live demo or just slides?
- Should limitations get a dedicated slide or just a bullet in conclusion?
