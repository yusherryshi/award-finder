from __future__ import annotations

import abc
from datetime import date
from typing import List, Literal, Optional

import httpx

from ..schemas import Cabin, FlightOffer


Implementation = Literal["live", "launcher"]


class Provider(abc.ABC):
    program: str
    program_name: str
    alliance: Optional[str] = None
    implementation: Implementation = "launcher"
    notes: Optional[str] = None

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
        """Return award availability offers. Return [] for launcher-only providers."""
        ...

    @abc.abstractmethod
    def deep_link(
        self,
        origin: str,
        destination: str,
        depart_date: date,
        cabin: Cabin,
        passengers: int,
    ) -> str:
        """Return the airline's own award search URL with the trip pre-filled."""
        ...
