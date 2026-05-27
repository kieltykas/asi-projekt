import os
import requests
import logging
from datetime import datetime
from app.db import get_conn

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

NASA_API_KEY = os.getenv("NASA_API_KEY")
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = os.getenv("CITY_NAME", "Warsaw")

def fetch_and_save_data():
    now = datetime.now().replace(second=0, microsecond=0)
    logger.info(f"Rozpoczynam synchronizację danych dla: {now.strftime('%Y-%m-%d %H:%M')}")
    
    nasa_url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={now.date()}&end_date={now.date()}&api_key={NASA_API_KEY}"
    try:
        nasa_resp = requests.get(nasa_url, timeout=10)
        nasa_resp.raise_for_status()
        asteroid_count = nasa_resp.json().get("element_count", 0)
    except Exception as e:
        logger.error(f"Błąd NASA: {e}")
        asteroid_count = 0

    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
    try:
        weather_resp = requests.get(weather_url, timeout=10)
        weather_resp.raise_for_status()
        w_data = weather_resp.json()
        temp = w_data["main"]["temp"]
        desc = w_data["weather"][0]["description"]
    except Exception as e:
        logger.error(f"Błąd Pogoda: {e}")
        temp, desc = 0.0, "brak danych"

    upsert_sql = """
        INSERT INTO space_earth_data (timestamp, city, temp, weather_desc, asteroid_count)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (timestamp) DO UPDATE SET
            temp = EXCLUDED.temp,
            weather_desc = EXCLUDED.weather_desc,
            asteroid_count = EXCLUDED.asteroid_count;
    """
    
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(upsert_sql, (now, CITY, temp, desc, asteroid_count))
            conn.commit()
        logger.info("Dane zapisane pomyślnie.")
    except Exception as e:
        logger.error(f"Krytyczny błąd zapisu do bazy: {e}")

if __name__ == "__main__":
    fetch_and_save_data()
