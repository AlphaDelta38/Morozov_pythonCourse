from homework3.part2.error_handler import message_handler
from homework3.utils import clean_text, is_valid_date


def user_pipe(**user_data):
    """
    description:
    validate user data, split full name, also check id on type int,
    and also check valid birth_day

    :param user_data: user data

    :return: validated data
    """

    user_full_name = clean_text(user_data["user_full_name"])

    if "id" in user_data and not isinstance(user_data["id"], int):
        raise message_handler(400, "fullname must contain two words")

    if len(user_full_name.split(" ")) > 2:
        raise message_handler(400, "fullname must contain two words")

    if "birth_day" in user_data and not is_valid_date(user_data["birth_day"], "%Y-%m-%d"):
        raise message_handler(400, "birth_day must be such as format YY-MM-DD")

    validated = {
        "name": user_full_name.split(" ")[0],
        "surname": user_full_name.split(" ")[1],
        "birth_day": user_data["birth_day"],
    }

    if "id" in user_data:
        validated["id"] = user_data["id"]

    return validated
