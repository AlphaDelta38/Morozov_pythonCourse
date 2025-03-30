from datetime import datetime, timedelta, timezone
from collections import Counter
from dotenv import load_dotenv
import argparse
import requests
import logging
import shutil
import json
import csv
import os
import io


load_dotenv()
PARSER = argparse.ArgumentParser()

PARSER.add_argument("--path", required=True, help="Path to the folder")
PARSER.add_argument("--file_name", required=True, default="output", help="Name of the output file, default is output")
PARSER.add_argument("--gender", required=False, help="Gender for filter request data user [not required]")
PARSER.add_argument("--amount", required=False, default=5000, help="Amount for request row of data user [not required]")
PARSER.add_argument("--log_level", required=False, default="INFO", help="Logging level [not required]")

args = PARSER.parse_args()

file_logger = logging.getLogger("file_logger")
file_handler = logging.FileHandler("file.log")
file_handler.setLevel(args.log_level)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s"))
file_logger.setLevel(args.log_level)
file_logger.addHandler(file_handler)

API_URL = os.getenv("API_URL")
SAVE_FOLDER = "saves"
TIME_FORMAT = "%H:%M:%S"
DOB_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
REGISTER_DATE_FORMAT = "%m-%d-%YT%H:%M:%S"

file_logger.info(f"Entered flags path: {args.path}, file name: {args.file_name}, gender: {args.gender}, amount: {args.amount}, log_level: {args.log_level}")
file_path = os.path.join(args.path, args.file_name)

if not os.path.exists(args.path) or not os.path.isdir(args.path):
    os.makedirs(SAVE_FOLDER, exist_ok=True)
    args.path = SAVE_FOLDER
    file_logger.info(f"General directory changed to {SAVE_FOLDER}")


def main():
    csv_list = download_user_data()
    file_logger.info("Downloading successfully")
    transform_and_write(csv_list)
    file_logger.info("Transform and write successfully")
    csv_transforms()
    file_logger.info("CSV transform and packing successfully")


def download_user_data():
    file_logger.debug("Start to downloading user data")
    try:
        response = requests.get(f"{API_URL}/?results={args.amount}&gender={args.gender or '{!!!!}'}&format=csv")
        file_logger.debug("Data successfully downloaded")

        csv_file = io.StringIO(response.text)
        csv_reader = list(csv.reader(csv_file))
        file_logger.debug("successfully transform response data to list (from csv)")
        return csv_reader
    except Exception as e:
        file_logger.debug("Unexpected error with data request")
        file_logger.error(e)
        exit(1)


