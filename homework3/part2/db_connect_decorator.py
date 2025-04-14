from homework3.part2.db_connect_controller import DBConnectController

def db_connector(func):
    """
    description:
    take func who will be wrapped,

    :param func:

    :return: --> wrapper func
    """

    def wrapper(*args, **kwargs):
        """
        description:
        open db connection with DBConnectController,
        and transmits cursor from db connection to main func, after actions close connection  and commit db.

        :param args: all positional arguments
        :param kwargs: all keyword arguments

        :return: --> response from main func
        """

        db = DBConnectController()
        cursor = db.get_cursor()

        x = func(*args, **kwargs, connector=cursor)

        db.commit()
        db.close()

        return x
    return wrapper
