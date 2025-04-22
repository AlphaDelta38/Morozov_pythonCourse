import argparse
from realization_of_main import (
    get_random_discount_for_users,
    get_users_with_debts,
    get_most_bank_by_capital_using,
    get_bank_with_oldest_client,
    get_highest_number_of_unique_user_bank,
    get_transaction_information_by_user
)
from initial_db_setup import initial_db_setup
from homework3.part2.error_handler import CustomException, message_handler
from homework3.logger import get_logger


logger = get_logger()


def main():
    """
    description:
    setup database, and manage API through API controller

    :return: --> void
    """

    args = parse_args()

    try:
        if args.initial_db_flag:
            initial_db_setup(args.unique_user_fullname)
            logger.info("Initial database setup complete")

        print(get_random_discount_for_users())
        logger.info("random discount calculation complete")

        print(get_users_with_debts())
        logger.info("users with debt successful received")

        print(get_most_bank_by_capital_using())
        logger.info("banks with most capital using received")

        print(get_bank_with_oldest_client())
        logger.info("oldest client has been received")

        print(get_highest_number_of_unique_user_bank())
        logger.info("highest unique user bank has been received")

        print(get_transaction_information_by_user("Charlie Evans", "2025/03/11", "2025/04/16"))
        logger.info("information about transaction received")

    except Exception as e:
        error = e if isinstance(e, CustomException) else message_handler(500, str(e)).data
        logger.error(error)
        print(error)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--initial_db_flag", required=False, default=False,
                        help="initial flag which allow to initialize database")
    parser.add_argument("--unique_user_fullname", required=False, default=True,
                        help="turn off if flag is false, default True")

    return parser.parse_args()


if __name__ == '__main__':
    main()
