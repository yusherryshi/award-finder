from __future__ import annotations

from typing import List

from ..schemas import FlightOffer
from .base import Provider


class FlyingBlueProvider(Provider):
    program = "flying_blue"
    program_name = "Air France/KLM Flying Blue"
    alliance = "SkyTeam"
    implementation = "launcher"
    notes = "Launches Flying Blue award search with route pre-filled."

    async def search(self, client, origin, destination, depart_date, cabin, passengers) -> List[FlightOffer]:
        return []

    def deep_link(self, origin, destination, depart_date, cabin, passengers):
        cabin_q = {"economy": "ECONOMY", "premium_economy": "PREMIUM", "business": "BUSINESS", "first": "FIRST"}.get(cabin, "ECONOMY")
        return (
            "https://wwws.airfrance.us/search/offers?"
            f"bookingFlow=REWARD&tripType=ONE_WAY"
            f"&origin.0={origin}&destination.0={destination}&date.0={depart_date.isoformat()}"
            f"&pax.adt={passengers}&cabin={cabin_q}"
        )
