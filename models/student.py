# defines the structure of the student, includes values and the type handling

from datetime import datetime


class Student:

    def __init__(self, name: str, std: str, roll: str, marks: list[int]):
        """Initialize a Student instance with validation and timestamp."""

        self._name = name
        self._std = std
        self._roll = roll
        self._marks = marks
        self._date_created = datetime.now().strftime("%d-%m-%y %H:%M:%S")

    def to_dict(self) -> dict:
        """Returns a dictionary with a fixed order of fields."""
        return {
            "name": self._name,
            "standard": self._std,
            "roll_number": self._roll,
            "marks": self._marks,
            "percentage": self.percentage,
            "date_created": self._date_created,
        }

    @property
    def percentage(self):
        marks = self._marks
        if not marks:
            return None
        return (sum(marks) / (len(marks) * 100)) * 100
