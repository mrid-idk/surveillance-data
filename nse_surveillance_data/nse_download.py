#!/usr/bin/env python
# coding: utf-8

# In[6]:


import os
import time
import datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Change SAVE_DIR to 'nse_data'
SAVE_DIR = "nse_data"
os.makedirs(SAVE_DIR, exist_ok=True)

def get_cookie_session():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.nseindia.com")
    print("🌐 Opened NSE home page to set cookies...")
    time.sleep(5)

    cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
    driver.quit()
    return cookies

def download_past_year_files():
    cookies = get_cookie_session()
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.nseindia.com/all-reports",
        "Accept": "application/octet-stream",  # Explicitly accept the download type
        "Connection": "keep-alive",  # Keep connection alive for faster retries
    }

    today = datetime.date.today()
    success = 0

    for i in range(1, 366):  # Last 365 days (approx. 1 year)
        date = today - datetime.timedelta(days=i)
        date_str = date.strftime("%d%m%y")
        url = f"https://nsearchives.nseindia.com/content/cm/REG1_IND{date_str}.csv"
        file_path = os.path.join(SAVE_DIR, f"REG1_IND{date_str}.csv")

        print(f"🔄 Fetching: {url}")
        
        try:
            response = requests.get(url, headers=headers, cookies=cookies, timeout=10)

            if response.status_code == 200:
                if response.content:  # Check if content is returned
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    print(f"✅ Saved: {file_path}")
                    success += 1
                else:
                    print(f"❌ Skipped: Empty content for {date_str}")
            else:
                print(f"❌ Skipped: Failed to fetch {url} (Status: {response.status_code})")
        except requests.RequestException as e:
            print(f"❌ Skipped: Error fetching {url} - {str(e)}")

    print(f"\n🎯 Downloaded {success} valid report(s).")

if __name__ == "__main__":
    download_past_year_files()




