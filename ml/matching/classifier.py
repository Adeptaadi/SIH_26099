from ml.config import THRESHOLD_EQUIVALENT, THRESHOLD_REVIEW

def classify_match(score, differences):
    """
    Classifies a match based on the hybrid score and critical attribute differences.
    Returns:
        classification (str): EQUIVALENT, REVIEW, or DIFFERENT.
        is_overridden (bool): True if overridden due to critical mismatch.
    """
    # Default threshold-based classification
    if score >= THRESHOLD_EQUIVALENT:
        classification = "EQUIVALENT"
    elif score >= THRESHOLD_REVIEW:
        classification = "REVIEW"
    else:
        classification = "DIFFERENT"
        
    # Check for critical attribute differences
    # Critical attributes: material, size, grade, standard, schedule, pressure_class
    critical_attributes = {"material", "size", "grade", "standard", "schedule", "pressure_class"}
    
    has_critical_difference = False
    critical_mismatches = []
    
    for diff in differences:
        attr = diff.get("attribute")
        if attr in critical_attributes:
            has_critical_difference = True
            critical_mismatches.append(attr)
            
    is_overridden = False
    if has_critical_difference and classification != "DIFFERENT":
        # Override classification to DIFFERENT due to critical parameter mismatch
        classification = "DIFFERENT"
        is_overridden = True
        
    return classification, is_overridden, critical_mismatches

