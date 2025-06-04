import logging


BASE_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"


def get_logger(log_level=logging.INFO, log_file_name="file.log", log_format=BASE_FORMAT):
    file_logger = logging.getLogger("file_logger")
    file_logger.setLevel(log_level)

    if not file_logger.handlers:
        file_handler = logging.FileHandler(log_file_name)
        file_handler.setFormatter(logging.Formatter(log_format))
        file_logger.addHandler(file_handler)

    return file_logger
