from homework3.part2.error_handler import error_handler
import re


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
        error_handler(400, "Invalid currency code, must contain 3 letters")
    if amount <= 0:
        error_handler(400, "Invalid amount, must be greater than 0")

    return {
        "amount": amount,
        "to_currency": to_currency,
        "from_currency": from_currency,
    }