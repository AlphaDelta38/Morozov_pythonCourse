from homework3.part2.validation.account_pipe import account_pipe
from homework3.part2.validation_decorator import validate
from homework3.part2.error_handler import message_handler
from homework3.part2.API.transaction_service import transaction_service
from homework3.part1.sqlite3_orm import Sqlite_ORM
from homework3.part2.API.currnecy_service import currency_service
from homework3.utils import read_dict_csv
from homework3.part2.API.bank_service import bank_service
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
    def create(account_data):
        """
        description:
        create account from validate data

        :return: --> dict with message and status code
        """

        Sqlite_ORM.create(colum_name, account_data)

        return message_handler(200, "successfully created account").data


    def create_many(csv_file_path):
        """
        description:
        create account from data by csv file

        :return: --> dict with message and status code
        """

        data = read_dict_csv(csv_file_path)
        Sqlite_ORM.create_many(colum_name, data)

        return message_handler(200, "successfully created accounts").data


    @validate(account_pipe)
    def update(new_date):

        """
        description:
        update data in account

        :return: --> dict with message and status code
        """

        Sqlite_ORM.update(colum_name, new_date, f"id = {new_date["id"]}")

        return message_handler(200, "successfully updated account").data


    def delete(input_id):
        """
        description:
        delete data about account by account id

        :return: --> dict with message and status code
        """

        if not isinstance(input_id, int):
            raise message_handler(400, "id must be number")
        Sqlite_ORM.delete(colum_name,f"id = {input_id}")

        return message_handler(200, "successfully deleted account").data


    def get_one(condition):
        """
        description:
        get one account by condition

        :return: --> dict with message and status code, and response
        """

        return message_handler(
            200,
            "successfully got one  account",
            Sqlite_ORM.get_one(colum_name, condition)
        ).data


    def get_many(condition="", limit=0):
        """
        description:
        get many account by condition

        :return: --> dict with message and status code, and response
        """

        return message_handler(
            200,
            "successfully got many  account",
            Sqlite_ORM.get_many(colum_name, search_by=condition, limit=limit)
        ).data


    def transfer(**data):
        """
        description:
        transfer money from one account to another, also converted if currency different

        :return: --> dict with message and status code
        """

        keys = ["sender_account_number", "receiver_account_number", "amount"]
        sender_number, receiver_number, amount = [data[key] for key in keys]

        sender_account = get_one(f"account_number=\"{sender_number}\"")["response"]
        receiver_account = get_one(f"account_number=\"{receiver_number}\"")["response"]

        if not sender_account or not receiver_account:
            raise message_handler(400, "bad request sender_account_id or receiver_account_id are bad")

        if (float(sender_account["amount"] - float(amount))) < 0:
            raise message_handler(402, "Not enough money in the account")

        converted_currency = curren_service["translate"](
            from_currency=sender_account["currency"],
            to_currency=receiver_account["currency"],
            amount=amount)["response"]

        update(id=sender_account["id"], amount= float(sender_account["amount"]) - float(amount))
        update(id=receiver_account["id"], amount= float(receiver_account["amount"]) + converted_currency)

        bank_sender = bank_services["get"](f"id = {sender_account['bank_id']}")["response"]
        bank_receiver = bank_services["get"](f"id = {receiver_account['bank_id']}")["response"]

        if not bank_sender or not bank_receiver:
            raise message_handler(400, "bad request bank_sender_id or bank_receiver_id are bad")

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

        return message_handler(200, "successfully transfer between account").data


    return {
        "create": create,
        "creates": create_many,
        "update": update,
        "delete": delete,
        "get": get_one,
        "gets": get_many,
        "transfer": transfer,
    }
