import spacy
import re
import pandas as pd

# load the pre-trained english nlp model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("model not found. please run: python -m spacy download en_core_web_sm")
    exit()

def extract_entities_from_text(review_text):
    """
    uses spacy ner and heuristic matching to extract structured data from text.
    """
    # pass the text through the nlp pipeline
    doc = nlp(review_text)
    
    # initialize our default extracted values
    extracted_data = {
        "transaction_amount": None,
        "merchant_location": "Unknown",
        "merchant_category": "General Retail" 
    }
    
    # 1. extract money and locations using spacy's named entity recognition
    for ent in doc.ents:
        # extract the first money entity we find
        if ent.label_ == "MONEY" and extracted_data["transaction_amount"] is None:
            # clean the string (e.g. "$450.50" -> 450.50) using regex
            clean_amount = re.sub(r"[^\d.]", "", ent.text)
            if clean_amount:
                try:
                    extracted_data["transaction_amount"] = float(clean_amount)
                except ValueError:
                    pass
                    
        # extract the first location (geopolitical entity) we find
        if ent.label_ == "GPE" and extracted_data["merchant_location"] == "Unknown":
            extracted_data["merchant_location"] = ent.text

    # 2. extract categories using keyword heuristics (rule-based nlp)
    # customers usually say "i bought a laptop", not "i bought electronics"
    text_lower = review_text.lower()
    
    apparel_keywords = ["shirt", "shoes", "dress", "pants", "clothing", "apparel"]
    electronics_keywords = ["phone", "laptop", "computer", "tv", "headphones", "tablet"]
    home_keywords = ["furniture", "curtains", "bed", "sofa", "kitchen"]
    
    if any(word in text_lower for word in apparel_keywords):
        extracted_data["merchant_category"] = "Apparel"
    elif any(word in text_lower for word in electronics_keywords):
        extracted_data["merchant_category"] = "Electronics"
    elif any(word in text_lower for word in home_keywords):
        extracted_data["merchant_category"] = "Home Goods"

    return extracted_data

# test execution block
if __name__ == "__main__":
    print("testing spacy entity extraction...")
    
    # let's test it with a fake review based on the ones we scraped earlier
    test_review = "I paid $145.99 to a seller in California for some new shoes, but it was a total scam!"
    
    print(f"\nraw text: '{test_review}'")
    extracted = extract_entities_from_text(test_review)
    
    print("\n--- extracted features ---")
    for key, value in extracted.items():
        print(f"{key}: {value}")
        
    print("\ntest complete.")