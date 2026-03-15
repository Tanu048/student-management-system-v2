from fastapi import FastAPI, Query, HTTPException, status

from services.manager import StudentManager
from routers import auth, student, admin
from schemas.student import MessageResponse

app = FastAPI()
manager = StudentManager()

app.include_router(auth.router, prefix="/auth", tags=["auth"]) 
app.include_router(student.router, prefix="/stduent", tags=["student"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

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
