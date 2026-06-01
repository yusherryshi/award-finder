from __future__ import annotations

from datetime import date
from typing import List

import httpx

from ..schemas import Cabin, FlightOffer
from .base import Provider


class TurkishProvider(Provider):
    program = "turkish"
    program_name = "Turkish Miles&Smiles"
    alliance = "Star Alliance"
    implementation = "stub"
    notes = "TODO: turkishairlines.com loyalty award search. Known Star sweet spot. Mock for now."
    base_rates = {"economy": 30000, "premium_economy": 45000, "business": 45000, "first": 90000}

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
