from homework3.part2.API.service_controller import ServiceController
from homework3.part2.validation.user_pipe import user_pipe
from homework3.part2.validation_decorator import validate
from homework3.part2.error_handler import message_handler
from homework3.part1.sqlite3_orm import SQLite3ORM
from homework3.utils import read_dict_csv


COLUM_NAME = "user"


class UserService(ServiceController):
    """
    description:
    service which use validation decorator and pipes for validation data,
    also realize CRUD pattern

    """

    @staticmethod
    @validate(user_pipe)
    def create(user_data):
        """
        description:
        create user from validate data

        :return: --> dict with message and status code
        """

        SQLite3ORM.create(COLUM_NAME, user_data)

        return message_handler(200,  "successfully created user").data

    @staticmethod
    def create_many(csv_file_path):
        """
        description:
        create user from data by csv file

        :return: --> dict with message and status code
        """

        data = read_dict_csv(csv_file_path)
        SQLite3ORM.create_many(COLUM_NAME, data)

        return message_handler(200,  "successfully created users").data

    @staticmethod
    @validate(user_pipe)
    def update(new_date):
        """
        description:
        update data about user

        :return: --> dict with message and status code
        """

        SQLite3ORM.update(COLUM_NAME, new_date, f"id = {new_date["id"]}")

        return message_handler(200,  "successfully updated user").data

    @staticmethod
    def delete(input_id):
        """
        description:
        delete data about user by user id

        :return: --> dict with message and status code
        """

        if not isinstance(input_id, int):
            raise message_handler(400, "id must be number")
        SQLite3ORM.delete(COLUM_NAME, f"id = {input_id}")

        return message_handler(200, "successfully deleted user").data

    @staticmethod
    def get_one(condition):
        """
        description:
        get one transaction by condition

        :return: --> dict with message and status code, and response
        """

        return message_handler(
            200,
            "successfully got one user",
            SQLite3ORM.get_one(COLUM_NAME, condition)
        ).data

    @staticmethod
    def get_many(condition="", limit=0):
        """
        description:
        get many users by condition

        :return: --> dict with message and status code, and response
        """

        return message_handler(
            200,
            "successfully got many user",
            SQLite3ORM.get_many(COLUM_NAME, search_by=condition, limit=limit)
        ).data
