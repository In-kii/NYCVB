import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
print("🔍 DB_HOST from env:", os.getenv("DB_HOST"))

# Fetch environment variables
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT", 5432)

def insert_test_event(cursor):
    insert_query = """
    INSERT INTO events (title, date_time, location_name, location_address, cost, level, link, organization, if_filled)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (link) DO NOTHING;
    """
    test_data = (
        "Test Event",
        "Saturday, May 10, 2025, 6:00 PM - 9:00 PM",
        "[Brooklyn] Sunset Park School",
        "123 Sunset Blvd, Brooklyn, NY",
        "$25.00",
        "BB",
        "https://example.com/test-event",
        "Big City Volleyball",
        "3 spots left"
    )
    cursor.execute(insert_query, test_data)

def run_tests():
    connection = None
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            cursor_factory=RealDictCursor
        )
        cursor = connection.cursor()

        # Insert test
        insert_test_event(cursor)
        connection.commit()
        print("✅ Test event inserted (or already exists).")

        # Count total events
        cursor.execute("SELECT COUNT(*) FROM events;")
        total = cursor.fetchone()['count']
        print(f"📊 Total events in database: {total}")

        # Fetch latest 3 entries
        cursor.execute("SELECT title, date_time, organization, link FROM events ORDER BY created_at DESC LIMIT 3;")
        recent = cursor.fetchall()
        print("\n🆕 Latest 3 events:")
        for row in recent:
            print(f"• {row['title']} – {row['date_time']} ({row['organization']})\n  ↪ {row['link']}")

    except Exception as e:
        print("❌ Database test failed:", e)
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    run_tests()