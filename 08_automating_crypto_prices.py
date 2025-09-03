"""
depends on:
 - Day 7 of web scraping

Fetch crypto data every hour automatically

"""

import os
import csv
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import schedule
import time 

API_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 10,
    'page': 1,
    'sparkline': False
}

CSV_FILE = "crypto_prices.csv"

def save_data(data):
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["time", "coin", "price"])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for coin in data:
            writer.writerow([timestamp, coin['id'], coin['current_price']])

    print(f"Data saved to {CSV_FILE}!")

def fetch_crypto_data():
    try:
        response = requests.get(API_URL, params=PARAMS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []

def job():
    print("Fetching the crypto prices hourly !!")
    crypto_data = fetch_crypto_data()
    save_data(crypto_data)
    
#schedule.every().hour.at(":00").do(job)
schedule.every(1).minutes.do(job)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt as e: 
    print(f"\nGracefully handled KeyboardInterrupt !!")
