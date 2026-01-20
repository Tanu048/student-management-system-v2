#  to perform the functions user wants

from models.student import Student
from storage_handler.json_handler import StudentJson
from student_logging.student_log import LogInfo


class StudentManager:

    def __init__(self):
        self.data = self._load_initial_data()

    def _load_initial_data(self):
        """Internal helper to fetch data from JSON"""
        data = StudentJson.get_data()
        return data

    def add_student(
        self, name: str, std: str, roll: str, marks: list[int]
    ) -> bool:
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
        key = f"{std}-{roll}"
        if key in self.data:
            return False
        new = Student(name, std, roll, marks)
        self.data[key] = new.to_dict()
        return StudentJson.set_data(self.data)

    def view_list(self) -> list[dict]:
        """Return all students excluding creation timestamps."""
        return [
            {k: v for k, v in student.items() if k != "date_created"}
            for student in self.data.values()
        ]

    def search_by_roll(self, std: str, roll: str) -> dict | None:
        """
        Searches for a specific student by their unique class-roll key.
        Returns:
            dict: Student data if found, None otherwise.
        """
        key = f"{std}-{roll}"

        # Use .get() - it returns None automatically if the key doesn't exist
        return self.data.get(key)

    def search_by_name(self, name: str) -> list:
        """Returns list of matching students (empty if none found)."""
        return [
            {k: v for k, v in student.items() if k != "date_created"}
            for student in self.data.values()
            if name in student["name"]
        ]

    def delete_student(self, std: str, roll: str) -> bool:
        if f"{std}-{roll}" in self.data:
            del self.data[f"{std}-{roll}"]
            StudentJson.set_data(self.data)
            return True
        else:
            return False

   
    def per_calc(self, std: str, roll: str) -> float | None:
        """Calculate and store average percentage for a student."""
        key = f"{std}-{roll}"
        student = self.data.get(key)
        if not student:
            return None
        percent = student["percentage"]
        if not percent:
            return None
        LogInfo.log_info("percentage accessed")
        StudentJson.set_data(self.data)
        return percent