from homework3.part2.API.service_controller import ServiceController
from homework3.part2.error_handler import message_handler
from homework3.part1.sqlite3_orm import Sqlite_ORM
from homework3.utils import read_dict_csv


colum_name = "transactions"


class TransactionService(ServiceController):
    """
    description:
    service which use validation decorator and pipes for validation data,
    also realize CRUD pattern

    """

    @staticmethod
    def create(transaction_data):
        """
        description:
        create transaction from validate data

        :return: --> dict with message and status code
        """

        Sqlite_ORM.create(colum_name, transaction_data)

        return message_handler(200, "successfully created transaction").data

    @staticmethod
    def create_many(csv_file_path):
        """
        description:
        create transaction from data by csv file

        :return: --> dict with message and status code
        """

        data = read_dict_csv(csv_file_path)
        Sqlite_ORM.create_many(colum_name, data)

        return message_handler(200, "successfully created many transaction").data

    @staticmethod
    def update(new_date):
        """
        description:
        update data in transaction

        :return: --> dict with message and status code
        """


        search_id, *args = new_date.values()
        Sqlite_ORM.update(colum_name, new_date, f"id = {search_id}")

        return message_handler(200, "successfully updated transaction").data

    @staticmethod
    def delete(input_id):
        """
        description:
        delete data about transaction by transaction id

        :return: --> dict with message and status code
        """

        if not isinstance(input_id, int):
            raise message_handler(400, "id must be number")
        Sqlite_ORM.delete(colum_name,f"id = {input_id}")

        return message_handler(200, "successfully deleted transaction").data

    @staticmethod
    def get_one(condition):
        """
        description:
        get one transaction by condition

        :return: --> dict with message and status code, and response
        """

        return message_handler(
            200,
            "successfully got one transaction",
            Sqlite_ORM.get_one(colum_name, condition)
        ).data

    @staticmethod
    def get_many(condition="", limit=0):
        """
        description:
        get many transactions by condition

        :return: --> dict with message and status code, and response
        """

        return message_handler(
            200,
            "successfully got many transaction",
            Sqlite_ORM.get_many(colum_name, search_by=condition, limit=limit)
        ).data
