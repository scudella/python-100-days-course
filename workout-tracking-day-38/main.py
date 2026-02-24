import datetime
import requests
from requests.auth import HTTPBasicAuth
import os

user_input = input("Tell me which exercises you did: ")
print(user_input)

nutrition_url = "https://app.100daysofpython.dev"

my_query = {
    "query": user_input,
}

APP_ID = os.environ.get("APP_ID")
APP_KEY = os.environ.get("APP_KEY")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY
}

response = requests.post(f"{nutrition_url}/v1/nutrition/natural/exercise", json=my_query, headers=headers)
print(response.json())

sheety_url = os.environ.get("SHEETY_URL")

date_now = datetime.datetime.now()

workout = {
    "workout": {
        "date": date_now.strftime("%d/%m/%Y"),
        "time": date_now.strftime("%H:%M:%S"),
        "exercise": response.json()["exercises"][0]["name"].title(),
        "duration": response.json()["exercises"][0]["duration_min"],
        "calories": response.json()["exercises"][0]["nf_calories"]
    }
}
print(workout)

sheety_user = os.environ.get("SHEETY_USER")
sheety_pass = os.environ.get("SHEETY_PASS")

basic = HTTPBasicAuth(sheety_user, sheety_pass)

headers = {
    "content-type": "application/json",
}

try:
    response_sheety = requests.post(url=sheety_url, json=workout, headers=headers, auth=basic)
    response_sheety.raise_for_status()
except requests.exceptions.HTTPError as error:
    print(error)
else:
    print(response_sheety.json())

all_sheets = requests.get(f"{sheety_url}", auth=basic)
print(all_sheets.json())
