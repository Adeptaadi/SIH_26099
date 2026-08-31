import os
import csv
from ml.pipeline import find_matches

WORKSPACE = r"c:\Users\Aaditya Rana\OneDrive\Desktop\SEM5\SIH"

def load_csv(path):
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows

def main():
    print("Running model evaluation pipeline...")
    
    # 1. Load data
    materials_a = load_csv(os.path.join(WORKSPACE, "data/raw/organization_a.csv"))
    materials_b = load_csv(os.path.join(WORKSPACE, "data/raw/organization_b.csv"))
    ground_truth = load_csv(os.path.join(WORKSPACE, "data/ground_truth/ground_truth.csv"))
    
    if not materials_a or not materials_b or not ground_truth:
        print("Error: Missing required datasets for evaluation.")
        return
        
    # 2. Run pipeline
    print(f"Running pipeline on {len(materials_a)} Org A and {len(materials_b)} Org B materials...")
    match_results = find_matches(materials_a, materials_b)
    print(f"Pipeline returned {len(match_results)} match candidate records.")
    
    # Map match_results to a lookup dictionary: (mat_a_id, mat_b_id) -> classification
    predictions = {}
    for m in match_results:
        key = (m["material_a_id"], m["material_b_id"])
        predictions[key] = m["classification"]
        
    # 3. Compute Metrics
    # We define:
    # Ground Truth: EQUIVALENT (Positive), DIFFERENT (Negative)
    # Predicted Positive: EQUIVALENT or REVIEW
    # Predicted Negative: DIFFERENT (or not in predictions)
    
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    
    # For hard-negatives subset tracking
    hn_total = 0
    hn_correct = 0
    
    for gt in ground_truth:
        a_id = gt["material_a_id"]
        b_id = gt["material_b_id"]
        true_label = gt["label"] # EQUIVALENT or DIFFERENT
        
        pred_class = predictions.get((a_id, b_id), "DIFFERENT")
        pred_label = "EQUIVALENT" if pred_class in ["EQUIVALENT", "REVIEW"] else "DIFFERENT"
        
        # Hard negative identification: true label is DIFFERENT but IDs are from same base index (e.g. A031 vs B031)
        # Note: In generate_dataset.py, hard negatives have index from 31 to 50 (i.e. A031 to A050 matching B031 to B050)
        # Let's check if the index matches
        is_hard_negative = False
        try:
            a_idx = int(a_id[1:])
            b_idx = int(b_id[1:])
            if a_idx == b_idx and true_label == "DIFFERENT":
                is_hard_negative = True
        except:
            pass
            
        if is_hard_negative:
            hn_total += 1
            if pred_label == "DIFFERENT":
                hn_correct += 1
                
        if true_label == "EQUIVALENT" and pred_label == "EQUIVALENT":
            tp += 1
        elif true_label == "DIFFERENT" and pred_label == "EQUIVALENT":
            fp += 1
        elif true_label == "DIFFERENT" and pred_label == "DIFFERENT":
            tn += 1
        elif true_label == "EQUIVALENT" and pred_label == "DIFFERENT":
            fn += 1
            
    total = len(ground_truth)
    accuracy = (tp + tn) / total if total > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    hn_accuracy = hn_correct / hn_total if hn_total > 0 else 0
    
    # 4. Report
    print("=" * 40)
    print("EVALUATION METRICS REPORT")
    print("=" * 40)
    print(f"Test pairs: {total}")
    print(f"True Positives (TP): {tp}")
    print(f"False Positives (FP): {fp}")
    print(f"True Negatives (TN): {tn}")
    print(f"False Negatives (FN): {fn}")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")
    print(f"F1 Score: {f1:.2%}")
    print(f"Hard-negative accuracy: {hn_accuracy:.2%}")
    print("=" * 40)
    
if __name__ == "__main__":
    main()

