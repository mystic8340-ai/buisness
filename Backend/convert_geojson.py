
import json
import csv
from pathlib import Path

# Project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_DIR / "data" / "raw" / "html" / "Patna.geojson"
OUTPUT_FILE = PROJECT_DIR / "data" / "processed" / "business_listings.csv"

# Read downloaded GeoJSON
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    geojson = json.load(file)

rows = []

for feature in geojson.get("features", []):
    tags = feature.get("properties", {})

    # Business name
    name = tags.get("name") or tags.get("brand")
    if not name:
        continue

    # Find business category
    category = (
        tags.get("shop")
        or tags.get("amenity")
        or tags.get("office")
        or tags.get("healthcare")
        or tags.get("tourism")
        or tags.get("craft")
        or tags.get("leisure")
        or "Other"
    )

    # Build address from available address tags
    address_parts = [
        tags.get("addr:housenumber"),
        tags.get("addr:street"),
        tags.get("addr:suburb"),
        tags.get("addr:neighbourhood"),
        tags.get("addr:postcode"),
    ]

    address = ", ".join(
        part for part in address_parts if part
    ) or "Not available"

    phone = (
        tags.get("phone")
        or tags.get("contact:phone")
        or "Not available"
    )

    rows.append({
        "Business Name": name,
        "Category": category,
        "City": tags.get("addr:city", "Patna"),
        "Address": address,
        "Phone": phone,
        "Source": "OpenStreetMap",
    })

# Remove duplicate records
unique_rows = []
seen = set()

for row in rows:
    key = (
        row["Business Name"].strip().lower(),
        row["Address"].strip().lower(),
    )

    if key not in seen:
        seen.add(key)
        unique_rows.append(row)

# Create output folder
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Write CSV
fieldnames = [
    "Business Name",
    "Category",
    "City",
    "Address",
    "Phone",
    "Source",
]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(unique_rows)

print("Conversion completed!")
print("Total unique businesses:", len(unique_rows))
print("CSV saved at:", OUTPUT_FILE)
