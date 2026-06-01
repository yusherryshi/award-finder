from __future__ import annotations

from datetime import date
from typing import List

import httpx

from ..schemas import Cabin, FlightOffer
from .base import Provider


class ANAProvider(Provider):
    program = "ana"
    program_name = "ANA Mileage Club"
    alliance = "Star Alliance"
    implementation = "stub"
    notes = "TODO: ana.co.jp award booking endpoint (login wall). Mock for now."
    base_rates = {"economy": 55000, "premium_economy": 75000, "business": 88000, "first": 165000}

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
