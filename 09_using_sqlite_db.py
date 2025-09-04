"""
 Challenge: Store & Search Crypto Prices in SQLite

Goal:
- Save hourly top 10 crypto prices into a local SQLite database
- Each record should include timestamp, coin ID, and price
- Allow the user to search for a coin by name and return the latest price

Teaches: SQLite handling in Python, data storage, search queries, API + DB integration
"""

import csv
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import schedule
import time
import sqlite3

API_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 10,
    'page': 1,
    'sparkline': False
}
DB_NAME = "crypto_price.db"

def fetch_crypto_data():
    try:
        response = requests.get(API_URL, params=PARAMS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS crypto_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            coin TEXT,
            prices REAL 
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(data):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for coin in data:
        cur.execute(
            '''
            INSERT INTO crypto_prices (timestamp, coin, prices) VALUES (? , ? , ?)
        ''',(timestamp , coin['id'] , coin['current_price']))

    conn.commit()
    conn.close()
    print("Price saved to database !!")

def search_coin(coin_name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(''' 
        SELECT timestamp,prices FROM crypto_prices WHERE coin == ? ORDER BY timestamp DESC LIMIT 1
    ''', (coin_name,))
    result = cur.fetchone()
    conn.close()
    if result:
        print(f"\nLatest price of {coin_name} is ${result[1]} at {result[0]} !!")

def main():
    create_table()
    print("1. Fetch and store crypto data.")
    print("2. Search for a particular coin data.")
    choice = input("\nChoose an option: ").strip().lower()

    if choice == "1":
        data = fetch_crypto_data()
        save_to_db(data)
    elif choice == "2":
        coin = input("\nEnter the coin name to search: ").strip().lower()
        search_coin(coin)
    else:
        print("Invalid choice !!")

if __name__ == "__main__":
    main()
