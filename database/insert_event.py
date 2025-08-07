from database.db_connection import get_db_connection

# --- Insert function to use across scrapers ---
def insert_event(event):
    """
    Inserts a single volleyball event into the database.
    Expects `event` to be a dictionary with keys:
    title, date_time, location_name, location_address, cost,
    level, link, organization, if_filled
    """
    conn = get_db_connection()
    if not conn:
        print("❌ No connection available.")
        return

    try:
        cursor = conn.cursor()

        query = """
        INSERT INTO events (title, date_time, location_name, location_address, cost,
                            level, link, organization, if_filled)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (link) DO UPDATE
        SET 
            title = EXCLUDED.title,
            date_time = EXCLUDED.date_time,
            location_name = EXCLUDED.location_name,
            location_address = EXCLUDED.location_address,
            cost = EXCLUDED.cost,
            level = EXCLUDED.level,
            organization = EXCLUDED.organization,
            if_filled = EXCLUDED.if_filled;
        """

        cursor.execute(query, (
            event["title"],
            event["date_time"],
            event["location_name"],
            event["location_address"],
            event["cost"],
            event["level"],
            event["link"],
            event["organization"],
            event["if_filled"]
        ))

        conn.commit()
        print(f"✅ Event inserted: {event['title']}")

    except Exception as e:
        print("❌ Failed to insert event:", e)
    finally:
        cursor.close()
        conn.close()
