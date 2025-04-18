from pathlib import Path
import shutil
import csv
import os


def resolve_path(check_type, path, default):
    if (os.path.isfile(path) and check_type == "file") or (os.path.isdir(path) and check_type == "dir"):
        return path
    else:
        return default


def read_dict_csv(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data


def write_by_dict_csv(file_path, data):
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        fieldnames = data[0].keys()

        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)

        csv_writer.writeheader()
        csv_writer.writerows(data)


def move_file(file_path, destination_folder):
    file_name = Path(file_path).name
    if os.path.isfile(file_path) and os.path.isdir(destination_folder):
        destination_file_path = os.path.join(destination_folder, file_name)

        if os.path.isfile(destination_file_path):
            os.remove(destination_file_path)

        shutil.move(file_path, destination_folder)

        return os.path.join(destination_folder, file_name)
    else:
        return file_path


def get_tabs(n):
    return "\t" * n
