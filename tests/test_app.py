import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange
    # (No setup needed for this endpoint)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Arrange
    test_email = "teststudent@mergington.edu"
    activity = "Chess Club"
    # Ensure not already signed up
    client.post(f"/activities/{activity}/unregister", params={"email": test_email})

    # Act
    signup_response = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    duplicate_signup_response = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    unregister_response = client.post(f"/activities/{activity}/unregister", params={"email": test_email})
    duplicate_unregister_response = client.post(f"/activities/{activity}/unregister", params={"email": test_email})

    # Assert
    assert signup_response.status_code == 200
    assert f"Signed up {test_email}" in signup_response.json()["message"]
    assert duplicate_signup_response.status_code == 400
    assert unregister_response.status_code == 200
    assert f"Removed {test_email}" in unregister_response.json()["message"]
    assert duplicate_unregister_response.status_code == 400
