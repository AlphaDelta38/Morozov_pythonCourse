from utils import read_dict_csv, write_by_dict_csv, move_file, get_tabs
from transform_csv import transform_csv
from constants import (API_URL)
from collections import Counter
from logger import Logger
import argparse
import requests
import shutil
import os


def main():
    args = parse_args()
    Logger(log_level=args.log_level)

    file_path = f"{os.path.join(".", args.file_name)}.csv"

    try:
        download_user_data(args, file_path)
        Logger().info("download successful")

        transform_csv(file_path)
        Logger().info("transform successful")

        os.makedirs(args.path, exist_ok=True)

        move_file(file_path, args.path)
        Logger().info("move initial file successful")

        file_path = f"{os.path.join(args.path, args.file_name)}.csv"

        create_folder_structure(file_path, args.path)
        Logger().info("Folder structure successful created")

        delete_data_before_1960(args.path)
        Logger().info("Delete data have been successful")

        log_structure_tree(args.path)
        Logger().info("The tree has been logged")

        shutil.make_archive(args.file_name, 'zip', args.path)
        Logger().info("Archive the tree successfully")

        shutil.rmtree(args.path)
        Logger().info("Deleted the tree successfully")

    except Exception as e:
        Logger().error(e)
        exit(1)


def download_user_data(args, file_path):
    response = requests.get(f"{API_URL}/?results={args.amount}&gender={args.gender or '{!!!!}'}&format=csv")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(response.text)


def create_folder_structure(file_path, dir_path):
    data = read_dict_csv(file_path)
    result_dict = {}

    for row in data:
        year = int(row["dob.date"].split("/")[2]) // 100
        country = row["location.country"]
        full_decades = int(row["dob.date"].split("/")[2]) % 100
        rounded_decades = full_decades - (full_decades % 10)

        transform_decades = f"{year}{rounded_decades}s"

        if not transform_decades in result_dict:
            result_dict[transform_decades] = {}
        if country not in result_dict[transform_decades]:
            result_dict[transform_decades][country] = []
        result_dict[transform_decades][country].append(row)

    for _, (year_key, value) in enumerate(result_dict.items()):
        year_dir_path = os.path.join(dir_path, year_key)
        os.makedirs(year_dir_path, exist_ok=True)
        for index, country_key in enumerate(value.keys()):
            os.makedirs(os.path.join(year_dir_path, country_key), exist_ok=True)

    split_data_into_folders(dir_path, result_dict)
    Logger().info("data successfully entered into folder tree")


def split_data_into_folders(dir_path, data):
    for _, (year_key, year_Value) in enumerate(data.items()):
        year_dir_path = os.path.join(dir_path, year_key)
        for _, (country_key, country_value) in enumerate(year_Value.items()):
            country_dir_path = f"{year_dir_path}/{country_key}"

            avg_registered_age = (sum(int(user_data["registered.age"]) for user_data in country_value) /
                                  len(country_value))
            max_age = 0
            all_names_id = []

            for user in country_value:
                all_names_id.append(user["id.name"])
                if max_age < int(user["dob.age"]):
                    max_age = int(user["dob.age"])

            counter = Counter(all_names_id)
            most_common = counter.most_common(1)[0]

            file_path = os.path.join(
                country_dir_path,
                f"max_age_{max_age}_avg_registered_{avg_registered_age}_popular_id_{most_common}.csv"
            )

            write_by_dict_csv(file_path, country_value)
            Logger().debug(file_path)


def delete_data_before_1960(dir_path):
    items = os.listdir(dir_path)
    for item in items:
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path) and int(item[:-1]) < 1960:
                shutil.rmtree(item_path)


def log_structure_tree(dir_path):
    t_index = 0
    full_structure_tree = "structure tree: \n"
    stack = os.listdir(dir_path)

    def recursive_walk(data_path):
        nonlocal full_structure_tree, t_index

        temp_t_index = t_index + 1
        t_index += 1
        temp_stack = []

        if os.path.isdir(data_path):
            temp_stack = os.listdir(data_path)
        else:
            return

        for temp_element in temp_stack:
            temp_element_path = f"{data_path}/{temp_element}"

            if os.path.isdir(temp_element_path):
                full_structure_tree += f"{get_tabs(t_index)}{temp_element} d \n"

                recursive_walk(temp_element_path)
                t_index = temp_t_index
            else:
                full_structure_tree += f"{get_tabs(t_index)}{temp_element} f \n"

    for element in stack:
        t_index = 0
        path = f"{dir_path}/{element}"
        if os.path.isdir(path):
            full_structure_tree += f"{element} d \n"
        else:
            full_structure_tree += f"{element} f \n"

        recursive_walk(path)

    Logger().info(full_structure_tree)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--path",required=True,help="Path to the folder")
    parser.add_argument("--file_name", required=True, default="output",
                        help="Name of the output file, default is output")
    parser.add_argument("--gender", required=False,
                        help="Gender for filter request data user [not required]")
    parser.add_argument("--amount", required=False, default=5000,
                        help="Amount for request row of data user [not required]")
    parser.add_argument("--log_level", required=False, default="INFO",
                        help="Logging level [not required]")

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    main()
