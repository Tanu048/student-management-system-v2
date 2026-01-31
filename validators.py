from student_logging.student_log import LogInfo

empty_error = "Empty value entered."
type_error = "Value error"


def check_inputs(
    name: str | None = None,
    std: str | None = None,
    roll: str | None = None,
    marks: list[int] | None = None,
) -> bool:
    """
    Validate student input data.
    Performs comprehensive validation on student fields.
    Logs errors to application logger.
    Prints user-friendly error messages to console.
    Args:
        name: Student name (optional). Must be non-empty string.
        std: Class/standard (optional). Must be non-empty string.
        roll: Roll number (optional). Must be non-empty string.
        marks: List of marks (optional). Must be:
               - Non-empty list
               - All integers
               - Each mark between 0-100
    """
    checker = True
    if name is not None:
        if not str(name).strip():
            checker = False
            LogInfo.log_error(empty_error)
            print("Error: Name cannot be empty")
        if type(name) is not str:
            LogInfo.log_error(type_error)
            print("Error: Name is supposed to be a string")
            checker = False
    if std is not None:
        if not str(std).strip():
            checker = False
            LogInfo.log_error(empty_error)
            print("Error: Standard cannot be empty")
        if type(std) is not str:
            LogInfo.log_error(type_error)
            print("Error:  is supposed to be a string")
            checker = False
    if roll is not None:
        if not str(roll).strip():
            checker = False
            LogInfo.log_error(empty_error)
            print("Error: Roll number cannot be empty")
        if type(roll) is not str:
            LogInfo.log_error(type_error)
            print("Error: Roll Number is supposed to be a string")
            checker = False
    if marks is not None:
        if not isinstance(marks, list):
            LogInfo.log_error(type_error)
            print("Error: Marks must be a list")
            checker = False
        elif len(marks) == 0:
            LogInfo.log_error(empty_error)
            print("Error: Marks cannot be empty")
            checker = False
        elif not all(isinstance(m, int) and 0 <= m <= 100 for m in marks):
            LogInfo.log_error("Marks value exceeded")
            print("Error: All marks must be integers between 0-100")
            checker = False

    return checker


def check_choice(choice: str) -> bool:
    """
     Validate menu choice from user input.    
    Checks if user's menu selection is valid.    
    Args:
        choice: User's menu input (1-6 for number options, a-b for letter options)    
    Returns:
        bool: True if valid choice, False otherwise    
    Valid Choices:
        - "1": Add Student
        - "2": View All Students
        - "3": Search Student
        - "4": Delete Student
        - "5": Calculate Percentage
        - "6": Exit
        - "a": Search by roll number
        - "b": Search by name
    """
    if choice in ["1", "2", "3", "4", "5", "6", "a", "b"]:
        return True
    else:
        print("Please choose from the above given options!!!")
        LogInfo.log_error(type_error)
        return False
