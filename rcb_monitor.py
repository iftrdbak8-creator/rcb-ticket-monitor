from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import time

# Telegram details
BOT_TOKEN = "8783234413:AAGkYucqDPXwRrqy_s3q2H_5QlXdWxPfDec"
CHAT_ID = "769922656"

URL = "https://shop.royalchallengers.com/ticket"

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

print("RCB Monitor started...")

last_update_time = time.time()

try:
    driver.get(URL)

    try:
        # Check "Tickets not available"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'Tickets not available')]")
            )
        )

        print("Still not available")

        # send status update every 30 minutes
        if time.time() - last_update_time >= 1800:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={
                    "chat_id": CHAT_ID,
                    "text": "⏳ RCB tickets still not available. I'm checking regularly."
                }
            )
            last_update_time = time.time()

    except TimeoutException:
        # Check if BUY TICKETS appears
        buttons = driver.find_elements(By.XPATH, "//button[contains(.,'BUY')]")

        if len(buttons) > 0:
            print("Tickets available! Sending alerts...")

            # send 3 alerts
            for i in range(3):
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    data={
                        "chat_id": CHAT_ID,
                        "text": "🚨 RCB Tickets LIVE!\nhttps://shop.royalchallengers.com/ticket"
                    }
                )
                time.sleep(2)

        else:
            print("Page load delay - retry later")

finally:
    driver.quit()
