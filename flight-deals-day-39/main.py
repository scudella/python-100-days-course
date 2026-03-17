#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
import time
from datetime import datetime, timedelta
from flight_data import find_cheapest_flight

sheet_data = DataManager()
desirable_destinations = sheet_data.get_all_flights()

pprint(desirable_destinations)

flight_search = FlightSearch()

ORIGIN_CITY_IATA = "LON"

# Request a new token
amadeus_access_token = flight_search.request_access_token()

for destination in desirable_destinations["prices"]:
    if destination["iataCode"] == "":
        row_id = destination["id"]
        # load iata codes
        city_data = flight_search.search_iata_code(destination["city"])

        if city_data["data"]:
            iata_code = city_data["data"][0]["iataCode"]
            pprint(iata_code)
            update_destinations = sheet_data.set_iata_code(iata_code, row_id)
        else:
            print(f"No iata code found for {destination['city']}")

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in desirable_destinations["prices"]:
    print(f"Getting flights for {destination['city']}...")
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: £{cheapest_flight.price}")
    # Slowing down requests to avoid rate limit
    time.sleep(2)