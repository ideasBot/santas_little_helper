import re
from playwright.sync_api import Playwright, sync_playwright, TimeoutError, expect
from typing import Any
from enum import Enum
from bs4 import BeautifulSoup, Tag
from agno.tools import tool
from pydantic import BaseModel
from decimal import Decimal


class SeatType(str, Enum):
    economy = "economy"
    premium_economy = "premium-economy"
    business = "business"
    first = "first"

    def convert_to_code(self) -> str:
        mapping = {
            "economy": "Y",
            "premium-economy": "S",
            "business": "C",
            "first": "F",
        }
        return mapping[self.value]


class FlightData(BaseModel):
    carrier: str
    flight_number_and_model: str
    departure_airport: str
    departure_time: str
    arrival_airport: str
    arrival_time: str
    flight_duration: str
    currency: str
    price: Decimal


def _construct_base_url(
    from_airport_code: str,
    to_airport_code: str,
    departure_date: str,
    is_round_trip: bool = False,
    return_date: str = None,
    seat_type: SeatType = SeatType.economy,
    adult_count: int = 1,
    child_count: int = 0,
) -> str:
    base_url = "https://www.hopegoo.com/en-US/iflight/"
    trip_type = "1" if is_round_trip else "0"
    travel_class = seat_type.convert_to_code()
    unused_bit = "1"
    if is_round_trip and return_date is None:
        raise ValueError("Return date must be provided for round trip flights.")
    if is_round_trip:
        url = f"{base_url}{from_airport_code.lower()}-{to_airport_code.lower()}?para={trip_type}*{from_airport_code}*{to_airport_code}*{departure_date}*{return_date}*{travel_class}*{adult_count}*{child_count}*{unused_bit}"
    else:
        url = f"{base_url}{from_airport_code.lower()}-{to_airport_code.lower()}?para={trip_type}*{from_airport_code}*{to_airport_code}*{departure_date}**{travel_class}*{adult_count}*{child_count}*{unused_bit}"
    url += "&refid=2000401679"
    return url


def _retrieve_pricing_data_core(
    _playwright: Playwright,
    hopegoo_url: str,
) -> Any:
    browser = _playwright.firefox.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        page.goto(hopegoo_url, wait_until="networkidle", timeout=30000)
    except TimeoutError:
        pass
    expect(page.get_by_role("progressbar")).to_be_hidden()

    return page.content()


def _canonicalize_string(s: str) -> str:
    s = s.strip()
    s = re.sub(r"[\n\r]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s


def _parse_single_price(pricing: Tag) -> FlightData:
    carrier = _canonicalize_string(pricing.ul.dl.dt.text)
    flight_number_and_model = _canonicalize_string(pricing.ul.dl.dd.text)
    departure_info = pricing.ul.div.find_all("div")[0]
    arrival_info = pricing.ul.div.find_all("div")[2]

    return FlightData(
        carrier=carrier,
        flight_number_and_model=flight_number_and_model,
        departure_time=_canonicalize_string(departure_info.find_all("p")[0].text),
        departure_airport=_canonicalize_string(departure_info.find_all("p")[1].text),
        arrival_time=_canonicalize_string(arrival_info.find_all("p")[0].text),
        arrival_airport=_canonicalize_string(arrival_info.find_all("p")[1].text),
        flight_duration=_canonicalize_string(pricing.ul.p.text),
        currency=_canonicalize_string(
            pricing.ul.find_all("div", recursive=False)[1].div.em.text
        ),
        price=_canonicalize_string(
            pricing.ul.find_all("div", recursive=False)[1].div.span.text.replace(
                ",", ""
            )
        ),
    )


def _parse_pricing_data_from_html(html_content: str) -> Any:
    result = []
    html = BeautifulSoup(html_content, "html.parser")

    filter = html.find_all(string="Filter")[0]
    pricing_section = filter.parent.parent.parent.parent.find_all("section")[1].div
    for pricing in pricing_section.children:
        if not isinstance(pricing, Tag):
            continue

        result.append(_parse_single_price(pricing))

    return result

@tool()
def advanced_search_flight(
    from_airport_code: str,
    to_airport_code: str,
    departure_date: str,
    is_round_trip: bool = False,
    return_date: str = None,
    seat_type: SeatType = SeatType.economy,
    adult_count: int = 1,
    child_count: int = 0,
):
    """
    Perform an advanced flight search from HopeGoo.
    Args:
        from_airport_code (str): IATA code of the departure airport.
        to_airport_code (str): IATA code of the destination airport.
        departure_date (str): Departure date in 'YYYY-MM-DD' format.
        is_round_trip (bool): Whether the trip is round trip. Default is False.
        return_date (str): Return date in 'YYYY-MM-DD' format. Required if is_round_trip is True.
        seat_type (SeatType): Type of seat. Default is economy.
        adult_count (int): Number of adult passengers. Default is 1.
        child_count (int): Number of child passengers. Default is 0.
    """
    hopegoo_url = _construct_base_url(
        from_airport_code,
        to_airport_code,
        departure_date,
        is_round_trip,
        return_date,
        seat_type,
        adult_count,
        child_count,
    )
    with sync_playwright() as playwright:
        pricing_html = _retrieve_pricing_data_core(playwright, hopegoo_url)
        pricing_data = _parse_pricing_data_from_html(pricing_html)
        return pricing_data


if __name__ == "__main__":
    # playwright_advanced_search("SIN", "PEK", "2026-01-02")
    ...
