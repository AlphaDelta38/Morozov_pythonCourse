from realisation_of_main import (
    download_user_data,
    create_folder_structure,
    split_data_into_folders,
    delete_data_before_1960,
    string_structure_tree,
)
from utils import move_file
from transform_csv import transform_csv
from logger import Logger
import argparse
import shutil
import os


def main():
    args = parse_args()
    set_log = Logger(log_level=args.log_level)

    file_path = f"{os.path.join(".", args.file_name)}.csv"

    try:
        download_user_data(args, file_path)
        set_log.info("download successful")

        transform_csv(file_path)
        set_log.info("transform successful")

        os.makedirs(args.path, exist_ok=True)

        move_file(file_path, args.path)
        set_log.info("move initial file successful")

        file_path = f"{os.path.join(args.path, args.file_name)}.csv"

        structure_dict = create_folder_structure(file_path, args.path)
        set_log.info("Folder structure successful created")

        split_data_into_folders(args.path, structure_dict)
        Logger().info("data successfully entered into folder tree")

        delete_data_before_1960(args.path)
        set_log.info("Delete data have been successful")

        string_tree = string_structure_tree(args.path)
        set_log.info(string_tree)

        shutil.make_archive(args.file_name, 'zip', args.path)
        set_log.info("Archive the tree successfully")

        shutil.rmtree(args.path)
        set_log.info("Deleted the tree successfully")

    except Exception as e:
        Logger().error(e)
        exit(1)


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

    return parser.parse_args()


if __name__ == '__main__':
    main()