def transform_and_write(csv_list):
    file_logger.debug("Start to transforming and writing user data")
    csv_list[0].append("global_index")
    csv_list[0].append("current_time")

    time_zone_index = csv_list[0].index("location.timezone.offset")
    title_name_index = csv_list[0].index("name.title")
    dob_data_index = csv_list[0].index("dob.date")
    registered_date_index = csv_list[0].index("registered.date")

    VALUES_TRANSFORM = {"Mrs": "missis", "Ms": "miss", "Mr": "mister", "Madame": "mademoiselle"}

    try:
        for index, row in enumerate(csv_list):
            if index > 0:
                row.append(f"{index}")

                hours, minutes = map(int, row[time_zone_index].split(":"))
                tz_offset = timezone(timedelta(hours=hours, minutes=minutes))
                current_time = datetime.now(tz_offset)
                row.append(current_time.strftime(TIME_FORMAT))

                if row[title_name_index] in VALUES_TRANSFORM:
                    row[title_name_index] = VALUES_TRANSFORM[row[title_name_index]]
                else:
                    logging.warning(f"value: {row[title_name_index]} not exist in enum dict")

                year_month_day = datetime.strptime(row[dob_data_index], DOB_DATE_FORMAT).date()
                year, month, day = year_month_day.isoformat().split("-")
                needed_dob_date_format = f"{month}/{day}/{year}"
                row[dob_data_index] = needed_dob_date_format

                registered_date = datetime.strptime(row[registered_date_index], "%Y-%m-%dT%H:%M:%S.%fZ")
                registered_formated_date = registered_date.strftime(REGISTER_DATE_FORMAT)
                row[registered_date_index] = registered_formated_date
        file_logger.debug("CSV transform and packing successfully")
        with open(f"{file_path}.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(csv_list)
        file_logger.debug(f"Data successfully writed to csv file at path {file_path}.csv")
    except Exception as e:
        file_logger.debug("Unexpected error with transform and write")
        file_logger.error(e)
        exit(1)


def csv_transforms():
    file_logger.debug("Start to transforming and packing csv file")
    try:
        with open(f"{file_path}.csv", mode="r", newline="", encoding="utf-8") as file:
            csv_list = list(csv.reader(file))
            file_logger.debug("Successfully read csv file")
            dob_data_index = csv_list[0].index("dob.date")
            country_data_index = csv_list[0].index("location.country")
            result_dict = {}

            for index, row in enumerate(csv_list):
                if index > 0:
                    year, decades = row[dob_data_index].split("/")[2][:2], row[dob_data_index].split("/")[2][2:]
                    country = row[country_data_index]
                    user_data_dict = {}

                    transform_decades = f"{year}{(int(decades) // 10) * 10}s"
                    if int(transform_decades[:-1]) < 1960:
                        continue
                    if not transform_decades in result_dict:
                        result_dict[transform_decades] = {}
                    if country not in result_dict[transform_decades]:
                        result_dict[transform_decades][country] = []

                    for header, value in zip(csv_list[0], row):
                        user_data_dict[header] = value

                    result_dict[transform_decades][country].append(user_data_dict)
            file_logger.debug("Successfully transform to dictionary")
            json_object = json.dumps(result_dict, indent=4)
            with open(f"{file_path}.json", "w", encoding="utf-8") as json_file:
                json_file.write(json_object)
            file_logger.debug("Successfully write to json file")

            new_general_dir_path = f"{args.path}/{args.file_name}"
            os.makedirs(new_general_dir_path, exist_ok=True)
            age_key = "dob.age"
            registered_age_key = "registered.age"
            id_name_key = "id.name"

            full_structure_tree = args.file_name

            for year_key, year_value in result_dict.items():
                decades_dir__path = f"{new_general_dir_path}/{year_key}"
                os.makedirs(decades_dir__path, exist_ok=True)
                full_structure_tree += f"\n\t{year_key}"

                for country_key, country_value in year_value.items():
                    country_dir_path = f"{decades_dir__path}/{country_key}"
                    os.makedirs(country_dir_path, exist_ok=True)
                    full_structure_tree += f"\n\t\t{country_key}"
                    max_age = 0

                    avg_registered_age = sum(int(user_data[registered_age_key]) for user_data in country_value) / len(country_value)
                    all_names_id = []

                    for user in country_value:
                        all_names_id.append(user[id_name_key])
                        if max_age < int(user[age_key]):
                            max_age = int(user[age_key])

                    counter = Counter(all_names_id)
                    most_common = counter.most_common(1)[0]

                    current_file_name = f"max_age_{max_age}_avg_registered_{avg_registered_age}_popular_id_{most_common}"
                    full_structure_tree += f"\n\t\t\t{current_file_name}.csv"

                    file_path_in_tree = f"{country_dir_path}/{current_file_name}.csv"
                    file_logger.debug(file_path_in_tree)
                    with open(file_path_in_tree, mode="w", newline="", encoding="utf-8") as csv_file:
                        fieldnames = csv_list[0]
                        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(country_value)
                    file_logger.debug("Successfully write csv file ")

            file_logger.info(f"File structure tree: \n {full_structure_tree}")
            shutil.make_archive(f"{args.path}/{args.file_name}", 'zip', new_general_dir_path)
            file_logger.info(f"Successfully converted to zip")
    except Exception as e:
        file_logger.debug("Unexpected error with read and transform csv")
        file_logger.error(e)
        exit(1)


if __name__ == '__main__':
    main()
