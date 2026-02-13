import requests

parameters = {
    "amount": 10,
    "type": "boolean",
    "category": 18
}

try:
    response = requests.get("https://opentdb.com/api.php", params=parameters)
    response.raise_for_status()
except:
    question_data = []
    quit()
else:
    question_data = response.json()["results"]
