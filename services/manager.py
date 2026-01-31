#  to perform the functions user wants
from models.student import Student
from storage_handler.db_handler.db_handler import StudentDB
from storage_handler.db_handler.db_mapper import db_to_student_dict
from storage_handler.json_handler import StudentJson
from student_logging.student_log import LogInfo


class StudentManager:

    def __init__(self):
        self.db = StudentDB()
        self.data = self._load_initial_data()

    def _load_initial_data(self) -> dict:
        """
        Fetch all students from database and cache them.
        Loads complete dataset from PostgreSQL into memory.
        This cache is refreshed after mutations (add/delete).
        Returns:
        dict: Keyed by 'std-roll', values are student dictionaries
        """
        data = {s.id: db_to_student_dict(s) for s in self.db.get_all()}
        return data

    def add_student(self, name: str, std: str, roll: str, marks: list[int]) -> bool:
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
        student = Student(name, std, roll, marks)
        success = self.db.add(student)
        self.data = self._load_initial_data()
        return success

    def view_list(self) -> dict:
        """Return all students excluding creation timestamps."""
        LogInfo.log_info("List viewed")
        self.data = self._load_initial_data()
        return {keys: values for keys, values in self.data.items()}

    def search_by_roll(self, std: str, roll: str) -> dict | None:
        """
        Search for a specific student by class and roll number.
        Args:
           std: Class/standard (e.g., "10", "11")
           roll: Roll number (e.g., "1", "5")
        Returns:
           dict: Student data if found, None otherwise
        """
        self.data = self._load_initial_data()
        LogInfo.log_info("Stduent searched")
        key = f"{std}-{roll}"
        # Use .get() - it returns None automatically if the key doesn't exist
        return self.data.get(key)

    def search_by_name(self, name: str) -> dict:
        """Returns matching students keyed by std-roll."""
        LogInfo.log_info("Stduent searched")
        self.data = self._load_initial_data(self)
        result = {}
        for key, student in self.data.items():
            if name.lower() in student["name"].lower():
                result[key] = student
        return result

    def delete_student(self, std: str, roll: str) -> bool:
        key = f"{std}-{roll}"
        if key not in self.data:
            return False
        success = self.db.delete_db(key)
        self.data = self._load_initial_data(self)
        if success:
            del self.data[key]
            LogInfo.log_info("Student deleted")
        return success

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
        return percent
