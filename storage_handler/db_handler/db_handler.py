import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from storage_handler.db_handler.db_model import StudentDBModel, Base
from storage_handler.db_handler.db_mapper import student_to_db

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgresdatabase2026@localhost:5432/student_management_database"
)

class StudentDB:
    engine = create_engine(DATABASE_URL)
    
    def __init__(self):
        """Initialize a new database session.
        Creates a new session for database operations."""
        Base.metadata.create_all(StudentDB.engine)
        sessionLocal = sessionmaker(bind=StudentDB.engine)
        self.session = sessionLocal()

    def add(self, student) -> bool:
        try:
            db_student = student_to_db(student)
            self.session.add(db_student)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def delete_db(self, key: str) -> bool:
        try:
            student = self.session.get(StudentDBModel, key)
            if student:
                self.session.delete(student)
                self.session.commit()
                return True
            else:
                return False
        except IntegrityError:
            self.session.rollback()
            return False

    def get_all(self) -> list[StudentDBModel]:
        return self.session.query(StudentDBModel).order_by(StudentDBModel.id).all()
