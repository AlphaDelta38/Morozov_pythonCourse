from homework3.part2.API.api_constants_endpoints import (
    ACCOUNT_ENV_CREATE_ENDPOINT,
    USER_ENV_CREATE_ENDPOINT,
    BANK_ENV_CREATE_ENDPOINT,
)


# // get_random_discount_for_users // #
DISCOUNT = (25, 30, 50)

# // get_bank_with_oldest_client // #
USER_BIRTHDAY_FORMAT = "%Y-%m-%d"

# // get_transaction_information_by_user // #
DATE_FORMAT = "%Y/%m/%d"
TRANSACTION_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# // paths of endpoint and csv files,  for fill base by csv // #
PATHS = [
    (USER_ENV_CREATE_ENDPOINT, r"D:\pythonLabs\Morozov_pythonCourse\homework3\users.csv"),
    (ACCOUNT_ENV_CREATE_ENDPOINT, r"D:\pythonLabs\Morozov_pythonCourse\homework3\accounts.csv"),
    (BANK_ENV_CREATE_ENDPOINT, r"D:\pythonLabs\Morozov_pythonCourse\homework3\banks.csv")
]