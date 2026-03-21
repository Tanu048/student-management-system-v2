from storage_handler.db_handler.db_handler import StudentDB
from models.student import Student

def test_add_success(mocker):
    mock_session = mocker.Mock()

    mocker.patch(
        "storage_handler.db_handler.db_handler.SessionLocal",
        return_value=mock_session
    )

    db = StudentDB()

    student = mocker.Mock()
    mocker.patch(
        "storage_handler.db_handler.db_handler.student_to_db",
        return_value=student
    )

    result = db.add(student)

    assert result is True
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


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
