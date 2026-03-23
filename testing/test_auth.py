import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def create_user(username, role="viewer"):
    return client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "department": "IT",
            "email": f"{username}@test.com",
            "username": username,
            "password": "password123",
            "role": role,
            "admin_key": "testkey" if role == "admin" else None,
        },
    )


def get_token(username):
    response = client.post(
        "/auth/login",
        json={"username": username, "password": "password123"},
    )
    return response.json()["access_token"]


def test_login_success():
    create_user("user1")
    response = client.post(
        "/auth/login",
        json={"username": "user1", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password():
    create_user("user2")
    response = client.post(
        "/auth/login",
        json={"username": "user2", "password": "wrongpass"},
    )
    assert response.status_code == 401


def test_protected_route_requires_token():
    response = client.get("/student/view_students")
    assert response.status_code == 401


def test_viewer_cannot_add_student():
    create_user("viewer1", role="viewer")
    token = get_token("viewer1")
    response = client.post(
        "/admin/add_students",
        json={
            "name": "Asha",
            "std": "10",
            "roll": "1",
            "marks": [80, 90],
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403
