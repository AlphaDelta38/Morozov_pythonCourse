from homework3.part2.API.transaction_service import TransactionService
from homework3.part2.API.service_controller import ServiceController
from homework3.part2.validation.account_pipe import account_pipe
from homework3.part2.API.currnecy_service import CurrencyService
from homework3.part2.validation_decorator import validate
from homework3.part2.error_handler import message_handler
from homework3.part2.API.bank_service import BankService
from homework3.part1.sqlite3_orm import SQLite3ORM
from homework3.utils import read_dict_csv
from datetime import datetime


COLUM_NAME = "account"


class AccountService(ServiceController):
    """
    description:
    service which use validation decorator and pipes for validation data,
    also realize CRUD pattern

    """

    @staticmethod
    @validate(account_pipe)
    def create(account_data):
        """
        description:
        create account from validate data

        :return: --> dict with message and status code
        """

        SQLite3ORM.create(COLUM_NAME, account_data)

        return message_handler(200, "successfully created account").data

    @staticmethod
    def create_many(csv_file_path):
        """
        description:
        create account from data by csv file

        :return: --> dict with message and status code
        """

        data = read_dict_csv(csv_file_path)
        SQLite3ORM.create_many(COLUM_NAME, data)

        return message_handler(200, "successfully created accounts").data

    @staticmethod
    @validate(account_pipe)
    def update(new_date):

        """
        description:
        update data in account

        :return: --> dict with message and status code
        """

        SQLite3ORM.update(COLUM_NAME, new_date, f"id = {new_date["id"]}")

        return message_handler(200, "successfully updated account").data

    @staticmethod
    def delete(input_id):
        """
        description:
        delete data about account by account id

        :return: --> dict with message and status code
        """

        if not isinstance(input_id, int):
            raise message_handler(400, "id must be number")
        SQLite3ORM.delete(COLUM_NAME, f"id = {input_id}")

        return message_handler(200, "successfully deleted account").data

    @staticmethod
    def get_one(condition):
        """
        description:
        get one account by condition

        :return: --> dict with message and status code, and response
        """

        return message_handler(
            200,
            "successfully got one  account",
            SQLite3ORM.get_one(COLUM_NAME, condition)
        ).data

    @staticmethod
    def get_many(condition="", limit=0):
        """
        description:
        get many account by condition

        :return: --> dict with message and status code, and response
        """

        return message_handler(
            200,
            "successfully got many  account",
            SQLite3ORM.get_many(COLUM_NAME, search_by=condition, limit=limit)
        ).data

    @staticmethod
    def transfer(**data):
        """
        description:
        transfer money from one account to another, also converted if currency different

        :return: --> dict with message and status code
        """

        keys = ["sender_account_number", "receiver_account_number", "amount"]
        sender_number, receiver_number, amount = [data[key] for key in keys]

        sender_account = AccountService.get_one(f"account_number=\"{sender_number}\"")["response"]
        receiver_account = AccountService.get_one(f"account_number=\"{receiver_number}\"")["response"]

        if not sender_account or not receiver_account:
            raise message_handler(400, "bad request sender_account_id or receiver_account_id are bad")

        if (float(sender_account["amount"] - float(amount))) < 0:
            raise message_handler(402, "Not enough money in the account")

        converted_currency = CurrencyService.translate(
            from_currency=sender_account["currency"],
            to_currency=receiver_account["currency"],
            amount=amount)["response"]

        AccountService.update(id=sender_account["id"], amount=float(sender_account["amount"]) - float(amount))
        AccountService.update(id=receiver_account["id"], amount=float(receiver_account["amount"]) + converted_currency)

        bank_sender = BankService.get_one(f"id = {sender_account['bank_id']}")["response"]
        bank_receiver = BankService.get_one(f"id = {receiver_account['bank_id']}")["response"]

        if not bank_sender or not bank_receiver:
            raise message_handler(400, "bad request bank_sender_id or bank_receiver_id are bad")

        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d %H:%M:%S")

        TransactionService.create({
            "bank_sender_name": bank_sender["name"],
            "bank_receiver_name": bank_receiver["name"],
            "account_sender_id": sender_account["id"],
            "account_receiver_id": receiver_account["id"],
            "sent_currency": sender_account["currency"],
            "sent_amount": float(amount),
            "datetime": date_str
        })

        return message_handler(200, "successfully transfer between account").data
