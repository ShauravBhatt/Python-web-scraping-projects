"""
 Challenge: Quote of the Day Image Maker

Goal:
- Scrape random quotes from https://quotes.toscrape.com/
- Extract quote text and author for the first 5 quotes
- Create an image for each quote using PIL (Pillow)
- Save images in 'quotes/' directory using filenames like quote_1.png, quote_2.png, etc.
"""

import os
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import textwrap

BASE_URL = "https://quotes.toscrape.com/"
OUTPUT_DIR = "quotes"

def fetch_quotes():
    try:
        response = requests.get(BASE_URL, timeout=7)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Error:", e)
        return []

    quotes = []
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.select("div.quote")[:5]

    for row in data:
        quote = row.find("span", class_="text").text.strip("“”")
        author = row.find("small", class_="author").text.strip()
        quotes.append((quote, author))

    return quotes

def create_image(text, author, indx):
    width, height = 1000, 600
    background_color = "#fffbea"
    text_color = "#333333"
    author_color = "#555555"

    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 28)
        author_font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
        author_font = ImageFont.load_default()

    wrapped_text = textwrap.fill(text, width=70)
    author_text = f"- {author}"

    text_y = 100
    draw.text((80, text_y), wrapped_text, font=font, fill=text_color)

    text_lines = wrapped_text.count('\n') + 1
    author_y = text_y + text_lines * 35 + 20
    draw.text((width - 300, author_y), author_text, font=author_font, fill=author_color)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    filename = os.path.join(OUTPUT_DIR, f"quote_{indx}.png")
    image.save(filename)
    print(f"Saved: {filename}")

def main():
    quotes = fetch_quotes()
    for indx, (quote, author) in enumerate(quotes, start=1):
        create_image(quote, author, indx)

if __name__ == "__main__":
    main()
