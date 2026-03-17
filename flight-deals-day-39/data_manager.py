import os
import requests
from requests.auth import HTTPBasicAuth


# This class is responsible for talking to the Google Sheet.
class DataManager:
    def __init__(self):
        self.sheety_url = os.environ.get("SHEETY_URL")
        self.sheety_user = os.environ.get("SHEETY_USER")
        self.sheety_pass = os.environ.get("SHEETY_PASS")
        self.basic = HTTPBasicAuth(self.sheety_user, self.sheety_pass)
        self.headers = {
            "content-type": "application/json",
        }




# date_now = datetime.datetime.now()


    def set_iata_code(self, iata_code, id):
        price = {
            "price": {
                "iataCode": iata_code,
            }
        }

        sheety_user = os.environ.get("SHEETY_USER")
        sheety_pass = os.environ.get("SHEETY_PASS")

        basic = HTTPBasicAuth(sheety_user, sheety_pass)

        headers = {
            "content-type": "application/json",
        }

        try:
            update_url = f"{self.sheety_url}/{id}"
            response_sheety = requests.put(url=update_url, json=price , headers=headers, auth=basic)
            response_sheety.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(error)
        else:
            print(response_sheety.json())
            return response_sheety.json()

    def get_all_flights(self):
        try:
            response_sheety = requests.get(url=self.sheety_url, headers=self.headers, auth=self.basic)
            response_sheety.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(error)
        else:
            return response_sheety.json()