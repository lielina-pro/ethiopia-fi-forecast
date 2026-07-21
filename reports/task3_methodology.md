# Task 3 Methodology: Event Impact Modeling

**Full analysis, code, and all figures:** `notebooks/03_impact_modeling.ipynb`
**Refined estimates:** `data/processed/refined_impact_estimates.csv`

This document summarizes the methodology, sources, validation results, and limitations for the
event-indicator impact model, as required by the Task 3 deliverables.

## 1. Functional Form

Each event's effect on an indicator is modeled as a **logistic ramp**:

```
effect(t) = magnitude x 1 / (1 + exp(-k(t - lag)))
```

where `t` is months since the event, `lag` is the `lag_months` value from the `impact_link` record (time
to reach 50% of the full effect), and `k` is chosen so the effect reaches ~95% of full magnitude by
`2 x lag` months. Before the event (`t < 0`), the effect is 0.

**Why a logistic ramp instead of alternatives:**
- *Step function* (effect appears fully and instantly) — rejected as unrealistic; financial-product
  adoption takes time to spread through a population.
- *Linear ramp* — rejected because it doesn't capture the slow-start / fast-middle / plateau shape typical
  of technology adoption curves (S-curves), which is well documented in the mobile-money literature.
- *Logistic ramp* — captures gradual build-up, an inflection point at the specified lag, and a natural
  plateau, using only the two parameters already present in the schema (`lag_months`, `impact_estimate`).

**Combining multiple events on the same indicator:** effects are **summed (additive)**. This is the
standard starting assumption for a sparse-data event-study setup; it is an explicit simplification (see
Limitations) rather than a claim that effects truly interact this way.

## 2. Sources for All Impact Estimates

All 16 `impact_link` records and their sources are listed in full in the notebook (Section 1, the
event-indicator join) and in the underlying `data/processed/enriched_dataset.csv`. In summary:

| Evidence basis | Count | Notes |
|---|---|---|
| `empirical` | 6 | Estimated from real pre/post Ethiopian data |
| `literature` | 8 | Documented effects from comparable markets (Kenya, Rwanda, India, Tanzania) or published research |
| `theoretical` | 2 | No empirical or literature precedent; analyst judgment based on mechanism |

Comparable-country analogs used: **Kenya** (M-Pesa's home market) for Fayda Digital ID's expected Access
effect; **Rwanda** for a data-affordability effect; **India** (UPI) for two NDPS/instant-payment analogs;
**Tanzania** for M-Pesa/EthSwitch interoperability effects. All four are kept at `medium` or `low`
confidence, never treated as equivalent to direct Ethiopian evidence.

## 3. Validation Results: Predicted vs. Observed

**The brief's own worked example:** Telebirr launched May 2021; mobile money account ownership
(`ACC_MM_ACCOUNT`) went from 4.7% (2021) to 9.45% (2024).

### Validation 1 — Telebirr to Account Ownership (IMP_0001, the one clean case)

| | Value |
|---|---|
| Predicted effect (logistic ramp, 42 months post-launch, ~100% realized) | **+15.0 pp** |
| Actual observed change in `ACC_OWNERSHIP`, 2021-2024 | **+3.0 pp** |
| Overestimate | ~5x |

**Interpretation:** the Kenya-analog literature estimate does not transfer 1:1. Two plausible, non-exclusive
explanations: (1) Kenya's M-Pesa entered a market with no serious competitor and a decade head start,
while Telebirr faced M-Pesa's own Ethiopian entry just two years later; (2) the original estimate may have
targeted the wrong indicator — Telebirr's effect shows up far more clearly in its own product category.

### Validation 2 — the gap this task found

No `impact_link` connected Telebirr to `ACC_MM_ACCOUNT` at all, despite this being the project brief's own
headline example. Back-calculating from the actual +4.75 pp change (assuming the same 12-month lag as
IMP_0001) implies a full-ramp magnitude of **+4.75 pp** — this is recommended as a new record (`IMP_0017`)
in a future enrichment pass (see `data/processed/refined_impact_estimates.csv`).

### Validation 3 — Safaricom entry to 4G coverage (illustrative only)

Predicted +14.9 pp by mid-2025 vs. an actual (non-exact-window) increase of +33.3 pp from the earliest
available post-event data point. Not a clean validation — no 4G coverage observation exists at the actual
event date — kept as an illustrative check pending a closer observation.

## 4. Refinements Made

Recorded explicitly in `data/processed/refined_impact_estimates.csv` (original estimate is never
overwritten in place, to preserve the audit trail):

| Link | Indicator | Original | Refined | Why |
|---|---|---|---|---|
| IMP_0001 | ACC_OWNERSHIP | 15.0 pp (literature) | 3.0 pp | Calibrated to match actual observed change |
| IMP_0017 (new, recommended) | ACC_MM_ACCOUNT | *(not modeled)* | 4.75 pp | Fills the gap found in Validation 2 |
| IMP_0004 | ACC_4G_COV | 15.0 pp (empirical) | 15.0 pp (unchanged) | Comparison window not clean enough to justify a change |

## 5. Key Assumptions and Uncertainties

**Assumptions:**
- Each event's effect on an indicator is independent of every other event (no interaction terms).
- Lag reflects adoption speed only, not concurrent external shocks (e.g., the 2024 forex liberalization
  coincided with several fintech launches; no adjustment was made for this overlap).
- Comparable-country magnitudes assume similar-enough market structure to transfer directly — Validation 1
  shows this assumption deserves real skepticism, not just a footnote caveat.

**Uncertainties / confidence:**
- **High confidence:** empirically-derived, directly-validated estimates (IMP_0017 recommendation).
- **Medium confidence:** empirical Ethiopian estimates without a clean validation window (IMP_0004), and
  literature-based estimates now cross-checked once (IMP_0001, refined).
- **Low confidence:** literature/theoretical estimates for very recent events with no Ethiopian post-launch
  data yet (e.g., NDPS 2.0's impact links, IMP_0015/IMP_0016).

**Limitations:**
- Only one clean pre/post validation case exists in the whole dataset (Telebirr to Account Ownership);
  every other estimate in the association matrix remains unvalidated against real Ethiopian outcomes.
- Additive combination likely overstates compound effects as more events accumulate on one indicator
  (e.g., `ACC_OWNERSHIP` now has three contributing events) — a saturating/diminishing-returns combination
  function is a natural next refinement with more data.
- Confidence levels are analyst judgment, not statistically estimated standard errors; they should be read
  as relative rankings, not calibrated probabilities.
