import re
from ml.normalization.normalizer import normalize_description
from ml.extraction.patterns import PATTERNS

def extract_attributes(text):
    # Initialize all possible attributes with None
    attributes = {
        "material": None,
        "type": None,
        "size": None,
        "grade": None,
        "standard": None,
        "schedule": None,
        "pressure_class": None,
        "diameter": None,
        "length": None,
        "voltage": None
    }
    
    if not text or not isinstance(text, str):
        return attributes
        
    normalized = normalize_description(text)
    
    for attr, pattern in PATTERNS.items():
        match = re.search(pattern, normalized)
        if match:
            if attr == "schedule":
                # Extract the group containing the actual schedule designation (e.g., 40, 80, 10S)
                attributes[attr] = match.group(1).strip()
            elif attr == "pressure_class":
                attributes[attr] = match.group(0).strip()
            elif attr == "voltage":
                attributes[attr] = match.group(0).strip()
            else:
                attributes[attr] = match.group(0).strip()
                
    # Additional refinement: if size contains bearing/cable dimensions, format properly
    # Ensure standard names and formats align with specs
    return attributes

