"""
 Challenge: Download Cover Images Using wget

Goal:
- Scrape https://books.toscrape.com/
- Collect the first 10 books on the homepage
- Extract the title and image URL for each book
- Use the `wget` library to download and save images in a folder called 'images/'
- Use book titles (sanitized) as image filenames

Bonus:
- Add progress for each download
- Ensure folder is created if it doesn't exist
"""

import os 
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests 
import re
import wget

BASE_URL = "https://books.toscrape.com/"
IMAGE_DIR = "images"

def sanitize_filename(title):
    return re.sub(r'[^\w\-._ ]' , '',title).replace(" ","_")

def download_image():
    try:
        url = BASE_URL
        response = requests.get(url ,timeout=7)
        response.raise_for_status()
    except Exception as e:
        print("Error: ",e)

    raw_data = BeautifulSoup(response.text , "html.parser")
    articles = raw_data.select("article.product_pod")[:10]

    if not os.path.exists(IMAGE_DIR):
        os.mkdir(IMAGE_DIR)

    for article in articles:
        title = article.select_one('h3 > a').get('title').strip()
        image = article.find('img')['src']
        img_url = urljoin(BASE_URL , image)
        print(f"\n\nImage url: {img_url}")

        filename = sanitize_filename(title)+'.jpg'
        filepath = os.path.join(IMAGE_DIR, filename)
        print(f"Filepath: {filepath}")

        print(f"Downloading: {title}")

        wget.download(img_url, filepath)

    print(f"\n\nSuccessfully Downloaded all the images in {IMAGE_DIR} folder !!")

if __name__ == "__main__":
    download_image()

