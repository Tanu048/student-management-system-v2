from storage_handler.db_handler.db_handler import StudentDB
from models.student import Student


def test_db_add_success():
    db = StudentDB()
    student = Student("Ashi", "1", "1", [10, 10, 10, 10, 10])
    result = db.add(student)
    assert result is True


def test_db_add_duplicate():
    db = StudentDB()
    student = Student("Ashi", "1", "1", [10, 10, 10, 10, 10])
    db.add(student)
    duplicate = Student("Ashi", "1", "1", [10, 10, 10, 10, 10])
    result = db.add(duplicate)
    assert result is False


def test_db_get_all():
    db = StudentDB()
    student = Student("Ashi", "1", "2", [10, 10, 10, 10, 10])
    db.add(student)
    data = db.get_all()
    assert len(data) >= 1


def test_db_delete_success():
    db = StudentDB()
    student = Student("Ashi", "1", "3", [10, 10, 10, 10, 10])
    db.add(student)
    result = db.delete_db("1-3")
    assert result is True


def test_db_delete_not_found():
    db = StudentDB()
    result = db.delete_db("99-99")
    assert result is False
