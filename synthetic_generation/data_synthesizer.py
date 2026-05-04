import pandas as pd
import numpy as np
from faker import Faker
import os
import random

fake = Faker()

def generate_master_dataset(seed_file, output_file, target_rows=1000000):
    print(f"--- Generating 1M rows with Overlapping Probabilistic Distributions ---")
    
    if not os.path.exists(seed_file):
        print(f"Error: Seed file {seed_file} not found.")
        return
        
    seed_df = pd.read_csv(seed_file)
    merchants = seed_df['merchant_name'].unique()
    
    hot_devices = [fake.sha1()[:12].upper() for _ in range(5000)]
    user_avg_spend = {f"USR-{i}": random.uniform(20, 100) for i in range(100000, 200000)}

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    chunk_size = 100000
    num_chunks = target_rows // chunk_size

    for i in range(num_chunks):
        print(f"processing chunk {i+1}/{num_chunks}...")
        
        # Base metadata
        uids = [random.choice(list(user_avg_spend.keys())) for _ in range(chunk_size)]
        base_times = [fake.date_time_this_year() for _ in range(chunk_size)]
        
        # Pre-allocate lists
        amounts = [0.0] * chunk_size
        balances = [0.0] * chunk_size
        timestamps = [""] * chunk_size
        ips = [""] * chunk_size
        user_locs = [""] * chunk_size
        merchant_locs = [""] * chunk_size
        categories = [""] * chunk_size
        device_types = [""] * chunk_size
        payment_methods = [""] * chunk_size
        transaction_statuses = [""] * chunk_size
        d_ids = [""] * chunk_size
        is_fraud = []
        
        for j in range(chunk_size):
            # 1. Target Label (18% Fraud)
            is_this_fraud = 1 if random.random() < 0.18 else 0
            is_fraud.append(is_this_fraud)
            
            if is_this_fraud:
                # --- FRAUD DISTRIBUTIONS (High Variance & Overlap) ---
                ips[j] = random.choice(["0.0.0.0", "127.0.0.1"]) if random.random() < 0.45 else fake.ipv4()
                
                # 60% chance of night, 40% chance of day (Overlap)
                hour = random.randint(1, 4) if random.random() < 0.60 else random.randint(5, 23)
                
                # Amounts center at $650 but swing widely
                amounts[j] = max(5.0, round(random.gauss(650, 350), 2))
                
                # Balances: 65% drain accounts (high ratio), 35% steal rich accounts
                if random.random() < 0.65:
                    balances[j] = round(amounts[j] + random.uniform(-20, 100), 2)
                else:
                    balances[j] = max(0.0, round(random.gauss(2500, 1500), 2))
                    
                # Devices: 75% use a botnet (triggers velocity feature)
                d_ids[j] = random.choice(hot_devices) if random.random() < 0.75 else fake.sha1()[:12].upper()
                
                categories[j] = random.choices(['Electronics', 'Apparel', 'Home Goods', 'General Retail'], weights=[0.5, 0.2, 0.1, 0.2])[0]
                user_locs[j] = random.choice(['USA', 'UK', 'Canada'])
                merchant_locs[j] = random.choice(['China', 'Russia', 'USA']) if random.random() < 0.6 else user_locs[j]

            else:
                # --- SAFE DISTRIBUTIONS (Overlaps with Fraud) ---
                ips[j] = random.choice(["0.0.0.0", "127.0.0.1"]) if random.random() < 0.02 else fake.ipv4()
                
                # 5% chance of night, 95% chance of day
                hour = random.randint(1, 4) if random.random() < 0.05 else random.randint(5, 23)
                
                # Amounts center at $120
                amounts[j] = max(2.0, round(random.gauss(120, 80), 2))
                balances[j] = max(150.0, round(random.gauss(4000, 2000), 2))
                
                # Devices: 10% use shared public computers (triggers false positive velocity)
                d_ids[j] = random.choice(hot_devices) if random.random() < 0.10 else fake.sha1()[:12].upper()
                
                categories[j] = random.choices(['Electronics', 'Apparel', 'Home Goods', 'General Retail'], weights=[0.15, 0.40, 0.25, 0.20])[0]
                user_locs[j] = random.choice(['USA', 'UK', 'Canada'])
                merchant_locs[j] = user_locs[j] if random.random() < 0.9 else random.choice(['China', 'USA'])

            # Apply Time and Standard Choices
            timestamps[j] = base_times[j].replace(hour=hour).strftime('%Y-%m-%d %H:%M:%S.%f')
            device_types[j] = random.choice(['Mobile', 'Desktop', 'Tablet'])
            
            # Subtle payment/status correlations
            if is_this_fraud:
                payment_methods[j] = random.choices(['Credit Card', 'Debit Card', 'PayPal', 'Apple Pay', 'Crypto'], weights=[0.2, 0.2, 0.2, 0.1, 0.3])[0]
                transaction_statuses[j] = random.choices(['Approved', 'Declined', 'Refunded'], weights=[0.4, 0.4, 0.2])[0]
            else:
                payment_methods[j] = random.choices(['Credit Card', 'Debit Card', 'PayPal', 'Apple Pay', 'Crypto'], weights=[0.4, 0.3, 0.15, 0.1, 0.05])[0]
                transaction_statuses[j] = random.choices(['Approved', 'Declined', 'Refunded'], weights=[0.85, 0.10, 0.05])[0]

        chunk_df = pd.DataFrame({
            "transaction_id": [fake.uuid4() for _ in range(chunk_size)],
            "user_id": uids,
            "transaction_amount": amounts,
            "transaction_timestamp": timestamps,
            "user_location": user_locs,
            "merchant_location": merchant_locs,
            "merchant_category": categories,
            "merchant_name": [random.choice(merchants) for _ in range(chunk_size)],
            "device_id": d_ids,
            "device_type": device_types,
            "payment_method": payment_methods,
            "account_balance": balances,
            "transaction_status": transaction_statuses,
            "ip_address": ips,
            "is_fraudulent": is_fraud
        })
        
        mode = 'w' if i == 0 else 'a'
        header = True if i == 0 else False
        chunk_df.to_csv(output_file, index=False, mode=mode, header=header)

    print(f"\n--- Master Dataset complete at {output_file} ---")

if __name__ == "__main__":
    seed_path = "data/processed/master_seed_data.csv"
    final_path = "data/final/nexflow_master_dataset.csv"
    generate_master_dataset(seed_path, final_path)