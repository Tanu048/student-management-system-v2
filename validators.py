from student_logging.student_log import LogInfo

empty_error = "Empty value entered."
type_error = "Value error"


def check_inputs(
    name: str | None = None,
    std: str | None = None,
    roll: str | None = None,
    marks: list[int] | None = None,
) -> bool:
    
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
    if choice in ["1","2","3","4","5","6","a","b"]:
        return True
    else:
        print("Please choose from the above given options!!!")
        LogInfo.log_error(type_error)
        return False
