# Data Enrichment Log

**Task:** Task 1 — Data Exploration and Enrichment
**Collected by:** Claude (AI analyst), working with the project owner
**Collection date:** 2026-07-18
**Starter dataset:** `data/raw/ethiopia_fi_unified_data_original_starter.csv` — 57 records (30 observation, 10 event, 14 impact_link, 3 target)
**Enriched dataset:** `data/processed/enriched_dataset.csv` — 69 records (39 observation, 11 event, 16 impact_link, 3 target)

This log, together with the two CSV files above, is the complete Task 1 deliverable:
- `data/raw/ethiopia_fi_unified_data_original_starter.csv` = the untouched starter data, kept for before/after comparison.
- `data/processed/enriched_dataset.csv` = the final enriched dataset (starter + all additions below), ready for Task 2+ analysis.
- This log = the full audit trail explaining every addition.

---

## 1. Summary of additions

| Added | Count | Record IDs |
|---|---|---|
| Observations | 9 | REC_0034–REC_0042 |
| Events | 1 | EVT_0011 |
| Impact links | 2 | IMP_0015–IMP_0016 |

All additions follow the unified schema (`data/raw/SCHEMA_README.md`): events are recorded neutrally (no `pillar` pre-assignment), and their effects are captured only through `impact_link` records, consistent with the "don't force interpretation onto data" design principle.

---

## 2. Full Per-Record Audit Trail

Every field needed to audit and reproduce this enrichment -- `source_url`, `original_text` (a verbatim
quote from the source), `confidence`, `collected_by`, `collection_date`, and `notes` -- is listed below for
**all 12 new records**. These fields are also present as columns in `data/processed/enriched_dataset.csv`;
this section is a human-readable view of the same information, not a separate claim.

### REC_0034 — Account Ownership Rate

| Field | Value |
|---|---|
| **record_type** | observation |
| **indicator_code** | ACC_OWNERSHIP |
| **value_numeric** | 73.0 |
| **gender / location** | all / urban |
| **observation_date** | 2024-12-31 |
| **source_name** | Global Findex 2025 (via DFS Ethiopia Hub / Shega) |
| **source_url** | https://digitalfinance.shega.co/insights/articles/findex-2025-and-ethiopia-s-digital-financial-leap-momentum-without-maturity |
| **confidence** | medium |
| **collected_by** | Claude (AI analyst, working with trainee) |
| **collection_date** | 2026-07-18 |
| **original_text** (as quoted from source) | "Urban adults and those with secondary education or higher recorded the highest account ownership rates, at 73% and 80%, respectively." |
| **notes** | Fills urban/rural disaggregation gap noted in Task 1 instructions. Secondary source citing World Bank Global Findex 2025 release; treat as medium confidence pending direct Findex microdata confirmation. |

### REC_0035 — Account Ownership Rate

| Field | Value |
|---|---|
| **record_type** | observation |
| **indicator_code** | ACC_OWNERSHIP |
| **value_numeric** | 57.0 |
| **gender / location** | male / national |
| **observation_date** | 2024-12-31 |
| **source_name** | Global Findex 2025 (via Birr Metrics) |
| **source_url** | https://birrmetrics.com/49-of-ethiopians-are-banked-as-findex-2025-highlights-the-next-inclusion-challenge/ |
| **confidence** | medium |
| **collected_by** | Claude (AI analyst, working with trainee) |
| **collection_date** | 2026-07-18 |
| **original_text** (as quoted from source) | "While 57 percent of men in Ethiopia report having an account, only 42 percent of women do—a 15-point gap that has not narrowed since the last survey." |
| **notes** | Extends existing 2021 gender split (REC_0004/REC_0005) forward to 2024, enabling a gender-gap trend line instead of a single point. NOTE: implies a 15pp gap, vs the 18pp already recorded in REC_0028 (also 2024) -- flagged as a data conflict in enrichment log, likely reflects rounding/differing Findex release vintages (2024 preliminary vs 2025 final). |

### REC_0036 — Account Ownership Rate

