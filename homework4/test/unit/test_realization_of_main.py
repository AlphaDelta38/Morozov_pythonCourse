from constants import USERS, get_accounts, BANKS, TRANSACTIONS, SIDE_EFFECT_TRANSACTIONS_INFORMATION_BY_USER
from homework3.part1.constants import DISCOUNT
from unittest.mock import patch
import pytest
from homework3.part1.realization_of_main import (
    get_transaction_information_by_user,
    get_most_bank_by_capital_using,
    get_random_discount_for_users,
    get_bank_with_oldest_client,
    get_users_with_debts
)


@patch("homework3.part1.realization_of_main.api_controller")
def test_get_random_discount_for_users(mock_api_controller):
    mock_api_controller.return_value = {"response": USERS}
    result = get_random_discount_for_users()
    for user in result:
        if not user.get("discount") or not user["discount"] in DISCOUNT:
            assert False


@patch("homework3.part1.realization_of_main.api_controller", side_effect=[
    {"response": get_accounts(-100)}, {"response": USERS}
])
def test_get_users_with_debts(mock_api_controller):
    result = get_users_with_debts()
    expected = ["Alice Johnson", "Bob Smith"]
    assert result == expected


@patch("homework3.part1.realization_of_main.api_controller", side_effect=[
    {"response": get_accounts(100, 2)},
    {"response": 100},{"response": 200}, {"response": 300}, {"response": 400},
    {"response": BANKS[1]}
])
def test_get_most_bank_by_capital_using(mock_api_controller):
    result = get_most_bank_by_capital_using()
    expected = BANKS[1]["name"]
    assert result == expected


@patch("homework3.part1.realization_of_main.api_controller", side_effect=[
    {"response": [*USERS, {'id': 3, 'name': 'Bob', 'surname': 'Smith', 'birth_day': '1985-11-23', 'accounts': None}]},
    {"response": [get_accounts(100,)[1],
        {
            'id': 3, 'user_id': 3, 'type': 'credit', 'account_number': 'ID--X-3-QwL9e70966',
            'bank_id': 3,'currency': 'USD', 'amount': 1, 'status': 'gold'
         }
    ]},
    {"response": [BANKS[1], {"id": 3, "name": "BANK16"}]},
])
def test_get_bank_with_oldest_client(mock_api_controller):
    result = get_bank_with_oldest_client()
    expected = ["BANK15", "BANK16"]
    assert result == expected



@pytest.mark.parametrize("input_data, expected, side_effect", [
    ({
    "fullname": "Alice Johnson",
    "from_date": "2025/04/14",
    "to_date":  "2025/04/16",
    "user": USERS[0],
    "account": get_accounts(100)[0],
    },
    TRANSACTIONS,
    SIDE_EFFECT_TRANSACTIONS_INFORMATION_BY_USER[0],
    ),
    ({
    "fullname": "Bob Smith",
    "from_date": "2025/04/11",
    "to_date": "2025/04/12",
    "user":  USERS[1],
    "account": get_accounts(100)[1],
    },
    [],
    SIDE_EFFECT_TRANSACTIONS_INFORMATION_BY_USER[1],
    )
])
@patch("homework3.part1.realization_of_main.api_controller")
def test_get_transaction_information_by_user(mock_api_controller, input_data, expected, side_effect):
    mock_api_controller.side_effect = side_effect
    result = get_transaction_information_by_user(input_data["fullname"], input_data["from_date"], input_data["to_date"])
    assert result == expected
