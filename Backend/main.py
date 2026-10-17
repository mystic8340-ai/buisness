
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# 1. Load the .env file from the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# 2. Read MySQL settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "business_dashboard")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# 3. Create the database connection
database_url = URL.create(
    "mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    query={"charset": "utf8mb4"},
)

engine = create_engine(database_url, pool_pre_ping=True)

# 4. Create the FastAPI application
app = FastAPI(title="Business Listings Dashboard API")

# 5. Allow the React development server to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 6. Define the format for new business listings
class Listing(BaseModel):
    business_name: str
    category: str | None = None
    city: str | None = None
    address: str | None = None
    phone: str | None = None
    source: str = "OpenStreetMap"


# 7. Home endpoint
@app.get("/")
def home():
    return {"message": "Business Dashboard API is running"}


# 8. Test the MySQL connection
@app.get("/api/health")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "connected",
            "database": DB_NAME,
        }
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {error}",
        )


# 9. Get dashboard summary cards
@app.get("/api/dashboard/summary")
def dashboard_summary():
    query = text("""
        SELECT
            COUNT(*) AS total_businesses,
            COUNT(DISTINCT city) AS total_cities,
            COUNT(DISTINCT category) AS total_categories,
            COUNT(DISTINCT source) AS total_sources
        FROM listing_master
    """)

    try:
        with engine.connect() as connection:
            row = connection.execute(query).mappings().one()
            return dict(row)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


# 10. Get city-wise business counts
@app.get("/api/dashboard/cities")
def city_counts():
    query = text("""
        SELECT
            COALESCE(NULLIF(city, ''), 'Unknown') AS city,
            COUNT(*) AS count
        FROM listing_master
        GROUP BY COALESCE(NULLIF(city, ''), 'Unknown')
        ORDER BY count DESC
    """)

    try:
        with engine.connect() as connection:
            rows = connection.execute(query).mappings().all()
            return [dict(row) for row in rows]
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


# 11. Get category-wise business counts
@app.get("/api/dashboard/categories")
def category_counts():
    query = text("""
        SELECT
            COALESCE(NULLIF(category, ''), 'Uncategorized')
                AS category,
            COUNT(*) AS count
        FROM listing_master
        GROUP BY COALESCE(NULLIF(category, ''), 'Uncategorized')
        ORDER BY count DESC
    """)

    try:
        with engine.connect() as connection:
            rows = connection.execute(query).mappings().all()
            return [dict(row) for row in rows]
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


# 12. Get source-wise business counts
@app.get("/api/dashboard/sources")
def source_counts():
    query = text("""
        SELECT
            COALESCE(NULLIF(source, ''), 'Unknown') AS source,
            COUNT(*) AS count
        FROM listing_master
        GROUP BY COALESCE(NULLIF(source, ''), 'Unknown')
        ORDER BY count DESC
    """)

    try:
        with engine.connect() as connection:
            rows = connection.execute(query).mappings().all()
            return [dict(row) for row in rows]
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


# 13. Bulk insert new business listings
@app.post("/api/listings/bulk")
def bulk_insert_listings(listings: list[Listing]):
    if not listings:
        raise HTTPException(
            status_code=400,
            detail="The listings list cannot be empty",
        )

    query = text("""
        INSERT INTO listing_master
            (business_name, category, city, address, phone, source)
        VALUES
            (:business_name, :category, :city, :address, :phone, :source)
    """)

    records = [item.model_dump() for item in listings]

    try:
        with engine.begin() as connection:
            connection.execute(query, records)

        return {
            "message": "Listings inserted successfully",
            "inserted_count": len(records),
        }
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
