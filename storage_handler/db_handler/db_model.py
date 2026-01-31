from sqlalchemy import Column, String, Integer, Float, DateTime, ARRAY
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class StudentDBModel(Base):
    """
    SQLAlchemy ORM model for Student database table.
    Represents the 'student' table in PostgreSQL.
    Defines schema, constraints, and relationships.
    Attributes:
        id (str): Primary key, composite of standard-roll
        name (str): Student name, required
        std (str): Class/standard, required
        roll (str): Roll number, required
        marks (list[int]): PostgreSQL ARRAY of integers, required
        per (float): Average percentage (nullable)
        date_created (datetime): Auto-set timestamp
    Table: student
    """

    __tablename__ = "student"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    std = Column(String, nullable=False)
    roll = Column(String, nullable=False)
    marks = Column(ARRAY(Integer), nullable=False)
    per = Column(Float)
    date_created = Column(DateTime, default=datetime.utcnow)
