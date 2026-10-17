
from pathlib import Path
from getpass import getpass

import pandas as pd
from sqlalchemy import create_engine, URL, text

# Find the CSV file
project_dir = Path(__file__).resolve().parent.parent
csv_file = project_dir / "data" / "processed" / "business_listings_utf8.csv"

if not csv_file.exists():
    raise FileNotFoundError(f"CSV not found: {csv_file}")

# Read the CSV
df = pd.read_csv(csv_file, encoding="utf-8-sig")
df.columns = df.columns.str.strip()

# Match CSV headings to MySQL column names
column_mapping = {
    "Business Name": "business_name",
    "Category": "category",
    "City": "city",
    "Address": "address",
    "Phone": "phone",
    "Source": "source",
}

df = df.rename(columns=column_mapping)

required = [
    "business_name",
    "category",
    "city",
    "address",
    "phone",
    "source",
]

missing = [col for col in required if col not in df.columns]
if missing:
    raise ValueError(
        f"Missing CSV columns: {missing}. "
        f"Found columns: {list(df.columns)}"
    )

df = df[required].copy()

# Clean text fields and replace missing values
for col in required:
    df[col] = df[col].map(
        lambda value: (
            str(value).strip()
            if pd.notna(value) and str(value).strip()
            else None
        )
    )

df = df.dropna(subset=["business_name", "source"])

print("CSV rows ready to import:", len(df))

# Enter your MySQL connection details
username = input("MySQL username (often root): ").strip()
password = getpass("MySQL password: ")
host = input("MySQL host [localhost]: ").strip() or "localhost"
port = int(input("MySQL port [3306]: ").strip() or "3306")

url = URL.create(
    drivername="mysql+pymysql",
    username=username,
    password=password,
    host=host,
    port=port,
    database="business_dashboard",
    query={"charset": "utf8mb4"},
)

engine = create_engine(url)

# Check the connection and insert the rows
with engine.begin() as connection:
    connection.execute(text("SELECT 1"))

    existing = connection.execute(
        text("SELECT COUNT(*) FROM listing_master")
    ).scalar_one()

    print("Rows already in MySQL:", existing)

    if existing > 0:
        raise RuntimeError(
            "The table already contains rows. "
            "Import cancelled to prevent duplicates. "
            "Check the table before importing again."
        )

    df.to_sql(
        name="listing_master",
        con=connection,
        if_exists="append",
        index=False,
        chunksize=200,
        method="multi",
    )

    total = connection.execute(
        text("SELECT COUNT(*) FROM listing_master")
    ).scalar_one()

print("Import successful!")
print("Total rows in listing_master:", total)

engine.dispose()
