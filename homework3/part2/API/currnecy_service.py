from homework3.part2.validation.currency_translate_pipe import translate_pipe
from homework3.part2.API.service_controller import ServiceController
from homework3.part2.validation_decorator import validate
from homework3.part2.error_handler import message_handler
from dotenv import load_dotenv
import requests
import os


load_dotenv()
base_currency_api_url = f"{os.getenv("BASE_CURRENCY_API_URL")}?apikey={os.getenv("CURRENCY_API_KEY")}"


class CurrencyService(ServiceController):
    """
    description:
    service which use validation decorator and pipes for validation data,
    also realize CRUD pattern

    """

    @staticmethod
    @validate(translate_pipe)
    def translate(data):
        """
        description:
        translate from one currency to different currency
        :return: --> dict with message and status code, and response
        """

        amount, to_currency, from_currency = data.values()
        response = requests.get(f"{base_currency_api_url}&currencies={",".join([from_currency, to_currency])}").json()

        return message_handler(
            200,
            "successfully deleted",
            amount * (response["data"][to_currency] / response["data"][from_currency])
        ).data
