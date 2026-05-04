import pandas as pd
import os

def save_batch_to_csv(data_batch, filename="data/raw/raw_reviews.csv"):
    """
    takes a list of dictionaries and appends it to a csv.
    creates the file and directory if they don't exist.
    """
    if not data_batch:
        return

    # ensure the target directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # convert the batch of dictionaries into a pandas dataframe
    df = pd.DataFrame(data_batch)
    
    # if the file already exists, append (mode='a') and skip headers
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        # if it is a new file, write (mode='w') and include headers
        df.to_csv(filename, mode='w', header=True, index=False)
        
    print(f"successfully saved a batch of {len(data_batch)} rows to {filename}")