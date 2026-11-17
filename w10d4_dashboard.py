from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from w10d4_forecasting import REPORT_DIR, run_analysis

st.set_page_config(
    page_title="W10D4 Forecasting Dashboard",
    page_icon="📈",
    layout="wide",
)

st.title("Indian Business Sales — Forecasting Dashboard")
st.caption(
    "W10D4 | Holt-Winters forecasting | Plotly + Streamlit"
)

@st.cache_data(show_spinner="Loading data and fitting forecasting models...")
def get_analysis(horizon):
    return run_analysis(horizon=horizon)


with st.sidebar:
    st.header("Dashboard settings")
    horizon = st.slider(
        "Future forecast horizon (days)",
        min_value=7,
        max_value=30,
        value=14,
        step=1,
    )
    st.caption("Holdout validation remains fixed at 14 days.")

try:
    result = get_analysis(horizon)
except Exception as exc:
    st.error(f"Could not build the forecast: {exc}")
    st.stop()

daily = result["daily"]
validation = result["validation"]
future = result["future"]
metrics = result["metrics"]
diagnostics = result["diagnostics"]

st.subheader("Forecast validation performance")
c1, c2, c3, c4 = st.columns(4)
c1.metric("MAE", f"{metrics['mae']:,.2f}")
c2.metric("RMSE", f"{metrics['rmse']:,.2f}")
c3.metric(
    "MAPE",
    "N/A" if metrics["mape_percent"] is None
    else f"{metrics['mape_percent']:.2f}%",
)
c4.metric(
    "WAPE",
    "N/A" if metrics["wape_percent"] is None
    else f"{metrics['wape_percent']:.2f}%",
)

st.caption(
    f"Validation: {metrics['validation_observations']} days | "
    f"MAPE calculated on {metrics['mape_observations']} non-zero actual days"
)

st.subheader("Historical amounts, holdout forecast and future forecast")
date_range = st.date_input(
    "Historical date range",
    value=(daily.index.min().date(), daily.index.max().date()),
    min_value=daily.index.min().date(),
    max_value=daily.index.max().date(),
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = daily.index.min().date(), daily.index.max().date()

visible = daily.loc[
    (daily.index.date >= start_date) & (daily.index.date <= end_date)
]

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=visible.index,
    y=visible.values,
    mode="lines",
    name="Actual recorded amount",
    line=dict(width=2),
))
fig.add_trace(go.Scatter(
    x=validation.index,
    y=validation["forecast_amount"],
    mode="lines+markers",
    name="14-day holdout forecast",
    line=dict(dash="dash"),
))
fig.add_trace(go.Scatter(
    x=future.index,
    y=future["forecast_amount"],
    mode="lines+markers",
    name="Future forecast",
    line=dict(dash="dot"),
))
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Recorded order amount (Amount column units)",
    hovermode="x unified",
    legend_title="Series",
    height=520,
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Forecast data")
left, right = st.columns(2)
with left:
    st.markdown("**Holdout validation**")
    st.dataframe(validation.round(2), use_container_width=True)
with right:
    st.markdown("**Future forecast**")
    st.dataframe(future.round(2), use_container_width=True)

st.subheader("Data quality")
q1, q2, q3 = st.columns(3)
q1.metric("Source rows", f"{diagnostics['source_rows']:,}")
q2.metric("Missing Amount values", f"{diagnostics['missing_amounts']:,}")
q3.metric("Daily observations", diagnostics["daily_observations"])

st.info(
    "Interpretation: Amount is the dataset's recorded order amount, "
    "not verified net revenue. Missing Amount values are excluded from "
    "daily sums. This dataset contains only 91 days, so forecasts are "
    "estimates and should be interpreted cautiously."
)

st.subheader("Download evidence")
st.download_button(
    "Download validation CSV",
    data=validation.to_csv(index_label="date"),
    file_name="validation_forecast.csv",
    mime="text/csv",
)
st.download_button(
    "Download future forecast CSV",
    data=future.to_csv(index_label="date"),
    file_name="future_forecast.csv",
    mime="text/csv",
)
st.download_button(
    "Download daily history CSV",
    data=daily.to_csv(index_label="date", header=["recorded_order_amount"]),
    file_name="daily_recorded_amount.csv",
    mime="text/csv",
)

st.caption(f"Evidence files are also saved locally in: {REPORT_DIR}")
