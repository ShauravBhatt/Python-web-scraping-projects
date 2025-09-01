"""
 Challenge: Download Cover Images of First 10 Books

Goal:
- Visit https://books.toscrape.com/
- Scrape the first 10 books listed on the homepage
- For each book, extract:
  • Title
  • Image URL

Then:
- Download each image
- Save it to a local `images/` folder with the filename as the book title (sanitized)

Example:
 Title: "A Light in the Attic"
 Saved as: images/A_Light_in_the_Attic.jpg

Bonus:
- Handle invalid filename characters
- Show download progress
"""

import os 
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re 

BASE_URL = 'https://books.toscrape.com/'
IMAGE_DIR = 'images'

def sanitized_filename(title):
    return re.sub(r'[^\w\-_. ]','' , title).replace(" " , "_")

def download_image(img_url , filename):
    try:
        response = requests.get(img_url , stream=True ,  timeout=7)
        response.raise_for_status()
        with open(filename , "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    except Exception as e:
        print(f"Error while downloading {filename} : ", e)

def scrape_and_download_images():
    url = BASE_URL
    response = requests.get(url , timeout=10)
    response.raise_for_status()

    raw_data = BeautifulSoup(response.text , "html.parser")
    articles = raw_data.select("article.product_pod")[:10]
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
        
    for article in articles:
        image_title = article.select_one("h3 > a").get('title').strip()
        relative_image = article.find("img")["src"].strip()
        image_url = urljoin(url , relative_image)
        print(f"\nurl : {image_url}")

        filename = sanitized_filename(image_title)+".jpg"
        filepath = os.path.join(IMAGE_DIR,filename)
        print(f"Filepath: {filepath}")

        print(f"Downloading : {image_title}")

        download_image(image_url , filepath)
    
    print(f"All 10 book's cover images are downloaded in images/ folder !!")

if __name__ == "__main__":
    scrape_and_download_images()



