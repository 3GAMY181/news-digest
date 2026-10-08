from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_api_status():
    # بنجرب الـ health endpoint كبداية لأنه سريع وسهل
    response = client.get("/health") 
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}