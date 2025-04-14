from homework3.part2.error_handler import error_handler


def bank_pipe(data):
    """
    description:
    check name on max length

    :param data: bank create data

    :return: validated data
    """

    if "name" in data and len(data["name"]) > 255:
        error_handler(400, "name too long must be less than 255 characters")

    return data

