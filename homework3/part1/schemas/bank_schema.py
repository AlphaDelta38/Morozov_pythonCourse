from homework3.part1.orm_constants_templates import *


def get_bank_schema():
    """
    description:
    store and retrieve schema

    :return: --> tuple of db table name, settings for colum, and additional settings for colum
    """

    return ("Bank"
        ,
        {
        "id": [INTEGER, PRIMARY_KEY],
        "name": [VARCHAR(255), NOT_NULL, UNIQUE]
        },
        []
    )
