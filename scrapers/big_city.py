from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from database.insert_event import insert_event

def scrape_big_city_volleyball():
    print("🔁 Starting Big City Volleyball scraper (Selenium)")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("https://bigcityvolleyball.com/adult-open-play")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"🔍 Found {len(iframes)} iframes")


        # 💡 Switch to the first iframe (which contains the events)
        driver.switch_to.frame(iframes[0])
        print("🔁 Switched into iframe")

        try:
            # Scroll to bottom to trigger lazy loading
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # let new content render

            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "h3"))
            )
            soup = BeautifulSoup(driver.page_source, "html.parser")
            titles = soup.find_all("h3")
            print("📋 Found titles:")
            for t in titles:
                print(" •", t.get_text(strip=True))
            divs = soup.find_all("div")
            print("📦 All visible <div> classes after scroll:")
            for div in divs[:30]:
                if div.get("class"):
                    print(" ➤", " ".join(div.get("class")))
            """ # ⏳ Wait for the event cards to load
            WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='card']"))
            )
            print("✅ Event cards loaded!")

            soup = BeautifulSoup(driver.page_source, "html.parser")
            # 🌟 NEW: Print first few div class names
            all_divs = soup.find_all("div")
            print("📦 First 20 <div> classes in iframe:")
            for div in all_divs[:20]:
                class_name = div.get("class")
                if class_name:
                    print(" ➤", " ".join(class_name))
            titles = soup.find_all("h3")
            print("📋 Found titles:")
            for t in titles:
                print(" •", t.get_text(strip=True)) """
        except Exception as wait_error:
            print("❌ Failed to find event cards inside iframe")
            print("💥 Exception:", wait_error)
            print("🧾 Iframe HTML preview:\n", driver.page_source[:1000])
            return

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        game_cards = soup.find_all(class_="IFrame_card__mwm8Z")
        print(f"🃏 Found {len(game_cards)} cards")

        for card in game_cards:
            try:
                # Extract game link
                link_tag = card.find("a", href=True)
                game_link = link_tag["href"] if link_tag else None

                # Extract availability
                availability_tag = card.find(class_="Games_statusTag__aRusA Games_filled__QhGp_")
                availability = availability_tag.get_text(strip=True) if availability_tag else "Available"

                # Extract level (A, BB, etc.)
                level_tag = card.find("span", class_="PostCard_cardSkill__HCcDc")
                level = level_tag.get_text(strip=True) if level_tag else "Unknown Level"

                # Extract title
                title_tag = card.find(class_="PostCard_titleText__cNsYT")
                title = title_tag.get_text(strip=True) if title_tag else "Unknown Title"

                # Extract date & time
                date_time_tag = card.find(class_="fa-calendar-o")
                date_time = date_time_tag.find_next("span").get_text(strip=True) if date_time_tag else "Unknown Date/Time"

                # Extract location
                location_tag = card.find(class_="fa-map-marker")
                location_name = location_tag.find_next("span").get_text(strip=True) if location_tag else "Unknown Location"

                # Extract cost
                cost_tag = card.find(class_="PostCard_priceText__eU_V2")
                cost = cost_tag.get_text(strip=True) if cost_tag else "Unknown Cost"

                # Organization name (assumed from source site)
                organization = "Big City Volleyball"

                # Construct event dictionary
                event = {
                    "title": title,
                    "date_time": date_time,
                    "location_name": location_name,
                    "location_address": "",  # not available from this site
                    "cost": cost,
                    "level": level,
                    "link": game_link,
                    "organization": organization,
                    "if_filled": availability
                }

                print("📦 Inserting:", event)
                # Insert into database
                insert_event(event)

            except Exception as card_error:
                print(f"❌ Error processing card: {card_error}")

    except Exception as e:
        print(f"❌ Error during scraping Big City Volleyball: {e}")
    
    finally:
        driver.quit()
        print("✅ Finished scraping Big City Volleyball.")
