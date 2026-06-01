from __future__ import annotations

from typing import List

from ..schemas import FlightOffer
from .base import Provider


class DeltaProvider(Provider):
    program = "delta"
    program_name = "Delta SkyMiles"
    alliance = "SkyTeam"
    implementation = "launcher"
    notes = "Launches delta.com award search with route pre-filled."

    async def search(self, client, origin, destination, depart_date, cabin, passengers) -> List[FlightOffer]:
        return []

    def deep_link(self, origin, destination, depart_date, cabin, passengers):
        cabin_q = {"economy": "BE", "premium_economy": "PE", "business": "BU", "first": "FC"}.get(cabin, "BE")
        return (
            "https://www.delta.com/flight-search/book-a-flight?"
            f"tripType=ONE_WAY&priceSchedule=PRICE&awardTravel=true"
            f"&originCity={origin}&destinationCity={destination}"
            f"&departureDate={depart_date.isoformat()}&paxCount={passengers}&cabinFareClass={cabin_q}"
        )
