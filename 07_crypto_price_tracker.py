"""
 Challenge: Crypto Price Tracker with Graphs

Goal:
- Fetch live prices of the top 10 cryptocurrencies using CoinGecko's free public API
- Store prices in a CSV file with timestamp
- Generate a line graph for a selected coin over time (price vs. time)
- Repeatable — user can run this multiple times to log data over time

JSON handling, API usage, CSV storage, matplotlib graphing
"""
import os
import csv
import matplotlib.pyplot as plt
import requests
from datetime import datetime

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

def plot_graph(coin_id):
    times = []
    prices = []

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['coin'] == coin_id:
                times.append(row['time'])
                prices.append(float(row['price']))

    if not times:
        print(f"No data found for '{coin_id}'!")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(times, prices, marker='o', label=coin_id.upper())
    plt.title(f"Price of {coin_id.capitalize()} Over Time")
    plt.xlabel("Time")
    plt.ylabel("Price (USD)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    print("\nFetching live crypto data...")
    data = fetch_crypto_data()

    if not data:
        print("No data received. Exiting.")
        return

    print("\nSaving data to CSV file...")
    save_data(data)

    print('-' * 40)
    for coin in data:
        print(f"{coin['id']} - ${coin['current_price']}")
    print('-' * 40)

    choice = input("\nEnter the coin name to plot its price history: ").strip().lower()
    plot_graph(choice)

if __name__ == "__main__":
    main()

