from __future__ import annotations

from datetime import date
from typing import List

import httpx

from ..schemas import Cabin, FlightOffer
from .base import Provider


class VirginAtlanticProvider(Provider):
    program = "virgin"
    program_name = "Virgin Atlantic Flying Club"
    alliance = "SkyTeam"
    implementation = "stub"
    notes = "TODO: virginatlantic.com flight-search-r3. Good for Delta partner sweet spots. Mock for now."
    base_rates = {"economy": 20000, "premium_economy": 35000, "business": 47500, "first": 100000}

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
