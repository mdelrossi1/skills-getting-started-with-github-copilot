import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

def test_signup_and_unregister():
    activity = next(iter(client.get("/activities").json().keys()))
    email = "testuser@example.com"
    # Ensure not already signed up
    client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    # Duplicate signup should fail
    response_dup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response_dup.status_code == 400
    # Unregister
    response_unreg = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response_unreg.status_code == 200
    assert "Unregistered" in response_unreg.json()["message"]
    # Unregister again should fail
    response_unreg2 = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response_unreg2.status_code == 400
