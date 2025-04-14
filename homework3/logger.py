import logging

def get_logger(log_level=logging.INFO, log_file_name="file.log", log_format= "%(asctime)s - %(levelname)s - %(name)s - %(message)s"):
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setFormatter(logging.Formatter(log_format))

    file_logger = logging.getLogger("file_logger")
    file_logger.setLevel(log_level)
    file_logger.addHandler(file_handler)

    return file_logger