# Task 4 Methodology: Forecasting Access and Usage (2025-2027)

**Full analysis, code, and all figures:** `notebooks/04_forecasting.ipynb`
**Forecast table:** `data/processed/forecast_2025_2027.csv`

## 1. Targets

- **Access — Account Ownership Rate**: % of adults with an account at a financial institution or mobile money.
- **Usage — Digital Payment Usage**: % of adults who made or received a digital payment (the project brief's
  definition; see the baseline-choice note in Section 3).

## 2. Data Available and Approach Selected

| | Historical points | Approach used |
|---|---|---|
| Access | 4 (2014, 2017, 2021, 2024) | Recent-trend (2021-2024) baseline + event-augmented adjustments + scenarios |
| Usage | 1 (2024 only) | 2024 baseline + small organic-growth assumption + event-augmented adjustment + scenarios |

Trend regression is feasible for Access but not for Usage (a single point cannot support a fitted trend).
For Access, we deliberately compare **two trend options** before choosing one:
- Full-history OLS across all 4 points: **2.71 pp/year** — driven mostly by the fast 2014-2021 growth spurt.
- Recent-trend (2021-2024 only): **1.00 pp/year** — reflects the deceleration documented in Task 2.

**The recent-trend rate is used as the baseline**, since it is far more relevant to near-term conditions;
the full-history OLS is kept only as a comparison point and as the basis for a formal (intentionally wide)
statistical prediction interval in Section 5.

## 3. Usage Baseline Choice

The enriched dataset's own `USG_DIGITAL_PAYMENT` observation is 21% (Task 1, flagged low-confidence — a
different Findex sub-metric, likely measured among account holders rather than all adults). The project
brief's own figure is ~35% ("made or received digital payment"). Per the Task 2 data-quality
recommendation, **the brief's ~35% figure is used as the 2024 baseline**, since it matches the target's
own definition; the 21% figure is not used in the forecast.

## 4. Event-Augmented Adjustments

Using Task 3's logistic-ramp functional form, each forecast adds the *incremental* (not yet realized as of
the 2024 baseline) effect of every event still ramping up during 2025-2027:

**Access:** Telebirr (using Task 3's refined, empirically-calibrated +3pp estimate), Fayda Digital ID
Rollout (+10pp literature/India-analog), NDPS 2.0 (+3pp, theoretical).

**Usage:** only one impact_link quantitatively targets this indicator — NDPS 2.0 (+10pp,
literature/India-UPI-analog, 18-month lag).

**The 0.3x haircut:** Task 3 found that the one literature-based estimate we could validate against real
Ethiopian data (Telebirr's effect on Account Ownership) overestimated the actual outcome by ~5x (predicted
+15pp vs. actual +3pp). We apply that lesson forward: every *not-yet-validated* literature/theoretical
estimate is scaled to 30% of its stated magnitude in the **base** scenario, and used at full stated
magnitude only in the **optimistic** scenario. This is an explicit judgment call, not a statistically fit
parameter, and is documented here rather than buried in the numbers.

## 5. Forecast Table

| Year | Access — Pessimistic | Access — Base | Access — Optimistic | Access Base 80% PI | Usage — Pessimistic | Usage — Base | Usage — Optimistic |
|---|---|---|---|---|---|---|---|
| 2025 | 49.5% | 51.0% | 53.3% | (45.1%, 63.4%) | 35.3% | 36.2% | 37.5% |
| 2026 | 50.0% | 53.1% | 58.0% | (47.3%, 66.6%) | 35.6% | 37.8% | 41.7% |
| 2027 | 50.5% | 54.8% | 61.4% | (49.4%, 69.9%) | 35.9% | 40.2% | 48.3% |

**Scenario definitions:**
- *Pessimistic*: Access grows at half the recent trend rate with no event effects materializing; Usage
  grows only via minimal organic drift, NDPS 2.0 fails to move the needle.
- *Base*: recent trend continues; unvalidated event estimates apply at 30% of stated magnitude.
- *Optimistic*: recent trend continues; event estimates apply at their full literature-analog magnitude.

**Uncertainty quantification, two complementary methods:**
1. A **formal 80% prediction interval** (Access only, since it's the only indicator with enough points to
   fit one) — intentionally wide (45-70% by 2027), an honest reflection of forecasting from just 4 points,
   not a computational error.
2. **Scenario ranges** for both indicators, serving as a practical uncertainty band where a formal
   statistical interval either isn't meaningful (Usage, 1 data point) or would understate true uncertainty
   if derived only from the event model (Access).

## 6. Interpretation

**What the model predicts:**
- Access reaches 51.0-53.3% by 2025 and 54.8-61.4% by 2027 (base-to-optimistic), remaining well below the
  NFIS-II policy target of 70% by end-2025 under every scenario modeled, including optimistic.
- Usage reaches 36.2-37.5% by 2025 and 40.2-48.3% by 2027, with almost all growth beyond simple organic
  drift attributable to a single, still-unobserved policy event (NDPS 2.0).

**Events with the largest potential impact:**
- **Fayda Digital ID Rollout** — the single largest lever for Access (up to +7.9pp by 2027 optimistic),
  plausibly because national digital ID removes a genuine KYC/onboarding barrier, a more direct mechanism
  than a payments app launch.
- **NDPS 2.0** — the largest lever for Usage, but also the most speculative: launched only weeks before
  this dataset's cutoff, so its entire effect here is extrapolated from India's UPI experience with zero
  Ethiopian data to check it against.

**Key uncertainties:**
1. The Usage forecast rests on a single 2024 baseline value and a single quantified event driver — the
   weakest link in this task. A different NDPS 2.0 rollout speed, or a revision to the 35%-vs-21% Findex
   conflict, would move this forecast substantially.
2. The 0.3x haircut is a judgment call motivated by one validated case, not a statistically estimated
   parameter.
3. Effects are combined additively across events (per Task 3), which likely overstates the true combined
   effect on Access as three events all ramp up in the same window — the real effect probably saturates
   below the simple sum.
4. The formal 80% prediction interval is uncomfortably wide — presented deliberately rather than hidden,
   as the honest cost of forecasting from 4 historical points.
