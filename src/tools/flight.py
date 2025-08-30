from typing import List
from fast_flights import get_flights
from fast_flights.model import Flights
import time
from fast_flights.querying import (
    FlightQuery,
    create_query,
    SeatType,
    TripType,
    Passengers,
    Query,
)


def search_flights(
    from_airport_code: str,
    to_airport_code: str,
    date_YYYY_MM_DD: str,
    seat_class: SeatType = "economy",
    trip: TripType = "one-way",
    adult_count: int = 1,
    child_count: int = 0,
    currency: str = "CNY",
) -> list[Flights]:
    """
    Perform a flight search.
    Args:
        from_airport_code (str): code of the departure airport, e.g. HKG for Hong Kong International Airport.
        to_airport_code (str): code of the destination airport, e.g. PEK for Beijing Capital International Airport.
        date_YYYY_MM_DD (str): Date of the flight in YYYY-MM-DD format.
        seat_class (strenum, default economy): Class of the seat, "economy", "premium-economy", "business", "first".
        trip (strenum, default one-way): Type of the trip, "round-trip", "one-way", "multi-city".
        adult_count (int, optional, default 1): Number of adult passengers.
        child_count (int, optional, default 0): Number of child passengers.
        currency (str, optional, default CNY): Currency code for the prices, e.g. "CNY" for Chinese Yuan.
    Recommends:
        * Ask user for currency perferences if not provided.
    """
    query: Query = create_query(
        flights=[
            FlightQuery(
                date=date_YYYY_MM_DD,
                from_airport=from_airport_code,
                to_airport=to_airport_code,
            )
        ],
        seat=seat_class,
        trip=trip,
        passengers=Passengers(adults=adult_count, children=child_count),
        language="en",
        currency=currency,
    )

    max_tries = 5
    tries = 0
    while tries < max_tries:
        try:
            flights: List[Flights] = get_flights(query)
        except IndexError:
            tries += 1
            time.sleep(1)
            continue
        break
    else:
        raise RuntimeError("Failed to get flights after several tries.")

    return flights


if __name__ == "__main__":
    print(
        search_flights(
            from_airport_code="SIN",
            to_airport_code="OKA",
            date_YYYY_MM_DD="2025-12-25",
            seat_class="economy",
            trip="one-way",
            adult_count=1,
            child_count=0,
            currency="CNY",
        )
    )
