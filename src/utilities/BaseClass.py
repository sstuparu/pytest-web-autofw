import inspect
import logging
import pytest
import os

UTILITIES_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
ROOT_DIRECTORY = os.path.abspath(os.path.join(UTILITIES_DIRECTORY, "../../"))
REPORTS_DIRECTORY = os.path.join(ROOT_DIRECTORY, "reports")
LOGGER_FORMATTER = "%(asctime)s: %(levelname)s: %(name)s: %(message)s"

@pytest.mark.usefixtures("setup")
class BaseClass:
    @staticmethod
    def get_logger():
        logger_name = inspect.stack()[1][3]
        logger = logging.getLogger(name=logger_name)

        file_handler = logging.FileHandler(os.path.join(REPORTS_DIRECTORY, "logfile.log"))  # filehandler object
        formatter = logging.Formatter(LOGGER_FORMATTER)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        logger.setLevel(logging.DEBUG)
        return logger


