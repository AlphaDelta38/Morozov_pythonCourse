from constants import (LOG_FILE_NAME, LOG_FORMAT, LOG_LEVEL)
import logging


class Logger:
    _instance = None

    def __new__(cls, log_level = LOG_LEVEL, log_file_name = LOG_FILE_NAME, log_format = LOG_FORMAT):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.__instance_logger = cls.__setup_logger__(log_level, log_file_name, log_format)
        return cls._instance.__instance_logger

    @staticmethod
    def __setup_logger__(log_level, log_file_name, log_format):
        file_handler = logging.FileHandler(log_file_name)
        file_handler.setFormatter(logging.Formatter(log_format))

        file_logger = logging.getLogger("file_logger")
        file_logger.setLevel(log_level)
        file_logger.addHandler(file_handler)

        return file_logger
