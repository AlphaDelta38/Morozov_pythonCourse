from dataclasses import dataclass
from typing import List, Dict
from homework3.part1.orm_constants_templates import (
    PRIMARY_KEY,
    NOT_NULL,
    INTEGER,
    VARCHAR,
    DEFAULT,
    UNIQUES,
    UNIQUE,
    ENUM,
    REAL
)


@dataclass
class DB_Schema:
    table_name: str
    colum_settings: Dict[str, List[str]]
    add: List[str] = None


account_schema = DB_Schema(
    table_name="Account",
    colum_settings={
        "id": [INTEGER, PRIMARY_KEY],
        "user_id": [INTEGER, NOT_NULL],
        "type": [VARCHAR(15), ENUM("type", ["credit", "debit"]), NOT_NULL],
        "account_number": [VARCHAR(19), NOT_NULL, UNIQUE],
        "bank_id": [INTEGER, NOT_NULL],
        "currency": [VARCHAR(50), NOT_NULL],
        "amount": [REAL, NOT_NULL],
        "status": [VARCHAR(15), ENUM("status", ["gold", "silver", "platinum", "NULL"]), DEFAULT("NULL")],
    },
)

bank_schema = DB_Schema(
    table_name="Bank",
    colum_settings={
        "id": [INTEGER, PRIMARY_KEY],
        "name": [VARCHAR(255), NOT_NULL, UNIQUE]
    },
)

transaction_schema = DB_Schema(
    table_name="Transactions",
    colum_settings={
        "id": [INTEGER, PRIMARY_KEY],
        "bank_sender_name": [VARCHAR(122), NOT_NULL],
        "account_sender_id": [INTEGER, NOT_NULL],
        "bank_receiver_name": [VARCHAR(122), NOT_NULL],
        "account_receiver_id": [INTEGER, NOT_NULL],
        "sent_currency": [VARCHAR(50), NOT_NULL],
        "sent_amount": [REAL, NOT_NULL],
        "datetime": [VARCHAR(100)],
    },
)

user_schema = DB_Schema(
    table_name="User",
    colum_settings={
        "id": [INTEGER, PRIMARY_KEY],
        "name": [VARCHAR(122), NOT_NULL],
        "surname": [VARCHAR(122), NOT_NULL],
        "birth_day": [VARCHAR(32)],
        "accounts": [VARCHAR(122)],
    },
    add=[UNIQUES(["name", "surname"])]
)


DB_SCHEMAS = [
    transaction_schema,
    account_schema,
    bank_schema,
    user_schema
]







