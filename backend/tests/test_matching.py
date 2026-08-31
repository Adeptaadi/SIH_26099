import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_matching_flow():
    # Upload materials for Org A
    csv_a = "material_id,description\nA001,SS PIPE 2 IN SCH40 ASTM A312 TP304\n"
    client.post(
        "/api/materials/upload",
        data={"organization_id": "ORG_A"},
        files={"file": ("org_a.csv", io.BytesIO(csv_a.encode("utf-8")), "text/csv")}
    )

    # Upload materials for Org B
    csv_b = "material_id,description\nB001,STAINLESS STEEL PIPE 2 IN SCHEDULE 40 ASTM A312 TP304\n"
    client.post(
        "/api/materials/upload",
        data={"organization_id": "ORG_B"},
        files={"file": ("org_b.csv", io.BytesIO(csv_b.encode("utf-8")), "text/csv")}
    )

    # Run matching
    response = client.post(
        "/api/matching/run",
        json={"organization_a": "ORG_A", "organization_b": "ORG_B"}
    )
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["status"] == "COMPLETED"

    # List matches
    list_res = client.get("/api/matches")
    assert list_res.status_code == 200
    matches = list_res.json()
    assert len(matches) > 0
    match_id = matches[0]["match_id"]

    # Get single match
    detail_res = client.get(f"/api/matches/{match_id}")
    assert detail_res.status_code == 200
    assert detail_res.json()["match_id"] == match_id
