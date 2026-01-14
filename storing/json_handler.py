#  file made to retrive and save data to the json file

# leave the corrupted lines and print the warning
# do not add the duplicated values to the file
# file gets updated and the updated time stamp changes while the student created remains the same

from pathlib import Path

import json

parent_dir = (
    Path(__file__).resolve().parent.parent
)  # added path to the root directory in resolve method so that the code works from any destination and the adress is not just relative
data_file = Path(parent_dir) / "data" / "students.json"


def get_data() -> dict:
    """
    Returns student data as dict.
    Returns empty dict if file does not exist or is corrupted.
    """
    if not data_file.exists():
        return {}

    try:
        with open(data_file) as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("File not accessible or doesn't access")
        return {}
    except FileNotFoundError:
        print("File not accessible or doesn't access")
        return {}

    return data


def set_data(data: dict) -> bool:
    """
    Writes student data to JSON file.
    :rtype: bool
    """
    try:
        data_file.parent.mkdir(
            parents=True, exist_ok=True
        )  # here the parent of the json file checks for the existance of directory and parent of directory as arguments are used and won't throw error even if file exists already
        temp_file = data_file.with_suffix(".tmp")
        with open(data_file, "w") as f:
            json.dump(data, f, indent=4)
        temp_file.replace(data_file)
        return True
    except (TypeError, ValueError, OSError):
        return False
