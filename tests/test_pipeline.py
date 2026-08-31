from ml.pipeline import find_matches

def test_pipeline():
    materials_a = [
        {"material_id": "A001", "description": "SS PIPE 2\" SCH40 ASTM A312 TP304"},
        {"material_id": "A002", "description": "CS PIPE 4\" SCH40 ASTM A106 GRADE B"}
    ]
    materials_b = [
        {"material_id": "B001", "description": "STAINLESS STEEL SEAMLESS PIPE 2 IN SCHEDULE 40 ASTM A312 GRADE TP304"},
        {"material_id": "B002", "description": "CARBON STEEL WELDED PIPE 4 IN SCHEDULE 40 ASTM A106 GRADE B"}
    ]
    
    results = find_matches(materials_a, materials_b)
    
    assert len(results) > 0
    # A001 should match B001 as EQUIVALENT
    a001_b001 = [r for r in results if r["material_a_id"] == "A001" and r["material_b_id"] == "B001"]
    assert len(a001_b001) > 0
    assert a001_b001[0]["classification"] == "EQUIVALENT"

