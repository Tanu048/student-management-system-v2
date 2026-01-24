import pytest
from validators import check_inputs, check_choice

@pytest.fixture(autouse=True)
def mock_logging(mocker):
    mocker.patch("student_logging.student_log.LogInfo.log_info")
    mocker.patch("student_logging.student_log.LogInfo.log_error")

def test_check_inputs_valid():
    assert check_inputs(
        name="riya",
        std="10",
        roll="1",
        marks=[80, 90],
    ) is True


def test_check_inputs_empty_name():
    assert check_inputs(name="") is False


def test_check_inputs_empty_std():
    assert check_inputs(std="") is False


def test_check_inputs_empty_roll():
    assert check_inputs(roll="") is False


def test_check_inputs_marks_empty():
    assert check_inputs(marks=[]) is False


def test_check_inputs_marks_out_of_range():
    assert check_inputs(marks=[120]) is False


def test_check_inputs_marks_non_int():
    assert check_inputs(marks=[80, "90"]) is False


def test_check_choice_valid():
    for choice in ["1", "2", "3", "4", "5", "6", "a", "b"]:
        assert check_choice(choice) is True


def test_check_choice_invalid():
    assert check_choice("x") is False
