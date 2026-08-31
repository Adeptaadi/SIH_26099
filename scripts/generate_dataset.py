import os
import csv
import random

WORKSPACE = r"c:\Users\Aaditya Rana\OneDrive\Desktop\SEM5\SIH"

# Define the seed canonical materials
# Each item: category, material, type, size, grade, standard, schedule
seed_materials = [
    # PIPES
    ("PIPE", "STAINLESS STEEL", "SEAMLESS PIPE", "2 IN", "TP304", "ASTM A312", "40"),
    ("PIPE", "STAINLESS STEEL", "SEAMLESS PIPE", "3 IN", "TP316", "ASTM A312", "80"),
    ("PIPE", "CARBON STEEL", "WELDED PIPE", "4 IN", "GRADE B", "ASTM A106", "40"),
    ("PIPE", "CARBON STEEL", "SEAMLESS PIPE", "1 IN", "GRADE B", "ASTM A53", "80"),
    ("PIPE", "STAINLESS STEEL", "SEAMLESS PIPE", "6 IN", "TP316L", "ASTM A312", "40"),
    ("PIPE", "CARBON STEEL", "SEAMLESS PIPE", "8 IN", "GRADE B", "ASTM A106", "80"),
    ("PIPE", "ALLOY STEEL", "SEAMLESS PIPE", "2 IN", "P11", "ASTM A335", "160"),
    ("PIPE", "STAINLESS STEEL", "WELDED PIPE", "1/2 IN", "TP304L", "ASTM A312", "10S"),

    # VALVES
    ("VALVE", "BRASS", "BALL VALVE", "1/2 IN", "C37700", "ANSI B16.5", ""),
    ("VALVE", "STAINLESS STEEL", "GATE VALVE", "3 IN", "CF8M", "ANSI B16.34", ""),
    ("VALVE", "CARBON STEEL", "GLOBE VALVE", "2 IN", "WCB", "API 600", ""),
    ("VALVE", "CAST IRON", "BUTTERFLY VALVE", "6 IN", "GG25", "API 609", ""),
    ("VALVE", "STAINLESS STEEL", "CHECK VALVE", "4 IN", "CF8", "API 594", ""),
    ("VALVE", "BRONZE", "GATE VALVE", "1 IN", "B62", "MSS SP-80", ""),
    ("VALVE", "CARBON STEEL", "BALL VALVE", "2 IN", "LF2", "API 6D", ""),

    # BEARINGS
    ("BEARING", "CHROME STEEL", "BALL BEARING", "50MM", "6210-2RS", "ISO 15", ""),
    ("BEARING", "CHROME STEEL", "ROLLER BEARING", "80MM", "NU2211", "DIN 5412", ""),
    ("BEARING", "CHROME STEEL", "TAPERED ROLLER BEARING", "45MM", "30209", "ISO 355", ""),
    ("BEARING", "STAINLESS STEEL", "BALL BEARING", "25MM", "S6205-2RS", "ISO 15", ""),
    ("BEARING", "CHROME STEEL", "NEEDLE ROLLER BEARING", "20MM", "HK2016", "ISO 3245", ""),

    # FASTENERS
    ("FASTENER", "STAINLESS STEEL", "HEX BOLT", "M12", "A2-70", "DIN 933", ""),
    ("FASTENER", "CARBON STEEL", "HEX NUT", "M16", "CLASS 8", "DIN 934", ""),
    ("FASTENER", "STAINLESS STEEL", "WASHER", "M12", "A4", "DIN 125", ""),
    ("FASTENER", "CARBON STEEL", "SOCKET HEAD CAP SCREW", "M8", "GRADE 12.9", "DIN 912", ""),
    ("FASTENER", "BRASS", "HEX BOLT", "M10", "C3604", "DIN 931", ""),

    # CABLES
    ("CABLE", "COPPER", "XLPE CABLE", "4 CORE 16 SQMM", "1.1KV", "IEC 60502", ""),
    ("CABLE", "ALUMINUM", "PVC CABLE", "3 CORE 70 SQMM", "1.1KV", "IS 1554", ""),
    ("CABLE", "COPPER", "INSTRUMENTATION CABLE", "2 PAIR 1.5 SQMM", "500V", "BS 5308", ""),
    ("CABLE", "COPPER", "FLEXIBLE CABLE", "3 CORE 2.5 SQMM", "300/500V", "IEC 60227", ""),
    ("CABLE", "ALUMINUM", "XLPE CABLE", "4 CORE 120 SQMM", "11KV", "IEC 60502-2", ""),
]

