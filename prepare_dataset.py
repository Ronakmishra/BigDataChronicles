from datasets import load_dataset

def download_and_save_gaia_metadata():
    # Load the GAIA dataset
    dataset = load_dataset("gaia-benchmark/GAIA", "2023_all")

    # Save the metadata.jsonl file for the 'validation' split
    dataset["validation"].to_json("metadata.jsonl", orient="records", lines=True)
    print("metadata.jsonl saved successfully!")

if __name__ == "__main__":
    download_and_save_gaia_metadata()
