from homework3.part2.validation.currency_translate_pipe import translate_pipe
from homework3.part2.validation_decorator import validate
from dotenv import load_dotenv
import requests
import os


load_dotenv()


def currency_service():
    """
    description:
    service which use validation decorator and pipes for validation data,
    also realize CRUD pattern

    :return: dict of methods
    """

    base_currency_api_url = f"{os.getenv("BASE_CURRENCY_API_URL")}?apikey={os.getenv("CURRENCY_API_KEY")}"

    try:
        @validate(translate_pipe)
        def translate(from_currency, to_currency, amount):
            """
            description:
            translate from one currency to different currency

            :return: --> dict with message and status code, and response
            """

            response = requests.get(f"{base_currency_api_url}&currencies={",".join([from_currency, to_currency])}").json()

            return {
                "status": 200,
                "message": "successfully deleted",
                "response": amount * (response["data"][to_currency] / response["data"][from_currency])
            }

    except Exception as e:
        return e if isinstance(e, dict) else {"status": 500, "message": str(e)}

    return {
        "translate": translate,
    }


