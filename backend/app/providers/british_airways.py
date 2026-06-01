from __future__ import annotations

from datetime import date
from typing import List

import httpx

from ..schemas import Cabin, FlightOffer
from .base import Provider


CABIN_MAP = {
    "economy": "M",
    "premium_economy": "W",
    "business": "C",
    "first": "F",
}


class BritishAirwaysProvider(Provider):
    program = "ba_avios"
    program_name = "British Airways Executive Club (Avios)"
    alliance = "Oneworld"
    implementation = "live"
    notes = (
        "Calls BA reward-flight search. BA frequently rotates anti-bot tokens; "
        "falls back to mock data on failure."
    )

    base_rates = {
        "economy": 26000,
        "premium_economy": 52000,
        "business": 75000,
        "first": 110000,
    }

    URL = "https://www.britishairways.com/travel/rewardflightsearch/public/en_gb"

    async def search(
        self,
        client: httpx.AsyncClient,
        origin: str,
        destination: str,
        depart_date: date,
        cabin: Cabin,
        passengers: int,
    ) -> List[FlightOffer]:
        params = {
            "departurePoint": origin,
            "arrivalPoint": destination,
            "departureDate": depart_date.isoformat(),
            "passengers": passengers,
            "cabinClass": CABIN_MAP.get(cabin, "M"),
        }
        headers = {
            "Accept": "application/json",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124 Safari/537.36"
            ),
            "Referer": "https://www.britishairways.com/",
        }
        resp = await client.get(self.URL, params=params, headers=headers, timeout=20)
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
        for itin in data.get("itineraries", []) or []:
            segments = itin.get("segments", []) or []
            if not segments:
                continue
            miles = int(itin.get("avios") or 0)
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
                    depart_time=(segments[0].get("departure", {}).get("time") or None),
                    arrive_time=(segments[-1].get("arrival", {}).get("time") or None),
                    flight_numbers=[s.get("flightNumber") for s in segments if s.get("flightNumber")],
                    operating_airlines=[s.get("operatingCarrier") for s in segments if s.get("operatingCarrier")],
                    cabin=cabin,
                    miles=miles,
                    taxes_currency=itin.get("taxesCurrency", "GBP"),
                    taxes_amount=float(itin.get("taxes") or 0) or None,
                    seats_available=itin.get("seatsRemaining"),
                    direct=len(segments) == 1,
                    stops=max(0, len(segments) - 1),
                    source_url="https://www.britishairways.com/travel/redeem/public/en_gb",
                )
            )
        return offers
