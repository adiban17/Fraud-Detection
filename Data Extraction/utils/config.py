# standard headers to mimic a real browser for basic requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# configuration for the static html scraper
STATIC_TARGETS = {
    "books_to_scrape": {
        "base_url": "http://books.toscrape.com/catalogue/category/books_1/page-{}.html",
        "selectors": {
            "container": {"tag": "article", "class": "product_pod"},
            "price": {"tag": "p", "class": "price_color"},
            "category_default": "books_and_media"
        }
    }
}

# configuration for the dynamic playwright scraper
# Updated utils/config.py
DYNAMIC_TARGETS = {
    "trustpilot": {
        "base_url": "https://www.trustpilot.com/review/{}?page={}",
        "merchants_to_track": [
            "www.amazon.com",
            "www.shein.com",
            "www.newegg.com",      
            "www.tripadvisor.com", 
            "www.asos.com",        
            "www.ebay.com"        
        ],
        "selectors": {
            "review_card": {"tag": "article"},
            "review_text": {"tag": "p"}
        }
    }
}