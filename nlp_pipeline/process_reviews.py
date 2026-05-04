import pandas as pd
import re
import os
import sys

# append root to path to import your verified spacy extractor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nlp_pipeline.spacy_extractor import extract_entities_from_text

def heuristic_fraud_check(text):
    """
    a fast rule-based nlp check for explicit scam indicators.
    matches the 'understanding of nlp techniques' requirement.
    """
    scam_keywords = r"\b(scam|stolen|unauthorized|fake|never received|robbed|stole|fraud)\b"
    if re.search(scam_keywords, text.lower()):
        return True
    return False

def run_nlp_pipeline(input_file, output_file):
    print(f"--- starting nlp pipeline on {input_file} ---")
    
    # load the raw scraped data
    if not os.path.exists(input_file):
        print(f"error: {input_file} not found. please run the extraction pipeline first.")
        return

    df = pd.read_csv(input_file)
    processed_results = []

    print(f"processing {len(df)} reviews...")

    for index, row in df.iterrows():
        text = str(row['Review Text'])
        merchant = row['Merchant Name']
        
        # 1. extract entities using the verified spacy model
        entities = extract_entities_from_text(text)
        
        # 2. apply our heuristic fraud scoring logic
        is_fraudulent = heuristic_fraud_check(text)
        
        # 3. combine everything into a structured format
        processed_results.append({
            "merchant_name": merchant,
            "review_text": text[:100] + "...", # keep snippet for reference
            "transaction_amount": entities["transaction_amount"],
            "merchant_location": entities["merchant_location"],
            "merchant_category": entities["merchant_category"],
            "fraudulent": is_fraudulent
        })

    # create a clean, structured dataframe
    seed_df = pd.DataFrame(processed_results)
    
    # ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    seed_df.to_csv(output_file, index=False)
    
    print(f"\n--- nlp pipeline complete ---")
    print(f"structured seed data saved to: {output_file}")
    print(seed_df.head())

if __name__ == "__main__":
    # pathing based on your directory structure
    input_path = "data/raw/dynamic_reviews.csv" 
    output_path = "data/processed/structured_seed_data.csv"
    
    run_nlp_pipeline(input_path, output_path)