def generate_org_a_description(seed):
    cat, mat, typ, size, grade, std, sch = seed
    
    # Randomly use abbreviations
    mat_abbr = mat
    if "STAINLESS STEEL" in mat:
        mat_abbr = random.choice(["SS", "S.S.", "STAINLESS STEEL"])
    elif "CARBON STEEL" in mat:
        mat_abbr = random.choice(["CS", "C.S.", "CARBON STEEL"])

    size_abbr = size
    if "IN" in size:
        size_abbr = size.replace(" IN", '"')
    
    sch_abbr = f"SCH{sch}" if sch else ""
    if sch_abbr and random.random() > 0.5:
        sch_abbr = f"SCHEDULE {sch}"

    parts = [mat_abbr, typ, size_abbr]
    if sch_abbr:
        parts.append(sch_abbr)
    if std:
        parts.append(std)
    if grade:
        parts.append(grade)

    # Shuffled or joined with spaces
    desc = " ".join([p for p in parts if p]).strip()
    # Add minor noise (like double spaces or trailing punctuation)
    if random.random() > 0.8:
        desc += "."
    return desc

def generate_org_b_description(seed):
    cat, mat, typ, size, grade, std, sch = seed

    # Organization B uses full terms and occasionally metric equivalents
    size_term = size
    if "2 IN" in size:
        size_term = random.choice(["2 IN", "50.8MM", "50.8 MM"])
    elif "1 IN" in size:
        size_term = random.choice(["1 IN", "25.4MM", "25.4 MM"])
    elif "3 IN" in size:
        size_term = random.choice(["3 IN", "76.2MM", "76.2 MM"])

    sch_term = f"SCHEDULE {sch}" if sch else ""

    parts = [mat, typ, size_term]
    if sch_term:
        parts.append(sch_term)
    if std:
        parts.append(std)
    if grade:
        parts.append(f"GRADE {grade}")

    desc = " ".join([p for p in parts if p]).strip()
    return desc

