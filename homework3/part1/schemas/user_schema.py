from homework3.part1.orm_constants_templates import *


def get_user_schema():
    """
    description:
    store and retrieve schema

    :return: --> tuple of db table name, settings for colum, and additional settings for colum
    """

    return ("User"
        ,
        {
        "id": [INTEGER, PRIMARY_KEY],
        "name": [VARCHAR(122), NOT_NULL],
        "surname": [VARCHAR(122), NOT_NULL],
        "birth_day": [VARCHAR(32)],
        "accounts": [VARCHAR(122)],
        },
        [UNIQUES(["name", "surname"])],
    )
