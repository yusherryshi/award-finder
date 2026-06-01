from __future__ import annotations

from typing import Dict

# Minimal airport metadata focused on transatlantic Europe <> US/Canada routes.
# Extend freely.
AIRPORTS: Dict[str, dict] = {
    # North America
    "JFK": {"city": "New York", "country": "US", "tz": "America/New_York"},
    "EWR": {"city": "Newark", "country": "US", "tz": "America/New_York"},
    "BOS": {"city": "Boston", "country": "US", "tz": "America/New_York"},
    "IAD": {"city": "Washington", "country": "US", "tz": "America/New_York"},
    "PHL": {"city": "Philadelphia", "country": "US", "tz": "America/New_York"},
    "ORD": {"city": "Chicago", "country": "US", "tz": "America/Chicago"},
    "DFW": {"city": "Dallas", "country": "US", "tz": "America/Chicago"},
    "IAH": {"city": "Houston", "country": "US", "tz": "America/Chicago"},
    "ATL": {"city": "Atlanta", "country": "US", "tz": "America/New_York"},
    "MIA": {"city": "Miami", "country": "US", "tz": "America/New_York"},
    "LAX": {"city": "Los Angeles", "country": "US", "tz": "America/Los_Angeles"},
    "SFO": {"city": "San Francisco", "country": "US", "tz": "America/Los_Angeles"},
    "SEA": {"city": "Seattle", "country": "US", "tz": "America/Los_Angeles"},
    "YYZ": {"city": "Toronto", "country": "CA", "tz": "America/Toronto"},
    "YUL": {"city": "Montreal", "country": "CA", "tz": "America/Toronto"},
    "YVR": {"city": "Vancouver", "country": "CA", "tz": "America/Vancouver"},
    # Europe
    "LHR": {"city": "London Heathrow", "country": "GB", "tz": "Europe/London"},
    "LGW": {"city": "London Gatwick", "country": "GB", "tz": "Europe/London"},
    "MAN": {"city": "Manchester", "country": "GB", "tz": "Europe/London"},
    "DUB": {"city": "Dublin", "country": "IE", "tz": "Europe/Dublin"},
    "CDG": {"city": "Paris CDG", "country": "FR", "tz": "Europe/Paris"},
    "ORY": {"city": "Paris Orly", "country": "FR", "tz": "Europe/Paris"},
    "AMS": {"city": "Amsterdam", "country": "NL", "tz": "Europe/Amsterdam"},
    "FRA": {"city": "Frankfurt", "country": "DE", "tz": "Europe/Berlin"},
    "MUC": {"city": "Munich", "country": "DE", "tz": "Europe/Berlin"},
    "ZRH": {"city": "Zurich", "country": "CH", "tz": "Europe/Zurich"},
    "GVA": {"city": "Geneva", "country": "CH", "tz": "Europe/Zurich"},
    "VIE": {"city": "Vienna", "country": "AT", "tz": "Europe/Vienna"},
    "MAD": {"city": "Madrid", "country": "ES", "tz": "Europe/Madrid"},
    "BCN": {"city": "Barcelona", "country": "ES", "tz": "Europe/Madrid"},
    "LIS": {"city": "Lisbon", "country": "PT", "tz": "Europe/Lisbon"},
    "FCO": {"city": "Rome FCO", "country": "IT", "tz": "Europe/Rome"},
    "MXP": {"city": "Milan MXP", "country": "IT", "tz": "Europe/Rome"},
    "CPH": {"city": "Copenhagen", "country": "DK", "tz": "Europe/Copenhagen"},
    "ARN": {"city": "Stockholm", "country": "SE", "tz": "Europe/Stockholm"},
    "OSL": {"city": "Oslo", "country": "NO", "tz": "Europe/Oslo"},
    "HEL": {"city": "Helsinki", "country": "FI", "tz": "Europe/Helsinki"},
    "IST": {"city": "Istanbul", "country": "TR", "tz": "Europe/Istanbul"},
    "ATH": {"city": "Athens", "country": "GR", "tz": "Europe/Athens"},
    "WAW": {"city": "Warsaw", "country": "PL", "tz": "Europe/Warsaw"},
    "PRG": {"city": "Prague", "country": "CZ", "tz": "Europe/Prague"},
    "BRU": {"city": "Brussels", "country": "BE", "tz": "Europe/Brussels"},
    "KEF": {"city": "Reykjavik", "country": "IS", "tz": "Atlantic/Reykjavik"},
}


def airport_label(iata: str) -> str:
    info = AIRPORTS.get(iata.upper())
    if not info:
        return iata.upper()
    return f"{iata.upper()} - {info['city']}"
