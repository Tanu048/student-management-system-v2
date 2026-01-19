from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from models.student import Student
from services.manager import StudentManager

app = FastAPI()
manager = StudentManager()


class ValidateStudent(BaseModel):
    name: str
    std: str
    roll: str
    marks: list[int]


class ValidatePer(BaseModel):
    std: str
    roll: str


@app.post("/add_students")
def add_student(student: ValidateStudent):
    try:
        manager.add_student(
            name=student.name, std=student.std, roll=student.roll, marks=student.marks
        )
        return {"message": "Student added successfully"}
    except ValueError as e:
        raise e(status_code=400, detail=str(e))


@app.get("/view_students")
def get_student():
    return manager.view_list()


@app.get("/students/search/by_roll")
def get_student_by_roll(std, roll):
    try:
        return manager.search_by_roll(std, roll)
    except ValueError as e:
        raise e(status_code=422, detail=str(e))


@app.get("/students/search/by_name")
def get_student_by_roll(name: str):
    try:
        return manager.search_by_name(name)
    except ValueError as e:
        raise e(status_code=422, detail=str(e))
