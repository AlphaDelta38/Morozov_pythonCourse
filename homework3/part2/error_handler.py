class CustomException(Exception):
    def __init__(self, data: dict):
        self.data = data
        super().__init__(data["message"])


def message_handler(status, message, response = ()):
    """"
    description:
    take status, and message for throw error

    :param status: status code of error or success
    :param message: message of error or success
    :param response: data if massage has been successfully

    :return: --> void
    """

    return CustomException({"status":status, "message":message, "response": response})
