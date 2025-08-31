"""
Challenge: Hacker News Top Posts Scraper

Build a Python script that:
1. Fetches the HN homepage (news.ycombinator.com).
2. Extracts the top 20 post titles and URLs.
3. Saves the results into a CSV file (`hn_top20.csv`) with columns:
   – Title
   – URL
4. Handles network errors and uses a clean CSV structure.
"""

import requests
from bs4 import BeautifulSoup
import csv

HN_URL = 'https://news.ycombinator.com/'
CSV_FILE = 'current-top20-news.csv'

def fetch_top_post():
    try: 
        response = requests.get(HN_URL , timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Error: ",e)
        return []

    soup = BeautifulSoup(response.text , "html.parser")
    posts = soup.select("span.titleline > a")
    
    top20 = []
    for news in posts[:20]:
        title = news.text.strip()
        url = news.get('href').strip()
        top20.append({'title': title , 'url': url})

    return top20

def save_to_csv(posts):
    if not posts:
        print("Nothing to save !!")
        return 
    with open(CSV_FILE , "w", newline="" , encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title" , "url"])
        writer.writeheader()
        writer.writerows(posts)

    print(f"\nSaved Hacker News to {CSV_FILE} !!")

def main():
    print("Scanning Hacker News Website...")
    news = fetch_top_post()
    print("\nCollected All Data...")
    save_to_csv(news)

if __name__ == "__main__":
    main()

