# defines the structure of the student, includes values and the type handling

from datetime import datetime

class Student:

    def __init__(self, name: str, standard: str, roll_number: str, marks:list[int]):
        try:
            self.name = name
            self.standard = standard
            self.roll_number = roll_number
            self.marks = marks
            self.date_created = datetime.now().strftime("%d-%m-%y %H:%M:%S")
        except ValueError:
            print("Enter valid values!")
    
    def to_dict(self):
        return self.__dict__    # python objects are already stored as dictionaries 
