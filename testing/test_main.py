import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# def add_student():
#     response = client.get("/add_students?name=ashi&std=1&roll=1&marks=[15,18,16,14,20]")
#     assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_view_student():
    response = client.get("/view_students")
    assert response.status_code == status.HTTP_200_OK

def test_serch_by_roll():
    response = client.get("/students/search/by_roll?std=1&roll=5")
    assert response.status_code == status.HTTP_200_OK

def test_serch_by_name():
    response = client.get("/students/search/by_name?name=ashi")
    assert response.status_code == status.HTTP_200_OK
