import subprocess
import sys

def run_command(command, description):
    print(f"\n>>> RUNNING: {description}")
    try:
        # Run the command and wait for it to finish
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR during {description}: {e}")
        sys.exit(1)

def execute_full_pipeline():
    print("=== NEXFLOW MASTER PIPELINE EXECUTION ===")

    # 1. Scrape fresh data for ALL merchants in config.py
    run_command("python \"Data Extraction/main_extraction.py\"", "Data Extraction (Scraping)")

    # 2. Process the new reviews through spaCy NLP
    run_command("python \"nlp_pipeline/process_reviews.py\"", "NLP Processing (Entity Extraction)")

    # 3. Merge the new merchant data with the static baseline
    run_command("python \"nlp_pipeline/merge_data_sources.py\"", "Data Merging")

    # 4. Generate the 1 Million row dataset using the new diversity
    run_command("python \"synthetic_generation/data_synthesizer.py\"", "Synthetic Scaling (1M Rows)")

    print("\n=== PIPELINE SUCCESSFUL ===")
    print("Your nexflow_master_dataset.csv is now updated with all merchants!")

if __name__ == "__main__":
    execute_full_pipeline()