from datetime import datetime, timedelta, timezone
from utils import write_by_dict_csv
from constants import (
    LOCATION_TIMEZONE_OFFSET_KEY,
    YEAR_MONTH_DAY_FORMANT,
    REGISTER_DATE_FORMAT,
    REGISTER_DATE_KEY,
    CURRENT_TIME_KEY,
    DOB_DATE_FORMAT,
    NAME_TITLE_KEY,
    DOB_DATE_KEY,
    TIME_FORMAT
)
from utils import read_dict_csv
from logger import Logger


VALUES_TRANSFORM = {"Mrs": "missis", "Ms": "miss", "Mr": "mister", "Madame": "mademoiselle"}


def transform_csv(file_path):
    data = read_dict_csv(file_path)

    for index, row in enumerate(data):
        add_global_index(row, index)
        add_current_time(row)
        change_title(row)
        convert_dob_date(row)
        convert_register_date(row)

    write_by_dict_csv(file_path, data)


def add_global_index(row, index):
    new_row = {"global_index": index, **row}
    row[index] = new_row


def add_current_time(row):
    hours, minutes = map(int, row[LOCATION_TIMEZONE_OFFSET_KEY].split(":"))
    tz_offset = timezone(timedelta(hours=hours, minutes=minutes))
    current_time = datetime.now(tz_offset)

    row[CURRENT_TIME_KEY] = current_time.strftime(TIME_FORMAT)


def change_title(row):
    if row[NAME_TITLE_KEY] in VALUES_TRANSFORM:
        row[NAME_TITLE_KEY] = VALUES_TRANSFORM[row[NAME_TITLE_KEY]]
    else:
        Logger().warning(f"value: {row[NAME_TITLE_KEY]} not exist in enum dict")


def convert_dob_date(row):
    year_month_day = datetime.strptime(row[DOB_DATE_KEY], DOB_DATE_FORMAT).date()
    row[DOB_DATE_KEY] = year_month_day.strftime(YEAR_MONTH_DAY_FORMANT)


def convert_register_date(row):
    registered_date = datetime.strptime(row[REGISTER_DATE_KEY], DOB_DATE_FORMAT)
    row[REGISTER_DATE_KEY] = registered_date.strftime(REGISTER_DATE_FORMAT)
