from agno.tools import tool
from httpx import Client
from enum import Enum
from src.utils.settings import settings

class TravelClass(str, Enum):
    economy = "economy"
    premium_economy = "premium_economy"
    business = "business"
    first = "first"
    
    def to_int_value(self):
        if self == TravelClass.economy:
            return 1
        elif self == TravelClass.premium_economy:
            return 2
        elif self == TravelClass.business:
            return 3
        elif self == TravelClass.first:
            return 4
        else:
            raise ValueError("Invalid travel class")

@tool()
def advanced_search_flight(
    from_airport_code: str,
    to_airport_code: str,
    departure_date: str,
    is_round_trip: bool = False,
    return_date: str = None,
    seat_type: TravelClass = TravelClass.economy,
    adult_count: int = 1,
    child_count: int = 0,
    currency: str = "CNY",
):
    """
    Perform an advanced flight search from Google Flight.
    Args:
        from_airport_code (str): IATA code of the departure airport, e.g. SIN.
        to_airport_code (str): IATA code of the destination airport, e.g. PEK.
        departure_date (str): Departure date in 'YYYY-MM-DD' format.
        is_round_trip (bool): Whether the trip is round trip. Default is False.
        return_date (str): Return date in 'YYYY-MM-DD' format. Required if is_round_trip is True.
        seat_type (TravelClass): Travel class. Default is economy.
        adult_count (int): Number of adults. Default is 1.
        child_count (int): Number of children. Default is 0.
        currency (str): Currency code for pricing. Default is "CNY".
    Returns:
        dict: JSON response containing flight search results.
    """
    base_url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_flights",
        "departure_id": from_airport_code,
        "arrival_id": to_airport_code,
        "gl": "sg",
        "hl": "en",
        "currency": currency,
        "type": 1 if is_round_trip else 2,
        "outbound_date": departure_date,
        "return_date": return_date if is_round_trip else "",
        "travel_class": seat_type.to_int_value(),
        "adults": adult_count,
        "children": child_count,
        "deep_search": "true",
        "api_key": settings.serpapi_api_key,
    }
    
    client = Client()
    
    response = client.get(base_url, params=params, timeout=300)
    
    data = response.json()
    return data

if __name__ == "__main__":
    ...