from __future__ import annotations

from datetime import date
from typing import List

import httpx

from ..schemas import Cabin, FlightOffer
from .base import Provider


CABIN_MAP = {
    "economy": "eco",
    "premium_economy": "ecoPremium",
    "business": "business",
    "first": "first",
}


class AeroplanProvider(Provider):
    program = "aeroplan"
    program_name = "Air Canada Aeroplan"
    alliance = "Star Alliance"
    implementation = "live"
    notes = (
        "Calls Aeroplan public search endpoint. Endpoint, key, and payload format "
        "change occasionally; falls back to mock data on failure."
    )

    base_rates = {
        "economy": 35000,
        "premium_economy": 50000,
        "business": 70000,
        "first": 100000,
    }

    URL = (
        "https://akamai-gw.dbaas.aircanada.com/loyalty/dapidynamic/"
        "1ASIUDALAC/v2/search/air-bounds"
    )

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
            "bounds": [
                {
                    "originLocationCode": origin,
                    "destinationLocationCode": destination,
                    "departureDate": depart_date.isoformat(),
                }
            ],
            "passengers": {"adults": passengers, "children": 0, "infants": 0},
            "cabin": CABIN_MAP.get(cabin, "eco"),
            "solutionSet": "AwardBounds",
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "https://www.aircanada.com",
            "Referer": "https://www.aircanada.com/",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124 Safari/537.36"
            ),
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
        for bound in data.get("data", {}).get("airBoundGroups", []) or []:
            air_bound = bound.get("airBound", {})
            segments = air_bound.get("travelSegments") or []
            if not segments:
                continue
            flight_numbers = [s.get("flightNumber") for s in segments if s.get("flightNumber")]
            operating = [s.get("operatingAirlineCode") for s in segments if s.get("operatingAirlineCode")]
            offers_block = bound.get("airBound", {}).get("availabilityDetails", []) or []
            for item in offers_block:
                miles = int(item.get("quantity") or 0)
                if not miles:
                    continue
                taxes = item.get("totalTaxAmount") or item.get("taxesAndFeesAmount") or 0
                offers.append(
                    FlightOffer(
                        program=self.program,
                        program_name=self.program_name,
                        alliance=self.alliance,
                        origin=origin,
                        destination=destination,
                        depart_date=depart_date.isoformat(),
                        depart_time=(segments[0].get("departureDateTime") or "")[11:16] or None,
                        arrive_time=(segments[-1].get("arrivalDateTime") or "")[11:16] or None,
                        flight_numbers=flight_numbers,
                        operating_airlines=operating,
                        cabin=cabin,
                        miles=miles,
                        taxes_currency=item.get("currencyCode"),
                        taxes_amount=float(taxes) if taxes else None,
                        seats_available=item.get("quota"),
                        direct=len(segments) == 1,
                        stops=max(0, len(segments) - 1),
                        source_url="https://www.aircanada.com/aeroplan/redeem/",
                    )
                )
        return offers
