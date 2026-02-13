import requests
import os
from twilio.rest import Client

api_key = os.environ.get("WEATHER_API_KEY")
account_sid = ""
auth_token = ""

weather_parameters = {
    "lat": -22.93,
    "lon": -47.07,
    "appid": api_key,
    "cnt": 4,
    "units": "metric"
}

try:
    response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=weather_parameters)
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
else:
    print(response.status_code)
    weather_data = response.json()
    is_raining = False
    for daily in weather_data["list"]:
        for three_hour_forecast in daily["weather"]:
            if int(three_hour_forecast["id"]) < 700:
                is_raining = True
    if is_raining:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body = "It's going to rain today. Remember to bring an umbrella",
            from_ = "+13337777777",
            to = "+5519988884444"
        )

        print(message.status)
