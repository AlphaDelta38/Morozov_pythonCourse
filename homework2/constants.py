import logging


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

#// CSV Keys Constants //#
LOCATION_TIMEZONE_OFFSET_KEY = "location.timezone.offset"
LOCATION_COUNTRY_KEY = "location.country"
REGISTER_DATE_KEY = "registered.date"
REGISTER_AGE_KEY = "registered.age"
CURRENT_TIME_KEY = "current_time"
NAME_TITLE_KEY = "name.title"
DOB_DATE_KEY = "dob.date"
DOB_AGE_KEY = "dob.age"
ID_NAME_KEY = "id.name"
