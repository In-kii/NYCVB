from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

def scrape_volleyball_nyc_events():
    url = "https://www.volleyball-nyc.com/events"

    # --- Setup Selenium ---
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1200,800")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "rounded-lg")))
    time.sleep(2)

    # --- Collect all event cards and buttons ---
    event_cards = driver.find_elements(By.CLASS_NAME, "rounded-lg")
    view_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'View')]")

    print(f"Found {len(event_cards)} cards and {len(view_buttons)} view buttons")

    events = []

    for i, (card, button) in enumerate(zip(event_cards, view_buttons)):
        try:
            # Scroll into view for clickability
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(0.5)

            # Extract static data from event card (before clicking)
            try:
                title = card.find_element(By.TAG_NAME, "h3").text.strip()
            except:
                title = "Unknown Title"

            try:
                availability = card.find_element(By.CSS_SELECTOR, "div.rounded-full.border.w-full.flex.justify-center").text.strip()
            except:
                availability = "N/A"

            # Use SVG icon detection to extract date and time more robustly
            try:
                soup = BeautifulSoup(card.get_attribute("outerHTML"), "html.parser")
                info_blocks = soup.find_all("div", class_="flex items-center text-gray-600")
                date, time_str = "N/A", "N/A"
                for block in info_blocks:
                    svg = block.find("svg")
                    if svg and "lucide-calendar" in svg.get("class", []):
                        date = block.find("span").get_text(strip=True)
                    elif svg and "lucide-clock" in svg.get("class", []):
                        time_str = block.find("span").get_text(strip=True)
                date_time = f"{date}, {time_str}"
            except:
                date_time = "N/A"

            # Extract both location name and address
            try:
                location_name = soup.select_one("svg.lucide-map-pin ~ span").get_text(strip=True)
                location_address = soup.select_one(".ml-7.text-sm.text-gray-500").get_text(strip=True)
            except:
                location_name = "Unknown Location"
                location_address = "Unknown Address"

            try:
                cost = card.find_element(By.CLASS_NAME, "text-lg").text.strip()
            except:
                cost = "Unknown Cost"

            level = title.split()[0] if title else "Unknown"

            # --- Click and get link ---
            button.click()
            wait.until(EC.url_changes(driver.current_url))
            event_url = driver.current_url

            # Save data
            events.append({
                "title": title,
                "date_time": date_time,
                "location_name": location_name,
                "location_address": location_address,
                "level": level,
                "cost": cost,
                "organization": "Volleyball NYC",
                "link": event_url,
                "ifFilled": availability
            })

            print(f"[{i+1}] {title} -> {event_url}")

            # Go back
            driver.back()
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "rounded-lg")))
            time.sleep(1)

            # Refresh cards and buttons for next iteration
            event_cards = driver.find_elements(By.CLASS_NAME, "rounded-lg")
            view_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'View')]")

        except Exception as e:
            print(f"❌ Error on event #{i+1}: {e}")
            continue

    driver.quit()
    print(f"\n🎉 Done! Extracted {len(events)} events.")
    return events

# Example usage
if __name__ == "__main__":
    events = scrape_volleyball_nyc_events()
    for e in events:
        print(e)
