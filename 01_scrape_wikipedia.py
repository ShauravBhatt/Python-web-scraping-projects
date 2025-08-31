"""
Challenge: Scrape Wikipedia h2 Headers

Use the `requests` and `BeautifulSoup` libraries to fetch the Wikipedia page 
on Python (programming language).

Your task is to:
1. Download the HTML of the page.
2. Parse all `<h2>` section headers.
3. Store the clean header titles in a list.
4. Print the total count and display the first 10 section titles.

Bonus:
- Handle network errors gracefully.
"""
 
import requests 
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Python_(programming_language)"

def get_h2_headers(URL):
    try: 
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
        }
        response = requests.get(URL , headers = headers ,timeout=7)
        response.raise_for_status()
    except requests.RequestException as e :
        print(f"Failed to fetch page: \n{e}")
        return []
    if response.status_code == 200: 
        soup = BeautifulSoup(response.text , "html.parser" )
        h2_tags = soup.find_all("h2")
        headers = []
        for tag in h2_tags:
            header_text = tag.get_text(strip=True)
            if header_text and header_text.lower() != "contents":
                headers.append(header_text)

        print(f"\nTotal Count of headers are : {len(headers)} !!")
        print(f"\nFirst 10 titles are: ")
        for indx , title in enumerate(headers[:10], 1):
            print(f"{indx}.) {title}")

    elif response.status_code == 400:
        print("Invalid request: ",response.reason)

    elif response.status_code == 404:
        print("Page doesn't exists: ",response.reason)

    elif response.status_code == 403:
        print("Access denied: ",response.reason)
    
    else:
        print("Error occurred, Try again !!")

get_h2_headers(URL)


