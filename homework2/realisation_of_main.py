from constants import DOB_AGE_KEY, ID_NAME_KEY, DOB_DATE_KEY, REGISTER_AGE_KEY, LOCATION_COUNTRY_KEY
from utils import read_dict_csv, write_by_dict_csv, move_file, get_tabs
from collections import Counter
from dotenv import load_dotenv
from logger import Logger
import requests
import shutil
import os


load_dotenv()

set_logs = Logger()


def download_user_data(args, file_path):
    gender = f"&gender={args.gender}" if args.gender else ""
    response = requests.get(f"{os.getenv("API_URL")}/?results={args.amount}{gender}&format=csv")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(response.text)


def create_folder_structure(file_path, dir_path):
    data = read_dict_csv(file_path)
    result_dict = {}

    for row in data:
        country = row[LOCATION_COUNTRY_KEY]
        transform_decades = f"{row[DOB_DATE_KEY].split("/")[2][:-1]}0s"

        result_dict.setdefault(transform_decades, {})
        result_dict[transform_decades].setdefault(country, []).append(row)

    for year_key, value in result_dict.items():
        for country_key in value.keys():
            os.makedirs(os.path.join(dir_path, year_key, country_key), exist_ok=True)

    return result_dict


def get_filename(user_data_rows):
    avg_registered_age = sum(int(user_data[REGISTER_AGE_KEY]) for user_data in user_data_rows) / len(user_data_rows)

    max_age = max([int(user[DOB_AGE_KEY]) for user in user_data_rows])

    counter = Counter([user[ID_NAME_KEY] for user in user_data_rows])
    most_common = counter.most_common(1)[0]

    return f"max_age_{max_age}_avg_registered_{avg_registered_age}_popular_id_{most_common}.csv"


def split_data_into_folders(dir_path, data):
    for year_key, year_value in data.items():
        for country_key, user_data_rows in year_value.items():
            file_path =  os.path.join(dir_path, year_key, country_key, get_filename(user_data_rows))

            write_by_dict_csv(file_path, user_data_rows)
            Logger().debug(file_path)


def delete_data_before_1960(dir_path):
    items = os.listdir(dir_path)
    for item in items:
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path) and int(item[:-1]) < 1960:
            shutil.rmtree(item_path)


def string_structure_tree(dir_path):
    result_structure_tree = "structure tree: \n"

    for items in os.walk(dir_path):
        path_dir, dirs, files = items
        t_index = len(path_dir.split("\\")) - 1

        result_structure_tree += f"{get_tabs(t_index)}{path_dir.split("\\")[-1]} d \n "

        for file in files:
            result_structure_tree += f"{get_tabs(t_index + 1)}{file} f \n"

    return result_structure_tree
