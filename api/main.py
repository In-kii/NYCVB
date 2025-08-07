from fastapi import FastAPI, Query
from database.db_connection import get_db_connection
from scrapers import run_all_scrapers
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
import traceback
from selenium import webdriver


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root
@app.get("/")
def read_root():
    return {"message": "🏐 NYC Volleyball API is alive!"}

# Events
@app.get("/events")
def get_all_events(
    organization: str = Query(None),
    level: str = Query(None),
    date: str = Query(None)
):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed.")

    try:
        cursor = conn.cursor()
        query = "SELECT * FROM events WHERE TRUE"
        params = []

        if organization:
            query += " AND organization ILIKE %s"
            params.append(f"%{organization}%")
        if level:
            query += " AND level ILIKE %s"
            params.append(f"%{level}%")
        if date:
            query += " AND date_time ILIKE %s"
            params.append(f"%{date}%")

        query += " ORDER BY date_time"
        cursor.execute(query, params)
        events = cursor.fetchall()
        return events

    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

# Health Check
@app.get("/health")
def health_check():
    conn = get_db_connection()
    if not conn:
        return {"status": "❌ DB not connected"}
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        return {"status": "✅ DB is connected"}
    except Exception as e:
        return {"status": f"❌ DB error: {str(e)}"}
    finally:
        cursor.close()
        conn.close()

# Refresh Scraper
@app.post("/refresh")
def refresh_data():
    print("🚨 /refresh endpoint hit!")
    run_all_scrapers()
    return {"status": "refreshed"}