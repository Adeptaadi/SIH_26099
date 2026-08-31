import numpy as np
from ml.normalization.normalizer import normalize_description
from ml.extraction.attribute_extractor import extract_attributes
from ml.matching.scorer import calculate_semantic_score, compare_attributes
from ml.matching.classifier import classify_match
from ml.matching.matcher import match_materials

def run_ablation_study(materials_a, materials_b, ground_truth, embedder):
    """
    Evaluates 4 different matching methods against the ground truth dataset.
    Args:
        materials_a (list): list of dicts from Org A
        materials_b (list): list of dicts from Org B
        ground_truth (list): list of ground truth dicts
        embedder (MaterialEmbedder): initialized embedder object
    Returns:
        ablation_results (dict): Contract R ablation results comparison.
    """
    # 1. Map ID to record
    map_a = {m["material_id"]: m for m in materials_a}
    map_b = {m["material_id"]: m for m in materials_b}
    
    # Pre-embed and pre-extract B
    desc_b = [normalize_description(m.get("description", "")) for m in materials_b]
    emb_b_matrix = embedder.embed(desc_b)
    map_emb_b = {m["material_id"]: emb_b_matrix[i] for i, m in enumerate(materials_b)}
    map_attrs_b = {m["material_id"]: extract_attributes(m.get("description", "")) for m in materials_b}
    
    # Pre-embed and pre-extract A
    desc_a = [normalize_description(m.get("description", "")) for m in materials_a]
    emb_a_matrix = embedder.embed(desc_a)
    map_emb_a = {m["material_id"]: emb_a_matrix[i] for i, m in enumerate(materials_a)}
    map_attrs_a = {m["material_id"]: extract_attributes(m.get("description", "")) for m in materials_a}
    
    # We will accumulate tp, fp, tn, fn for all 4 methods
    methods_stats = {
        1: {"tp": 0, "fp": 0, "tn": 0, "fn": 0},
        2: {"tp": 0, "fp": 0, "tn": 0, "fn": 0},
        3: {"tp": 0, "fp": 0, "tn": 0, "fn": 0},
        4: {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
    }
    
    for gt in ground_truth:
        a_id = gt.get("material_a_id")
        b_id = gt.get("material_b_id")
        true_label = gt.get("label") # EQUIVALENT or DIFFERENT
        
        mat_a = map_a.get(a_id)
        mat_b = map_b.get(b_id)
        
        if not mat_a or not mat_b:
            continue
            
        emb_a = map_emb_a[a_id]
        emb_b = map_emb_b[b_id]
        attrs_a = map_attrs_a[a_id]
        attrs_b = map_attrs_b[b_id]
        
        norm_a = normalize_description(mat_a.get("description", ""))
        norm_b = normalize_description(mat_b.get("description", ""))
        
        # Calculate semantic and attribute scores
        sem_score = calculate_semantic_score(emb_a, emb_b)
        matched_attributes, differences, attribute_score, specification_score = compare_attributes(attrs_a, attrs_b)
        
        # Define 4 predictions:
        
        # Method 1: Exact string match
        pred_class_1 = "EQUIVALENT" if norm_a == norm_b else "DIFFERENT"
        
        # Method 2: Semantic only
        pred_class_2 = "EQUIVALENT" if sem_score >= 0.85 else ("REVIEW" if sem_score >= 0.60 else "DIFFERENT")
        
        # Method 3: Semantic + Basic Attributes (No overrides)
        hybrid_score_basic = 0.5 * sem_score + 0.5 * attribute_score
        pred_class_3 = "EQUIVALENT" if hybrid_score_basic >= 0.85 else ("REVIEW" if hybrid_score_basic >= 0.60 else "DIFFERENT")
        
        # Method 4: Hybrid System (Full pipeline with overrides)
        res_4 = match_materials(mat_a, mat_b, emb_a, emb_b)
        pred_class_4 = res_4["classification"]
        
        # Map classes to binary decision
        predictions = {
            1: "EQUIVALENT" if pred_class_1 in ["EQUIVALENT", "REVIEW"] else "DIFFERENT",
            2: "EQUIVALENT" if pred_class_2 in ["EQUIVALENT", "REVIEW"] else "DIFFERENT",
            3: "EQUIVALENT" if pred_class_3 in ["EQUIVALENT", "REVIEW"] else "DIFFERENT",
            4: "EQUIVALENT" if pred_class_4 in ["EQUIVALENT", "REVIEW"] else "DIFFERENT"
        }
        
        # Accumulate metrics
        for m_num in range(1, 5):
            pred_label = predictions[m_num]
            stats = methods_stats[m_num]
            
            if true_label == "EQUIVALENT" and pred_label == "EQUIVALENT":
                stats["tp"] += 1
            elif true_label == "DIFFERENT" and pred_label == "EQUIVALENT":
                stats["fp"] += 1
            elif true_label == "DIFFERENT" and pred_label == "DIFFERENT":
                stats["tn"] += 1
            elif true_label == "EQUIVALENT" and pred_label == "DIFFERENT":
                stats["fn"] += 1
                
    # Calculate Precision, Recall, F1 for each
    names = {
        1: "Exact String Matching",
        2: "Semantic Similarity Only",
        3: "Semantic + Attribute Matching",
        4: "Hybrid Pipeline (With Rules)"
    }
    
    ablation_results = []
    for m_num in range(1, 5):
        stats = methods_stats[m_num]
        tp, fp, fn = stats["tp"], stats["fp"], stats["fn"]
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        
        ablation_results.append({
            "name": names[m_num],
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1_score, 4)
        })
        
    return {"methods": ablation_results}
