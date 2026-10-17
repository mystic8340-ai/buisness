
import pandas as pd
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent

input_file = (
    project_dir / "data" / "processed" / "business_listings.csv"
)

output_file = (
    project_dir / "data" / "processed" / "business_listings_utf8.csv"
)

# Read the CSV, trying common encodings
df = None

for encoding in ["utf-8-sig", "cp1252", "latin-1"]:
    try:
        df = pd.read_csv(input_file, encoding=encoding)
        print("Read successfully using:", encoding)
        break
    except UnicodeDecodeError:
        continue

if df is None:
    raise ValueError("Could not read the CSV. Check the file encoding.")

# Save a clean UTF-8 CSV for MySQL Workbench
df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("Fixed CSV saved to:", output_file)
print("Total rows:", len(df))
print("Columns:", list(df.columns))
