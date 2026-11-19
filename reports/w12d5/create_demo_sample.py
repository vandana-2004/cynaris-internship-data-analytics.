import pandas as pd
from pathlib import Path

source = Path("data/w8d3/indian_business_sales.csv")
output = Path("reports/w12d5/indian_business_demo_sample.csv")

columns = [
    "Date", "Status", "Fulfilment", "Category",
    "Qty", "Amount", "ship-state", "ship-country"
]

df = pd.read_csv(source, usecols=columns)
sample = df.sample(n=min(5000, len(df)), random_state=42)
sample.to_csv(output, index=False)

print("Sample created:", output)
print("Rows:", len(sample))
print("Columns:", sample.columns.tolist())
print("Size (bytes):", output.stat().st_size)
print("Under 10 MB:", output.stat().st_size <= 10 * 1024 * 1024)
