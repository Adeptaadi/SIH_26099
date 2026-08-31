import os
import csv
from ml.normalization.normalizer import normalize_description

WORKSPACE = r"c:\Users\Aaditya Rana\OneDrive\Desktop\SEM5\SIH"

def preprocess_file(input_rel, output_rel):
    input_path = os.path.join(WORKSPACE, input_rel)
    output_path = os.path.join(WORKSPACE, output_rel)
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} does not exist.")
        return
        
    rows = []
    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get("description", "")
            norm_desc = normalize_description(desc)
            rows.append({
                "material_id": row.get("material_id"),
                "organization_id": row.get("organization_id"),
                "description": desc,
                "normalized_description": norm_desc
            })
            
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["material_id", "organization_id", "description", "normalized_description"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Preprocessed {len(rows)} records: {input_rel} -> {output_rel}")

def main():
    print("Preprocessing raw datasets...")
    preprocess_file("data/raw/organization_a.csv", "data/processed/normalized_a.csv")
    preprocess_file("data/raw/organization_b.csv", "data/processed/normalized_b.csv")
    print("Preprocessing complete!")

if __name__ == "__main__":
    main()

