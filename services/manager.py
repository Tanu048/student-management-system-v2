#  to perform the functions user wants

# topper in each class
# arrange student by name in the dict

from models.student import Student
from storing.json_handler import get_data, set_data


def add_student(name: str, standard: str, roll_no: str, marks: int) -> bool:
    new = Student(name, standard, roll_no, marks)
    new_dict = new.to_dict()
    data = get_data()  # -------> returns a dict
    key = f"{standard}-{roll_no}"
    if key in data:
        return False
    data[key] = new_dict
    set_data(data)
    return True


def view_list():
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
    return [student for student in data.values() if student["name"] == name] or False


def delete_student(std: str, roll: str) -> bool:
    data = get_data()
    print(data)
    if f"{std}-{roll}" in data:
        del data[f"{std}-{roll}"]
        print(data)
        set_data(data)
        return True
    else:
        return False


def per_marks(std: str, roll: str) -> int:
    data = get_data()
    key = f"{std}-{roll}"
    if not key in data:
        return False
    if key in data:
        res=0
        for i in data[key]["marks"]:
            res += i
        return (res / 5)
