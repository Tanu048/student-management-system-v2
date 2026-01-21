#  file made to retrive and save data to the json file

from pathlib import Path
import json

from student_logging.student_log import LogInfo

class StudentJson:
    # added path to the root directory in resolve method so that the code works from any destination and the adress is not just relative
    _data_file = Path((Path(__file__).resolve().parent.parent)) / "data" / "students.json"

    def get_data() -> dict:
        """
        Fetches the current student dataset from the JSON file.
        Returns:
            dict: A dictionary containing student records. Returns empty dict if file is missing/corrupt.
        """
        try:
            with open(StudentJson._data_file) as f:
                data = json.load(f)
        except json.JSONDecodeError:
            LogInfo.log_error("File not accessible")
            return {}
        except FileNotFoundError:
            LogInfo.log_error("File doesn't exist")
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
            StudentJson._data_file.parent.mkdir(
                parents=True, exist_ok=True )  # here the parent of the json file checks for the existance of directory and parent of directory as arguments are used and won't throw error even if file exists already
        
            temp_file = StudentJson._data_file.with_suffix(".tmp")
            with open(temp_file, "w") as f:
                json.dump(data, f, indent=4)
            temp_file.replace(StudentJson._data_file)
            return True    
        except TypeError as e:
            LogInfo.log_error(f"Type error in JSON serialization: {e}\n")
            return False
        except (ValueError, OSError) as e:
            LogInfo.log_error(f"Cannot write to file: {e}\n")
            return False