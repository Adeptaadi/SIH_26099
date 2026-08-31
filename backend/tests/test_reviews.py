import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_review_and_common_materials():
    # Setup upload and matching
    csv_a = "material_id,description\nA100,SS PIPE 2 IN SCH40 ASTM A312 TP304\n"
    csv_b = "material_id,description\nB100,STAINLESS STEEL PIPE 2 IN SCHEDULE 40 ASTM A312 TP304\n"
    client.post("/api/materials/upload", data={"organization_id": "ORG_A"}, files={"file": ("a.csv", io.BytesIO(csv_a.encode("utf-8")), "text/csv")})
    client.post("/api/materials/upload", data={"organization_id": "ORG_B"}, files={"file": ("b.csv", io.BytesIO(csv_b.encode("utf-8")), "text/csv")})
    client.post("/api/matching/run", json={"organization_a": "ORG_A", "organization_b": "ORG_B"})

    matches = client.get("/api/matches").json()
    assert len(matches) > 0
    match_id = matches[0]["match_id"]

    # Review match as APPROVED
    rev_res = client.post(f"/api/matches/{match_id}/review", json={"decision": "APPROVED"})
    assert rev_res.status_code == 200
    assert rev_res.json()["decision"] == "APPROVED"
    assert rev_res.json()["status"] == "APPROVED"

    # Check common materials list
    cm_res = client.get("/api/common-materials")
    assert cm_res.status_code == 200
    cms = cm_res.json()
    assert len(cms) > 0
