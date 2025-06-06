from homework3.part2.API.service_controller import ServiceController
from homework3.part2.validation.bank_pipe import bank_pipe
from homework3.part2.validation_decorator import validate
from homework3.part2.error_handler import message_handler
from homework3.part1.sqlite3_orm import SQLite3ORM
from homework3.utils import read_dict_csv


COLUM_NAME = "bank"


class BankService(ServiceController):
    """
    description:
    service which use validation decorator and pipes for validation data,
    also realize CRUD pattern

    """

    @staticmethod
    @validate(bank_pipe)
    def create(bank_data):
        """
        description:
        create bank from validate data

        :return: --> dict with message and status code
        """

        SQLite3ORM.create(COLUM_NAME, bank_data)

        return message_handler(200, "successfully created bank").data

    @staticmethod
    def create_many(csv_file_path):
        """
        description:
        create bank from data by csv file

        :return: --> dict with message and status code
        """

        data = read_dict_csv(csv_file_path)
        SQLite3ORM.create_many(COLUM_NAME, data)

        return message_handler(200, "successfully created banks").data

    @staticmethod
    @validate(bank_pipe)
    def update(new_date):
        """
        description:
        update data in bank

        :return: --> dict with message and status code
        """

        SQLite3ORM.update(COLUM_NAME, new_date, f"id = {new_date["id"]}")

        return message_handler(200, "successfully updated bank").data

    @staticmethod
    def get_one(condition):
        """
        description:
        get one bank by condition

        :return: --> dict with message and status code, and response
        """

        return message_handler(
            200,
            "successfully get one bank",
            SQLite3ORM.get_one(COLUM_NAME, condition)
        ).data

    @staticmethod
    def get_many(condition="", limit=0):
        """
        description:
        get many banks by condition

        :return: --> dict with message and status code, and response
        """

        return message_handler(
            200,
            "successfully get one  bank",
            SQLite3ORM.get_many(COLUM_NAME, search_by=condition, limit=limit)
        ).data

    @staticmethod
    def delete(input_id):
        """
        description:
        delete data about bank by bank id

        :return: --> dict with message and status code
        """

        if not isinstance(input_id, int):
            raise message_handler(400, "id must be number")
        SQLite3ORM.delete(COLUM_NAME, f"id = {input_id}")

        return message_handler(200,  "successfully deleted").data
