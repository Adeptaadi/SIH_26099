from ml.config import SEMANTIC_WEIGHT, ATTRIBUTE_WEIGHT, SPECIFICATION_WEIGHT
from ml.extraction.attribute_extractor import extract_attributes
from ml.matching.scorer import calculate_semantic_score, compare_attributes
from ml.matching.classifier import classify_match
from ml.matching.explanation import generate_explanation

def match_materials(material_a, material_b, emb_a, emb_b):
    """
    Computes matching scores, performs classification, and builds MatchResult.
    Args:
        material_a (dict): material record with 'material_id', 'description'.
        material_b (dict): material record with 'material_id', 'description'.
        emb_a (np.ndarray): embedding vector for material A.
        emb_b (np.ndarray): embedding vector for material B.
    Returns:
        match_result (dict): Contract E MatchResult dictionary.
    """
    # 1. Semantic Similarity
    semantic_score = calculate_semantic_score(emb_a, emb_b)
    
    # 2. Extract Attributes
    attrs_a = extract_attributes(material_a.get("description", ""))
    attrs_b = extract_attributes(material_b.get("description", ""))
    
    # 3. Compare Attributes
    matched_attributes, differences, attribute_score, specification_score = compare_attributes(attrs_a, attrs_b)
    
    # 4. Calculate Hybrid Score
    hybrid_score = (
        SEMANTIC_WEIGHT * semantic_score +
        ATTRIBUTE_WEIGHT * attribute_score +
        SPECIFICATION_WEIGHT * specification_score
    )
    
    # 5. Classification & Overrides
    classification, is_overridden, critical_mismatches = classify_match(hybrid_score, differences)
    
    # 6. Generate Explanation
    scores_dict = {
        "semantic": semantic_score,
        "attribute": attribute_score,
        "specification": specification_score
    }
    explanation = generate_explanation(
        classification, scores_dict, matched_attributes, differences, is_overridden, critical_mismatches
    )
    
    # Build unique match_id
    m_a_id = material_a.get("material_id", "A")
    m_b_id = material_b.get("material_id", "B")
    match_id = f"MATCH_{m_a_id}_{m_b_id}"
    
    # Adjust confidence: if overridden to DIFFERENT, set confidence to 0.0 or low, but keep hybrid_score in scores
    confidence = hybrid_score
    if classification == "DIFFERENT" and is_overridden:
        confidence = min(0.3, confidence) # cap confidence for critical mismatches
        
    return {
        "match_id": match_id,
        "material_a_id": m_a_id,
        "material_b_id": m_b_id,
        "classification": classification,
        "confidence": round(confidence, 4),
        "scores": {
            "semantic": round(semantic_score, 4),
            "attribute": round(attribute_score, 4),
            "specification": round(specification_score, 4)
        },
        "matched_attributes": matched_attributes,
        "differences": differences,
        "explanation": explanation,
        "status": "PENDING_REVIEW"
    }

