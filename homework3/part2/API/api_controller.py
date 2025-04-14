from transaction_service import transaction_service
from account_service import account_service
from homework3.logger import get_logger
from user_service import user_service
from bank_service import bank_service

API_PATH = {
    "user": user_service(),
    "bank": bank_service(),
    "account": account_service(),
    "transaction": transaction_service(),
}

logger = get_logger()


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
        return API_PATH[service][action](data)
    except Exception as e:
        error =  e if isinstance(e, dict) else {"status": 500, "message": str(e)}
        logger.error(error)
        return error


# api_controller("user/create", {
#     "user_full_name": "Morozovsdd Kirilddsd",
#     "birth_day": "2006/05/04",
# })

# api_controller("bank/create", {
#     "name": "Bank2"
# })

# api_controller("account/create", {
#     "user_id": 1,
#     "type": "credit",
#     "account_number": "ID--j3-q-432547-u9",
#     "bank_id": 1,
#     "currency": "USD",
#     "amount": 100,
# })

# api_controller("user/creates", r"D:\pythonLabs\Morozov_pythonCourse\homework3\users.csv")
# api_controller("account/creates", r"D:\pythonLabs\Morozov_pythonCourse\homework3\accounts.csv")
# api_controller("bank/creates", r"D:\pythonLabs\Morozov_pythonCourse\homework3\banks.csv")

# api_controller("bank/update", {"id": 2, "name": "BANK222"})
# api_controller("account/update", {"id": 3, "user_id": 4})
# api_controller("user/update", {"id": 2, "name": "BANK"})

# api_controller("bank/delete", 1)
# api_controller("account/delete", 1)
# api_controller("user/delete", 1)

# api_controller("account/transfer", {
#     "sender_account_number": 1003,
#     "receiver_account_number": 1002,
#     "amount": 100
# })