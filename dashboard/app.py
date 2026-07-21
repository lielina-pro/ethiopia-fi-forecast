"""
Ethiopia Financial Inclusion Forecasting -- Streamlit Dashboard

Run locally with:
    streamlit run dashboard/app.py

Reads from data/processed/ (enriched dataset, forecast table, refined impact estimates) via
src/data_loader.py, which validates the data on load and raises a clear error if something is
missing or malformed (see the "Data could not be loaded" message below if that happens).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import (
    load_unified_data,
    get_observations,
    get_events,
    get_impact_links,
    get_targets,
    DataLoadError,
)

DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

st.set_page_config(
    page_title="Ethiopia Financial Inclusion Forecast",
    page_icon="\U0001F1EA\U0001F1F9",
    layout="wide",
)


# ----------------------------------------------------------------------------
# Data loading (cached, with graceful error handling)
# ----------------------------------------------------------------------------
@st.cache_data
def load_all_data():
    df = load_unified_data(path=DATA_PROCESSED / "enriched_dataset.csv")
    obs = get_observations(df)
    obs["observation_date"] = pd.to_datetime(obs["observation_date"])
    events = get_events(df)
    events["observation_date"] = pd.to_datetime(events["observation_date"])
    links = get_impact_links(df)
    targets = get_targets(df)
    return df, obs, events, links, targets


@st.cache_data
def load_forecast():
    path = DATA_PROCESSED / "forecast_2025_2027.csv"
    if not path.exists():
        raise DataLoadError(
            f"Forecast file not found at '{path}'. Run notebooks/04_forecasting.ipynb first "
            f"to generate it."
        )
    return pd.read_csv(path)


@st.cache_data
def load_refined_estimates():
    path = DATA_PROCESSED / "refined_impact_estimates.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


try:
    unified_df, obs, events, links, targets = load_all_data()
    forecast_df = load_forecast()
    refined_df = load_refined_estimates()
except DataLoadError as e:
    st.error(
        f"**Data could not be loaded.**\n\n{e}\n\n"
        f"Make sure `data/processed/enriched_dataset.csv` and "
        f"`data/processed/forecast_2025_2027.csv` exist (run the Task 1-4 notebooks first if this "
        f"is a fresh clone) and that you're running Streamlit from the project root."
    )
    st.stop()
except Exception as e:  # noqa: BLE001 -- surface any other unexpected error clearly rather than a blank page
    st.error(f"**Unexpected error while loading data:** {e}")
    st.stop()


# ----------------------------------------------------------------------------
# Shared helpers
# ----------------------------------------------------------------------------
def get_series(indicator_code, gender="all", location="national"):
    """Get a clean, sorted time series for one indicator."""
    sub = obs[obs["indicator_code"] == indicator_code].copy()
    if gender is not None and "gender" in sub.columns:
        sub = sub[(sub["gender"] == gender) | (sub["gender"].isna())]
    if location is not None and "location" in sub.columns:
        loc_matches = sub[sub["location"] == location]
        if not loc_matches.empty:
            sub = loc_matches
    return sub.sort_values("observation_date")


def latest_value(indicator_code, gender="all", location="national"):
    s = get_series(indicator_code, gender, location)
    if s.empty:
        return None, None
    row = s.iloc[-1]
    return row["value_numeric"], row["observation_date"]


INDICATOR_LABELS = dict(zip(obs["indicator_code"], obs["indicator"]))


# ----------------------------------------------------------------------------
# Sidebar navigation + data download
# ----------------------------------------------------------------------------
st.sidebar.title("\U0001F1EA\U0001F1F9 Ethiopia FI Forecast")
page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Trends", "Forecasts", "Inclusion Projections"],
)

st.sidebar.divider()
st.sidebar.subheader("Download data")
st.sidebar.download_button(
    "Enriched dataset (CSV)",
    data=unified_df.to_csv(index=False).encode("utf-8"),
    file_name="ethiopia_fi_enriched_dataset.csv",
    mime="text/csv",
)
st.sidebar.download_button(
    "Forecast table (CSV)",
    data=forecast_df.to_csv(index=False).encode("utf-8"),
    file_name="forecast_2025_2027.csv",
    mime="text/csv",
)
st.sidebar.caption(
    "Data as of the Task 1-4 analysis. See `data/data_enrichment_log.md` and "
    "`reports/task3_methodology.md` / `task4_methodology.md` for full sourcing and methodology."
)


# ----------------------------------------------------------------------------
# PAGE 1: Overview
# ----------------------------------------------------------------------------
if page == "Overview":
    st.title("Overview")
    st.caption("Ethiopia's financial inclusion trajectory at a glance.")

    acc_val, acc_date = latest_value("ACC_OWNERSHIP")
    acc_series = get_series("ACC_OWNERSHIP")
    acc_prev = acc_series.iloc[-2]["value_numeric"] if len(acc_series) > 1 else None
    mm_val, mm_date = latest_value("ACC_MM_ACCOUNT")
    mm_series = get_series("ACC_MM_ACCOUNT")
    mm_prev = mm_series.iloc[-2]["value_numeric"] if len(mm_series) > 1 else None
    crossover_val, crossover_date = latest_value("USG_CROSSOVER")

    usg_row = obs[(obs["indicator_code"] == "USG_DIGITAL_PAYMENT") & (obs["gender"] == "all")]
    usg_val = usg_row["value_numeric"].iloc[0] if not usg_row.empty else None

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "Account Ownership (Access)",
            f"{acc_val:.0f}%" if acc_val is not None else "n/a",
            delta=f"+{acc_val - acc_prev:.0f}pp since 2021" if acc_prev is not None else None,
        )
        st.caption(f"As of {acc_date.strftime('%b %Y')}" if acc_date is not None else "")
    with col2:
        st.metric(
            "Digital Payment Usage",
            f"{usg_val:.0f}%" if usg_val is not None else "n/a",
            help="Project brief's headline definition: % who made/received a digital payment, 2024.",
        )
        st.caption("As of 2024 (single data point -- see Trends page)")
    with col3:
        st.metric(
            "Mobile Money Accounts",
            f"{mm_val:.2f}%" if mm_val is not None else "n/a",
            delta=f"+{mm_val - mm_prev:.2f}pp since 2021" if mm_prev is not None else None,
        )
        st.caption(f"As of {mm_date.strftime('%b %Y')}" if mm_date is not None else "")
    with col4:
        st.metric(
            "P2P / ATM Crossover Ratio",
            f"{crossover_val:.2f}x" if crossover_val is not None else "n/a",
            help="Ratio of P2P mobile-money transaction volume to ATM transaction volume. "
                 ">1 means P2P transactions now exceed ATM transactions.",
        )
        st.caption(
            f"As of {crossover_date.strftime('%b %Y')} -- "
            f"{'P2P now exceeds ATM volume' if crossover_val and crossover_val > 1 else 'ATM still exceeds P2P volume'}"
        )

    st.divider()
    st.subheader("Growth rate is decelerating, not accelerating")
    acc_hist = get_series("ACC_OWNERSHIP")
    acc_hist = acc_hist.assign(year=acc_hist["observation_date"].dt.year)
    growth_years = acc_hist["year"].values
    growth_vals = acc_hist["value_numeric"].values
    rates = []
    for i in range(1, len(growth_years)):
        rate = (growth_vals[i] - growth_vals[i - 1]) / (growth_years[i] - growth_years[i - 1])
        rates.append({"period": f"{growth_years[i-1]}-{growth_years[i]}", "pp_per_year": round(rate, 2)})
    rates_df = pd.DataFrame(rates)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        fig = px.bar(
            rates_df, x="period", y="pp_per_year",
            title="Account Ownership: Annualized Growth Rate Between Survey Waves",
            labels={"pp_per_year": "pp gained per year", "period": "Period"},
            color_discrete_sequence=["#2E5266"],
        )
        fig.update_layout(height=380)
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        st.markdown(
            """
            **What this means:** growth fell from **4.33 pp/year** (2014-17) to **2.75 pp/year** (2017-21)
            to just **1.00 pp/year** (2021-24) -- even as Telebirr and M-Pesa launched in that final
            period. See the Task 2 EDA notebook for the full analysis behind this finding.

            **Biggest current gaps:**
            - Gender gap in account ownership: **18 percentage points** (2024), barely down from 20pp in 2021.
            - Registered-vs-active gap: M-Pesa's 90-day active rate is only **66%** of its registered user base.
            - Smartphone penetration is only **15%**, vs. 70.8% 4G network coverage -- a likely bottleneck
              on Usage growth that network investment alone won't fix.
            """
        )


# ----------------------------------------------------------------------------
# PAGE 2: Trends
# ----------------------------------------------------------------------------
elif page == "Trends":
    st.title("Trends")
    st.caption("Explore any indicator's full history, and compare channels directly.")

    indicator_options = sorted(INDICATOR_LABELS.items(), key=lambda x: x[1])
    label_to_code = {v: k for k, v in indicator_options}

    col1, col2 = st.columns([2, 1])
    with col1:
        selected_label = st.selectbox(
            "Choose an indicator",
            options=[v for _, v in indicator_options],
            index=[v for _, v in indicator_options].index("Account Ownership Rate"),
        )
    selected_code = label_to_code[selected_label]
    series = get_series(selected_code, gender=None, location=None)

    if series.empty:
        st.warning(f"No observations found for {selected_label}.")
    else:
        min_date, max_date = series["observation_date"].min(), series["observation_date"].max()
        with col2:
            if min_date < max_date:
                date_range = st.slider(
                    "Date range",
                    min_value=min_date.to_pydatetime(),
                    max_value=max_date.to_pydatetime(),
                    value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
                )
            else:
                date_range = (min_date.to_pydatetime(), max_date.to_pydatetime())
                st.caption("Only one observation exists for this indicator -- no range to select.")

        filtered = series[
            (series["observation_date"] >= date_range[0]) & (series["observation_date"] <= date_range[1])
        ]

        fig = px.line(
            filtered, x="observation_date", y="value_numeric", markers=True,
            title=f"{selected_label} Over Time",
            labels={"value_numeric": filtered["unit"].iloc[0] if not filtered.empty and pd.notna(filtered["unit"].iloc[0]) else "value",
                     "observation_date": "Date"},
        )
        # Overlay event markers relevant to this indicator
        related_events = links[links["related_indicator"] == selected_code].merge(
            events[["record_id", "indicator", "observation_date"]].rename(
                columns={"observation_date": "event_date", "indicator": "event_name"}
            ),
            left_on="parent_id", right_on="record_id",
        )
        for _, ev in related_events.iterrows():
            fig.add_vline(x=ev["event_date"].timestamp() * 1000, line_dash="dash", line_color="gray", opacity=0.5)
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)

        if not related_events.empty:
            st.caption(
                "Dashed lines mark events with a modeled effect on this indicator: "
                + ", ".join(related_events["event_name"].unique())
            )

        with st.expander("View underlying data"):
            st.dataframe(
                filtered[["observation_date", "value_numeric", "gender", "location", "source_name", "confidence"]],
                use_container_width=True,
            )

    st.divider()
    st.subheader("Channel comparison: P2P vs. ATM transaction volume")
    p2p = get_series("USG_P2P_COUNT", gender=None, location=None)
    atm = get_series("USG_ATM_COUNT", gender=None, location=None)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=p2p["observation_date"], y=p2p["value_numeric"] / 1e6,
                               mode="lines+markers", name="P2P Transactions (M)", line=dict(color="#3A7D44")))
    fig2.add_trace(go.Scatter(x=atm["observation_date"], y=atm["value_numeric"] / 1e6,
                               mode="lines+markers", name="ATM Transactions (M)", line=dict(color="#6E8898")))
    fig2.update_layout(title="P2P vs. ATM Transaction Volume", yaxis_title="Transactions (millions)", height=420)
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(
        "P2P transaction volume overtook ATM volume for the first time in 2025 (crossover ratio 1.08x) -- "
        "the clearest visible shift toward mobile-money-first payment behavior in the dataset."
    )


# ----------------------------------------------------------------------------
# PAGE 3: Forecasts
# ----------------------------------------------------------------------------
elif page == "Forecasts":
    st.title("Forecasts")
    st.caption("2025-2027 projections for Access and Usage. See reports/task4_methodology.md for full methodology.")

    scenario = st.selectbox("Scenario", ["Base", "Pessimistic", "Optimistic"], index=0)
    scenario_key = scenario.lower()

    acc_hist = get_series("ACC_OWNERSHIP")
    usg_hist = obs[(obs["indicator_code"] == "USG_DIGITAL_PAYMENT") & (obs["gender"] == "all")]

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=acc_hist["observation_date"].dt.year, y=acc_hist["value_numeric"],
                                   mode="lines+markers", name="Observed", line=dict(color="#2E5266", width=3)))
        forecast_years = forecast_df["year"]
        fig.add_trace(go.Scatter(
            x=[2024] + list(forecast_years), y=[acc_hist["value_numeric"].iloc[-1]] + list(forecast_df[f"access_{scenario_key}"]),
            mode="lines+markers", name=f"{scenario} forecast", line=dict(color="#3A7D44", dash="dash"),
        ))
        if "access_base_80pct_PI_low" in forecast_df.columns:
            fig.add_trace(go.Scatter(
                x=list(forecast_years) + list(forecast_years[::-1]),
                y=list(forecast_df["access_base_80pct_PI_high"]) + list(forecast_df["access_base_80pct_PI_low"][::-1]),
                fill="toself", fillcolor="rgba(150,150,150,0.2)", line=dict(color="rgba(0,0,0,0)"),
                name="80% prediction interval", showlegend=True,
            ))
        fig.add_hline(y=70, line_dash="dot", line_color="purple", annotation_text="NFIS-II target: 70% by 2025")
        fig.update_layout(title="Access: Account Ownership Forecast", yaxis_title="% of adults with an account", height=450)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=usg_hist["observation_date"].dt.year, y=usg_hist["value_numeric"],
                                    mode="markers", name="Observed baseline (2024)", marker=dict(size=12, color="#2E5266")))
        fig2.add_trace(go.Scatter(
            x=[2024] + list(forecast_years), y=[35.0] + list(forecast_df[f"usage_{scenario_key}"]),
            mode="lines+markers", name=f"{scenario} forecast", line=dict(color="#3A7D44", dash="dash"),
        ))
        fig2.update_layout(title="Usage: Digital Payment Adoption Forecast", yaxis_title="% of adults using digital payments", height=450)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("Key projected milestones")
    m1, m2, m3 = st.columns(3)
    access_2027 = forecast_df.loc[forecast_df["year"] == 2027, f"access_{scenario_key}"].iloc[0]
    usage_2027 = forecast_df.loc[forecast_df["year"] == 2027, f"usage_{scenario_key}"].iloc[0]
    m1.metric("Access by 2027", f"{access_2027:.1f}%")
    m2.metric("Usage by 2027", f"{usage_2027:.1f}%")
    gap_to_target = 70 - access_2027
    m3.metric("Gap to NFIS-II 70% target", f"{gap_to_target:.1f}pp short", delta_color="inverse")

    st.caption(
        "Every scenario, including optimistic, falls short of the NFIS-II 70%-by-2025 Access target -- "
        "see reports/task4_methodology.md, Section 6, for the full interpretation."
    )

    with st.expander("View full forecast table"):
        st.dataframe(forecast_df, use_container_width=True)

    if refined_df is not None:
        with st.expander("View refined impact estimates (Task 3 calibration)"):
            st.dataframe(refined_df, use_container_width=True)


# ----------------------------------------------------------------------------
# PAGE 4: Inclusion Projections
# ----------------------------------------------------------------------------
elif page == "Inclusion Projections":
    st.title("Inclusion Projections")
    st.caption("Progress toward a financial inclusion target, under different scenarios.")

    col_a, col_b = st.columns(2)
    with col_a:
        target_pct = st.slider(
            "Target threshold (%)", min_value=40, max_value=90, value=60, step=5,
            help="Default 60%, adjustable. Ethiopia's own official NFIS-II target is 70% by end-2025 "
                 "(shown as a fixed reference line regardless of this slider).",
        )
    with col_b:
        scenario2 = st.selectbox("Scenario", ["Base", "Pessimistic", "Optimistic"], index=0, key="scenario2")
    scenario2_key = scenario2.lower()

    acc_hist = get_series("ACC_OWNERSHIP")
    forecast_years = list(forecast_df["year"])
    forecast_vals = list(forecast_df[f"access_{scenario2_key}"])
    all_years = list(acc_hist["observation_date"].dt.year) + forecast_years
    all_vals = list(acc_hist["value_numeric"]) + forecast_vals

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=all_years[:len(acc_hist)], y=all_vals[:len(acc_hist)],
                               mode="lines+markers", name="Observed", line=dict(color="#2E5266", width=3)))
    fig.add_trace(go.Scatter(x=[all_years[len(acc_hist)-1]] + all_years[len(acc_hist):],
                               y=[all_vals[len(acc_hist)-1]] + all_vals[len(acc_hist):],
                               mode="lines+markers", name=f"{scenario2} forecast", line=dict(color="#3A7D44", dash="dash")))
    fig.add_hline(y=target_pct, line_dash="dash", line_color="orange", annotation_text=f"Custom target: {target_pct}%")
    fig.add_hline(y=70, line_dash="dot", line_color="purple", annotation_text="Official NFIS-II target: 70% (2025)")
    fig.update_layout(title="Account Ownership: Progress Toward Target", yaxis_title="% of adults with an account", height=450)
    st.plotly_chart(fig, use_container_width=True)

    # Progress bar toward custom target
    current_access = acc_hist["value_numeric"].iloc[-1]
    progress = min(current_access / target_pct, 1.0)
    st.progress(progress, text=f"Currently at {current_access:.0f}% of {target_pct}% target ({progress*100:.0f}% of the way there)")

    proj_2027 = forecast_df.loc[forecast_df["year"] == 2027, f"access_{scenario2_key}"].iloc[0]
    if proj_2027 >= target_pct:
        st.success(f"Under the **{scenario2}** scenario, the {target_pct}% target is reached by 2027 (projected: {proj_2027:.1f}%).")
    else:
        st.warning(f"Under the **{scenario2}** scenario, the {target_pct}% target is **not** reached by 2027 (projected: {proj_2027:.1f}%, {target_pct - proj_2027:.1f}pp short).")

    st.divider()
    st.subheader("Answers to the consortium's key questions")
    st.markdown(
        f"""
        **Will Ethiopia reach the official 70%-by-2025 NFIS-II target?**
        No, under any scenario modeled. Even the optimistic case reaches only ~53% by 2025 and ~61% by 2027
        -- roughly 9-19pp short, three years past the original deadline.

        **What single event would move the needle most on Access?**
        The Fayda Digital ID rollout is the largest lever in the model (up to +7.9pp by 2027, optimistic
        scenario) -- plausibly because national digital ID removes a genuine KYC/onboarding barrier, a more
        direct mechanism than a payments app launch.

        **Is the gender gap closing?**
        Barely. Account ownership's gender gap moved from 20pp (2021) to 18pp (2024) -- a 2pp improvement
        over three years of major fintech launches. No current forecast in this dashboard models the gender
        gap separately; closing it will likely require a targeted intervention, not just aggregate growth.

        **What's the biggest risk to the Usage forecast specifically?**
        The Usage forecast leans on a single 2024 baseline value and a single quantified event driver (NDPS
        2.0, launched only weeks before this dataset's cutoff, modeled entirely off India's UPI experience
        with zero Ethiopian data to check it against). Treat the Usage numbers on this page as considerably
        less certain than the Access numbers.
        """
    )
