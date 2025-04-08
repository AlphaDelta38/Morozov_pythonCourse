from dotenv import load_dotenv
import logging
import os


load_dotenv()


#// API constants (from env) //#
API_URL = os.getenv("API_URL")

#// PATHS constants //#
SAVE_FOLDER = "saves"

#// Data / time constants //#
TIME_FORMAT = "%H:%M:%S"
DOB_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
REGISTER_DATE_FORMAT = "%m-%d-%YT%H:%M:%S"

#// logger constants //#
LOG_LEVEL = logging.INFO
LOG_FILE_NAME = "file.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"