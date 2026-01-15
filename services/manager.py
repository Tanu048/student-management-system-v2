#  to perform the functions user wants

from models.student import Student
from storage_handler.json_handler import get_data, set_data


class StudentManager:

    def __init__(self):
        self.data = self._load_initial_data()

    def _load_initial_data(self):
        """Internal helper to fetch data from JSON"""
        data = get_data()
        return data

    def add_student(
        self, name: str, standard: str, roll_no: str, marks: list[int]
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
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        if not standard or not standard.strip():
            raise ValueError("Standard cannot be empty")
        if not isinstance(marks, list) or not marks:
            raise ValueError("Marks must be a non-empty list")
        if not all(isinstance(m, int) and 0 <= m <= 100 for m in marks):
            raise ValueError("All marks must be integers between 0-100")

        key = f"{standard}-{roll_no}"
        if key in self.data:
            return False
        new = Student(name, standard, roll_no, marks)
        self.data[key] = new.to_dict()
        return set_data(self.data)

    def view_list(self) -> list[dict]:
        """Return all students excluding creation timestamps."""
        return [
            {k: v for k, v in student.items() if k != "date_created"}
            for student in self.data.values()
        ]

    def search_by_roll(self, std: str, roll_no: str) -> dict | None:
        """
        Searches for a specific student by their unique class-roll key.
        Returns:
            dict: Student data if found, None otherwise.
        """
        key = f"{std}-{roll_no}"

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
            set_data(self.data)
            return True
        else:
            return False

   
    def per_marks(self, std: str, roll: str) -> float | None:
        """Calculate and store average percentage for a student."""
        key = f"{std}-{roll}"
        student = self.data.get(key)
        if not student:
            return None
        marks = student.get("marks", [])
        if not marks:
            return None
        percentage = sum(marks) / len(marks)
        student["percentage"] = round(percentage, 2)
        set_data(self.data)
        return student["percentage"]
