import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_materials_upload():
    csv_data = "material_id,description\nA001,SS PIPE 2 IN SCH40 ASTM A312 TP304\nA002,VALVE GATE 3 IN 150# RF FLANGED\n"
    file = io.BytesIO(csv_data.encode("utf-8"))
    
    response = client.post(
        "/api/materials/upload",
        data={"organization_id": "ORG_A"},
        files={"file": ("test_a.csv", file, "text/csv")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["organization_id"] == "ORG_A"
    assert data["records_processed"] == 2
    assert data["status"] == "SUCCESS"

def test_invalid_file_type():
    file = io.BytesIO(b"dummy data")
    response = client.post(
        "/api/materials/upload",
        data={"organization_id": "ORG_A"},
        files={"file": ("test.txt", file, "text/plain")}
    )
    assert response.status_code == 400
