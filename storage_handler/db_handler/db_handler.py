from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from storage_handler.db_handler.db_model import StudentDBModel, Base
from storage_handler.db_handler.db_mapper import student_to_db


class StudentDB:
    engine = create_engine("postgresql://postgres:postgresdatabase2026@localhost:5432/student_management_database")

    def __init__(self):
        sessionLocal = sessionmaker(bind=StudentDB.engine)
        self.session=sessionLocal()

    def add(self, student) -> bool:
        try:
            db_student = student_to_db(student)
            self.session.add(db_student)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def get_all(self) -> list[StudentDBModel]:
        return self.session.query(StudentDBModel).all()

    def make_relation():
        Base.metadata.create_all(StudentDB.engine)