| Field | Value |
|---|---|
| **record_type** | observation |
| **indicator_code** | ACC_OWNERSHIP |
| **value_numeric** | 42.0 |
| **gender / location** | female / national |
| **observation_date** | 2024-12-31 |
| **source_name** | Global Findex 2025 (via Birr Metrics) |
| **source_url** | https://birrmetrics.com/49-of-ethiopians-are-banked-as-findex-2025-highlights-the-next-inclusion-challenge/ |
| **confidence** | medium |
| **collected_by** | Claude (AI analyst, working with trainee) |
| **collection_date** | 2026-07-18 |
| **original_text** (as quoted from source) | "While 57 percent of men in Ethiopia report having an account, only 42 percent of women do—a 15-point gap that has not narrowed since the last survey." |
| **notes** | Paired with REC_0035 (male). See same data-conflict note re: GEN_GAP_ACC (REC_0028). |

### REC_0037 — Digital Payment Adoption Rate

| Field | Value |
|---|---|
| **record_type** | observation |
| **indicator_code** | USG_DIGITAL_PAYMENT |
| **value_numeric** | 26.0 |
| **gender / location** | male / national |
| **observation_date** | 2024-12-31 |
| **source_name** | Global Findex 2025 (via Birr Metrics) |
| **source_url** | https://birrmetrics.com/49-of-ethiopians-are-banked-as-findex-2025-highlights-the-next-inclusion-challenge/ |
| **confidence** | medium |
| **collected_by** | Claude (AI analyst, working with trainee) |
| **collection_date** | 2026-07-18 |
| **original_text** (as quoted from source) | "Only 26 percent of men and 13 percent of women used digital payments in the past year." |
| **notes** | New indicator code USG_DIGITAL_PAYMENT introduced -- not present in starter dataset even though it is one of the two core Findex targets named in the project brief (Usage/Digital Payment Adoption Rate). This is arguably the single most important gap filled in this enrichment pass; see enrichment log. |

### REC_0038 — Digital Payment Adoption Rate

| Field | Value |
|---|---|
| **record_type** | observation |
| **indicator_code** | USG_DIGITAL_PAYMENT |
| **value_numeric** | 13.0 |
| **gender / location** | female / national |
| **observation_date** | 2024-12-31 |
| **source_name** | Global Findex 2025 (via Birr Metrics) |
| **source_url** | https://birrmetrics.com/49-of-ethiopians-are-banked-as-findex-2025-highlights-the-next-inclusion-challenge/ |
| **confidence** | medium |
| **collected_by** | Claude (AI analyst, working with trainee) |
| **collection_date** | 2026-07-18 |
| **original_text** (as quoted from source) | "Only 26 percent of men and 13 percent of women used digital payments in the past year." |
| **notes** | Paired with REC_0037 (male). |

### REC_0039 — Digital Payment Adoption Rate

| Field | Value |
|---|---|
| **record_type** | observation |
| **indicator_code** | USG_DIGITAL_PAYMENT |
| **value_numeric** | 21.0 |
| **gender / location** | all / national |
| **observation_date** | 2024-12-31 |
| **source_name** | Global Findex 2025 (via Birr Metrics) |
| **source_url** | https://birrmetrics.com/49-of-ethiopians-are-banked-as-findex-2025-highlights-the-next-inclusion-challenge/ |
| **confidence** | low |
| **collected_by** | Claude (AI analyst, working with trainee) |
| **collection_date** | 2026-07-18 |
| **original_text** (as quoted from source) | "Just four percent reported borrowing, 36 percent saved in account with 21 percent using digital payments" |
| **notes** | CONFLICTS with the project brief's own figure of 'made or received digital payment ~35%'. Both are plausible Findex sub-metrics (this 21% appears to be 'used a digital payment' among account holders vs. the ~35% 'made or received digital payment' among ALL adults). Kept as low-confidence pending reconciliation -- see enrichment log and Task 2 data-quality notes; do not treat as a clean replacement for the brief's 35% figure. |

### REC_0040 — Electricity Access Rate

