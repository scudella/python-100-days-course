from datetime import datetime, date
import requests

USERNAME = ""
TOKEN = ""

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

# response = requests.post(url=pixela_endpoint, json=user_params)
# response.raise_for_status()

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {
    "id": "graph1",
    "name": "Cycling Graph",
    "unit": "Km",
    "type": "float",
    "color": "ajisai"
}

headers = {
    "X-USER-TOKEN": TOKEN,
}

# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)
# my_date = str(date(2026, 2, 19))
# date = my_date.replace("-", "")
# print(date)

today = datetime.now()

pixels_config = {
    "date": today.strftime("%Y%m%d"),
    "quantity": "8",
}
pixel_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/graph1"

# pixel_response = requests.post(pixel_endpoint, json=pixels_config, headers=headers)
# print(pixel_response.json())

update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/graph1/{today.strftime('%Y%m%d')}"

new_pixel_data = {
    "quantity": "5",
}

# response = requests.put(update_endpoint, headers=headers, json=new_pixel_data)
# print(response.text)

delete_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/graph1/{today.strftime('%Y%m%d')}"

response = requests.delete(delete_endpoint, headers=headers)
print(response.text)
