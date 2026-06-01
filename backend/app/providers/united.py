from __future__ import annotations

from datetime import date
from typing import List

import httpx

from ..schemas import Cabin, FlightOffer
from .base import Provider


class UnitedProvider(Provider):
    program = "united"
    program_name = "United MileagePlus"
    alliance = "Star Alliance"
    implementation = "stub"
    notes = (
        "TODO: united.com/api/flight/FetchFlights with proper Akamai bot bypass. "
        "Currently returns mock data."
    )
    base_rates = {"economy": 33000, "premium_economy": 50000, "business": 70000, "first": 110000}

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
