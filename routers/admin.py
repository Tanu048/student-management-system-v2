from fastapi import APIRouter, HTTPException, status, Depends

from schemas.student import ValidateStudent, MessageResponse
from services.manager import StudentManager
from storage_handler.db_handler.db_model import AdminDBModel
from routers.auth import require_role

router = APIRouter()

manager = StudentManager()

@router.post("/add_students", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def add_student(
    student: ValidateStudent,
    current_user: AdminDBModel = Depends(require_role("admin")),
):
    """
    Add a new student record.
    Requires role: **admin**
    """
    key = f"{student.std}-{student.roll}"
    if key in manager.data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student already exists",
        )
    manager.add_student(
        name=student.name,
        std=student.std,
        roll=student.roll,
        marks=student.marks,
    )
    return {"message": "Student added successfully"}
 
 
@router.delete("/delete_students", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def delete_student(
    std: str,
    roll: str,
    current_user: AdminDBModel = Depends(require_role("admin")),
):
    """
    Delete a student by standard and roll number.
    Requires role: **admin**
    """
    deleted = manager.delete_student(std, roll)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return {"message": "Student deleted"}