# import pytest
# import uuid
# from fastapi import status

# from testing.conftest import create_user, get_token


# # ── Registration ──────────────────────────────────────────────────────────────


# def test_register_viewer_success(client):
#     response = create_user(client, role="viewer", username="viewer1")
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["message"] == "User registered successfully"


# def test_register_admin_success(client):
#     response = create_user(client, role="admin", username="admin1")
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["message"] == "User registered successfully"


# def test_register_duplicate_username(client):
#     create_user(client, role="viewer", username="dupuser")
#     response = create_user(client, role="viewer", username="dupuser")
#     assert response.status_code == status.HTTP_409_CONFLICT
#     assert "Username already exists" in response.json()["detail"]


# def test_register_duplicate_email(client):
#     create_user(client, role="viewer", username="user1")
#     response = client.post(
#         "/auth/register",
#         json={
#             "name": "Other",
#             "department": "IT",
#             "email": "user1@example.com",
#             "username": "user2",
#             "password": "password123",
#             "role": "viewer",
#         },
#     )
#     assert response.status_code == status.HTTP_409_CONFLICT


# def test_register_admin_wrong_key(client):
#     response = client.post(
#         "/auth/register",
#         json={
#             "name": "Fake Admin",
#             "department": "IT",
#             "email": "fakeadmin@example.com",
#             "username": "fakeadmin",
#             "password": "password123",
#             "role": "admin",
#             "admin_key": "WRONGKEY",
#         },
#     )
#     assert response.status_code == status.HTTP_403_FORBIDDEN
#     assert response.json()["detail"] == "Invalid admin key"


# def test_register_admin_missing_key(client):
#     response = client.post(
#         "/auth/register",
#         json={
#             "name": "No Key Admin",
#             "department": "IT",
#             "email": "nokey@example.com",
#             "username": "nokeyadmin",
#             "password": "password123",
#             "role": "admin",
#             "admin_key": None,
#         },
#     )
#     assert response.status_code == status.HTTP_400_BAD_REQUEST
#     assert "admin_key is required" in response.json()["detail"]


# def test_register_password_too_short(client):
#     response = client.post(
#         "/auth/register",
#         json={
#             "name": "Short Pass",
#             "department": "IT",
#             "email": "short@example.com",
#             "username": "shortpass",
#             "password": "short",
#             "role": "viewer",
#         },
#     )
#     assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# def test_register_missing_fields(client):
#     response = client.post("/auth/register", json={"username": "incomplete"})
#     assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# # ── Login ─────────────────────────────────────────────────────────────────────


# def test_login_success(client):
#     create_user(client, role="viewer", username="loginuser")
#     response = client.post(
#         "/auth/login",
#         json={
#             "username": "loginuser",
#             "password": "password123",
#         },
#     )
#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     assert "access_token" in data
#     assert data["token_type"] == "bearer"


# def test_login_wrong_password(client):
#     create_user(client, role="viewer", username="wrongpass")
#     response = client.post(
#         "/auth/login",
#         json={
#             "username": "wrongpass",
#             "password": "notmypassword",
#         },
#     )
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()["detail"] == "Incorrect username or password"


# def test_login_nonexistent_user(client):
#     response = client.post(
#         "/auth/login",
#         json={
#             "username": "nobody",
#             "password": "password123",
#         },
#     )
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED


# # ── Token verification ────────────────────────────────────────────────────────


# def test_is_auth_valid_token(client):
#     token = get_token(client, role="viewer", username="authuser")
#     response = client.get("/auth/is_auth", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["username"] == "authuser"
#     assert response.json()["role"] == "viewer"


# def test_is_auth_no_token(client):
#     response = client.get("/auth/is_auth")
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED


# def test_is_auth_invalid_token(client):
#     response = client.get(
#         "/auth/is_auth", headers={"Authorization": "Bearer invalidtoken"}
#     )
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()["detail"] == "Invalid token"


# def test_is_auth_expired_token(client):
#     import jwt
#     from datetime import datetime, timedelta, timezone

#     expired = jwt.encode(
#         {
#             "username": "someone",
#             "role": "viewer",
#             "exp": datetime.now(timezone.utc) - timedelta(hours=1),
#         },
#         "test-secret-key",
#         algorithm="HS256",
#     )
#     response = client.get(
#         "/auth/is_auth", headers={"Authorization": f"Bearer {expired}"}
#     )
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()["detail"] == "Token expired"


