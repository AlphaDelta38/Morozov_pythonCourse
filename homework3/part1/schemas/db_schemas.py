from dataclasses import dataclass
from typing import List, Dict
from homework3.part1.orm_constants_templates import (
    PRIMARY_KEY,
    NOT_NULL,
    INTEGER,
    UNIQUE,
    REAL,
    create_varchar,
    create_default,
    create_uniques,
    create_enum,
)


@dataclass
class DBSchema:
    table_name: str
    colum_settings: Dict[str, List[str]]
    add: List[str] = None


account_schema = DBSchema(
    table_name="Account",
    colum_settings={
        "id": [INTEGER, PRIMARY_KEY],
        "user_id": [INTEGER, NOT_NULL],
        "type": [create_varchar(15), create_enum("type", ["credit", "debit"]), NOT_NULL],
        "account_number": [create_varchar(19), NOT_NULL, UNIQUE],
        "bank_id": [INTEGER, NOT_NULL],
        "currency": [create_varchar(50), NOT_NULL],
        "amount": [REAL, NOT_NULL],
        "status": [
            create_varchar(15),
            create_enum(
                "status",
                ["gold", "silver", "platinum", "NULL"]
            ),
            create_default("NULL")
        ],
    },
)

bank_schema = DBSchema(
    table_name="Bank",
    colum_settings={
        "id": [INTEGER, PRIMARY_KEY],
        "name": [create_varchar(255), NOT_NULL, UNIQUE]
    },
)

transaction_schema = DBSchema(
    table_name="Transactions",
    colum_settings={
        "id": [INTEGER, PRIMARY_KEY],
        "bank_sender_name": [create_varchar(122), NOT_NULL],
        "account_sender_id": [INTEGER, NOT_NULL],
        "bank_receiver_name": [create_varchar(122), NOT_NULL],
        "account_receiver_id": [INTEGER, NOT_NULL],
        "sent_currency": [create_varchar(50), NOT_NULL],
        "sent_amount": [REAL, NOT_NULL],
        "datetime": [create_varchar(100)],
    },
)

user_schema = DBSchema(
    table_name="User",
    colum_settings={
        "id": [INTEGER, PRIMARY_KEY],
        "name": [create_varchar(122), NOT_NULL],
        "surname": [create_varchar(122), NOT_NULL],
        "birth_day": [create_varchar(32)],
        "accounts": [create_varchar(122)],
    },
    add=[create_uniques(["name", "surname"])]
)


DB_SCHEMAS = [
    transaction_schema,
    account_schema,
    bank_schema,
    user_schema
]
