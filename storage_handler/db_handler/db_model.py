from sqlalchemy import Column, String, Integer, Float, DateTime, ARRAY
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class StudentDBModel(Base):
    __tablename__ = "student"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    std = Column(String, nullable=False)
    roll = Column(String, nullable=False)
    marks = Column(ARRAY(Integer), nullable=False)
    per = Column(Float)
    date_created = Column(DateTime, default=datetime.utcnow)

    