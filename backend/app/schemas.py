from __future__ import annotations

from datetime import date
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator

Cabin = Literal["economy", "premium_economy", "business", "first"]


class SearchRequest(BaseModel):
    origin: str = Field(..., min_length=3, max_length=3, description="IATA code")
    destination: str = Field(..., min_length=3, max_length=3, description="IATA code")
    depart_date: date
    return_date: Optional[date] = None
    cabin: Cabin = "economy"
    passengers: int = Field(1, ge=1, le=9)
    programs: Optional[List[str]] = None  # if None, query all

    @field_validator("origin", "destination")
    @classmethod
    def upper(cls, v: str) -> str:
        return v.upper()


class FlightOffer(BaseModel):
    program: str
    program_name: str
    alliance: Optional[str] = None
    origin: str
    destination: str
    depart_date: str
    depart_time: Optional[str] = None
    arrive_time: Optional[str] = None
    flight_numbers: List[str] = []
    operating_airlines: List[str] = []
    cabin: Cabin
    miles: int
    taxes_currency: Optional[str] = None
    taxes_amount: Optional[float] = None
    seats_available: Optional[int] = None
    direct: bool = True
    stops: int = 0
    source_url: Optional[str] = None


class ProgramStatus(BaseModel):
    program: str
    program_name: str
    alliance: Optional[str] = None
    queried: bool
    succeeded: bool
    duration_ms: int
    error: Optional[str] = None
    offers_found: int = 0


class ProviderLink(BaseModel):
    program: str
    program_name: str
    alliance: Optional[str] = None
    implementation: Literal["live", "launcher"]
    url: str


class SearchResponse(BaseModel):
    origin: str
    destination: str
    depart_date: str
    cabin: Cabin
    passengers: int
    cached: bool
    offers: List[FlightOffer]
    program_statuses: List[ProgramStatus]
    provider_links: List[ProviderLink]


class ProgramInfo(BaseModel):
    program: str
    program_name: str
    alliance: Optional[str] = None
    implementation: Literal["live", "launcher"]
    notes: Optional[str] = None
