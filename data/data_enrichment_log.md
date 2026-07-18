# Data Enrichment Log

**Task:** Task 1 — Data Exploration and Enrichment
**Collected by:** Claude (AI analyst), working with the project owner
**Collection date:** 2026-07-18
**Starter dataset:** 57 records (30 observation, 10 event, 14 impact_link, 3 target)
**After enrichment:** 69 records (39 observation, 11 event, 16 impact_link, 3 target)

---

## 1. Summary of additions

| Added | Count | Record IDs |
|---|---|---|
| Observations | 9 | REC_0034–REC_0042 |
| Events | 1 | EVT_0011 |
| Impact links | 2 | IMP_0015–IMP_0016 |

All additions follow the unified schema (`data/raw/SCHEMA_README.md`): events are recorded neutrally (no `pillar` pre-assignment), and their effects are captured only through `impact_link` records, consistent with the "don't force interpretation onto data" design principle.

---

## 2. Why these additions

Reviewing the starter dataset against the project brief surfaced three concrete gaps:

1. **No `USG_DIGITAL_PAYMENT` indicator existed**, even though "Digital Payment Adoption Rate" is one of the two official forecasting targets named in the brief (Access and Usage). The starter dataset had proxies (P2P counts, Telebirr users) but not the Findex-defined Usage measure itself. This was the highest-priority gap to fill.
2. **No urban/rural or 2024 gender disaggregation for Access.** Task 2 explicitly asks to analyze the gender gap and urban/rural gap, but the starter dataset only had a 2021 gender split (REC_0004/REC_0005) and no urban/rural split at all.
3. **No infrastructure/enabler indicators** (electricity, smartphone penetration, internet penetration) beyond 4G coverage and mobile subscriptions — these are exactly the "indirect correlation" variables flagged in Enrichment Guide Sheet C as useful leading indicators.

## 3. New observations (REC_0034–REC_0042)

| ID | Indicator | Value | Disaggregation | Date | Source | Confidence |
|---|---|---|---|---|---|---|
| REC_0034 | ACC_OWNERSHIP | 73% | urban | 2024 | Global Findex 2025 (via Shega/DFS Ethiopia Hub) | medium |
| REC_0035 | ACC_OWNERSHIP | 57% | male | 2024 | Global Findex 2025 (via Birr Metrics) | medium |
| REC_0036 | ACC_OWNERSHIP | 42% | female | 2024 | Global Findex 2025 (via Birr Metrics) | medium |
| REC_0037 | USG_DIGITAL_PAYMENT (new code) | 26% | male | 2024 | Global Findex 2025 (via Birr Metrics) | medium |
| REC_0038 | USG_DIGITAL_PAYMENT | 13% | female | 2024 | Global Findex 2025 (via Birr Metrics) | medium |
| REC_0039 | USG_DIGITAL_PAYMENT | 21% | all/national | 2024 | Global Findex 2025 (via Birr Metrics) | **low** |
| REC_0040 | ACC_ELECTRICITY (new code) | 55.4% | national | 2023 | World Bank SDG7 Tracking / ESMAP | high |
| REC_0041 | ACC_SMARTPHONE_PEN (new code) | 15% | national | 2024 | GSMA Mobile Gender Gap (via Birr Metrics) | medium |
| REC_0042 | ACC_INTERNET_PEN (new code) | 21.3% | national | Jan 2025 | DataReportal Digital 2025: Ethiopia | high |

**New indicator codes introduced:** `USG_DIGITAL_PAYMENT`, `ACC_ELECTRICITY`, `ACC_SMARTPHONE_PEN`, `ACC_INTERNET_PEN`.

## 4. New event (EVT_0011)

**National Digital Payment Strategy 2026–2030 (NDPS 2.0) & National Instant Payment System launch**, 2025-12-09, category=`policy`, source: National Bank of Ethiopia / ENA (high confidence).

This is Ethiopia's successor to the 2021–2024 NDPS / NFIS-II era and is directly relevant to the 2025–2027 forecast window this project targets. `pillar` is left empty per schema.

## 5. New impact links (IMP_0015–IMP_0016)

Both link EVT_0011 to indicators, using comparable-country evidence (per Task 3 methodology) since no Ethiopian post-launch data exists yet:
- **IMP_0015**: NDPS 2.0 → `USG_DIGITAL_PAYMENT`, increase, medium magnitude, 18-month lag, based on India's UPI experience (low confidence — too early for empirical Ethiopian evidence).
- **IMP_0016**: NDPS 2.0 → `ACC_OWNERSHIP`, increase, low magnitude, 24-month lag, enabling relationship, theoretical basis (strategy documents tend to act indirectly on Access, per the pattern seen with NFIS-II).

## 6. Data quality issues flagged during enrichment (important — read before modeling)

1. **Gender-gap conflict:** REC_0035/REC_0036 (male 57% / female 42%, implying a 15pp gap) come from a different secondary source than the starter dataset's own 2024 gender-gap record (REC_0028, 18pp). Both cite the Global Findex 2024/2025 release but likely reflect different report vintages (preliminary vs. final) or rounding. **Do not average these** — treat REC_0028 (which came from the vetted starter dataset, `Global Findex 2024` as source_name) as the primary series, and REC_0035/REC_0036 as a secondary cross-check, until reconciled against the official Findex microdata.
2. **Digital payment usage conflict:** The project brief itself states "made or received digital payment: ~35%" for 2024, while REC_0039 (21%) is a different Findex sub-metric ("used a digital payment," possibly measured among account holders rather than all adults). These are **not interchangeable** — REC_0039 is marked low confidence for this reason. Recommend treating the brief's ~35% figure as the primary Usage headline number for forecasting, and using REC_0039/REC_0037/REC_0038 mainly for the gender-gap analysis, not as the absolute Usage level.
3. **Possible event near-duplicate:** EVT_0011 (NDPS 2.0 policy launch, Dec 9 2025) and the starter dataset's EVT_0008 (EthioPay Instant Payment System, Dec 18 2025) were announced at the same conference and may represent overlapping developments reported with different dates by different outlets. Kept as separate records (policy document vs. specific payment rail) but flagged for review before Task 3 impact modeling — double-counting their effects would bias the event-impact model.
4. **Secondary-source risk:** Most new observations are cited via news/blog coverage of the Global Findex 2025 release rather than the World Bank's own microdata portal (which requires registration and wasn't accessible in this session). All such records are marked `confidence: medium` rather than `high`, and `source_type: research` rather than `survey`. Recommend validating against `microdata.worldbank.org` before final submission if time allows.

## 7. Additions considered but not made

- **Wealth-quintile account ownership** (richest 60%: 53%, poorest 40%: 43%, per Birr Metrics) — not added because the schema's `location` field only supports `national/urban/rural`, not wealth quintiles. Adding it would require a schema extension outside this task's scope; noted here for the team to consider in Task 2's insights writeup instead.
- **Rural-specific account ownership %** — searched for but could not find a directly reported rural Findex 2024 figure (only the urban 73% figure was explicitly reported); adding an inferred rural number (e.g., back-calculated from national and urban) was judged too speculative to record as an "observation" and is left as an analysis step for Task 2 instead.
