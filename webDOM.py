from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://www.volleyball-nyc.com/events")

# 等页面加载
time.sleep(5)

with open("page.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)