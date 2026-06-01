from __future__ import annotations

from typing import List

from ..schemas import FlightOffer
from .base import Provider


class AmericanProvider(Provider):
    program = "aa"
    program_name = "American AAdvantage"
    alliance = "Oneworld"
    implementation = "launcher"
    notes = "Launches aa.com award search with route pre-filled."

    async def search(self, client, origin, destination, depart_date, cabin, passengers) -> List[FlightOffer]:
        return []

    def deep_link(self, origin, destination, depart_date, cabin, passengers):
        cabin_q = {"economy": "COACH", "premium_economy": "PREMIUM_ECONOMY", "business": "BUSINESS", "first": "FIRST"}.get(cabin, "COACH")
        return (
            "https://www.aa.com/booking/find-flights?"
            f"tripType=oneWay&adult={passengers}&cabin={cabin_q}&awardBooking=true"
            f"&segments[0].origin={origin}&segments[0].destination={destination}"
            f"&segments[0].travelDate={depart_date.isoformat()}"
        )
