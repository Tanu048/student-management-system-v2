# defines the structure of the student, includes values and the type handling

from datetime import datetime


class Student:

    def __init__(self, name: str, standard: str, roll_number: str, marks: list[int]):
        """Initialize a Student instance with validation and timestamp."""
        if not name or not isinstance(name, str):
            raise ValueError("Name must be non-empty string")
        
        self._name = name
        self._standard = standard
        self._roll_number = roll_number
        self._marks = marks
        self._date_created = datetime.now().strftime("%d-%m-%y %H:%M:%S")
        

    def to_dict(self) -> dict:
        """Returns a dictionary with a fixed order of fields."""
        return {
            "name": self._name,
            "standard": self._standard,
            "roll_number": self._roll_number,
            "marks": self._marks,
            "date_created": self._date_created,
        }
