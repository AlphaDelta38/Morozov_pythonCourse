from homework3.part2.validation.bank_pipe import bank_pipe
from homework3.part2.validation_decorator import validate
from homework3.part2.error_handler import error_handler
from homework3.part1.sqlite3_orm import Sqlite_ORM
from homework3.utils import read_dict_csv

def bank_service():
    """
    description:
    service which use validation decorator and pipes for validation data,
    also realize CRUD pattern

    :return: dict of methods
    """

    colum_name = "bank"


    @validate(bank_pipe)
    def create(bank_data):
        """
        description:
        create bank from validate data

        :return: --> dict with message and status code
        """

        try:
            Sqlite_ORM.create(colum_name, bank_data)
            return {"status": 200, "message": "successfully created"}
        except Exception as e:
            return e if isinstance(e, dict) else {"status": 500, "message": str(e)}


    def create_many(csv_file_path):
        """
        description:
        create bank from data by csv file

        :return: --> dict with message and status code
        """

        try:
            data = read_dict_csv(csv_file_path)
            Sqlite_ORM.create_many(colum_name, data)
            return {"status": 200, "message": "successfully created"}
        except Exception as e:
            return e if isinstance(e, dict) else {"status": 500, "message": str(e)}


    @validate(bank_pipe)
    def update(new_date):
        """
        description:
        update data in bank

        :return: --> dict with message and status code
        """

        try:
            Sqlite_ORM.update(colum_name, new_date, f"id = {new_date["id"]}")
            return {"status": 200, "message": "successfully updated"}
        except Exception as e:
            return e if isinstance(e, dict) else {"status": 500, "message": str(e)}


    def get_one(condition):
        """
        description:
        get one bank by condition

        :return: --> dict with message and status code, and response
        """

        try:
            return {"status": 200, "message": "successfully got one", "response": Sqlite_ORM.get_one(colum_name, condition)}
        except Exception as e:
            return e if isinstance(e, dict) else {"status": 500, "message": str(e)}


    def get_many(condition):
        """
        description:
        get many banks by condition

        :return: --> dict with message and status code, and response
        """

        try:
            return {"status":200, "message": "successful got many rows", "response": Sqlite_ORM.get_many(colum_name)}
        except Exception as e:
            return e if isinstance(e, dict) else {"status": 500, "message": str(e)}


    def delete(input_id):
        """
        description:
        delete data about bank by bank id

        :return: --> dict with message and status code
        """

        try:
            if not isinstance(input_id, int):
                error_handler(400, "id must be number")
            Sqlite_ORM.delete(colum_name,f"id = {input_id}")
            return {"status": 200, "message": "successfully deleted"}
        except Exception as e:
            return e if isinstance(e, dict) else {"status": 500, "message": str(e)}


    return {
        "create": create,
        "creates": create_many,
        "update": update,
        "delete": delete,
        "get": get_one,
        "gets": get_many,
    }