import requests
from datetime import datetime
import smtplib
import time

LATITUDE = -22.9056
LONGITUDE = -47.0608

sunrise_day = 0
sunrise = 0
sunset = 0

my_email = "test@gmail.com"
password = ""
to_email = "test@hotmail.com"

def iss_position():
    try:
        response = requests.get(url="http://api.open-notify.org/iss-now.json")
        response.raise_for_status()
    except:
        print("Iss not available")
        return (0, 0)
    else:
        data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    iss_position = (iss_latitude, iss_longitude)
    print(iss_position)
    return iss_position


def is_ISS_close_to_my_position(position):
    # Your position is within +5 or -5 degrees of the ISS position.
    iss_latitude = position[0]
    iss_longitude = position[1]
    if LATITUDE - 5 <= iss_latitude <= LATITUDE + 5 and LONGITUDE - 5 <= iss_longitude <= LONGITUDE + 5:
        print("ISS is in a close position")
        return True

def is_dark(sunrise, sunset):
    time_now = datetime.now()
    print(time_now.hour)
    if 0 <= time_now.hour <= sunrise or time_now.hour >= sunset:
        print("is dark now")
        return True


def sunrise_sunset():
    parameters = {
        "lat": LATITUDE,
        "lng": LONGITUDE,
        "formatted": 0,
        "tzid": "America/Sao_Paulo",
    }

    today = datetime.now().day
    global sunrise_day
    global sunrise, sunset
    if today == sunrise_day:
        return {"sunrise": sunrise, "sunset": sunset}

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    print(f"new day: {data}")
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunrise_day = int(data["results"]["sunrise"].split("T")[0].split("-")[2])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    return {"sunrise": sunrise, "sunset": sunset}

def send_iss_email():
    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=to_email,
            msg=f"Subject: ISS Overhead !!!\n\n LOOK UP: time: {datetime.now()}" )


def check_for_position_and_time():
    iss_lat_long = iss_position()

    hours = sunrise_sunset()

    # If the ISS is close to my current position
    # and it is currently dark
    if is_ISS_close_to_my_position(iss_lat_long) and is_dark(hours["sunrise"], hours["sunset"]):
        # Then send me an email to tell me to look up.
        send_iss_email()


# BONUS: run the code every 60 seconds.

def main():
    print(f"Function called at: {time.ctime()}")
    check_for_position_and_time()

print("Starting the 60-second loop...")
while True:
    main()
    time.sleep(60) # Wait for 60 seconds
