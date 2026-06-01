from __future__ import annotations

from datetime import date
from typing import List

import httpx

from ..schemas import Cabin, FlightOffer
from .base import Provider


class FlyingBlueProvider(Provider):
    program = "flying_blue"
    program_name = "Air France/KLM Flying Blue"
    alliance = "SkyTeam"
    implementation = "stub"
    notes = "TODO: api.airfranceklm.com travel/availabilities. Mock for now."
    base_rates = {"economy": 25000, "premium_economy": 50000, "business": 70000, "first": 130000}

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
