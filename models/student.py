# defines the structure of the student, includes values and the type handling

from datetime import datetime


class Student:

    def __init__(self, name: str, standard: str, roll_number: str, marks: list[int]):
        """
        Initializes a Student instance with a unique creation timestamp.
        """
        try:
            self.name = name
            self.standard = standard
            self.roll_number = roll_number
            self.marks = marks
            self.date_created = datetime.now().strftime("%d-%m-%y %H:%M:%S")
        except ValueError:
            print("Enter valid values!")

    def to_dict(self) -> dict:
        """Returns a dictionary with a fixed order of fields."""
        return {
            "name": self.name,
            "standard": self.standard,
            "roll_number": self.roll_number,
            "marks": self.marks,
            "date_created": self.date_created,
        }
