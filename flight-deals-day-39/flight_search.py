# This class is responsible for talking to the Flight Search API.
import requests
import os
from datetime import datetime

FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"

class FlightSearch:
    def __init__(self):
        self.base_url = "https://test.api.amadeus.com/v1"
        self.iata_code_api = "/reference-data/locations"
        self.token_endpoint= "/security/oauth2/token"

        self.api_key = os.environ.get("AMADEUS_API_KEY")
        self.api_secret = os.environ.get("AMADEUS_API_SECRET")

        self.access_token = None

    def search_iata_code(self, city_name):
        if not self.access_token:
            self.request_access_token()

        url = f"{self.base_url}{self.iata_code_api}?subType=CITY&keyword={city_name}"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            return response.json()

    def request_access_token(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        url = f"{self.base_url}{self.token_endpoint}"

        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }

        try:
            print("Requesting access token...")
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            token_data = response.json()
            self.access_token = token_data["access_token"]
            return self.access_token

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        """
        Searches for flight options between two cities on specified departure and return dates
        using the Amadeus API.
        Parameters:
            origin_city_code (str): The IATA code of the departure city.
            destination_city_code (str): The IATA code of the destination city.
            from_time (datetime): The departure date.
            to_time (datetime): The return date.
        Returns:
            dict or None: A dictionary containing flight offer data if the query is successful; None
            if there is an error.
        The function constructs a query with the flight search parameters and sends a GET request to
        the API. It handles the response, checking the status code and parsing the JSON data if the
        request is successful. If the response status code is not 200, it logs an error message and
        provides a link to the API documentation for status code details.
        """

        # print(f"Using this token to check_flights() {self._token}")
        headers = {"Authorization": f"Bearer {self.access_token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP",
            "max": "10",
        }

        response = requests.get(
            url=FLIGHT_ENDPOINT,
            headers=headers,
            params=query,
        )

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        return response.json()



