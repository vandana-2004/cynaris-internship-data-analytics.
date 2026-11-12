from pathlib import Path
import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from w10d4_forecasting import run_analysis
from w10d5_eda import run_eda, REPORT_DIR as EDA_REPORT_DIR

st.set_page_config(
    page_title="W10D5 Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("Indian Business Sales — Intelligence Dashboard")
st.caption(
    "W10D5 | Exploratory analysis + Holt-Winters forecasting | "
    "Historical 2022 dataset"
)


@st.cache_data(show_spinner="Analyzing business data...")
def get_eda():
    return run_eda()


@st.cache_data(show_spinner="Fitting forecasting model...")
def get_forecast(horizon):
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
    st.caption("Forecast validation uses a fixed 14-day holdout.")

try:
    eda = get_eda()
    forecast = get_forecast(horizon)
except Exception as exc:
    st.error(f"Dashboard analysis failed: {exc}")
    st.stop()

quality = eda["quality"]
metrics = forecast["metrics"]
daily = forecast["daily"]
validation = forecast["validation"]
future = forecast["future"]

# ---------------------------------------------------------------------
# Business overview
# ---------------------------------------------------------------------
st.header("1. Business overview")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Source rows", f"{quality['source_rows']:,}")
k2.metric("Recorded Amount", f"{quality['recorded_amount_total']:,.2f}")
k3.metric("Total quantity", f"{quality['quantity_total']:,.0f}")
k4.metric("Daily observations", f"{quality['daily_observations']:,}")

k5, k6, k7, k8 = st.columns(4)
k5.metric("Average Amount per row", f"{quality['recorded_amount_average']:,.2f}")
k6.metric("Amount coverage", f"{quality['amount_coverage_percent']:.2f}%")
k7.metric("Cancelled-status rows", f"{quality['cancelled_rows']:,}")
k8.metric("Exact duplicate rows", f"{quality['duplicate_rows']:,}")

st.caption(
    f"Dataset period: {quality['date_start']} to {quality['date_end']} | "
    f"{quality['category_count']} categories | "
    f"{quality['normalized_state_count']} normalized state values"
)

# ---------------------------------------------------------------------
# Date filtering
# ---------------------------------------------------------------------
st.header("2. Historical business trends")

data = eda["data"]
min_date = data["Date"].min().date()
max_date = data["Date"].max().date()

selected_dates = st.date_input(
    "Select analysis date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date, end_date = min_date, max_date

category_options = sorted(data["Category"].dropna().unique().tolist())
state_options = sorted(data["ship-state"].dropna().unique().tolist())

selected_categories = st.multiselect(
    "Filter categories",
    options=category_options,
    default=category_options,
)

selected_states = st.multiselect(
    "Filter states",
    options=state_options,
    default=state_options,
)

filtered = data.loc[
    data["Date"].between(
        pd.Timestamp(start_date),
        pd.Timestamp(end_date),
    )
    & data["Category"].isin(selected_categories)
    & data["ship-state"].isin(selected_states)
].copy()

if filtered.empty:
    st.warning("No records match the selected date, category, and state filters.")
    st.stop()

daily_filtered = (
    filtered.dropna(subset=["Date"])
    .groupby("Date")
    .agg(
        recorded_amount=("Amount", "sum"),
        quantity=("Qty", "sum"),
        order_rows=("Order ID", "size"),
    )
    .reset_index()
)

monthly_filtered = (
    filtered.dropna(subset=["Date"])
    .assign(month=lambda x: x["Date"].dt.to_period("M").astype(str))
    .groupby("month", as_index=False)
    .agg(
        recorded_amount=("Amount", "sum"),
        quantity=("Qty", "sum"),
        order_rows=("Order ID", "size"),
    )
)

left, right = st.columns(2)

with left:
    st.subheader("Daily recorded amount")
    daily_fig = px.line(
        daily_filtered,
        x="Date",
        y="recorded_amount",
        markers=True,
        labels={
            "Date": "Date",
            "recorded_amount": "Recorded Amount",
        },
    )
    daily_fig.update_layout(height=380)
    st.plotly_chart(daily_fig, width="stretch")

with right:
    st.subheader("Monthly recorded amount")
    monthly_fig = px.bar(
        monthly_filtered,
        x="month",
        y="recorded_amount",
        labels={
            "month": "Month",
            "recorded_amount": "Recorded Amount",
        },
        text_auto=".2s",
    )
    monthly_fig.update_layout(height=380)
    st.plotly_chart(monthly_fig, width="stretch")

# ---------------------------------------------------------------------
# Category and geographic performance
# ---------------------------------------------------------------------
st.header("3. Category and state performance")

category_filtered = (
    filtered.groupby("Category", as_index=False)
    .agg(
        recorded_amount=("Amount", "sum"),
        order_rows=("Order ID", "size"),
        quantity=("Qty", "sum"),
    )
    .sort_values("recorded_amount", ascending=False)
)

state_filtered = (
    filtered.groupby("ship-state", as_index=False)
    .agg(
        recorded_amount=("Amount", "sum"),
        order_rows=("Order ID", "size"),
    )
    .query("`ship-state` != 'UNKNOWN'")
    .sort_values("recorded_amount", ascending=False)
)

left, right = st.columns(2)

with left:
    st.subheader("Category performance")
    category_fig = px.bar(
        category_filtered,
        x="recorded_amount",
        y="Category",
        orientation="h",
        labels={
            "recorded_amount": "Recorded Amount",
            "Category": "Category",
        },
    )
    category_fig.update_layout(
        height=430,
        yaxis={"categoryorder": "total ascending"},
    )
    st.plotly_chart(category_fig, width="stretch")

with right:
    st.subheader("Top 10 states")
    state_fig = px.bar(
        state_filtered.head(10).sort_values("recorded_amount"),
        x="recorded_amount",
        y="ship-state",
        orientation="h",
        labels={
            "recorded_amount": "Recorded Amount",
            "ship-state": "State",
        },
    )
    state_fig.update_layout(
        height=430,
        yaxis={"categoryorder": "total ascending"},
    )
    st.plotly_chart(state_fig, width="stretch")

# ---------------------------------------------------------------------
# Fulfilment and order status
# ---------------------------------------------------------------------
st.header("4. Fulfilment and order status")

left, right = st.columns(2)

with left:
    st.subheader("Fulfilment distribution")
    fulfilment = (
        filtered["Fulfilment"]
        .value_counts()
        .rename_axis("Fulfilment")
        .reset_index(name="order_rows")
    )
    fulfilment_fig = px.pie(
        fulfilment,
        names="Fulfilment",
        values="order_rows",
        hole=0.4,
    )
    fulfilment_fig.update_layout(height=380)
    st.plotly_chart(fulfilment_fig, width="stretch")

with right:
    st.subheader("Order status distribution")
    status = (
        filtered["Status"]
        .value_counts()
        .rename_axis("Status")
        .reset_index(name="order_rows")
        .sort_values("order_rows", ascending=True)
    )
    status_fig = px.bar(
        status,
        x="order_rows",
        y="Status",
        orientation="h",
        labels={
            "order_rows": "Order rows",
            "Status": "Status",
        },
    )
    status_fig.update_layout(height=430)
    st.plotly_chart(status_fig, width="stretch")

# ---------------------------------------------------------------------
# Forecasting
# ---------------------------------------------------------------------
st.header("5. Forecast validation and future outlook")
st.caption(
    "Forecast uses the complete historical series and is independent "
    "of the selected EDA date filter."
)

st.markdown(
    "**Model:** Holt-Winters additive trend and additive weekly "
    "seasonality (7-day period)."
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("MAE", f"{metrics['mae']:,.2f}")
m2.metric("RMSE", f"{metrics['rmse']:,.2f}")
m3.metric(
    "MAPE",
    "N/A" if metrics["mape_percent"] is None
    else f"{metrics['mape_percent']:.2f}%",
)
m4.metric(
    "WAPE",
    "N/A" if metrics["wape_percent"] is None
    else f"{metrics['wape_percent']:.2f}%",
)

st.caption(
    f"Holdout: {metrics['validation_observations']} days | "
    f"MAPE observations: {metrics['mape_observations']} non-zero actual days"
)

forecast_fig = go.Figure()

forecast_fig.add_trace(go.Scatter(
    x=daily.index,
    y=daily.values,
    mode="lines",
    name="Historical recorded amount",
))

forecast_fig.add_trace(go.Scatter(
    x=validation.index,
    y=validation["forecast_amount"],
    mode="lines+markers",
    name="14-day holdout forecast",
    line=dict(dash="dash"),
))

forecast_fig.add_trace(go.Scatter(
    x=future.index,
    y=future["forecast_amount"],
    mode="lines+markers",
    name="Future forecast",
    line=dict(dash="dot"),
))

forecast_fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Recorded order amount",
    hovermode="x unified",
    height=520,
)

st.plotly_chart(forecast_fig, width="stretch")

left, right = st.columns(2)

with left:
    st.subheader("Holdout validation")
    st.dataframe(validation.round(2), width="stretch")

with right:
    st.subheader("Future forecast")
    st.dataframe(future.round(2), width="stretch")

# ---------------------------------------------------------------------
# Data quality and downloads
# ---------------------------------------------------------------------
st.header("6. Data quality")

q1, q2, q3, q4 = st.columns(4)
q1.metric("Missing Amount", f"{quality['missing_amounts']:,}")
q2.metric("Invalid dates", f"{quality['invalid_dates']:,}")
q3.metric("Missing states", f"{quality['missing_states_after_normalization']:,}")
q4.metric("Exact duplicates", f"{quality['duplicate_rows']:,}")

st.info(
    "Interpretation: Amount is recorded order amount, not verified net "
    "revenue. Missing Amount values are excluded from amount totals. "
    "Status counts represent recorded order rows, not confirmed final "
    "customer outcomes. The source covers a limited historical period "
    "in 2022, and forecasts are analytical estimates rather than guarantees."
)

st.header("7. Download reports")

downloads = [
    ("Daily business summary", "daily_business_summary.csv"),
    ("Monthly business summary", "monthly_business_summary.csv"),
    ("Category performance", "category_performance.csv"),
    ("State performance", "state_performance.csv"),
    ("Fulfilment summary", "fulfilment_summary.csv"),
    ("Status summary", "status_summary.csv"),
    ("Missing Amount by status", "missing_amount_by_status.csv"),
    ("Missing Amount by fulfilment", "missing_amount_by_fulfilment.csv"),
]

for label, filename in downloads:
    path = EDA_REPORT_DIR / filename
    if path.exists():
        st.download_button(
            label=f"Download {label}",
            data=path.read_bytes(),
            file_name=filename,
            mime="text/csv",
        )

st.download_button(
    "Download holdout validation CSV",
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
    "Download data quality JSON",
    data=json.dumps(quality, indent=2),
    file_name="data_quality.json",
    mime="application/json",
)

st.caption(
    "W10D5 Sales Intelligence Dashboard | "
    "EDA evidence: reports/w10d5 | Forecast engine: W10D4"
)
