USERS = [
    {'id': 1, 'name': 'Alice', 'surname': 'Johnson', 'birth_day': '1990-04-12', 'accounts': None},
    {'id': 2, 'name': 'Bob', 'surname': 'Smith', 'birth_day': '1985-11-23', 'accounts': None}
]


def get_accounts(x, multiplier = 1):
    return [
        {'id': 1, 'user_id': 1, 'type': 'credit', 'account_number': 'ID--j3-q-432547-u9', 'bank_id': 1,
         'currency': 'USD', 'amount': 5 * x, 'status': None},
        {'id': 2, 'user_id': 2, 'type': 'credit', 'account_number': 'ID--X-3-QwL9e70966', 'bank_id': 2,
         'currency': 'USD', 'amount': 1 * x, 'status': 'gold'}
    ] * multiplier


BANKS = [
    {"id": 1, "name": "BANK03"},
    {"id": 2, "name": "BANK15"}
]

TRANSACTIONS = [
    {'id': 1, 'bank_sender_name': 'BANK03', 'account_sender_id': 4, 'bank_receiver_name': 'BANK04',
     'account_receiver_id': 5, 'sent_currency': 'USD', 'sent_amount': 100.0, 'datetime': '2025-04-15 01:04:30'},

    {'id': 2, 'bank_sender_name': 'BANK04', 'account_sender_id': 5, 'bank_receiver_name': 'BANK03',
     'account_receiver_id': 4, 'sent_currency': 'RUB', 'sent_amount': 100.0, 'datetime': '2025-04-15 01:06:06'},

    {'id': 3, 'bank_sender_name': 'BANK13', 'account_sender_id': 14, 'bank_receiver_name': 'BANK14',
     'account_receiver_id': 15, 'sent_currency': 'USD', 'sent_amount': 100.0, 'datetime': '2025-04-15 01:06:51'},

    {'id': 4, 'bank_sender_name': 'BANK04', 'account_sender_id': 14, 'bank_receiver_name': 'BANK05',
     'account_receiver_id': 15, 'sent_currency': 'USD', 'sent_amount': 100.0, 'datetime': '2025-04-15 01:06:51'},
]



# // test_get_transaction_information_by_user //

SIDE_EFFECT_TRANSACTIONS_INFORMATION_BY_USER = [
    [
        {"response": USERS[0]},
        {"response": get_accounts(100)[0]},
        {"response": TRANSACTIONS},
    ],
    [
        {"response": USERS[1]},
        {"response": get_accounts(100)[0]},
        {"response": TRANSACTIONS},
    ]
]

# // test_get_transaction_information_by_user //