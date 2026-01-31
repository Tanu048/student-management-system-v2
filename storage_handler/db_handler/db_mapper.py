from models.student import Student
from storage_handler.db_handler.db_model import StudentDBModel

def student_to_db(student: Student) -> StudentDBModel:
    return StudentDBModel(
        id=f'{student._std}-{student._roll}',
        name=student._name,
        std=student._std,
        roll=student._roll,
        marks=student._marks,
        per=student.per,
    )

def db_to_student_dict(db: StudentDBModel) -> dict:
    return {
        "key": db.id, 
        "name": db.name,
        "standard": db.std,
        "roll_number": db.roll,
        "marks": db.marks,
        "percentage": db.per,
    }
