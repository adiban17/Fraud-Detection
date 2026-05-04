import requests
from bs4 import BeautifulSoup
import time
import random
import sys
import os
import re

# append the parent directory to the path so we can import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import HEADERS, STATIC_TARGETS

def scrape_static_sites(max_pages=2):
    # load the configuration for the static site
    config = STATIC_TARGETS["books_to_scrape"]
    base_url = config["base_url"]
    selectors = config["selectors"]
    
    for page in range(1, max_pages + 1):
        url = base_url.format(page)
        
        try:
            response = requests.get(url, headers=HEADERS)
            
            # break the loop if the page does not exist
            if response.status_code != 200:
                break
                
            soup = BeautifulSoup(response.text, "html.parser")
            
            # find all product containers using config selectors
            containers = soup.find_all(
                selectors["container"]["tag"], 
                class_=selectors["container"]["class"]
            )
            
            for container in containers:
                price_elem = container.find(
                    selectors["price"]["tag"], 
                    class_=selectors["price"]["class"]
                )
                
                if price_elem:
                    # extract only numbers and decimals using regex
                    raw_text = price_elem.text.strip()
                    price = re.sub(r"[^\d.]", "", raw_text)
                    
                    # yield the dictionary in the exact format required for the nlp pipeline
                    yield {
                        "Merchant Name": "books.toscrape.com",
                        "Review Text": f"transaction amount: {price} for category: {selectors['category_default']}"
                    }
                    
        except Exception as e:
            print(f"error scraping {url}: {e}")
            
        # add a polite delay to avoid overwhelming the server
        time.sleep(random.uniform(1.0, 2.0))

# this block allows you to test the scraper directly
if __name__ == "__main__":
    print("testing static scraper...")
    scraper_generator = scrape_static_sites(max_pages=1)
    
    # print the first 3 yielded items to verify it works
    for i, item in enumerate(scraper_generator):
        print(item)
        if i >= 2:
            break
    print("test complete.")