
def error_handler(status, message):
    """"
    description:
    take status, and message for throw error

    :param status: status code of error
    :param message: message of error

    :return: --> void
    """

    raise ValueError({"status": status, "message": message})