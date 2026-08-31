def generate_explanation(classification, scores, matched_attributes, differences, is_overridden, critical_mismatches):
    """
    Generates a structured, human-readable explanation of the match decision.
    """
    if classification == "EQUIVALENT":
        # All matched attributes
        if len(matched_attributes) > 0:
            attrs_str = ", ".join(matched_attributes)
            return f"Both records describe technically equivalent materials. Matched attributes: {attrs_str}."
        else:
            return "Both records describe technically equivalent materials."
            
    elif classification == "DIFFERENT":
        if is_overridden:
            # Tell which critical attribute mismatched
            reasons = []
            for diff in differences:
                attr = diff.get("attribute")
                if attr in critical_mismatches:
                    reasons.append(f"{attr} differs: {diff.get('value_a')} vs {diff.get('value_b')}")
            reasons_str = "; ".join(reasons)
            return f"The descriptions are similar, but a critical mismatch was detected: {reasons_str}."
        else:
            # Look at differences in general
            if len(differences) > 0:
                reasons = [f"{d['attribute']} mismatch ({d['value_a']} vs {d['value_b']})" for d in differences]
                reasons_str = ", ".join(reasons)
                return f"The materials are different: {reasons_str}."
            else:
                return "The materials are different and do not have sufficient semantic similarity."
                
    elif classification == "REVIEW":
        if len(differences) > 0:
            reasons = [f"{d['attribute']} ({d['value_a']} vs {d['value_b']})" for d in differences]
            reasons_str = ", ".join(reasons)
            return f"Under review. The materials are semantically similar, but have some differences: {reasons_str}."
        else:
            return "Under review. The materials match semantically, but some technical attributes are missing. Recommended for human review."
            
    return "No match decision could be determined."

