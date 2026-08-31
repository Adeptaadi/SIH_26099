from ml.embeddings.embedder import MaterialEmbedder
from ml.matching.ablation import run_ablation_study

def test_ablation_study():
    materials_a = [
        {"material_id": "A001", "description": "SS PIPE 2\" SCH40 ASTM A312 TP304"},
        {"material_id": "A002", "description": "CS PIPE 4\" SCH80 ASTM A106 GRADE B"}
    ]
    materials_b = [
        {"material_id": "B001", "description": "STAINLESS STEEL SEAMLESS PIPE 2 IN SCHEDULE 40 ASTM A312 GRADE TP304"},
        {"material_id": "B002", "description": "CARBON STEEL SEAMLESS PIPE 4 IN SCHEDULE 80 ASTM A106 GRADE B"}
    ]
    
    ground_truth = [
        {"material_a_id": "A001", "material_b_id": "B001", "label": "EQUIVALENT"},
        {"material_a_id": "A002", "material_b_id": "B002", "label": "EQUIVALENT"},
        {"material_a_id": "A001", "material_b_id": "B002", "label": "DIFFERENT"}
    ]
    
    embedder = MaterialEmbedder()
    res = run_ablation_study(materials_a, materials_b, ground_truth, embedder)
    
    assert "methods" in res
    assert len(res["methods"]) == 4
    
    method_names = [m["name"] for m in res["methods"]]
    assert "Exact String Matching" in method_names
    assert "Semantic Similarity Only" in method_names
    assert "Semantic + Attribute Matching" in method_names
    assert "Hybrid Pipeline (With Rules)" in method_names
    
    for m in res["methods"]:
        assert 0.0 <= m["precision"] <= 1.0
        assert 0.0 <= m["recall"] <= 1.0
        assert 0.0 <= m["f1_score"] <= 1.0
