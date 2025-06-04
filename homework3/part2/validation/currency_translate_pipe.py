import re
from homework3.part2.error_handler import message_handler


def translate_pipe(from_currency, to_currency, amount):
    """
    description:
    check currency on code valid, and amount positive number

    :param from_currency: from the currency will be converted
    :param to_currency: currency to be converted
    :param amount: amount of money

    :return: validated data
    """

    pattern = r'^[A-Z]{3}$'
    if not re.match(pattern, from_currency.upper()) or not re.match(pattern, to_currency.upper()):
        raise message_handler(400, "Invalid currency code, must contain 3 letters")

    return {
        "amount": amount,
        "to_currency": to_currency,
        "from_currency": from_currency,
    }
