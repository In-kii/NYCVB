from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from database.insert_event import insert_event


def scrape_volleyball_nyc_events():
    try:
        options = Options()
        #options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        driver.get("https://www.volleyball-nyc.com/events")
        time.sleep(5)

        print("🚨 /refresh endpoint hit!")

        event_cards = driver.find_elements(By.CSS_SELECTOR, "div.rounded-lg.border.bg-card")
        print(f"📦 Found {len(event_cards)} posts")

        event_urls = []

        for i in range(len(event_cards)):
            try:
                # Refetch cards each time to avoid stale reference
                cards = driver.find_elements(By.CSS_SELECTOR, "div.rounded-lg.border.bg-card")
                card = cards[i]
                driver.execute_script("arguments[0].scrollIntoView(true);", card)
                view_button = card.find_element(By.XPATH, ".//button[contains(., 'View')]")
                view_button.click()
                time.sleep(2)
                current_url = driver.current_url
                print(f"🔗 Event URL: {current_url}")
                event_urls.append(current_url)
                driver.back()
                time.sleep(2)
            except Exception as e:
                print(f"❌ Error processing card {i}: {e}")

        # Second pass: visit each event page and scrape
        for event_url in event_urls:
            try:
                driver.get(event_url)
                time.sleep(2)
                
                # ✅ Wait for the page to load properly
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "h1"))
                )

                soup = BeautifulSoup(driver.page_source, "html.parser")

                title_tag = soup.find("h1")
                title = title_tag.get_text(strip=True) if title_tag else "Unknown Title"

                # Date & Time
                date_time_block = soup.find_all("div", class_="flex items-center text-gray-600")
                date = date_time_block[0].find("span").get_text(strip=True) if len(date_time_block) > 0 else "N/A"
                time_range = date_time_block[1].find("span").get_text(strip=True) if len(date_time_block) > 1 else "N/A"
                date_time = f"{date}, {time_range}"

                # Location
                location_tag = soup.find("p", string=lambda t: t and "Address" in t)
                location_address = location_tag.find_next_sibling("p").get_text(strip=True) if location_tag else ""

                # Cost
                cost_tag = soup.find("p", class_="font-semibold text-lg")
                cost = cost_tag.get_text(strip=True) if cost_tag else "Unknown Cost"

                # Availability
                availability_tag = soup.find("div", class_="items-center rounded-full border")
                availability = availability_tag.get_text(strip=True) if availability_tag else "N/A"

                # Level
                level = title.split()[0] if title else "Unknown"

                event = {
                    "title": title,
                    "date_time": date_time,
                    "location_name": "Volleyball NYC",
                    "location_address": location_address,
                    "cost": cost,
                    "level": level,
                    "link": event_url,
                    "organization": "Volleyball NYC",
                    "if_filled": availability
                }

                print(f"📥 Inserting: {title}")
                insert_event(event)
                print(f"✅ Event inserted: {title}")

            except Exception as e:
                print(f"❌ Error processing {event_url}: {e}")

        driver.quit()
        print("✅ Volleyball NYC scrape complete!")

    except Exception as e:
        print(f"❌ Error during scraping Volleyball NYC: {e}")