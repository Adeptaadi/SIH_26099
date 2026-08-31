from ml.evaluation.evaluator import compute_evaluation_metrics

def test_evaluation_metrics():
    # Mock database matches
    db_matches = [
        {"material_a_id": "A001", "material_b_id": "B001", "classification": "EQUIVALENT"},
        {"material_a_id": "A002", "material_b_id": "B002", "classification": "REVIEW"},
        {"material_a_id": "A003", "material_b_id": "B003", "classification": "DIFFERENT"}
    ]
    
    # Mock ground truth labels
    ground_truth = [
        {"material_a_id": "A001", "material_b_id": "B001", "label": "EQUIVALENT"}, # TP
        {"material_a_id": "A002", "material_b_id": "B002", "label": "EQUIVALENT"}, # TP (REVIEW maps to equivalent prediction)
        {"material_a_id": "A003", "material_b_id": "B003", "label": "DIFFERENT"},  # TN (DIFFERENT maps to different prediction)
        {"material_a_id": "A004", "material_b_id": "B004", "label": "EQUIVALENT"}  # FN (Not in DB matches -> default DIFFERENT)
    ]
    
    metrics = compute_evaluation_metrics(db_matches, ground_truth)
    
    assert metrics["total_pairs"] == 4
    assert metrics["confusion_matrix"]["true_positives"] == 2
    assert metrics["confusion_matrix"]["true_negatives"] == 1
    assert metrics["confusion_matrix"]["false_negatives"] == 1
    assert metrics["confusion_matrix"]["false_positives"] == 0
    assert metrics["accuracy"] == 0.75
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 0.6667
    assert metrics["f1_score"] == 0.8
