import holidays
import datetime
from typing import Dict
from agno.tools import tool

@tool()
def get_holidays(country_2_digit_code: str, years: int) -> str:
    """
    Get public holidays for a given country and year.

    Args:
        country_2_digit_code (str): The 2-digit country code (e.g., 'US', 'CN').
        years (int): The year for which to retrieve holidays, e.g. 2027.
    """
    country_holidays: Dict[datetime.date, str] = getattr(holidays, country_2_digit_code)(years=years)
    
    return {date.isoformat(): name for date, name in country_holidays.items()}

if __name__ == "__main__":
    print(get_holidays("CN", 2027))