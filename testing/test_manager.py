import pytest
from services.manager import StudentManager


@pytest.fixture
def empty_manager(monkeypatch):
    monkeypatch.setattr(
        "storage_handler.json_handler.StudentJson.get_data",
        lambda: {}
    )
    monkeypatch.setattr(
        "storage_handler.json_handler.StudentJson.set_data",
        lambda data: True
    )
    return StudentManager()


def test_add_student_success(empty_manager):
    result = empty_manager.add_student(
        name="tanu",
        standard="10",
        roll_no="1",
        marks=[80, 90, 70],
    )
    assert result is True
    assert "10-1" in empty_manager.data


def test_add_student_duplicate(empty_manager):
    empty_manager.add_student("tanu", "10", "1", [80])
    result = empty_manager.add_student("tanu", "10", "1", [90])
    assert result is False


def test_view_list_empty(empty_manager):
    assert empty_manager.view_list() == []


def test_view_list_populated(empty_manager):
    empty_manager.add_student("tanu", "10", "1", [80])
    students = empty_manager.view_list()
    assert len(students) == 1
    assert "date_created" not in students[0]


def test_search_by_roll_found(empty_manager):
    empty_manager.add_student("tanu", "10", "1", [80])
    student = empty_manager.search_by_roll("10", "1")
    assert student["name"] == "tanu"


def test_search_by_roll_not_found(empty_manager):
    assert empty_manager.search_by_roll("10", "99") is None


def test_search_by_name_found(empty_manager):
    empty_manager.add_student("tanu sharma", "10", "1", [80])
    result = empty_manager.search_by_name("tanu")
    assert len(result) == 1


def test_search_by_name_not_found(empty_manager):
    assert empty_manager.search_by_name("ghost") == []


def test_delete_student_success(empty_manager):
    empty_manager.add_student("tanu", "10", "1", [80])
    assert empty_manager.delete_student("10", "1") is True


def test_delete_student_missing(empty_manager):
    assert empty_manager.delete_student("10", "99") is False


def test_per_marks_success(empty_manager):
    empty_manager.add_student("tanu", "10", "1", [80, 90])
    percent = empty_manager.per_marks("10", "1")
    assert percent == 85.0


def test_per_marks_no_student(empty_manager):
    assert empty_manager.per_marks("10", "99") is None


def test_per_marks_empty_marks(empty_manager):
    empty_manager.add_student("tanu", "10", "1", [])
    assert empty_manager.per_marks("10", "1") is None