# # ── Unauthenticated access ────────────────────────────────────────────────────


# def test_unauthenticated_view_students(client):
#     response = client.get("/student/view_students")
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED


# def test_unauthenticated_add_student(client):
#     response = client.post(
#         "/admin/add_students",
#         json={
#             "name": "Asha",
#             "std": "10",
#             "roll": "1",
#             "marks": [80, 90],
#         },
#     )
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED


# def test_unauthenticated_delete_student(client):
#     response = client.delete(
#         "/admin/delete_students", params={"std": "10", "roll": "1"}
#     )
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED


# def test_unauthenticated_search(client):
#     response = client.get("/student/search_by_name", params={"name": "Asha"})
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED


# # ── RBAC: viewer allowed ──────────────────────────────────────────────────────


# def test_viewer_can_view_students(client):
#     token = get_token(client, role="viewer", username="viewer2")
#     response = client.get(
#         "/student/view_students", headers={"Authorization": f"Bearer {token}"}
#     )
#     assert response.status_code == status.HTTP_200_OK


# def test_viewer_can_search_by_name(client):
#     token = get_token(client, role="viewer", username="viewer3")
#     response = client.get(
#         "/student/search_by_name",
#         params={"name": "ghost"},
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert response.status_code in (status.HTTP_200_OK, status.HTTP_404_NOT_FOUND)


# def test_viewer_can_search_by_roll(client):
#     token = get_token(client, role="viewer", username="viewer4")
#     response = client.get(
#         "/student/search_by_roll",
#         params={"std": "10", "roll": "99"},
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert response.status_code in (status.HTTP_200_OK, status.HTTP_404_NOT_FOUND)


# def test_viewer_can_get_percentage(client):
#     token = get_token(client, role="viewer", username="viewer5")
#     response = client.get(
#         "/student/percent_student",
#         params={"std": "10", "roll": "99"},
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert response.status_code in (status.HTTP_200_OK, status.HTTP_404_NOT_FOUND)


# # ── RBAC: viewer blocked ──────────────────────────────────────────────────────


# def test_viewer_cannot_add_student(client):
#     token = get_token(client, role="viewer", username="viewer6")
#     response = client.post(
#         "/admin/add_students",
#         json={"name": "Asha", "std": "10", "roll": "1", "marks": [80]},
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert response.status_code == status.HTTP_403_FORBIDDEN
#     assert "Access denied" in response.json()["detail"]


# def test_viewer_cannot_delete_student(client):
#     token = get_token(client, role="viewer", username="viewer7")
#     response = client.delete(
#         "/admin/delete_students",
#         params={"std": "10", "roll": "1"},
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert response.status_code == status.HTTP_403_FORBIDDEN
#     assert "Access denied" in response.json()["detail"]


# # ── RBAC: admin allowed ───────────────────────────────────────────────────────


# def test_admin_can_view_students(client):
#     token = get_token(client, role="admin", username="admin2")
#     response = client.get(
#         "/student/view_students", headers={"Authorization": f"Bearer {token}"}
#     )
#     assert response.status_code == status.HTTP_200_OK


# def test_admin_can_add_student(client):
#     token = get_token(client, role="admin", username="admin3")
#     response = client.post(
#         "/admin/add_students",
#         json={"name": "Diya", "std": "10", "roll": "1", "marks": [80, 90, 70]},
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.json()["message"] == "Student added successfully"


# def test_admin_can_delete_student(client):
#     token = get_token(client, role="admin", username="admin4")
#     client.post(
#         "/admin/add_students",
#         json={"name": "Diya", "std": "10", "roll": "5", "marks": [80]},
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     response = client.delete(
#         "/admin/delete_students",
#         params={"std": "10", "roll": "5"},
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["message"] == "Student deleted"


# def test_admin_can_add_duplicate_gets_409(client):
#     token = get_token(client, role="admin", username="admin5")
#     client.post(
#         "/admin/add_students",
#         json={"name": "Diya", "std": "10", "roll": "9", "marks": [80]},
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     response = client.post(
#         "/admin/add_students",
#         json={"name": "Diya", "std": "10", "roll": "9", "marks": [80]},
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert response.status_code == status.HTTP_409_CONFLICT
