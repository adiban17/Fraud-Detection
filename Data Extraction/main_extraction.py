from scrapers.static_scraper import scrape_static_sites
from scrapers.dynamic_scraper import scrape_dynamic_sites
from utils.file_handler import save_batch_to_csv

def run_extraction_pipeline():
    print("--- starting nexflow data extraction pipeline ---")
    
    # stage 1: extract static baselines (amounts & categories)
    print("\n[stage 1] scraping static baselines...")
    static_batch = []
    
    for item in scrape_static_sites(max_pages=5):
        static_batch.append(item)
        
        # save in batches of 20 to prevent data loss
        if len(static_batch) >= 20:
            save_batch_to_csv(static_batch, "data/raw/static_baselines.csv")
            static_batch = []
            
    # save any remaining static items that didn't make a full batch
    if static_batch:
        save_batch_to_csv(static_batch, "data/raw/static_baselines.csv")
        
    # stage 2: extract dynamic text for nlp processing
    print("\n[stage 2] scraping dynamic reviews for nlp...")
    dynamic_batch = []
    
    for item in scrape_dynamic_sites(max_pages=3):
        dynamic_batch.append(item)
        
        # save in batches of 10 (dynamic is slower, save more frequently)
        if len(dynamic_batch) >= 10:
            save_batch_to_csv(dynamic_batch, "data/raw/dynamic_reviews.csv")
            dynamic_batch = []
            
    # save any remaining dynamic items
    if dynamic_batch:
        save_batch_to_csv(dynamic_batch, "data/raw/dynamic_reviews.csv")
        
    print("\n--- extraction pipeline complete! data saved to data/raw/ ---")

if __name__ == "__main__":
    run_extraction_pipeline()