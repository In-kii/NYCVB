import requests
from database.insert_event import insert_event

def scrape_big_city_opensports():
    print("🔁 Scraping Big City from OpenSports filtered post list")

    url = "https://osapi.opensports.ca/app/posts/listFiltered?groupID=1962&limit=48&limitedFields=true&rootTags%5B%5D=Open%20Play"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        events = data.get("result", [])

        print(f"📦 Found {len(events)} posts")

        for event in events:
            title = event.get("title", "Unknown Title")
            date_time = event.get("start", "Unknown Time")

            place = event.get("place", {})
            location_name = place.get("title", "Unknown Location")
            location_address = place.get("address", "")

            cost = f"${event.get('ticketsSummary', [{}])[0].get('price', 0):.2f}"
            level = event.get("data", {}).get("level", {}).get("title", "Unknown Level")

            joined = event.get("registeredAttendees", 0)
            total = event.get("maxAttendees", 0)
            availability = f"{joined} / {total} players"

            link = f"https://opensports.net/posts/{event.get('aliasID', '')}"
            organization = "Big City Volleyball"

            event_obj = {
                "title": title,
                "date_time": date_time,
                "location_name": location_name,
                "location_address": location_address,
                "cost": cost,
                "level": level,
                "link": link,
                "organization": organization,
                "if_filled": availability
            }

            print("📥 Inserting:", title)
            insert_event(event_obj)

        print("✅ Big City OpenSports scraping complete!")

    except Exception as e:
        print("❌ Error scraping Big City OpenSports:", e)