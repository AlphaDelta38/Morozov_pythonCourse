from homework3.part1.schemas.bank_schema import get_bank_schema
from homework3.part1.schemas.transaction_schema import get_transaction_schema
from homework3.part1.schemas.user_schema import get_user_schema
from homework3.part1.schemas.account_shema import get_account_schema


DB_SCHEMAS = [
    get_bank_schema(),
    get_transaction_schema(),
    get_user_schema(),
    get_account_schema(),
]
