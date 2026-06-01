from __future__ import annotations

from typing import List

from ..schemas import FlightOffer
from .base import Provider


class LufthansaProvider(Provider):
    program = "miles_and_more"
    program_name = "Lufthansa Miles & More"
    alliance = "Star Alliance"
    implementation = "launcher"
    notes = "Launches Miles & More award search with route pre-filled."

    async def search(self, client, origin, destination, depart_date, cabin, passengers) -> List[FlightOffer]:
        return []

    def deep_link(self, origin, destination, depart_date, cabin, passengers):
        cabin_q = {"economy": "E", "premium_economy": "N", "business": "C", "first": "F"}.get(cabin, "E")
        return (
            "https://www.miles-and-more.com/online/portal/mam/award?"
            f"l=en&from0={origin}&to0={destination}&date0={depart_date.isoformat()}"
            f"&adult={passengers}&cabinClass={cabin_q}&tripType=ONE_WAY"
        )
