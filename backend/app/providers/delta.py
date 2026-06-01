from __future__ import annotations

from datetime import date
from typing import List

import httpx

from ..schemas import Cabin, FlightOffer
from .base import Provider


class DeltaProvider(Provider):
    program = "delta"
    program_name = "Delta SkyMiles"
    alliance = "SkyTeam"
    implementation = "stub"
    notes = "TODO: delta.com shop endpoint. Heavily anti-botted. Mock for now."
    base_rates = {"economy": 50000, "premium_economy": 80000, "business": 100000, "first": 180000}

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