| Field | Value |
|---|---|
| **record_type** | observation |
| **indicator_code** | ACC_ELECTRICITY |
| **value_numeric** | 55.4 |
| **gender / location** | all / national |
| **observation_date** | 2023-12-31 |
| **source_name** | World Bank SDG7 Tracking / ESMAP |
| **source_url** | https://tradingeconomics.com/ethiopia/access-to-electricity-percent-of-population-wb-data.html |
| **confidence** | high |
| **collected_by** | Claude (AI analyst, working with trainee) |
| **collection_date** | 2026-07-18 |
| **original_text** (as quoted from source) | "Access to electricity (% of population) in Ethiopia was reported at 55.4 % in 2023, according to the World Bank collection of development indicators." |
| **notes** | Enabler/indirect-correlation variable per Enrichment Guide Sheet C (electricity access). Tagged pillar=ACCESS as a judgment call since it is a foundational infrastructure precondition, not a Findex pillar itself -- flagged explicitly as an interpretive choice in the enrichment log, consistent with the unified schema's caution against silent pillar assignment. |

### REC_0041 — Smartphone Penetration Rate

| Field | Value |
|---|---|
| **record_type** | observation |
| **indicator_code** | ACC_SMARTPHONE_PEN |
| **value_numeric** | 15.0 |
| **gender / location** | all / national |
| **observation_date** | 2024-12-31 |
| **source_name** | GSMA Mobile Gender Gap (via Birr Metrics) |
| **source_url** | https://birrmetrics.com/ethiopia-narrows-mobile-gender-gap-to-24-but-smartphone-access-for-women-remains-just-6/ |
| **confidence** | medium |
| **collected_by** | Claude (AI analyst, working with trainee) |
| **collection_date** | 2026-07-18 |
| **original_text** (as quoted from source) | "Smartphone penetration remains low, at just 15 percent of the population, and the gender gap in ownership is striking: only six percent of women own a smartphone compared to 18 percent of men a 43 percent gap." |
| **notes** | Direct enabler for USAGE per Enrichment Guide Sheet C -- smartphones are the on-ramp to app-based mobile money/digital payments (vs. basic-phone USSD access). Important because mobile phone ownership overall is high (86% men/65% women) but smartphone penetration specifically is very low, which may help explain the Usage lag despite high Access growth. |

### REC_0042 — Internet Penetration Rate

| Field | Value |
|---|---|
| **record_type** | observation |
| **indicator_code** | ACC_INTERNET_PEN |
| **value_numeric** | 21.3 |
| **gender / location** | all / national |
| **observation_date** | 2025-01-01 |
| **source_name** | DataReportal Digital 2025: Ethiopia |
| **source_url** | https://datareportal.com/reports/digital-2025-ethiopia |
| **confidence** | high |
| **collected_by** | Claude (AI analyst, working with trainee) |
| **collection_date** | 2026-07-18 |
| **original_text** (as quoted from source) | "There were 28.6 million individuals using the internet in Ethiopia at the start of 2025, when online penetration stood at 21.3 percent." |
| **notes** | Enabler/indirect-correlation variable per Enrichment Guide Sheet C (mobile internet usage). Useful leading indicator given 105M Ethiopians still offline per same source. |

### EVT_0011 — National Digital Payment Strategy 2026-2030 (NDPS 2.0) & National Instant Payment System Launch

| Field | Value |
|---|---|
| **record_type** | event |
| **indicator_code** | *(not applicable)* |
| **value_numeric** | *(not applicable)* |
| **gender / location** | *(not applicable)* / *(not applicable)* |
| **observation_date** | 2025-12-09 |
| **source_name** | National Bank of Ethiopia / Ethiopian News Agency |
| **source_url** | https://www.ena.et/web/eng/w/eng_7879526 |
| **confidence** | high |
| **collected_by** | Claude (AI analyst, working with trainee) |
| **collection_date** | 2026-07-18 |
| **original_text** (as quoted from source) | "Ethiopia's National Digital Payment Strategy (NDPS 2026-2030) and Instant Payment System launched today... at the second Ethiopia Digital Payment Conference." |
| **notes** | pillar intentionally left empty per schema (events are neutral). This is Ethiopia's successor to NFIS-II/NDPS 2021-2024 (EVT_0009), launched at the same conference as, and closely related to, the EthioPay Instant Payment System (EVT_0008, dated 2025-12-18 in the starter dataset) -- these two events likely describe overlapping developments from the same policy rollout in Dec 2025 (conference on Dec 9; EthioPay operational/press date on Dec 18). Kept as a separate record because the NDPS is the multi-year strategic policy document itself (category=policy) while EVT_0008 is the specific payment-rail infrastructure (category=infrastructure) -- flagged as a possible near-duplicate for the modeling team to review in Task 3. |

