import pandas as pd
import re
import os

def extract_price_from_static_text(text):
    # the static text looks like "transaction amount: 51.77 for category: books_and_media"
    match = re.search(r"transaction amount: ([\d.]+)", text)
    return float(match.group(1)) if match else 0.0

def merge_and_finalize_seed():
    print("--- merging static and dynamic data sources ---")
    
    # 1. Load the NLP-processed dynamic reviews
    dynamic_path = "data/processed/structured_seed_data.csv"
    if not os.path.exists(dynamic_path):
        print("error: run process_reviews.py first!")
        return
    
    seed_df = pd.read_csv(dynamic_path)
    
    # 2. Load the raw static baselines
    static_raw_path = "data/raw/static_baselines.csv"
    if os.path.exists(static_raw_path):
        static_raw = pd.read_csv(static_raw_path)
        
        static_processed = []
        for _, row in static_raw.iterrows():
            static_processed.append({
                "merchant_name": row["Merchant Name"],
                "review_text": "Standard transaction baseline (non-review data)",
                "transaction_amount": extract_price_from_static_text(row["Review Text"]),
                "merchant_location": "UK (Primary Warehouse)", # Sandbox site is UK based
                "merchant_category": "Books & Media",
                "fraudulent": False # Static sandbox data is our 'safe' baseline
            })
        
        static_df = pd.DataFrame(static_processed)
        
        # 3. Combine them
        final_seed_df = pd.concat([seed_df, static_df], ignore_index=True)
        
        # save the new Master Seed
        master_seed_path = "data/processed/master_seed_data.csv"
        final_seed_df.to_csv(master_seed_path, index=False)
        
        print(f"success! merged {len(static_df)} static rows with {len(seed_df)} dynamic rows.")
        print(f"new master seed saved to: {master_seed_path}")

        
        
    
        
    else:
        print(f"warning: static baselines not found. skipping static merge.")
        # ADD THESE TWO LINES:
        master_seed_path = "data/processed/master_seed_data.csv"
        seed_df.to_csv(master_seed_path, index=False)

if __name__ == "__main__":
    merge_and_finalize_seed()