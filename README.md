# Ethiopia Financial Inclusion Forecasting

Forecasting system for Ethiopia's digital financial transformation, built for a consortium of
development finance institutions, mobile money operators, and the National Bank of Ethiopia.

Forecasts two Global Findex-defined dimensions for 2025–2027:
1. **Access** — Account Ownership Rate
2. **Usage** — Digital Payment Adoption Rate

## Project status

- [x] Task 1 — Data Exploration & Enrichment
- [x] Task 2 — Exploratory Data Analysis
- [x] Task 3 — Event Impact Modeling
- [x] Task 4 — Forecasting Access and Usage
- [x] Task 5 — Dashboard Development

## Repository structure

```
ethiopia-fi-forecast/
├── .github/workflows/       # CI (unit tests)
├── data/
│   ├── raw/                 # Starter dataset + reference codes (unmodified except enrichment)
│   ├── processed/           # Analysis-ready data
│   └── data_enrichment_log.md
├── notebooks/                # Analysis notebooks (Task 2+)
├── src/                       # Reusable Python modules
├── dashboard/                 # Streamlit app (Task 5)
├── tests/                     # Unit tests
├── models/                    # Saved forecasting models (Task 4)
├── reports/figures/           # Exported charts for the final report
├── requirements.txt
└── README.md
```

## Data

`data/raw/ethiopia_fi_unified_data.csv` uses a **unified schema**: every row (observation, event,
impact_link, or target) shares the same columns; `record_type` tells you how to interpret it.
See `data/raw/SCHEMA_README.md` for the full schema design rationale and `data/raw/reference_codes.csv`
for valid values of every categorical field.

**Task 1 deliverables, explicitly:**
- `data/raw/ethiopia_fi_unified_data_original_starter.csv` — the untouched 57-record starter dataset (kept for before/after comparison).
- `data/processed/enriched_dataset.csv` — the final 69-record enriched dataset (starter + 12 new, sourced records) used by all analysis from Task 2 onward.
- `data/data_enrichment_log.md` — the full audit trail: every new record's `source_url`, verbatim `original_text`, `confidence`, `collected_by`, `collection_date`, and `notes`, plus the data-quality conflicts found during enrichment.

### Error handling

`src/data_loader.py` validates the dataset on load (missing file, empty file, missing required columns,
unrecognized `record_type` values, duplicate `record_id`s) and raises a `DataLoadError` with an actionable
message rather than failing silently or downstream. See `tests/test_data_loader.py` for the covered failure
modes.

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the dashboard

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

This opens a browser tab at `http://localhost:8501`. Requires `data/processed/enriched_dataset.csv` and
`data/processed/forecast_2025_2027.csv` to exist (both are already committed; regenerate them by running
`notebooks/01`-`04` in order if you ever need to rebuild from scratch).

**Pages:**
- **Overview** — key metric cards (Access, Usage, Mobile Money Accounts, P2P/ATM Crossover Ratio) and the
  Access growth-deceleration chart.
- **Trends** — pick any of the dataset's ~24 indicators, filter by date range, and see cataloged events
  overlaid on the chart; plus a dedicated P2P-vs-ATM channel comparison.
- **Forecasts** — 2025-2027 projections for Access and Usage under three scenarios (Pessimistic / Base /
  Optimistic), with a formal 80% prediction interval band for Access.
- **Inclusion Projections** — an adjustable target-threshold slider (default 60%, official NFIS-II target
  70% shown as a fixed reference line), a progress bar, and written answers to the consortium's key
  questions.

All four pages include a CSV download option in the sidebar (enriched dataset + forecast table).

## Team

Built for the 10 Academy KAIM 9 Week 11 challenge (15–21 Jul 2026).
