from initial_db_setup import initial_db_setup
from homework3.logger import get_logger


logger = get_logger()


def main():
    """
    description:
    setup database, and manage API through API controller

    :return: --> void
    """

    try:
        initial_db_setup()
        logger.info("Initial database setup complete")


    except Exception as e:
        error = e if isinstance(e, dict) else {"status": 500, "message": str(e)}
        logger.error(error)
        print(error)


if __name__ == '__main__':
    main()
