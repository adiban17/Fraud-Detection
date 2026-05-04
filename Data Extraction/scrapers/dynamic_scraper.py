from playwright.sync_api import sync_playwright
import json
import time
import random
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import DYNAMIC_TARGETS

def find_reviews_in_json(data):
    extracted = []
    if isinstance(data, dict):
        if "text" in data and isinstance(data["text"], str) and len(data["text"]) > 15:
            if "rating" in data or "consumer" in data or "language" in data or "id" in data:
                extracted.append(data["text"])
        for key, value in data.items():
            extracted.extend(find_reviews_in_json(value))
    elif isinstance(data, list):
        for item in data:
            extracted.extend(find_reviews_in_json(item))
    return extracted

def scrape_dynamic_sites(max_pages=3):
    config = DYNAMIC_TARGETS["trustpilot"]
    base_url = config["base_url"]
    merchants = config["merchants_to_track"]

    print(f"\n[Scraper] Initializing Playwright for {len(merchants)} merchants...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()

        for merchant in merchants:
            print(f"\n--- Merchant: {merchant} ---")
            for page_num in range(1, max_pages + 1):
                url = base_url.format(merchant, page_num)
                print(f"  > Scraping Page {page_num}: {url}")
                
                try:
                    # Navigate and wait
                    page.goto(url, wait_until="domcontentloaded", timeout=60000)
                    time.sleep(2) # Allow hydration
                    
                    # Strategy 1: JSON
                    json_text = page.evaluate("document.getElementById('__NEXT_DATA__') ? document.getElementById('__NEXT_DATA__').textContent : null")
                    
                    reviews_found = 0
                    if json_text:
                        site_data = json.loads(json_text)
                        full_reviews = find_reviews_in_json(site_data)
                        unique_reviews = list(set(full_reviews))
                        reviews_found = len(unique_reviews)
                        
                        for text in unique_reviews:
                            yield {"Merchant Name": merchant, "Review Text": text.strip()}
                    
                    # Fallback if JSON yielded nothing
                    if reviews_found == 0:
                        print(f"    ! No JSON found. Triggering DOM fallback...")
                        reviews_data = page.evaluate("""
                            () => Array.from(document.querySelectorAll('article')).map(card => {
                                let p = Array.from(card.querySelectorAll('p'));
                                return p.length > 0 ? p.reduce((a, b) => a.textContent.length > b.textContent.length ? a : b).textContent.trim() : null;
                            }).filter(t => t && t.length > 15)
                        """)
                        reviews_found = len(reviews_data)
                        for text in reviews_data:
                            yield {"Merchant Name": merchant, "Review Text": text}

                    print(f"    ✓ Successfully extracted {reviews_found} reviews.")
                                
                except Exception as e:
                    print(f"    ✕ Error on {merchant} P{page_num}: {str(e)[:50]}...")
                    
                time.sleep(random.uniform(2, 4))
                
        browser.close()
        print("\n[Scraper] Browser closed. Dynamic extraction finished.")

if __name__ == "__main__":
    # Test block
    for item in scrape_dynamic_sites(max_pages=1):
        pass