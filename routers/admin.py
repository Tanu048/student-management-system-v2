from fastapi import APIRouter, HTTPException, status

from schemas.student import ValidateStudent, MessageResponse
from services.manager import StudentManager

router = APIRouter()

manager = StudentManager()

@router.post("/add_students", response_model=MessageResponse)
def add_student(student: ValidateStudent):
    try:
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
    except Exception as e:
         raise HTTPException(status_code=401, detail=print(e))

