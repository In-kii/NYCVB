# scrapers/__init__.py

from selenium import webdriver
from scrapers.volleyball_nyc import scrape_volleyball_nyc_events
from scrapers.nyurban import scrape_nyurban_events
from scrapers.big_city_opensports import scrape_big_city_opensports

def run_all_scrapers():
    print("🚀 Starting all scrapers...")

    # Selenium-based scrapers
    driver = webdriver.Chrome()
    try:
        scrape_volleyball_nyc_events()
        # Add more Selenium scrapers here
    finally:
        driver.quit()

    # BeautifulSoup or simple HTML-based scrapers
    #scrape_nyurban_events()
    #scrape_big_city_opensports()
    # Add more scrapers here as you build them out

    print("✅ All scraping complete!")