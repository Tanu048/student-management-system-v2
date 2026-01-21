from fastapi import FastAPI, Query, HTTPException, status
from pydantic import BaseModel, Field
from typing import List

from models.student import Student
from services.manager import StudentManager

app = FastAPI()
manager = StudentManager()


class ValidateStudent(BaseModel):
    name: str = Field(..., min_length=1)
    std: str = Field(..., min_length=1)
    roll: str = Field(..., min_length=1)
    marks: List[int] = Field(..., min_size=1)


class MessageResponse(BaseModel):
    message: str


@app.post("/add_students")
def add_student(student: ValidateStudent) -> MessageResponse:
    try:
        key = f"{student.std}-{student.roll}"

        if key in manager.data:
            raise HTTPException(status_code=409, detail="Student already exists")
        manager.add_student(
            name=student.name, std=student.std, roll=student.roll, marks=student.marks
        )
        return {"message": "Student added successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/view_students")
def get_student() -> List[dict]:
    return manager.view_list()


@app.get("/students/search/by_roll")
def get_student_by_roll(
    std: str = Query(..., min_length=1), roll: str = Query(..., min_length=1)
) -> dict:
    try:
        return manager.search_by_roll(std, roll)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/students/search/by_name")
def get_student_by_roll(name: str = Query(..., min_length=1)) -> List[dict]:
    try:
        return manager.search_by_name(name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/percent_student")
def get_percentage(
    std: str = Query(..., min_length=1), roll: str = Query(..., min_length=1)
) -> dict:
    try:
        return manager.per_calc(std, roll)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/delete_students")
def delete_student(
    std: str = Query(..., min_length=1), roll: str = Query(..., min_length=1)
) -> MessageResponse:
    try:
        manager.delete_student(std, roll)
        return {"messagne": "student deleted"}
    except:
        raise HTTPException(status_code=404, detail="student does not exists")
