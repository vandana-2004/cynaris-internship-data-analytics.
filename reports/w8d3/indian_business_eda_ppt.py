
from pathlib import Path
import warnings

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from pptx import Presentation
from pptx.util import Inches, Pt

warnings.filterwarnings("ignore", category=FutureWarning)

ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "w8d3" / "indian_business_sales.csv"
OUTPUT_DIR = ROOT / "reports" / "w8d3"
CHART_DIR = OUTPUT_DIR / "charts"
PPT_FILE = OUTPUT_DIR / "indian_business_eda_report.pptx"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    """Load source data and validate required fields."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    try:
        df = pd.read_csv(DATA_FILE, low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(
            DATA_FILE, encoding="cp1252", low_memory=False
        )

    required = {
        "Date", "Status", "Fulfilment", "Category",
        "Qty", "Amount", "ship-city", "ship-state", "B2B"
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    # Convert fields to appropriate data types.
    df["Date"] = pd.to_datetime(
        df["Date"], format="%m-%d-%y", errors="coerce"
    )
    df["Amount"] = pd.to_numeric(
        df["Amount"], errors="coerce"
    )
    df["Qty"] = pd.to_numeric(
        df["Qty"], errors="coerce"
    )

    return df


def calculate_quality_metrics(df):
    """Measure data quality without deleting original records."""
    amount = df["Amount"].dropna()

    if amount.empty:
        raise ValueError("No valid Amount values available.")

    q1 = amount.quantile(0.25)
    q3 = amount.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    metrics = {
        "duplicate_rows": int(df.duplicated().sum()),
        "invalid_dates": int(df["Date"].isna().sum()),
        "missing_amount": int(df["Amount"].isna().sum()),
        "missing_city": int(df["ship-city"].isna().sum()),
        "missing_values": df.isna().sum(),
        "amount_count": int(amount.count()),
        "amount_mean": float(amount.mean()),
        "amount_median": float(amount.median()),
        "amount_std": float(amount.std()),
        "amount_skewness": float(amount.skew()),
        "amount_min": float(amount.min()),
        "amount_max": float(amount.max()),
        "q1": float(q1),
        "q3": float(q3),
        "outlier_lower_bound": float(lower_bound),
        "outlier_upper_bound": float(upper_bound),
        "outlier_count": int(
            ((amount < lower_bound) | (amount > upper_bound)).sum()
        ),
    }

    return metrics


def save_chart(
    series, title, xlabel, ylabel, filename, horizontal=False
):
    """Save a reproducible chart to the charts directory."""
    path = CHART_DIR / filename
    fig, ax = plt.subplots(figsize=(9, 3.8))

    if horizontal:
        series.sort_values().plot(kind="barh", ax=ax)
    else:
        series.plot(kind="bar", ax=ax)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(
        axis="x" if horizontal else "y",
        alpha=0.25
    )

    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return path


def save_amount_distribution(amount):
    """Create a histogram of recorded order amounts."""
    path = CHART_DIR / "amount_distribution.png"

    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.hist(amount, bins=40, edgecolor="black", alpha=0.8)

    ax.set_title("Distribution of Recorded Order Amounts")
    ax.set_xlabel("Amount (INR)")
    ax.set_ylabel("Frequency")
    ax.grid(axis="y", alpha=0.25)

    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return path


def add_text(
    slide, text, left, top, width, height,
    size=18, bold=False
):
    shape = slide.shapes.add_textbox(
        Inches(left), Inches(top),
        Inches(width), Inches(height)
    )

    frame = shape.text_frame
    frame.word_wrap = True

    paragraph = frame.paragraphs[0]
    paragraph.text = str(text)
    paragraph.font.size = Pt(size)
    paragraph.font.bold = bold

    return shape


def add_bullet_slide(prs, title, bullets):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_text(
        slide, title, 0.6, 0.35, 12, 0.65,
        26, True
    )

    box = slide.shapes.add_textbox(
        Inches(0.8), Inches(1.3),
        Inches(11.5), Inches(5.7)
    )

    frame = box.text_frame
    frame.word_wrap = True

    for i, item in enumerate(bullets):
        paragraph = (
            frame.paragraphs[0]
            if i == 0
            else frame.add_paragraph()
        )

        paragraph.text = str(item)
        paragraph.level = 0
        paragraph.font.size = Pt(15)
        paragraph.space_after = Pt(12)

    return slide


def add_chart_slide(prs, title, chart_path, note):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_text(
        slide, title, 0.6, 0.3, 12, 0.65,
        25, True
    )

    slide.shapes.add_picture(
        str(chart_path),
        Inches(1.25),
        Inches(1.2),
        width=Inches(10.8)
    )

    add_text(
        slide, note, 0.8, 6.2, 11.5, 0.65,
        11
    )

    return slide


def main():
    df = load_data()

    rows, columns = df.shape
    metrics = calculate_quality_metrics(df)

    duplicate_count = metrics["duplicate_rows"]
    missing_amount = metrics["missing_amount"]
    missing_city = metrics["missing_city"]

    valid_dates = df["Date"].dropna()

    if valid_dates.empty:
        raise ValueError("No valid dates available for analysis.")

    date_start = valid_dates.min().strftime("%d %b %Y")
    date_end = valid_dates.max().strftime("%d %b %Y")

    # Business summaries.
    category_sales = (
        df.groupby("Category")["Amount"]
        .sum(min_count=1)
        .sort_values(ascending=False)
        .head(8)
    )

    status_counts = df["Status"].value_counts().head(8)
    fulfilment_counts = df["Fulfilment"].value_counts()
    state_counts = df["ship-state"].value_counts().head(8)

    # Shipped-status records are not equivalent to realized revenue.
    shipped_records = df[
        df["Status"].astype(str).str.startswith("Shipped")
    ].copy()

    monthly_amount = (
        shipped_records.dropna(subset=["Date"])
        .set_index("Date")["Amount"]
        .resample("MS")
        .sum(min_count=1)
    )

    monthly_amount.index = monthly_amount.index.strftime("%b %Y")

    valid_amount = df["Amount"].dropna()

    # Generate six charts.
    chart_category = save_chart(
        category_sales / 100000,
        "Recorded Amount by Product Category",
        "Category",
        "Amount (INR lakh)",
        "category_sales.png",
        horizontal=True
    )

    chart_status = save_chart(
        status_counts,
        "Order Records by Status",
        "Status",
        "Records",
        "order_status.png",
        horizontal=True
    )

    chart_fulfilment = save_chart(
        fulfilment_counts,
        "Fulfilment Method Distribution",
        "Fulfilment",
        "Records",
        "fulfilment.png"
    )

    chart_monthly = save_chart(
        monthly_amount / 100000,
        "Monthly Amount in Shipped-Status Records",
        "Month",
        "Amount (INR lakh)",
        "monthly_amount.png"
    )

    chart_states = save_chart(
        state_counts,
        "Top Shipping States by Record Count",
        "State",
        "Records",
        "top_states.png",
        horizontal=True
    )

    chart_distribution = save_amount_distribution(valid_amount)

    # Reproducibility and data-quality summary.
    summary_path = OUTPUT_DIR / "eda_summary.txt"

    with summary_path.open("w", encoding="utf-8") as f:
        f.write("W8D3 INDIAN E-COMMERCE EDA\n")
        f.write("=" * 40 + "\n")

        f.write(f"Rows: {rows}\n")
        f.write(f"Columns: {columns}\n")
        f.write(f"Date range: {date_start} to {date_end}\n")
        f.write(f"Duplicate rows: {duplicate_count}\n")
        f.write(f"Invalid dates: {metrics['invalid_dates']}\n")
        f.write(f"Missing Amount: {missing_amount}\n")
        f.write(f"Missing shipping city: {missing_city}\n")

        f.write("\nDATA QUALITY: MISSING VALUES BY COLUMN\n")
        f.write(metrics["missing_values"].to_string())

        f.write("\n\nAMOUNT DISTRIBUTION\n")
        f.write(f"Count: {metrics['amount_count']}\n")
        f.write(f"Mean: {metrics['amount_mean']:.2f}\n")
        f.write(f"Median: {metrics['amount_median']:.2f}\n")
        f.write(f"Standard deviation: {metrics['amount_std']:.2f}\n")
        f.write(f"Skewness: {metrics['amount_skewness']:.3f}\n")
        f.write(f"Minimum: {metrics['amount_min']:.2f}\n")
        f.write(f"Maximum: {metrics['amount_max']:.2f}\n")

        f.write("\nIQR OUTLIER ANALYSIS\n")
        f.write(f"Q1: {metrics['q1']:.2f}\n")
        f.write(f"Q3: {metrics['q3']:.2f}\n")
        f.write(
            f"Lower bound: {metrics['outlier_lower_bound']:.2f}\n"
        )
        f.write(
            f"Upper bound: {metrics['outlier_upper_bound']:.2f}\n"
        )
        f.write(f"Potential outliers: {metrics['outlier_count']}\n")

        f.write("\nRECORDED AMOUNT BY CATEGORY\n")
        f.write(category_sales.to_string())

        f.write("\n\nORDER STATUS COUNTS\n")
        f.write(status_counts.to_string())

        f.write("\n\nANALYSIS ASSUMPTIONS\n")
        f.write(
            "Original source records were preserved; no rows were "
            "silently removed or imputed.\n"
        )
        f.write(
            "Date and numeric fields were converted with invalid "
            "values represented as missing.\n"
        )
        f.write(
            "Potential outliers were identified using the 1.5 x IQR "
            "rule and were not automatically removed.\n"
        )
        f.write(
            "Undocumented Unnamed: 22 was excluded from analysis.\n"
        )
        f.write(
            "Category amounts include all order statuses and are "
            "not net realized revenue.\n"
        )
        f.write(
            "Shipped-status monthly amounts include statuses "
            "beginning with Shipped, including returns.\n"
        )

    # Build PowerPoint.
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    top_category = (
        str(category_sales.index[0])
        if not category_sales.empty else "N/A"
    )

    top_category_amount = (
        float(category_sales.iloc[0])
        if not category_sales.empty else 0
    )

    top_status = (
        str(status_counts.index[0])
        if not status_counts.empty else "N/A"
    )

    top_state = (
        str(state_counts.index[0])
        if not state_counts.empty else "N/A"
    )

    # Slide 1: Executive takeaway.
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_text(
        slide, "Indian E-commerce Sales EDA",
        0.8, 0.65, 11.8, 0.8, 30, True
    )

    add_text(
        slide,
        f"{top_category} leads recorded category amount "
        f"with INR {top_category_amount / 100000:.2f} lakh.",
        0.8, 1.8, 11.5, 1.0, 23, True
    )

    add_text(
        slide,
        f"{top_status} is the most frequent order status. "
        f"The most frequent shipping state is {top_state}.",
        0.8, 3.1, 11.5, 0.9, 18
    )

    add_text(
        slide,
        f"Dataset: {rows:,} records | {date_start} to {date_end}",
        0.8, 4.5, 11.5, 0.5, 16
    )

    add_text(
        slide,
        "Note: Recorded amounts are not equivalent to net realized revenue.",
        0.8, 5.3, 11.5, 0.7, 13
    )

    add_text(
        slide,
        "Source: Amazon Sale Report CSV supplied for this project",
        0.8, 6.6, 11.5, 0.35, 10
    )

    # Slide 2: Dataset overview and quality.
    add_bullet_slide(prs, "Dataset Overview and Data Quality", [
        f"Dataset size: {rows:,} rows and {columns} columns.",
        f"Date coverage: {date_start} to {date_end}.",
        f"Duplicate rows: {duplicate_count:,}.",
        f"Missing Amount values: {missing_amount:,}.",
        f"Missing shipping city values: {missing_city:,}.",
        f"Invalid or missing dates: {metrics['invalid_dates']:,}.",
        "No source rows were automatically deleted or imputed.",
        "Undocumented Unnamed: 22 was excluded from analysis."
    ])

    # Slide 3: Category.
    add_chart_slide(
        prs,
        "Product Category Analysis",
        chart_category,
        "Set has the highest recorded amount. Amounts include all order statuses."
    )

    # Slide 4: Order status.
    add_chart_slide(
        prs,
        "Order Status Analysis",
        chart_status,
        "Cancelled, pending, shipped and returned records are shown separately."
    )

    # Slide 5: Fulfilment.
    add_chart_slide(
        prs,
        "Fulfilment Analysis",
        chart_fulfilment,
        "Compare Amazon and merchant fulfilment volumes when planning operations."
    )

    # Slide 6: Monthly trend.
    add_chart_slide(
        prs,
        "Monthly Shipped-Status Amount Trend",
        chart_monthly,
        "Includes statuses beginning with Shipped; this is not net realized revenue."
    )

    # Slide 7: Geography.
    add_chart_slide(
        prs,
        "Shipping Geography",
        chart_states,
        "These are the most frequent shipping states by order-record count."
    )

    # Slide 8: Distribution and outliers.
    add_chart_slide(
        prs,
        "Order Amount Distribution",
        chart_distribution,
        (
            f"Skewness: {metrics['amount_skewness']:.2f} | "
            f"Potential IQR outliers: {metrics['outlier_count']:,}. "
            "Outliers are flagged, not removed."
        )
    )

    # Slide 9: Business recommendations.
    add_bullet_slide(
        prs,
        "Business Insights and Recommendations",
        [
            f"{top_category} leads recorded category amount; "
            "review its inventory and demand patterns.",
            f"{top_status} is the most frequent status; "
            "monitor fulfilment and delivery performance.",
            f"{top_state} has the most shipping records; "
            "review regional logistics capacity.",
            "Analyze cancellations and returns separately before "
            "estimating net sales.",
            "Investigate missing Amount and shipping-location data "
            "to improve reporting completeness.",
            "Review potential high-value outliers individually "
            "before making business decisions."
        ]
    )

    prs.save(PPT_FILE)

    print("W8D3 EDA completed successfully.")
    print(f"Dataset shape: {df.shape}")
    print(f"Date range: {date_start} to {date_end}")
    print(f"Duplicate rows: {duplicate_count}")
    print(f"Potential Amount outliers: {metrics['outlier_count']}")
    print(f"PowerPoint: {PPT_FILE}")
    print(f"Summary: {summary_path}")
    print(f"Charts folder: {CHART_DIR}")


if __name__ == "__main__":
    main()
