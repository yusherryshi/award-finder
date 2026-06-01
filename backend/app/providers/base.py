from __future__ import annotations

import abc
import random
from datetime import date
from typing import List, Literal, Optional

import httpx

from ..schemas import Cabin, FlightOffer


Implementation = Literal["live", "stub", "mock"]


class Provider(abc.ABC):
    program: str
    program_name: str
    alliance: Optional[str] = None
    implementation: Implementation = "stub"
    notes: Optional[str] = None

    # Approximate published award rates (one-way, transatlantic) used by the
    # mock generator. Override in subclasses where useful.
    base_rates: dict = {
        "economy": 30000,
        "premium_economy": 45000,
        "business": 60000,
        "first": 110000,
    }

    @abc.abstractmethod
    async def search(
        self,
        client: httpx.AsyncClient,
        origin: str,
        destination: str,
        depart_date: date,
        cabin: Cabin,
        passengers: int,
    ) -> List[FlightOffer]:
        """Return award availability offers. Raise on error."""
        ...

    # ---- helpers shared by all providers -----------------------------------
    def make_mock(
        self,
        origin: str,
        destination: str,
        depart_date: date,
        cabin: Cabin,
        seed_suffix: str = "",
    ) -> List[FlightOffer]:
        """Generate plausible mock offers so the UI works without live data."""
        rng = random.Random(f"{self.program}|{origin}|{destination}|{depart_date}|{cabin}|{seed_suffix}")
        base = self.base_rates.get(cabin, 60000)
        offers: List[FlightOffer] = []
        n = rng.randint(0, 3)
        for i in range(n):
            jitter = rng.uniform(-0.15, 0.25)
            miles = int(base * (1 + jitter) / 500) * 500
            seats = rng.choice([1, 2, 2, 4, 6, 9])
            taxes = round(rng.uniform(5.6, 250.0), 2)
            dep_hour = rng.choice([8, 11, 17, 19, 21, 22])
            offers.append(
                FlightOffer(
                    program=self.program,
                    program_name=self.program_name,
                    alliance=self.alliance,
                    origin=origin,
                    destination=destination,
                    depart_date=depart_date.isoformat(),
                    depart_time=f"{dep_hour:02d}:{rng.choice(['00','15','30','45'])}",
                    arrive_time=None,
                    flight_numbers=[],
                    operating_airlines=[],
                    cabin=cabin,
                    miles=miles,
                    taxes_currency="USD",
                    taxes_amount=taxes,
                    seats_available=seats,
                    direct=rng.random() > 0.4,
                    stops=0 if rng.random() > 0.4 else 1,
                    is_mock=True,
                )
            )
        return offers
