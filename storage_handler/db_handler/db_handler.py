# adding database using sqlalchemy, postgres etc

from sqlalchemy import create_engine, Integer, String, Column, Float, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine('postgresql://postgres:postgresdatabase2026@localhost:5432/student_management_database', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Student(Base):
    __tablename__='student'
    student_id=Column(Integer, primary_key=True)
    student_name=Column(String)

Base.metadata.create_all(engine)

new_student=Student(student_id=8, student_name="bhumi")
session.add(new_student)

delete_student= session.query(Student).filter(Student.student_id>1).delete()
session.commit()

print([t.student_name for t in delete_student])