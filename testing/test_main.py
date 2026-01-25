import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.fixture
def client(mocker):
    mocker.patch("storage_handler.json_handler.StudentJson.get_data", return_value={})
    mocker.patch("storage_handler.json_handler.StudentJson.set_data", return_value=True)
    mocker.patch("student_logging.student_log.LogInfo.log_info")
    mocker.patch("student_logging.student_log.LogInfo.log_error")
    from main import app, manager

    manager.data = {}
    return TestClient(app)


valid_student = {
    "name": "ashi",
    "std": "1",
    "roll": "1",
    "marks": [15, 18, 16, 14, 20],
}


def test_add_student_success(client):
    response = client.post("/add_students", json=valid_student)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Student added successfully"}


def test_add_student_duplicate(client):
    client.post("/add_students", json=valid_student)
    response = client.post("/add_students", json=valid_student)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Student already exists"


def test_view_students_empty(client):
    response = client.get("/view_students")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {}


def test_view_students_populated(client):
    client.post("/add_students", json=valid_student)
    response = client.get("/view_students")
    assert response.status_code == status.HTTP_200_OK
    assert "1-1" in response.json()


def test_search_by_roll_found(client):
    client.post("/add_students", json=valid_student)
    response = client.get("/students/search/by_roll",params={"std": "1", "roll": "1"},)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "ashi"


def test_search_by_roll_not_found(client):
    response = client.get("/students/search/by_roll",params={"std": "9", "roll": "9"},)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_search_by_name_found(client):
    client.post("/add_students", json=valid_student)
    response = client.get("/students/search/by_name",params={"name": "ashi"},)
    assert response.status_code == status.HTTP_200_OK
    assert "1-1" in response.json()


def test_search_by_name_not_found(client):
    response = client.get("/students/search/by_name",params={"name": "ghost"},)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_percentage_found(client):
    client.post("/add_students", json=valid_student)
    response = client.get("/percent_student",params={"std": "1", "roll": "1"},)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == 16.6


def test_percentage_not_found(client):
    response = client.get("/percent_student",params={"std": "1", "roll": "99"},)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_student_success(client):
    client.post("/add_students", json=valid_student)
    response = client.delete("/delete_students",params={"std": "1", "roll": "1"},)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Student deleted"}


def test_delete_student_not_found(client):
    response = client.delete("/delete_students",params={"std": "1", "roll": "99"},)
    assert response.status_code == status.HTTP_404_NOT_FOUND
