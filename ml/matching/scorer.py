import numpy as np

def calculate_semantic_score(emb_a, emb_b):
    # Dot product of normalized embeddings is cosine similarity
    similarity = float(np.dot(emb_a, emb_b))
    # Clip between 0.0 and 1.0
    return max(0.0, min(1.0, similarity))

def is_compatible(key, val_a, val_b):
    if not val_a or not val_b:
        return False
        
    str_a = str(val_a).strip().upper()
    str_b = str(val_b).strip().upper()
    
    if str_a == str_b:
        return True
        
    if key == "type":
        generics = {
            "PIPE": {"SEAMLESS PIPE", "WELDED PIPE", "PIPE"},
            "VALVE": {"BALL VALVE", "GATE VALVE", "GLOBE VALVE", "BUTTERFLY VALVE", "CHECK VALVE", "VALVE"},
            "BEARING": {"BALL BEARING", "ROLLER BEARING", "TAPERED ROLLER BEARING", "NEEDLE ROLLER BEARING", "BEARING"},
            "CABLE": {"XLPE CABLE", "PVC CABLE", "INSTRUMENTATION CABLE", "FLEXIBLE CABLE", "CABLE"},
            "BOLT": {"HEX BOLT", "BOLT"},
            "NUT": {"HEX NUT", "NUT"},
            "SCREW": {"SOCKET HEAD CAP SCREW", "SCREW"}
        }
        for gen, specifics in generics.items():
            if (str_a == gen and str_b in specifics) or (str_b == gen and str_a in specifics):
                return True
                
    return False

def compare_attributes(attrs_a, attrs_b):
    """
    Compares two attribute dictionaries and calculates attribute & spec scores.
    Returns:
        matched_attributes (list): Keys that match.
        differences (list): List of dicts describing mismatched keys.
        attribute_score (float): Score based on common attributes.
        specification_score (float): Score based on spec attributes.
    """
    all_keys = ["material", "type", "size", "grade", "standard", "schedule", "pressure_class", "diameter", "length", "voltage"]
    spec_keys = ["grade", "standard", "schedule", "pressure_class"]
    
    matched_attributes = []
    differences = []
    
    common_keys = []
    common_spec_keys = []
    
    for k in all_keys:
        val_a = attrs_a.get(k)
        val_b = attrs_b.get(k)
        
        if val_a is not None and val_b is not None:
            common_keys.append(k)
            if k in spec_keys:
                common_spec_keys.append(k)
                
            # Compare using compatibility function
            if is_compatible(k, val_a, val_b):
                matched_attributes.append(k)
            else:
                differences.append({
                    "attribute": k,
                    "value_a": val_a,
                    "value_b": val_b
                })
                
    # Calculate attribute score
    if len(common_keys) > 0:
        matches_count = len([k for k in common_keys if k in matched_attributes])
        attribute_score = float(matches_count / len(common_keys))
    else:
        # Default if no common attributes are extracted
        attribute_score = 1.0
        
    # Calculate specification score
    if len(common_spec_keys) > 0:
        spec_matches_count = len([k for k in common_spec_keys if k in matched_attributes])
        specification_score = float(spec_matches_count / len(common_spec_keys))
    else:
        specification_score = 1.0
        
    return matched_attributes, differences, attribute_score, specification_score


