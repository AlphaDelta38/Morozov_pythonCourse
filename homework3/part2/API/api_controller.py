from homework3.part2.error_handler import CustomException, message_handler
from homework3.part2.API.transaction_service import TransactionService
from homework3.part2.API.currnecy_service import CurrencyService
from homework3.part2.API.account_service import AccountService
from homework3.part2.API.user_service import UserService
from homework3.part2.API.bank_service import BankService


API_PATH = {
    "transaction": TransactionService().controller,
    "currency": CurrencyService().controller,
    "account": AccountService().controller,
    "user": UserService().controller,
    "bank": BankService().controller
}


def api_controller(path, data):
    """
    description:
    take path to endpoint, and data from request,
    after transmits to necessary endpoint with dict logic,

    :param path: endpoint path
    :param data: request data

    :return: return data
    """

    try:
        service, action = path.split("/")
        return API_PATH[service](action, **data)
    except Exception as e:
        print("error", e)
        error = e if isinstance(e, CustomException) else message_handler(500, str(e))
        raise error
