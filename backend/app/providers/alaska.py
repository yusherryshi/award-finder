from __future__ import annotations

from datetime import date
from typing import List

import httpx

from ..schemas import Cabin, FlightOffer
from .base import Provider


CABIN_MAP = {
    "economy": "Coach",
    "premium_economy": "PremiumCoach",
    "business": "Business",
    "first": "First",
}


class AlaskaProvider(Provider):
    program = "alaska"
    program_name = "Alaska Mileage Plan"
    alliance = "Oneworld"
    implementation = "live"
    notes = (
        "Calls Alaska Air award search. Great for partner awards on BA, AA, "
        "Finnair, Iberia, Icelandair."
    )

    base_rates = {
        "economy": 30000,
        "premium_economy": 45000,
        "business": 70000,
        "first": 110000,
    }

    URL = "https://www.alaskaair.com/search/api/flights"

    async def search(
        self,
        client: httpx.AsyncClient,
        origin: str,
        destination: str,
        depart_date: date,
        cabin: Cabin,
        passengers: int,
    ) -> List[FlightOffer]:
        payload = {
            "SearchType": "Matrix",
            "AwardSearch": True,
            "Slices": [
                {
                    "Origin": origin,
                    "Destination": destination,
                    "DepartureDate": depart_date.isoformat(),
                    "CabinPreference": CABIN_MAP.get(cabin, "Coach"),
                }
            ],
            "PassengerCounts": {"Adult": passengers, "Child": 0, "Infant": 0},
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124 Safari/537.36"
            ),
            "Referer": "https://www.alaskaair.com/",
        }
        resp = await client.post(self.URL, json=payload, headers=headers, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        return self._parse(data, origin, destination, depart_date, cabin)

    def _parse(
        self,
        data: dict,
        origin: str,
        destination: str,
        depart_date: date,
        cabin: Cabin,
    ) -> List[FlightOffer]:
        offers: List[FlightOffer] = []
        for itin in (data.get("Slices") or [{}])[0].get("Itineraries", []) or []:
            segments = itin.get("Segments", []) or []
            fare = itin.get("AwardFare") or {}
            miles = int(fare.get("Miles") or 0)
            if not miles:
                continue
            offers.append(
                FlightOffer(
                    program=self.program,
                    program_name=self.program_name,
                    alliance=self.alliance,
                    origin=origin,
                    destination=destination,
                    depart_date=depart_date.isoformat(),
                    depart_time=(segments[0].get("DepartureTime") or "")[11:16] or None,
                    arrive_time=(segments[-1].get("ArrivalTime") or "")[11:16] or None,
                    flight_numbers=[s.get("FlightNumber") for s in segments if s.get("FlightNumber")],
                    operating_airlines=[s.get("OperatingCarrier") for s in segments if s.get("OperatingCarrier")],
                    cabin=cabin,
                    miles=miles,
                    taxes_currency=fare.get("Currency", "USD"),
                    taxes_amount=float(fare.get("Taxes") or 0) or None,
                    seats_available=fare.get("SeatsRemaining"),
                    direct=len(segments) == 1,
                    stops=max(0, len(segments) - 1),
                    source_url="https://www.alaskaair.com/",
                )
            )
        return offers
