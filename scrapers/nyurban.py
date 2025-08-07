import requests
from bs4 import BeautifulSoup
from database.insert_event import insert_event

def scrape_nyurban_events():
    try:
        url = "https://www.nyurban.com/?page_id=400&filter_id=1&gametypeid=1"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all rows in the table
        rows = soup.find_all("tr")
        event_count = 0

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 6:
                continue  # skip incomplete rows

            date = cols[0].get_text(strip=True).replace(u'\xa0', u' ')
            location = cols[1].get_text(strip=True).replace(u'\xa0', u' ')
            level = cols[2].get_text(strip=True).replace(u'\xa0', u' ')
            time_range = cols[3].get_text(strip=True).replace(u'\xa0', u' ')
            cost = cols[4].get_text(strip=True).replace(u'\xa0', u' ')
            availability = cols[5].get_text(strip=True).replace(u'\xa0', u' ')

            date_time = f"{date}, {time_range}"

            event = {
                "title": f"{level} @ {location}",
                "date_time": date_time,
                "location_name": location,
                "location_address": "",  # not provided
                "cost": f"${cost}",
                "level": level,
                "link": url,
                "organization": "NY Urban",
                "if_filled": availability
            }

            insert_event(event)
            print(f"✅ Inserted: {event['title']}")
            event_count += 1

        print(f"🎉 NY Urban scrape complete! {event_count} events inserted.")

    except Exception as e:
        print(f"❌ Error during NY Urban scraping: {e}")