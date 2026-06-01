from __future__ import annotations

from typing import List

from ..schemas import FlightOffer
from .base import Provider


class TurkishProvider(Provider):
    program = "turkish"
    program_name = "Turkish Miles&Smiles"
    alliance = "Star Alliance"
    implementation = "launcher"
    notes = "Launches Turkish Miles&Smiles award search with route pre-filled."

    async def search(self, client, origin, destination, depart_date, cabin, passengers) -> List[FlightOffer]:
        return []

    def deep_link(self, origin, destination, depart_date, cabin, passengers):
        cabin_q = {"economy": "ECONOMY", "premium_economy": "ECONOMY", "business": "BUSINESS", "first": "BUSINESS"}.get(cabin, "ECONOMY")
        return (
            "https://www.turkishairlines.com/en-int/flights/booking/?"
            f"awardTicket=true&tripType=oneWay&origin={origin}&destination={destination}"
            f"&departureDate={depart_date.isoformat()}&passengerAdult={passengers}&cabin={cabin_q}"
        )
