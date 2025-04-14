from homework3.part2.validation.account_pipe import account_pipe
from homework3.part2.validation_decorator import validate
from homework3.part2.error_handler import error_handler
from transaction_service import transaction_service
from homework3.part1.sqlite3_orm import Sqlite_ORM
from currnecy_service import currency_service
from homework3.utils import read_dict_csv
from bank_service import bank_service
from datetime import datetime


def account_service():
    """
    description:
    service which use validation decorator and pipes for validation data,
    also realize CRUD pattern

    :return: dict of methods
    """

    colum_name = "account"
    curren_service = currency_service()
    trans_service = transaction_service()
    bank_services = bank_service()


    @validate(account_pipe)
    def create(**account_data):
        """
        description:
        create account from validate data

        :return: --> dict with message and status code
        """

        try:
            Sqlite_ORM.create(colum_name, account_data)
            return {"status": 200, "message": "successfully created"}
        except Exception as e:
            return e if isinstance(e, dict) else {"status": 500, "message": str(e)}


    def create_many(csv_file_path):
        """
        description:
        create account from data by csv file

        :return: --> dict with message and status code
        """

        try:
            data = read_dict_csv(csv_file_path)
            Sqlite_ORM.create_many(colum_name, data)
            return {"status": 200, "message": "successfully created"}
        except Exception as e:
            return e if isinstance(e, dict) else {"status": 500, "message": str(e)}


    @validate(account_pipe)
    def update(**new_date):
        """
        description:
        update data in account

        :return: --> dict with message and status code
        """

        try:
            Sqlite_ORM.update(colum_name, new_date, f"id = {new_date["id"]}")
            return {"status": 200, "message": "successfully updated"}
        except Exception as e:
            return e if isinstance(e, dict) else {"status": 500, "message": str(e)}


    def delete(input_id):
        """
        description:
        delete data about account by account id

        :return: --> dict with message and status code
        """

        try:
            if not isinstance(input_id, int):
                error_handler(400, "id must be number")
            Sqlite_ORM.delete(colum_name,f"id = {input_id}")
            return {"status": 200, "message": "successfully deleted"}
        except Exception as e:
            return e if isinstance(e, dict) else {"status": 500, "message": str(e)}


    def get_one(condition):
        """
        description:
        get one account by condition

        :return: --> dict with message and status code, and response
        """

        try:
            return {"status":200, "message": "successful got one", "response": Sqlite_ORM.get_one(colum_name, condition)}
        except Exception as e:
            return e if isinstance(e, dict) else {"status": 500, "message": str(e)}


    def get_many(condition):
        """
        description:
        get many account by condition

        :return: --> dict with message and status code, and response
        """

        try:
            return {"status":200, "message": "successful got many rows", "response": Sqlite_ORM.get_many(colum_name)}
        except Exception as e:
            return e if isinstance(e, dict) else {"status": 500, "message": str(e)}


    def transfer(data):
        """
        description:
        transfer money from one account to another, also converted if currency different

        :return: --> dict with message and status code
        """

        try:
            keys = ["sender_account_number", "receiver_account_number", "amount"]
            sender_number, receiver_number, amount = [data[key] for key in keys]

            sender_account = get_one(f"account_number={sender_number}")
            receiver_account = get_one(f"account_number={receiver_number}")

            if (float(sender_account["amount"] - float(amount))) < 0:
                raise ValueError({"status": 402, "message": "Not enough money in the account"})

            converted_currency = curren_service["translate"](sender_account["currency"], receiver_account["currency"], amount)["response"]

            update({"id": sender_account["id"], "amount": float(sender_account["amount"]) - float(amount)})
            update({"id": receiver_account["id"], "amount": float(receiver_account["amount"]) + converted_currency})

            bank_sender = bank_services["get"](f"id = {sender_account['bank_id']}")
            bank_receiver = bank_services["get"](f"id = {receiver_account['bank_id']}")

            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d %H:%M:%S")

            trans_service["create"]({
                "bank_sender_name": bank_sender["name"],
                "bank_receiver_name": bank_receiver["name"],
                "account_sender_id": sender_account["id"],
                "account_receiver_id": receiver_account["id"],
                "sent_currency": sender_account["currency"],
                "sent_amount": float(amount),
                "datetime": date_str
            })

            return {"status": 200, "message": "successfully transferred"}
        except Exception as e:
            return e if isinstance(e, dict) else {"status": 500, "message": str(e)}


    return {
        "create": create,
        "creates": create_many,
        "update": update,
        "delete": delete,
        "get": get_one,
        "gets": get_many,
        "transfer": transfer,
    }