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
    implementation = "launcher"
    notes = "Launches united.com award search with route pre-filled."

    async def search(self, client, origin, destination, depart_date, cabin, passengers) -> List[FlightOffer]:
        return []

    def deep_link(self, origin, destination, depart_date, cabin, passengers):
        cabin_q = {"economy": "1", "premium_economy": "2", "business": "3", "first": "4"}.get(cabin, "1")
        return (
            "https://www.united.com/en/us/fsr/choose-flights?"
            f"f={origin}&t={destination}&d={depart_date.isoformat()}&tt=1&px={passengers}"
            f"&taxng=1&newHP=True&clm={cabin_q}&st=bestmatches&at=1"
        )
