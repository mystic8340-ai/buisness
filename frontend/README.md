
# Business Listings Dashboard

## Project Overview

This project is a full-stack Business Listings Dashboard
developed using React.js, FastAPI, and MySQL.

It stores business listings and displays analytical
reports through interactive charts.

## Technologies Used

- Python
- FastAPI
- MySQL
- React.js
- Recharts
- Pandas
- BeautifulSoup

## Features

- Bulk insertion of business listings
- City-wise business count
- Category-wise business count
- Source-wise business count
- Interactive charts
- REST APIs

## Project Structure

- backend/ : FastAPI application
- frontend/ : React dashboard
- scraper/ : Data collection and cleaning
- database/ : SQL database files

## Backend Setup

1. Create a Python virtual environment.
2. Install dependencies:

   pip install -r backend/requirements.txt

3. Create backend/.env with DATABASE_URL.
4. Start MySQL.
5. Run FastAPI from the backend folder:

   python -m uvicorn main:app --reload

## Frontend Setup

1. Open the frontend folder.
2. Install dependencies:

   npm install

3. Start React:

   npm run dev

## API Endpoints

- POST /listings/bulk
- GET /dashboard/cities
- GET /dashboard/categories
- GET /dashboard/sources
- GET /dashboard/summary

## Data Source

Describe the actual source used, the collection method,
the number of records, and whether the records are
real or synthetic.

## Challenges Faced

Document any problems encountered with scraping,
MySQL connections, API integration, or frontend charts.

## Author

Mritunjay Kumar