from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session, Query 

from services.manager import StudentManager

router = APIRouter()

manager = StudentManager()

@router.get("/view_students")
def get_student() -> dict[str, dict]:
    return manager.view_list()

@router.get("/search_by_roll")
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