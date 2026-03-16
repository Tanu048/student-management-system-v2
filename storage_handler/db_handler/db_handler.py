import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

from storage_handler.db_handler.db_model import StudentDBModel, Base
from storage_handler.db_handler.db_mapper import student_to_db

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgresdatabase2026@localhost:5432/student_management_database",
)
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


class StudentDB:

    def __init__(self):
        """Initialize a new database session.
        Creates a new session for database operations."""
        self.session = SessionLocal()

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

    @staticmethod
    def get_db():
        """FastAPI dependency: yields a per-request DB session and closes it after."""
        db: Session = SessionLocal()
        try:
            yield db
        finally:
            db.close()
