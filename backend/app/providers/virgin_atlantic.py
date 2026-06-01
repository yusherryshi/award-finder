from __future__ import annotations

from typing import List

from ..schemas import FlightOffer
from .base import Provider


class VirginAtlanticProvider(Provider):
    program = "virgin"
    program_name = "Virgin Atlantic Flying Club"
    alliance = "SkyTeam"
    implementation = "launcher"
    notes = "Launches Virgin Atlantic reward flight search with route pre-filled."

    async def search(self, client, origin, destination, depart_date, cabin, passengers) -> List[FlightOffer]:
        return []

    def deep_link(self, origin, destination, depart_date, cabin, passengers):
        cabin_q = {"economy": "economy", "premium_economy": "premium", "business": "upperclass", "first": "upperclass"}.get(cabin, "economy")
        return (
            "https://www.virginatlantic.com/flights-search/select?"
            f"action=rewardSearch&isOneWay=true"
            f"&origin={origin}&destination={destination}&departureDate={depart_date.isoformat()}"
            f"&numberAdults={passengers}&cabinClass={cabin_q}"
        )
