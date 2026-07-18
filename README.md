# Ethiopia Financial Inclusion Forecasting

Forecasting system for Ethiopia's digital financial transformation, built for a consortium of
development finance institutions, mobile money operators, and the National Bank of Ethiopia.

Forecasts two Global Findex-defined dimensions for 2025–2027:
1. **Access** — Account Ownership Rate
2. **Usage** — Digital Payment Adoption Rate

## Project status

- [x] Task 1 — Data Exploration & Enrichment
- [ ] Task 2 — Exploratory Data Analysis
- [ ] Task 3 — Event Impact Modeling
- [ ] Task 4 — Forecasting Access and Usage
- [ ] Task 5 — Dashboard Development

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

Enrichment additions (9 new observations, 1 new event, 2 new impact_links, all sourced) are documented
in `data/data_enrichment_log.md`, including data-quality conflicts found during enrichment.

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the dashboard (once Task 5 is complete)

```bash
streamlit run dashboard/app.py
```

## Team

Built for the 10 Academy KAIM 9 Week 11 challenge (15–21 Jul 2026).
