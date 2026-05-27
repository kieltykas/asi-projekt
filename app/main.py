from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.db import get_conn
from app.worker import fetch_and_save_data

app = FastAPI(title="Space & Earth API")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def index():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/api/sync")
def sync_data():
    try:
        fetch_and_save_data()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data")
def get_data():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT timestamp, city, temp, weather_desc, asteroid_count FROM space_earth_data ORDER BY timestamp DESC LIMIT 20")
            cols = [c.name for c in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
