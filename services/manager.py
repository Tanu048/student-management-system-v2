#  to perform the functions user wants

# topper in each class
# arrange student by name in the dict

from models.student import Student
from storage_handler.json_handler import get_data, set_data


def add_student(name: str, standard: str, roll_no: str, marks: int) -> bool:
    """
    Add a new student to the system.

    Args:
        name: Student's full name
        standard: Class/grade level
        roll_no: Unique roll number
        marks: List of subject marks

    Returns:
        bool: True if student added successfully, False if duplicate exists

    Raises:
        ValueError: If marks are invalid
    """
    if not name or not name.strip():
        raise ValueError("Name cannot be empty")
    if not standard or not standard.strip():
        raise ValueError("Standard cannot be empty")
    if not isinstance(marks, list) or not marks:
        raise ValueError("Marks must be a non-empty list")
    if not all(isinstance(m, int) and 0 <= m <= 100 for m in marks):
        raise ValueError("All marks must be integers between 0-100")

    new = Student(name, standard, roll_no, marks)
    new_dict = new.to_dict()
    data = get_data()  # -------> returns a dict
    key = f"{standard}-{roll_no}"
    if key in data:
        return False
    data[key] = new_dict
    set_data(data)
    return True


def view_list() -> dict:
    data = get_data()
    return [
        {k: v for k, v in info.items() if k != "date_created"} for info in data.values()
    ]


def search_by_roll(std: str, roll_no: str) -> bool | dict:
    data = get_data()
    if f"{std}-{roll_no}" in data:
        return data[f"{std}-{roll_no}"]
    else:
        return False


def search_by_name(name: str) -> bool | dict:
    data = get_data()
    return [{k: v for k, v in student.items() if k != "date_created"} for student in data.values() if student["name"] == name] or False


def delete_student(std: str, roll: str) -> bool:
    data = get_data()
    if f"{std}-{roll}" in data:
        del data[f"{std}-{roll}"]
        set_data(data)
        return True
    else:
        return False


def per_marks(std: str, roll: str) -> bool | float:
    """Calculate average percentage across subjects."""
    data = get_data()
    key = f"{std}-{roll}"
    if key not in data:
        return False
    if key in data:
        marks = data[key]["marks"]
        return (sum(marks) / len(marks)) if marks else 0

