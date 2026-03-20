import pytest
from fastapi.testclient import TestClient
import uuid

from main import app

@pytest.fixture
def client():
    return TestClient(app)


def create_user(client, role="viewer", username="testuser"):
    return client.post(
        "/auth/register",
        json={
            "name": "test",
            "department": "IT",
            "email": f"{username}@example.com",
            "username": username,
            "password": "password123",
            "role": role,
            "admin_key": "THEADMINKEY" if role == "admin" else None,
        },
    )


def get_token(client, role="viewer", username="testuser"):
    create_user(client, role=role, username=username)
    res = client.post(
        "/auth/login", json={"username": username, "password": "password123"}
    )
    return res.json()["access_token"]


def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "test",
            "department": "IT",
            "email": "[test@example.com](mailto:test@example.com)",
            "username": "testuser",
            "password": "password123",
            "role": "viewer",
        },
    )
    assert response.status_code == 200
    assert "message" in response.json()


def test_login_success(client):
    client.post(
        "/auth/register",
        json={
            "name": "test",
            "department": "IT",
            "email": "[test@example.com](mailto:test@example.com)",
            "username": "testuser",
            "password": "password123",
            "role": "viewer",
        },
    )
    response = client.post(
        "/auth/login", json={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid(client):
    response = client.post(
        "/auth/login", json={"username": "wrong", "password": "wrong"}
    )
    assert response.status_code in (400, 401)


def test_protected_route_no_token(client):
    response = client.get("/student/view_students")
    assert response.status_code in (401, 403)


def test_protected_route_with_token(client):
    token = get_token(client)
    response = client.get(
        "/student/view_students", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_viewer_cannot_add_student(client):
    token = get_token(client, role="viewer", username="viewer1")

    response = client.post(
        "/admin/add_students",
        json={"name": "ashi", "std": "1", "roll": "2", "marks": [10, 10, 10, 10, 10]},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code in (401, 403)


def test_admin_can_add_student(client):
    token = get_token(client, role="admin", username="admin1")

    response = client.post(
        "/admin/add_students",
        json={"name": "ashi", "std": "1", "roll":str(uuid.uuid4()), "marks": [10, 10, 10, 10, 10]},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
