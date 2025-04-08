from datetime import datetime, timedelta, timezone
from utils import write_by_dict_csv
from constants import TIME_FORMAT, DOB_DATE_FORMAT, REGISTER_DATE_FORMAT
from utils import read_dict_csv
from logger import Logger


VALUES_TRANSFORM = {"Mrs": "missis", "Ms": "miss", "Mr": "mister", "Madame": "mademoiselle"}


def transform_csv(file_path):
    data = read_dict_csv(file_path)

    add_global_index(data)
    add_current_time(data)
    change_title(data)
    convert_dob_date(data)
    convert_register_date(data)

    write_by_dict_csv(file_path, data)


def add_global_index(data):
    for index, row in enumerate(data):
        new_row = {"global_index": index, **row}
        data[index] = new_row


def add_current_time(data):
    for index, row in enumerate(data):
        hours, minutes = map(int, row["location.timezone.offset"].split(":"))
        tz_offset = timezone(timedelta(hours=hours, minutes=minutes))
        current_time = datetime.now(tz_offset)

        row["current_time"] = current_time.strftime(TIME_FORMAT)


def change_title(data):
    title_key = "name.title"
    for index, row in enumerate(data):
        if row[title_key] in VALUES_TRANSFORM:
            row[title_key] = VALUES_TRANSFORM[row[title_key]]
        else:
            Logger().warning(f"value: {row[title_key]} not exist in enum dict")


def convert_dob_date(data):
    dob_date_key = "dob.date"
    for row in data:
        year_month_day = datetime.strptime(row[dob_date_key], DOB_DATE_FORMAT).date()
        year, month, day = year_month_day.isoformat().split("-")
        needed_dob_date_format = f"{month}/{day}/{year}"
        row[dob_date_key] = needed_dob_date_format


def convert_register_date(data):
    registered_date_key = "registered.date"
    for row in data:
        registered_date = datetime.strptime(row[registered_date_key], "%Y-%m-%dT%H:%M:%S.%fZ")
        registered_formated_date = registered_date.strftime(REGISTER_DATE_FORMAT)
        row[registered_date_key] = registered_formated_date