from homework3.part1.orm_constants_templates import *


def get_transaction_schema():
    """
    description:
    store and retrieve schema

    :return: --> tuple of db table name, settings for colum, and additional settings for colum
    """

    return ("Transactions"
        ,
        {
        "id": [INTEGER, PRIMARY_KEY],
        "bank_sender_name": [VARCHAR(122), NOT_NULL],
        "account_sender_id": [INTEGER, NOT_NULL],
        "bank_receiver_name": [VARCHAR(122), NOT_NULL],
        "account_receiver_id": [INTEGER, NOT_NULL],
        "sent_currency": [VARCHAR(50), NOT_NULL],
        "sent_amount": [REAL, NOT_NULL],
        "datetime": [VARCHAR(100)],
    },
    []
    )
