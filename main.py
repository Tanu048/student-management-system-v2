from fastapi import FastAPI

from routers import auth, student, admin

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"]) 
app.include_router(student.router, prefix="/student", tags=["student"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])