### IMP_0015 (parent: EVT_0011) — NDPS 2.0 effect on Digital Payment Adoption

| Field | Value |
|---|---|
| **record_type** | impact_link |
| **indicator_code** | *(not applicable)* |
| **value_numeric** | *(not applicable)* |
| **gender / location** | all / national |
| **observation_date** | 2025-12-09 |
| **source_name** | *(not applicable)* |
| **source_url** | *(not applicable)* |
| **confidence** | low |
| **collected_by** | Claude (AI analyst, working with trainee) |
| **collection_date** | 2026-07-18 |
| **original_text** (as quoted from source) | "*(not applicable)*" |
| **notes** | India's UPI (a comparable national instant-payments rail) drove large digital payment usage gains after launch; used as the closest available analog. Ethiopia's NDPS 2.0 targets FY2030, so effects should build gradually -- low confidence given no Ethiopian post-launch data exists yet (launched Dec 2025, dataset cutoff). |

### IMP_0016 (parent: EVT_0011) — NDPS 2.0 effect on Account Ownership

| Field | Value |
|---|---|
| **record_type** | impact_link |
| **indicator_code** | *(not applicable)* |
| **value_numeric** | *(not applicable)* |
| **gender / location** | all / national |
| **observation_date** | 2025-12-09 |
| **source_name** | *(not applicable)* |
| **source_url** | *(not applicable)* |
| **confidence** | low |
| **collected_by** | Claude (AI analyst, working with trainee) |
| **collection_date** | 2026-07-18 |
| **original_text** (as quoted from source) | "*(not applicable)*" |
| **notes** | Strategy-level policies (like NFIS-II, EVT_0009) tend to have a slower, enabling rather than direct effect on Access; modest estimate reflecting the pattern that most of NDPS 2.0's account-ownership benefit is expected to route through Usage-side products, not direct account opening. |

---

## 3. Why these additions

Reviewing the starter dataset against the project brief surfaced three concrete gaps:

1. **No `USG_DIGITAL_PAYMENT` indicator existed**, even though "Digital Payment Adoption Rate" is one of the two official forecasting targets named in the brief (Access and Usage). The starter dataset had proxies (P2P counts, Telebirr users) but not the Findex-defined Usage measure itself. This was the highest-priority gap to fill.
2. **No urban/rural or 2024 gender disaggregation for Access.** Task 2 explicitly asks to analyze the gender gap and urban/rural gap, but the starter dataset only had a 2021 gender split (REC_0004/REC_0005) and no urban/rural split at all.
3. **No infrastructure/enabler indicators** (electricity, smartphone penetration, internet penetration) beyond 4G coverage and mobile subscriptions — these are exactly the "indirect correlation" variables flagged in Enrichment Guide Sheet C as useful leading indicators.

## 4. New event (EVT_0011) — narrative summary

**National Digital Payment Strategy 2026–2030 (NDPS 2.0) & National Instant Payment System launch**, 2025-12-09, category=`policy`, source: National Bank of Ethiopia / ENA (high confidence). See Section 2 for full audit fields.

This is Ethiopia's successor to the 2021–2024 NDPS / NFIS-II era and is directly relevant to the 2025–2027 forecast window this project targets. `pillar` is left empty per schema.

## 5. New impact links (IMP_0015–IMP_0016) — narrative summary

Both link EVT_0011 to indicators, using comparable-country evidence (per Task 3 methodology) since no Ethiopian post-launch data exists yet. See Section 2 for full audit fields:
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