def main():
    print("Generating dataset...")
    
    # 1. Write Canonical Materials
    canonical_rows = []
    for idx, seed in enumerate(seed_materials, 1):
        c_id = f"M{idx:03d}"
        canonical_rows.append({
            "canonical_id": c_id,
            "category": seed[0],
            "material": seed[1],
            "type": seed[2],
            "size": seed[3],
            "grade": seed[4],
            "standard": seed[5],
            "schedule": seed[6]
        })
        
    os.makedirs(os.path.join(WORKSPACE, "data/canonical"), exist_ok=True)
    with open(os.path.join(WORKSPACE, "data/canonical/canonical_materials.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["canonical_id", "category", "material", "type", "size", "grade", "standard", "schedule"])
        writer.writeheader()
        writer.writerows(canonical_rows)

    # 2. Write Organization A and B records
    org_a_rows = []
    org_b_rows = []
    
    # Map from canonical id to org_a_id/org_b_id for generating equivalents
    equiv_pairs = []
    
    for idx, seed in enumerate(seed_materials, 1):
        c_id = f"M{idx:03d}"
        org_a_id = f"A{idx:03d}"
        org_b_id = f"B{idx:03d}"
        
        desc_a = generate_org_a_description(seed)
        desc_b = generate_org_b_description(seed)
        
        org_a_rows.append({"material_id": org_a_id, "organization_id": "ORG_A", "description": desc_a})
        org_b_rows.append({"material_id": org_b_id, "organization_id": "ORG_B", "description": desc_b})
        
        # Ground truth EQUIVALENT pair
        equiv_pairs.append((org_a_id, org_b_id, "EQUIVALENT"))

    # Generate extra noise records to reach ~60 records
    # Also to create hard negatives
    hard_negatives = []
    
    # Hard negative 1: Different sizes (e.g. 2 IN vs 3 IN)
    # Let's clone some seeds but change size
    extra_idx = len(seed_materials) + 1
    for seed in seed_materials[:10]:
        c_id = f"M{extra_idx:03d}"
        # Mismatched sizes
        size_a = seed[3]
        size_b = "3 IN" if "2 IN" in size_a else "2 IN"
        if "MM" in size_a:
            size_b = "80MM" if "50MM" in size_a else "50MM"
            
        seed_a = list(seed)
        seed_b = list(seed)
        seed_b[3] = size_b
        
        org_a_id = f"A{extra_idx:03d}"
        org_b_id = f"B{extra_idx:03d}"
        
        desc_a = generate_org_a_description(seed_a)
        desc_b = generate_org_b_description(seed_b)
        
        org_a_rows.append({"material_id": org_a_id, "organization_id": "ORG_A", "description": desc_a})
        org_b_rows.append({"material_id": org_b_id, "organization_id": "ORG_B", "description": desc_b})
        
        # This is a hard negative DIFFERENT because sizes mismatch
        hard_negatives.append((org_a_id, org_b_id, "DIFFERENT"))
        extra_idx += 1
        
    # Hard negative 2: Different grades (e.g. TP304 vs TP316)
    for seed in seed_materials[5:15]:
        c_id = f"M{extra_idx:03d}"
        grade_a = seed[4]
        grade_b = "TP316" if "TP304" in grade_a else "TP304"
        if "CF8M" in grade_a:
            grade_b = "CF8"
        elif "CF8" in grade_a:
            grade_b = "CF8M"
            
        seed_a = list(seed)
        seed_b = list(seed)
        seed_b[4] = grade_b
        
        org_a_id = f"A{extra_idx:03d}"
        org_b_id = f"B{extra_idx:03d}"
        
        desc_a = generate_org_a_description(seed_a)
        desc_b = generate_org_b_description(seed_b)
        
        org_a_rows.append({"material_id": org_a_id, "organization_id": "ORG_A", "description": desc_a})
        org_b_rows.append({"material_id": org_b_id, "organization_id": "ORG_B", "description": desc_b})
        
        # This is a hard negative DIFFERENT because grades mismatch
        hard_negatives.append((org_a_id, org_b_id, "DIFFERENT"))
        extra_idx += 1

    # Write Raw Organization Files
    os.makedirs(os.path.join(WORKSPACE, "data/raw"), exist_ok=True)
    with open(os.path.join(WORKSPACE, "data/raw/organization_a.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["material_id", "organization_id", "description"])
        writer.writeheader()
        writer.writerows(org_a_rows)
        
    with open(os.path.join(WORKSPACE, "data/raw/organization_b.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["material_id", "organization_id", "description"])
        writer.writeheader()
        writer.writerows(org_b_rows)

    # 3. Ground truth generation
    # Include all equiv_pairs, hard_negatives, and random negatives (clearly different)
    all_pairs = list(equiv_pairs) + list(hard_negatives)
    
    # Add random completely different pairs
    all_a_ids = [r["material_id"] for r in org_a_rows]
    all_b_ids = [r["material_id"] for r in org_b_rows]
    
    # We want around 150 total labeled pairs
    needed = 150 - len(all_pairs)
    random.seed(42)
    
    while needed > 0:
        a_id = random.choice(all_a_ids)
        b_id = random.choice(all_b_ids)
        
        # Ensure we don't duplicate and they are not equivalent or hard negative pairs (which have same index/ID suffixes)
        a_idx = int(a_id[1:])
        b_idx = int(b_id[1:])
        
        if a_idx != b_idx and not any(p[0] == a_id and p[1] == b_id for p in all_pairs):
            all_pairs.append((a_id, b_id, "DIFFERENT"))
            needed -= 1
            
    os.makedirs(os.path.join(WORKSPACE, "data/ground_truth"), exist_ok=True)
    with open(os.path.join(WORKSPACE, "data/ground_truth/ground_truth.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["material_a_id", "material_b_id", "label"])
        writer.writerows(all_pairs)

    print(f"Generated {len(canonical_rows)} canonical items.")
    print(f"Generated {len(org_a_rows)} Org A items.")
    print(f"Generated {len(org_b_rows)} Org B items.")
    print(f"Generated {len(all_pairs)} labeled ground truth pairs.")

if __name__ == "__main__":
    main()

