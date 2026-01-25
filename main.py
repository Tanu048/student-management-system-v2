from fastapi import FastAPI, Query, HTTPException, status
from pydantic import BaseModel, Field, conint
from typing import List

from models.student import Student
from services.manager import StudentManager

app = FastAPI()
manager = StudentManager()


class ValidateStudent(BaseModel):
    name: str = Field(..., min_length=1)
    std: str = Field(..., min_length=1)
    roll: str = Field(..., min_length=1)
    marks: List[conint(ge=0, le=100)] = Field(
        min_length=1, max_length=5
    )  # best done via annotation


class MessageResponse(BaseModel):
    message: str


@app.post("/add_students", response_model=MessageResponse)
def add_student(student: ValidateStudent):
    key = f"{student.std}-{student.roll}"
    if key in manager.data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Student already exists"
        )
    manager.add_student(
        name=student.name,
        std=student.std,
        roll=student.roll,
        marks=student.marks,
    )
    return {"message": "Student added successfully"}


@app.get("/view_students")
def get_student() -> dict[str, dict]:
    return manager.view_list()


@app.get("/students/search/by_roll")
def get_student_by_roll(
    std: str = Query(..., min_size=1), roll: str = Query(..., min_size=1)
) -> dict:
    student = manager.search_by_roll(std, roll)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="student not found"
        )
    else:
        return student


@app.get("/students/search/by_name")
def get_student_by_name(name: str = Query(..., min_size=1)) -> dict:
    student = manager.search_by_name(name)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student {name} does not exist",
        )
    else:
        return student


@app.get("/percent_student")
def get_percentage(
    std: str = Query(..., min_size=1),
    roll: str = Query(..., min_size=1),
) -> float:
    percent = manager.per_calc(std, roll)
    if percent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )
    return percent


@app.delete("/delete_students", response_model=MessageResponse)
def delete_student(
    std: str = Query(..., min_size=1), roll: str = Query(..., min_size=1)
):
    deleted = manager.delete_student(std, roll)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )
    return {"message": "Student deleted"}
