from models.student import Student
from storage_handler.db_handler.db_model import StudentDBModel

def student_to_db(student: Student) -> StudentDBModel:
    """
    Convert Student domain model to database model.    
    Maps Student object to StudentDBModel for database persistence.
    Handles ID generation from standard-roll combination.    
    Args:
        student: Student domain model instance    
    Returns:
        StudentDBModel: Database model ready for persistence    
    Example:
        db_student = student_to_db(student)
        session.add(db_student)
    """
    return StudentDBModel(
        id=f'{student._std}-{student._roll}',
        name=student._name,
        std=student._std,
        roll=student._roll,
        marks=student._marks,
        per=student.percentage,
    )

def db_to_student_dict(db: StudentDBModel) -> dict:
    """
    Convert database model to dictionary representation.    
    Transforms StudentDBModel to plain dict for API responses.
    Excludes internal database fields.    
    Args:
        db: StudentDBModel instance from database    
    Returns:
        dict: Student data in API-friendly format with keys:
              - key: Composite ID (std-roll)
              - name: Student name
              - standard: Class/grade
              - roll_number: Roll number
              - marks: List of marks
              - percentage: Average percentage    
    Example:
        student_dict = db_to_student_dict(db_student)
    """
    return {
        "key": db.id, 
        "name": db.name,
        "standard": db.std,
        "roll_number": db.roll,
        "marks": db.marks,
        "percentage": db.per,
    }
