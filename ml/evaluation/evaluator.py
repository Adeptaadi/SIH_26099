def compute_evaluation_metrics(db_matches, ground_truth):
    """
    Computes evaluation metrics (Accuracy, Precision, Recall, F1-Score) and 
    the Confusion Matrix counts.
    Args:
        db_matches (list): list of dicts with 'material_a_id', 'material_b_id', 'classification'
        ground_truth (list): list of dicts with 'material_a_id', 'material_b_id', 'label'
    Returns:
        metrics (dict): Contract Q metrics response dictionary.
    """
    predictions = {}
    for m in db_matches:
        key = (m.get("material_a_id"), m.get("material_b_id"))
        predictions[key] = m.get("classification")
        
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    
    hn_total = 0
    hn_correct = 0
    
    for gt in ground_truth:
        a_id = gt.get("material_a_id")
        b_id = gt.get("material_b_id")
        true_label = gt.get("label") # EQUIVALENT or DIFFERENT
        
        pred_class = predictions.get((a_id, b_id), "DIFFERENT")
        pred_label = "EQUIVALENT" if pred_class in ["EQUIVALENT", "REVIEW"] else "DIFFERENT"
        
        # Hard Negative: true label is DIFFERENT but base indices match (e.g. A031 vs B031)
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
            
    total_pairs = len(ground_truth)
    accuracy = (tp + tn) / total_pairs if total_pairs > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    hn_accuracy = hn_correct / hn_total if hn_total > 0 else 0.0
    
    return {
        "total_pairs": total_pairs,
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1_score, 4),
        "hard_negative_accuracy": round(hn_accuracy, 4),
        "confusion_matrix": {
            "true_positives": tp,
            "false_positives": fp,
            "true_negatives": tn,
            "false_negatives": fn
        }
    }
