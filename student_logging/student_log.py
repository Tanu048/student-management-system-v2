import logging

class LogInfo:

    logger = logging.getLogger("Administrator")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(name)s : %(levelname)s : %(message)s : %(asctime)s")

    file_handler = logging.FileHandler("student_logging/students.log")
    file_handler.setFormatter(formatter)

    
    logger.addHandler(file_handler)

    def log_error(message:str):
        return LogInfo.logger.error(message)

    def log_info(message:str):
        return LogInfo.logger.info(message)
    
    def log_warning(message:str):
        return LogInfo.logger.warning(message)