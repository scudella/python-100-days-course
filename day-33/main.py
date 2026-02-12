import requests
from datetime import datetime

LATITUDE = -22.9056
LONGITUDE = -47.0608

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

longitude = float(response.json()["iss_position"]["longitude"])
latitude = float(response.json()["iss_position"]["latitude"])

iss_position = (longitude, latitude)
print(iss_position)

parameters = {
    "lat": LATITUDE,
    "lng": LONGITUDE,
    "formatted": 0,
    "tzid": "America/Sao_Paulo",
}

response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()

sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
print(sunrise)
print(sunset)

now = datetime.now()
print(now.hour)