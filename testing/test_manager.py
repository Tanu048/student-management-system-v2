import pytest
from services.manager import StudentManager


@pytest.fixture(autouse=True)
def mock_logging(mocker):
    mocker.patch("student_logging.student_log.LogInfo.log_info")
    mocker.patch("student_logging.student_log.LogInfo.log_error")


@pytest.fixture(autouse=True)
def empty_manager(mocker):
    mock_db_class = mocker.patch("services.manager.StudentDB")
    mock_db = mock_db_class.return_value

    fake_db = {}

    def get_all():
        return list(fake_db.values())

    def add(student):
        key = f"{student._std}-{student._roll}"
        db_obj = type("DBStudent", (), {})()
        db_obj.id = key
        db_obj.name = student._name
        db_obj.std = student._std
        db_obj.roll = student._roll
        db_obj.marks = student._marks
        db_obj.per = student.percentage
        fake_db[key] = db_obj
        return True

    def delete_db(student_id):
        if student_id in fake_db:
            del fake_db[student_id]
            return True
        return False

    mock_db.get_all.side_effect = get_all
    mock_db.add.side_effect = add
    mock_db.delete_db.side_effect = delete_db

    return StudentManager()


def test_add_student_success(empty_manager):
    result = empty_manager.add_student(
        name="Diya",
        std="10",
        roll="1",
        marks=[80, 90, 70],
    )
    assert result is True
    assert "10-1" in empty_manager.data


def test_add_student_duplicate(empty_manager):
    empty_manager.add_student("Diya", "10", "1", [80])
    result = empty_manager.add_student("Diya", "10", "1", [90])
    assert result is False


def test_view_list_empty(empty_manager):
    assert empty_manager.view_list() == {}


def test_view_list_populated(empty_manager):
    empty_manager.add_student("Diya", "10", "1", [80])
    students = empty_manager.view_list()
    assert len(students) == 1


def test_search_by_roll_found(empty_manager):
    empty_manager.add_student("Diya", "10", "1", [80])
    student = empty_manager.search_by_roll("10", "1")
    assert student["name"] == "Diya"


def test_search_by_roll_not_found(empty_manager):
    assert empty_manager.search_by_roll("10", "99") is None


def test_search_by_name_single(empty_manager):
    empty_manager.add_student("Diya sharma", "10", "1", [80])
    result = empty_manager.search_by_name("Diya sharma")
    assert len(result) >= 1


def test_search_by_name_multiple(empty_manager):
    empty_manager.add_student("Diya sharma", "10", "1", [80])
    empty_manager.add_student("Diya sharma", "11", "1", [80])
    result = empty_manager.search_by_name("Diya")
    assert len(result) == 2
    assert "10-1" in result
    assert "11-1" in result


def test_search_by_name_not_found(empty_manager):
    assert empty_manager.search_by_name("ghost") == {}


def test_delete_student_success(empty_manager):
    empty_manager.add_student("Diya", "10", "1", [80])
    assert empty_manager.delete_student("10", "1") is True


def test_delete_student_missing(empty_manager):
    assert empty_manager.delete_student("10", "99") is False


def test_per_calc_success(empty_manager):
    empty_manager.add_student("Diya", "10", "1", [80, 90])
    percent = empty_manager.per_calc("10", "1")
    assert percent == 85.0


def test_per_calc_no_student(empty_manager):
    assert empty_manager.per_calc("10", "99") is None


def test_per_calc_empty_marks(empty_manager):
    empty_manager.add_student("Diya", "10", "1", [])
    assert empty_manager.per_calc("10", "1") is None
