#  file made to retrive and save data to the json file

from pathlib import Path

import json

parent_dir = (
    Path(__file__).resolve().parent.parent
)  # added path to the root directory in resolve method so that the code works from any destination and the adress is not just relative
data_file = Path(parent_dir) / "data" / "students.json"


def get_data() -> dict:
    """
    Fetches the current student dataset from the JSON file.

    Returns:
        dict: A dictionary containing student records. Returns empty dict if file is missing/corrupt.
    """
    if not data_file.exists():
        return {}

    try:
        with open(data_file) as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Error: File not accessible \n")
        return {}
    except FileNotFoundError:
        print("Error: File doesn't access\n")
        return {}

    return data


def set_data(data: dict) -> bool:
    """
    Persists the student dataset to a JSON file using an atomic-style write.

    Args:
        data (dict): The complete dataset to be saved.
    Returns:
        bool: True if save was successful, False otherwise.
    """
    try:
        data_file.parent.mkdir(
            parents=True, exist_ok=True
        )  # here the parent of the json file checks for the existance of directory and parent of directory as arguments are used and won't throw error even if file exists already
       
        with open(data_file, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except TypeError as e:
        print(f"Type error in JSON serialization: {e}\n")
        return False
    except (ValueError, OSError) as e:
        print(f"Cannot write to file: {e}\n")
        return False
