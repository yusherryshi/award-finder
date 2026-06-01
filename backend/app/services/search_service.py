from __future__ import annotations

import asyncio
import logging
import time
from typing import List, Tuple

import httpx

from ..config import get_settings
from ..providers.base import Provider
from ..providers.registry import get_providers
from ..schemas import (
    FlightOffer,
    ProgramStatus,
    SearchRequest,
    SearchResponse,
)

logger = logging.getLogger(__name__)


async def _run_provider(
    provider: Provider,
    client: httpx.AsyncClient,
    req: SearchRequest,
) -> Tuple[List[FlightOffer], ProgramStatus]:
    settings = get_settings()
    start = time.perf_counter()
    used_mock = False
    error: str | None = None
    offers: List[FlightOffer] = []
    succeeded = False
    try:
        offers = await provider.search(
            client=client,
            origin=req.origin,
            destination=req.destination,
            depart_date=req.depart_date,
            cabin=req.cabin,
            passengers=req.passengers,
        )
        succeeded = True
    except Exception as e:  # broad: providers can fail in many ways
        error = f"{type(e).__name__}: {e}"
        logger.warning("Provider %s failed: %s", provider.program, error)
        if settings.use_mock_fallback:
            offers = provider.make_mock(req.origin, req.destination, req.depart_date, req.cabin)
            used_mock = True
    duration_ms = int((time.perf_counter() - start) * 1000)
    status = ProgramStatus(
        program=provider.program,
        program_name=provider.program_name,
        alliance=provider.alliance,
        queried=True,
        succeeded=succeeded,
        duration_ms=duration_ms,
        error=error,
        used_mock=used_mock,
    )
    return offers, status


async def run_search(req: SearchRequest) -> SearchResponse:
    settings = get_settings()
    providers = get_providers(req.programs)
    timeout = httpx.Timeout(settings.http_timeout_seconds)
    limits = httpx.Limits(max_connections=20, max_keepalive_connections=10)

    all_offers: List[FlightOffer] = []
    statuses: List[ProgramStatus] = []

    async with httpx.AsyncClient(timeout=timeout, limits=limits, http2=False) as client:
        results = await asyncio.gather(
            *[_run_provider(p, client, req) for p in providers],
            return_exceptions=False,
        )

    for offers, status in results:
        all_offers.extend(offers)
        statuses.append(status)

    all_offers.sort(key=lambda o: (o.miles, o.cabin))

    return SearchResponse(
        origin=req.origin,
        destination=req.destination,
        depart_date=req.depart_date.isoformat(),
        cabin=req.cabin,
        passengers=req.passengers,
        cached=False,
        offers=all_offers,
        program_statuses=statuses,
    )
