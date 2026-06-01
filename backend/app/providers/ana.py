from __future__ import annotations

from typing import List

from ..schemas import FlightOffer
from .base import Provider


class ANAProvider(Provider):
    program = "ana"
    program_name = "ANA Mileage Club"
    alliance = "Star Alliance"
    implementation = "launcher"
    notes = "Launches ANA partner award search (login required)."

    async def search(self, client, origin, destination, depart_date, cabin, passengers) -> List[FlightOffer]:
        return []

    def deep_link(self, origin, destination, depart_date, cabin, passengers):
        return (
            "https://aswbe-i.ana.co.jp/international_asr/award_search_input?"
            f"WAYTYPE=2&DEPARTURE_DATE_FW={depart_date.strftime('%Y%m%d')}"
            f"&DEPARTURE_AIRPORT_FW={origin}&ARRIVAL_AIRPORT_FW={destination}"
            f"&NUM_ADT={passengers}&LANG=en"
        )
