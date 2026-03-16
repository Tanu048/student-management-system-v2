from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from services.manager import StudentManager
from storage_handler.db_handler.db_model import AdminDBModel
from routers.auth import require_role

router = APIRouter()

manager = StudentManager()


@router.get("/view_students")
def get_students(
    current_user: AdminDBModel = Depends(require_role("admin", "viewer")),
) -> dict[str, dict]:
    """
    Return all student records.
    Requires role: **admin** or **viewer**
    """
    return manager.view_list()
 
 
@router.get("/search_by_roll")
def get_student_by_roll(
    std: str,
    roll: str,
    current_user: AdminDBModel = Depends(require_role("admin", "viewer")),
) -> dict:
    """
    Search for a student by standard and roll number.
    Requires role: **admin** or **viewer**
    """
    student = manager.search_by_roll(std, roll)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return student
 
 
@router.get("/search_by_name")
def get_student_by_name(
    name: str,
    current_user: AdminDBModel = Depends(require_role("admin", "viewer")),
) -> dict:
    """
    Search for students by name (partial match).
    Requires role: **admin** or **viewer**
    """
    students = manager.search_by_name(name)
    if not students:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No students found matching '{name}'",
        )
    return students
 
 
@router.get("/percent_student")
def get_percentage(
    std: str,
    roll: str,
    current_user: AdminDBModel = Depends(require_role("admin", "viewer")),
) -> float:
    """
    Get the average percentage for a student.
    Requires role: **admin** or **viewer**
    """
    percent = manager.per_calc(std, roll)
    if percent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return percent