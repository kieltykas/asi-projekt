import os
import psycopg
from dotenv import load_dotenv

load_dotenv()
DB_DSN = os.getenv("DB_DSN", "postgresql://db_user:password@localhost:5432/space_weather")

def get_conn():
    return psycopg.connect(DB_DSN)
