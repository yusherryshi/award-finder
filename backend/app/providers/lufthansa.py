from __future__ import annotations

from datetime import date
from typing import List

import httpx

from ..schemas import Cabin, FlightOffer
from .base import Provider


class LufthansaProvider(Provider):
    program = "miles_and_more"
    program_name = "Lufthansa Miles & More"
    alliance = "Star Alliance"
    implementation = "stub"
    notes = "TODO: miles-and-more.com award search. Mock for now."
    base_rates = {"economy": 35000, "premium_economy": 60000, "business": 85000, "first": 130000}

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
