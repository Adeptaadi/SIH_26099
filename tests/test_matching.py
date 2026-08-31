import numpy as np
from ml.matching.matcher import match_materials

def test_matching():
    # Test case 1: Equivalent materials
    mat_a = {"material_id": "A001", "description": "SS PIPE 2\" SCH40 ASTM A312 TP304"}
    mat_b = {"material_id": "B001", "description": "STAINLESS STEEL SEAMLESS PIPE 2 IN SCHEDULE 40 ASTM A312 GRADE TP304"}
    
    # Mock similar embeddings
    emb_a = np.array([1.0, 0.0, 0.0])
    emb_b = np.array([0.95, 0.1, 0.0])
    # Normalize mock embeddings
    emb_a = emb_a / np.linalg.norm(emb_a)
    emb_b = emb_b / np.linalg.norm(emb_b)
    
    res = match_materials(mat_a, mat_b, emb_a, emb_b)
    assert res["classification"] == "EQUIVALENT"
    assert "material" in res["matched_attributes"]
    assert "size" in res["matched_attributes"]
    assert len(res["differences"]) == 0
    
    # Test case 2: Hard negative (different sizes: 2" vs 3")
    mat_c = {"material_id": "B002", "description": "STAINLESS STEEL SEAMLESS PIPE 3 IN SCHEDULE 40 ASTM A312 GRADE TP304"}
    res2 = match_materials(mat_a, mat_c, emb_a, emb_b)
    assert res2["classification"] == "DIFFERENT"
    assert any(d["attribute"] == "size" for d in res2["differences"])
    assert "size differs" in res2["explanation"].lower()
    
    # Test case 3: Hard negative (different grades: TP304 vs TP316)
    mat_d = {"material_id": "B003", "description": "STAINLESS STEEL SEAMLESS PIPE 2 IN SCHEDULE 40 ASTM A312 GRADE TP316"}
    res3 = match_materials(mat_a, mat_d, emb_a, emb_b)
    assert res3["classification"] == "DIFFERENT"
    assert any(d["attribute"] == "grade" for d in res3["differences"])
    assert "grade differs" in res3["explanation"].lower()

