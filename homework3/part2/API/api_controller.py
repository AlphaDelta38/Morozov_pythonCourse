from homework3.part2.error_handler import CustomException, message_handler
from homework3.part2.API.transaction_service import transaction_service
from homework3.part2.API.currnecy_service import currency_service
from homework3.part2.API.account_service import account_service
from homework3.part2.API.user_service import user_service
from homework3.part2.API.bank_service import bank_service


API_PATH = {
    "transaction": transaction_service(),
    "currency": currency_service(),
    "account": account_service(),
    "user": user_service(),
    "bank": bank_service()
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
        return API_PATH[service][action](**data)
    except Exception as e:
        error = e if isinstance(e, CustomException) else message_handler(500, str(e))
        raise error
