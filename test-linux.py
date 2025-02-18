from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import subprocess
from selenium.webdriver.common.by import By

# T   o  ^q  ^qi t     ng ChromeOptions
chrome_options = Options()
chrome_options.binary_location = "/usr/bin/chromium-browser"
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--remote-debugging-port=9224")
chrome_options.add_argument("--no-sandbox")
service = Service(ChromeDriverManager(driver_version="133.0.6943.53").install())


# Kh  ^=i t   o WebDriver v  ^{i c  c t  y ch  ^mn
driver = webdriver.Chrome(service=service, options=chrome_options)

# M  ^= trang web
driver.get("https://youtube.com")



