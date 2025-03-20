"""
This script defines a class to interact with a faucet for claiming tokens for a given ERC20 address.
It reads the faucet URL from an environment variable and sends POST requests to the faucet
with the specified address. The response is checked for success or failure, and appropriate
messages are printed based on the response.
Modules:
    os: Provides a way of using operating system dependent functionality.
    requests: Allows sending HTTP requests.
    dotenv: Loads environment variables from a .env file.
Classes:
    MonadFaucet: A class to handle the interaction with the Monad faucet.
Functions:
    MonadFaucet.claim(address): Sends a POST request to the faucet with the given address and handles
    the response.

Variables:
    FAUCET_NAME (str): The name of the faucet.
    TICKER (str): The token ticker symbol.
    FAUCET_URL (str): The URL of the faucet to send requests to, read from an environment variable.
Exceptions:
    requests.exceptions.RequestException: Handles exceptions related to HTTP requests.
Response Codes:
    200: Indicates a successful claim.
    Other: Indicates a failure, and the script will print the failure message.
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()


class MonadFaucet:
    FAUCET_NAME = "Monad"
    TICKER = "MON"
    FAUCET_URL = os.getenv("MONAD_FAUCET_URL")

    def claim(self, address) -> bool:
        payload = {
            "address": address,
            # "token": os.getenv("CAPTCHA_TOKEN"), # Required reCAPTCHA token
        }

        response = requests.post(self.FAUCET_URL, json=payload, timeout=10)

        # TODO: TEST SUCCESSFUL CLAIM
        # response = type(
        #     "Response",
        #     (object,),
        #     {
        #         "status_code": 200,
        #         "headers": {"Content-Type": "application/json"},
        #         "json": lambda _: {"message": "Success"},
        #         "text": '{"message": "Success"}',
        #     },
        # )()

        # TODO: TEST FAILED CLAIM
        # response = type(
        #     "Response",
        #     (object,),
        #     {
        #         "status_code": 400,
        #         "headers": {"Content-Type": "application/json"},
        #         "json": lambda _: {"message": "Failed"},
        #         "text": '{"message": "Failed"}',
        #     },
        # )()

        success = response.status_code == 200
        if success:
            print(f"Success: Address {address} processed on {self.FAUCET_NAME} faucet")
        else:
            if response.headers.get("Content-Type") == "application/json":
                print(
                    f"Failed: Address {address} on {self.FAUCET_NAME}"
                    " - "
                    f"Status: {response.status_code}, Response: {response.json()}"
                )
            else:
                print(
                    f"Failed: Address {address} on {self.FAUCET_NAME}"
                    " - "
                    f"Status: {response.status_code}, Response: {response.text}"
                )
        return success
