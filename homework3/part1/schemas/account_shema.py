from homework3.part1.orm_constants_templates import *


def get_account_schema():
    """
    description:
    store and retrieve schema

    :return: --> tuple of db table name, settings for colum, and additional settings for colum
    """

    return ("Account"
        ,
        {
            "id": [INTEGER, PRIMARY_KEY],
            "user_id": [INTEGER, NOT_NULL],
            "type": [VARCHAR(15), ENUM("type",["credit", "debit"]), NOT_NULL],
            "account_number": [VARCHAR(19), NOT_NULL, UNIQUE],
            "bank_id": [INTEGER, NOT_NULL],
            "currency": [VARCHAR(50), NOT_NULL],
            "amount": [REAL, NOT_NULL],
            "status": [VARCHAR(15), ENUM("status", ["gold", "silver", "platinum", "NULL"]), DEFAULT("NULL")],
        },
        []
    )