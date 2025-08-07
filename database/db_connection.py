from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Load environment variables from .env
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path=dotenv_path)
DB_HOST = os.getenv("DB_HOST")
print("🔍 DB_HOST from env:", DB_HOST)

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT", 5432)

def get_db_connection():
    """Returns a PostgreSQL connection using environment variables."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print("❌ Could not establish DB connection:", e)
        return None
