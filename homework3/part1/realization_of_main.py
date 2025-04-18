from constants import DISCOUNT, USER_BIRTHDAY_FORMAT, DATE_FORMAT, TRANSACTION_DATETIME_FORMAT
from homework3.utils import get_milliseconds_from_date, clean_text
from homework3.part2.API.api_controller import api_controller
from homework3.part2.API.api_constants_endpoints import (
    USER_ENV_CREATE_ENDPOINT,
    USER_GET_ALL_ENDPOINT,
    USER_GET_ONE_ENDPOINT,
    ACCOUNT_ENV_CREATE_ENDPOINT,
    ACCOUNT_GET_ALL_ENDPOINT,
    ACCOUNT_GET_ONE_ENDPOINT,
    BANK_ENV_CREATE_ENDPOINT,
    BANK_GET_ONE_ENDPOINT,
    BANK_GET_ALL_ENDPOINT,
    CURRENCY_TRANSLATE_ENDPOINT,
    TRANSACTION_GET_ALL_ENDPOINT,
)
import random
import time


def load_data_from_csv():
    """
    description:
    fill db from csv file, take path from constant PATHS, and send request to create records
    for each row in csv

    :return: --> void
    """

    PATHS = [
            (USER_ENV_CREATE_ENDPOINT, r"D:\pythonLabs\Morozov_pythonCourse\homework3\users.csv"),
            (ACCOUNT_ENV_CREATE_ENDPOINT, r"D:\pythonLabs\Morozov_pythonCourse\homework3\accounts.csv"),
            (BANK_ENV_CREATE_ENDPOINT, r"D:\pythonLabs\Morozov_pythonCourse\homework3\banks.csv")
    ]

    for csv in PATHS:
        api_controller(csv[0], {"csv_file_path": csv[1]})


def get_random_discount_for_users():
    """
    description:
    takes random amount of users, and give them random discount in range 25,30,50

    :return: --> user data with additional field (discount)
    """

    users = api_controller(USER_GET_ALL_ENDPOINT,{
        "limit": random.randint(1, 10)
    })["response"]

    for user in users:
        random_discount = random.choice(DISCOUNT)
        user.update({"discount": random_discount})

    return users


def get_users_with_debts():
    """
    description:
    check all user on thei amount in account which < 0

    :return: --> user with debts
    """

    debt_accounts = api_controller(ACCOUNT_GET_ALL_ENDPOINT,{
        "condition": "amount < 0"
    })["response"]

    user_ids = [str(account["user_id"]) for account in debt_accounts]

    users = api_controller(USER_GET_ALL_ENDPOINT,{
        "condition": f"id IN ({", ".join(user_ids)})"
    })["response"]

    return [f"{user["name"]} {user["surname"]}" for user in users]


def get_most_bank_by_capital_using():
    """
    description:
    get account each banks, and transform money to USD,
    after calculate sum money on accounts

    :return: --> name of bank ,with most capital using
    """

    accounts = api_controller(ACCOUNT_GET_ALL_ENDPOINT,{})["response"]

    bank_sums = {}
    for account in accounts:
        amount_in_usd = api_controller(CURRENCY_TRANSLATE_ENDPOINT,{
            "amount": account["amount"],
            "to_currency": "USD",
            "from_currency": account["currency"],
        })["response"]

        bank_id = account["bank_id"]
        if bank_id in bank_sums:
            bank_sums[bank_id] = bank_sums[bank_id] + amount_in_usd
        else:
            bank_sums[bank_id] = account["amount"]
        time.sleep(4)

        bank_id_of_max = max(bank_sums, key=bank_sums.get)

        bank_with_max_capital = api_controller(BANK_GET_ONE_ENDPOINT,
        {"condition": f"id = {bank_id_of_max}"})["response"]

        return bank_with_max_capital["name"]


def get_bank_with_oldest_client():
    """
    description:
    comprasion bith_day of users, and definition oldest users, and after getting bank name by user id

    :return: --> banks name with oldest client
    """

    users = api_controller(USER_GET_ALL_ENDPOINT,{})["response"]
    oldest_users = []

    max_age = 0
    for user in users:
        user_age_in_milliseconds = get_milliseconds_from_date(user["birth_day"], USER_BIRTHDAY_FORMAT)

        if user_age_in_milliseconds > max_age:
            max_age = user_age_in_milliseconds
            oldest_users.clear()
            oldest_users.append(str(user["id"]))
        elif user_age_in_milliseconds == max_age:
            oldest_users.append(str(user["id"]))

    accounts = api_controller(ACCOUNT_GET_ALL_ENDPOINT, {
        "condition": f"user_id IN ({", ".join(oldest_users)})"
    })["response"]

    banks = api_controller(BANK_GET_ALL_ENDPOINT, {
        "condition": f"id IN ({", ".join([str(account["bank_id"]) for account in accounts])})"
    })["response"]

    return [bank["name"] for bank in banks]


def get_highest_number_of_unique_user_bank():
    """
    description:
    check each transactions on unique user name, after link with bank name, after
    calculate len of unique users each bank

    :return: --> bank name of highest number of unique users
    """

    transactions = api_controller(TRANSACTION_GET_ALL_ENDPOINT, {})["response"]
    bank_and_users_id = {}

    for transaction in transactions:
        sender_bank = transaction["bank_sender_name"]
        if sender_bank in bank_and_users_id:
            bank_and_users_id[sender_bank].append(transaction["account_sender_id"])
        else:
            bank_and_users_id[sender_bank] = [transaction["account_sender_id"]]

    return max(bank_and_users_id, key=lambda user_ids: len(user_ids))


def get_transaction_information_by_user(fullname, from_date, to_date):
    """
    description:
    get all transactions user, and check diapason from (from_date) to (to_date)
    and return transaction information in this diapason

    :return: --> transactions data
    """

    name, surname = clean_text(fullname).split(" ")
    user = api_controller(USER_GET_ONE_ENDPOINT, {
        "condition": f"name = \"{name}\" AND surname = \"{surname}\""
    })["response"]

    if not user:
        return []

    account = api_controller(ACCOUNT_GET_ONE_ENDPOINT, {
        "condition": f"user_id = {user['id']}"
    })["response"]

    if not account:
        return []

    transactions = api_controller(TRANSACTION_GET_ALL_ENDPOINT, {
        "condition": f"account_sender_id = {account['id']} or account_receiver_id = {account["id"]}"
    })["response"]

    from_date = get_milliseconds_from_date(from_date, DATE_FORMAT)
    to_date = get_milliseconds_from_date(to_date, DATE_FORMAT)

    return [transaction for transaction in transactions \
            if from_date >= get_milliseconds_from_date(transaction["datetime"], TRANSACTION_DATETIME_FORMAT) >= to_date
            ]
