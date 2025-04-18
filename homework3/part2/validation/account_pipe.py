from homework3.part2.error_handler import message_handler
import re


def account_pipe(**data):
    """
    description:
    check id on type int, check also type on Certain values,
    also validate account number by pattern, and check currency and amount on valid

    :param data: account create data

    :return: validated data
    """

    account_number_pattern = r"[a-zA-Z]{1,3}-\d+-"
    currency_pattern = r'^[A-Z]{3}$'

    if "bank_id" in data and not isinstance(data["bank_id"], int) or \
        "user_id" in data and not isinstance(data["user_id"], int) or \
        "id" in data and not isinstance(data["id"], int):
        raise message_handler(400, "id must be number")

    if "type" in data and not data["type"].lower() in ["credit", "debit"]:
        raise message_handler(400, "type must be credit or debit")

    if "account_number" in data and len(data["account_number"]) != 18:
        raise message_handler(400, f"{"many chars!" if data["account_number"] > 18 else "too little chars"}")

    if "account_number" in data and not data["account_number"].startswith("ID--"):
        raise message_handler(400, "wrong format!")

    if "account_number" in data and not re.search(account_number_pattern, data["account_number"]):
        raise message_handler(400, "broken ID!")

    if "currency" in data and not re.match(currency_pattern, data["currency"].upper()):
        raise message_handler(400, "invalid currency")

    return data
