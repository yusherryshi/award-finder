from __future__ import annotations

from datetime import date
from typing import List

import httpx

from ..schemas import Cabin, FlightOffer
from .base import Provider


class AmericanProvider(Provider):
    program = "aa"
    program_name = "American AAdvantage"
    alliance = "Oneworld"
    implementation = "stub"
    notes = "TODO: aa.com/booking/api/search/itinerary. Mock data for now."
    base_rates = {"economy": 30000, "premium_economy": 50000, "business": 57500, "first": 85000}

    async def search(
        self,
        client: httpx.AsyncClient,
        origin: str,
        destination: str,
        depart_date: date,
        cabin: Cabin,
        passengers: int,
    ) -> List[FlightOffer]:
        return self.make_mock(origin, destination, depart_date, cabin)
