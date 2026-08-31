# Normalization dictionaries

# Word/abbreviation mappings to preserve technical meaning
TERM_MAPPINGS = {
    r"\bSS(?!\w)": "STAINLESS STEEL",
    r"\bS\.S\.?(?!\w)": "STAINLESS STEEL",
    r"\bCS(?!\w)": "CARBON STEEL",
    r"\bC\.S\.?(?!\w)": "CARBON STEEL",
    r"\bSCH\.?\s*([0-9S]+)\b": r"SCHEDULE \1",
    r"\bSCH\.?(?!\w)": "SCHEDULE",
    r"\bDIA(?!\w)": "DIAMETER",
    r"\bDIA\.?(?!\w)": "DIAMETER",
}



# Unit mappings
UNIT_MAPPINGS = {
    r'(\d+)\s*"': r"\1 IN",
    r'(\d+/\d+)\s*"': r"\1 IN",
    r'(\d+\.\d+)\s*"': r"\1 IN",
    r"\b50\.8\s*MM\b": "2 IN",
    r"\b50\.8MM\b": "2 IN",
    r"\b25\.4\s*MM\b": "1 IN",
    r"\b25\.4MM\b": "1 IN",
    r"\b76\.2\s*MM\b": "3 IN",
    r"\b76\.2MM\b": "3 IN",
    r"\b12\.7\s*MM\b": "1/2 IN",
    r"\b12\.7MM\b": "1/2 IN",
    r"\b101\.6\s*MM\b": "4 IN",
    r"\b101\.6MM\b": "4 IN",
    r"\b152\.4\s*MM\b": "6 IN",
    r"\b152\.4MM\b": "6 IN",
    r"\b203\.2\s*MM\b": "8 IN",
    r"\b203\.2MM\b": "8 IN",
}

