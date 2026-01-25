import pytest
import json
from storage_handler.json_handler import StudentJson

data_dict= {
    "1-1": {
        "name": "ashi",
        "standard": "1",
        "roll_number": "1",
        "marks": [
            15,
            18,
            16,
            14,
            20
        ],
        "date_created": "15-01-26 23:02:57",
        "percentage": 16.6
    }
}

@pytest.fixture(autouse=True)
def empty_josn(mocker):
    mocker.patch("storage_handler.json_handler.StudentJson._data_file", return_value={})

@pytest.fixture(autouse=True)
def mock_logging(mocker):
    mocker.patch("student_logging.student_log.LogInfo.log_info")
    mocker.patch("student_logging.student_log.LogInfo.log_error")

def test_json_get_pass():
    response=StudentJson.get_data()
    assert response == {}
    assert not FileNotFoundError in response
    assert not json.JSONDecodeError in response

def test_json_get_data(mocker):
    mocker.patch("builtins.open",mocker.mock_open(read_data='{}'))
    mocker.patch("json.load", return_value=data_dict)
    response = StudentJson.get_data()
    assert response == data_dict
    
def test_json_get_file_not_found_error(mocker):
    mocker.patch("builtins.open",side_effect=FileNotFoundError)
    log_mock = mocker.patch("student_logging.student_log.LogInfo.log_error")
    response=StudentJson.get_data()
    assert response =={}
    log_mock.assert_called_once_with("File doesn't exist")

def test_json_get_json_decoder_error(mocker):
    mocker.patch("builtins.open",mocker.mock_open(read_data="invalid json"))
    mocker.patch("json.load",side_effect=json.JSONDecodeError("err", "doc", 0))
    log_mock = mocker.patch("student_logging.student_log.LogInfo.log_error")
    response=StudentJson.get_data()
    assert response =={}
    log_mock.assert_called_once_with("File not accessible")

def test_json_set_pass():
    response= StudentJson.set_data(data_dict)
    assert response is True

def test_json_set_type_error(mocker):
    mocker.patch("builtins.open", side_effect=TypeError)
    response=StudentJson.set_data(data_dict)
    assert response is False

def test_json_set_value_os_error(mocker):
    mocker.patch("builtins.open", side_effect=(ValueError,OSError))
    response=StudentJson.set_data(data_dict)
    assert response is False
