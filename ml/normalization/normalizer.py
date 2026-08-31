import re
from ml.normalization.dictionaries import TERM_MAPPINGS, UNIT_MAPPINGS

def normalize_description(text):
    if not text or not isinstance(text, str):
        return ""
    
    # 1. Upper case
    normalized = text.upper().strip()
    
    # Remove trailing punctuation (like trailing periods/dots)
    normalized = re.sub(r'[.,;:]+$', '', normalized)
    
    # 2. Apply Term Mappings
    for pattern, replacement in TERM_MAPPINGS.items():
        normalized = re.sub(pattern, replacement, normalized)
        
    # 3. Apply Unit Mappings
    for pattern, replacement in UNIT_MAPPINGS.items():
        normalized = re.sub(pattern, replacement, normalized)
        
    # 4. Clean extra spaces
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    return normalized

