# Interim Report — Ethiopia Financial Inclusion Forecasting

**Submitted by:** Selam Analytics project team
**Date:** 19 Jul 2026
**Covers:** Task 1 (Data Enrichment) and Task 2 (Exploratory Data Analysis)

---

## 1. Data Enrichment Summary

The starter dataset (57 records: 30 observations, 10 events, 14 impact_links, 3 targets) was enriched with
**9 new observations, 1 new event, and 2 new impact_links** (69 records total), all sourced from live web
research documented with `source_url`, `original_text`, and `confidence` per the schema's data-entry rules.

**What we added and why:**
- **`USG_DIGITAL_PAYMENT`** — this is one of the two official Findex forecasting targets named in the
  project brief, yet it did not exist as an indicator code in the starter dataset. Added with a
  gender split (male 26%, female 13%, 2024) from Global Findex 2025 reporting.
- **2024 gender and urban disaggregation for Access** — the starter dataset only had a 2021 gender split
  and no urban figure; Task 2 explicitly requires gender-gap and urban/rural analysis.
- **Three enabler indicators** — electricity access (55.4%), smartphone penetration (15%), and internet
  penetration (21.3%) — flagged in the Enrichment Guide as leading indicators for digital-finance uptake.
- **One new policy event** — Ethiopia's National Digital Payment Strategy 2026-2030 (NDPS 2.0), launched
  Dec 2025, directly relevant to the 2025-2027 forecast window.

Full details, sources, and — importantly — **data conflicts found during enrichment** are in
[`data/data_enrichment_log.md`](../data/data_enrichment_log.md). We deliberately did not silently resolve
these conflicts; they're flagged with confidence levels so Task 3/4 modeling can make an informed choice.

---

## 2. Key Insights from EDA (see `notebooks/02_eda.ipynb` for full analysis and charts)

1. **Access growth is decelerating, not accelerating** — from 4.33 pp/year (2014-17) to 2.75 (2017-21) to
   just 1.00 pp/year (2021-24) — despite major mobile money launches in that final period.
2. **The gender gap in account ownership is essentially frozen**: 20pp (2021) → 18pp (2024), a 2pp
   improvement over three years of digital-finance expansion.
3. **Usage lags Access by a wider margin than Access lags its potential.** Telebirr reports 54.8M
   registered users, but M-Pesa's active-user rate is only 66% of its registered base — registration is not
   translating into regular use.
4. **Smartphone penetration (15%), not network coverage (70.8% 4G), looks like the binding constraint on
   Usage.** Basic mobile connectivity is high; the ability to run digital-finance apps is not.
5. **M-Pesa's 2023 entry and 2025 EthSwitch integration coincide with the clearest visible event effect in
   the dataset** — P2P transaction volume grew 2.6x (49.7M → 128.3M) between 2024 and 2025.
6. **Urban account ownership (73%) implies a substantial urban-rural gap** that the current data cannot
   directly measure — a priority gap for future enrichment.

## 3. Preliminary Observations on Event-Indicator Relationships

Using the `impact_link` table (16 records, including 2 added in Task 1) rather than raw correlation — the
dataset is too sparse (most indicators have 1-2 timestamped points) for correlation analysis to be
statistically meaningful. Five events are linked to ACCESS-pillar indicators and several more to USAGE,
with impact estimates ranging from 3pp (low-magnitude, theoretical) to 25% (high-magnitude, empirical, for
Telebirr's effect on P2P transactions). This table — not a correlation matrix — is the right foundation for
Task 3's association matrix.

## 4. Data Limitations Identified

- **Sparse time series**: only Account Ownership has enough historical points (5) for real trend analysis;
  everything else is 1-2 snapshots, ruling out classical correlation/regression across indicators.
- **Conflicting secondary sources** for two 2024 figures (gender gap: 15pp vs. 18pp; digital payment usage:
  21% vs. the brief's ~35%) — both kept in the dataset with confidence flags rather than reconciled.
- **No direct rural Access observation** exists — inferred only indirectly via the urban/national gap.
- **A likely event near-duplicate** (NDPS 2.0 vs. EthioPay launch, both Dec 2025) risks double-counting in
  Task 3's impact model if not resolved first.
- Most enrichment observations are cited via news/blog coverage of the Global Findex 2025 release rather
  than the World Bank's own microdata portal (registration-gated); marked `confidence: medium` accordingly.

---

**Repository:** `data/raw/` (schema + data), `data/data_enrichment_log.md` (Task 1 detail),
`notebooks/02_eda.ipynb` (Task 2 full analysis + 11 charts in `reports/figures/`).
