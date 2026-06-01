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
    ProviderLink,
    SearchRequest,
    SearchResponse,
)

logger = logging.getLogger(__name__)


async def _run_provider(
    provider: Provider,
    client: httpx.AsyncClient,
    req: SearchRequest,
) -> Tuple[List[FlightOffer], ProgramStatus]:
    start = time.perf_counter()
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
    except Exception as e:
        error = f"{type(e).__name__}: {e}"
        logger.warning("Provider %s failed: %s", provider.program, error)
    duration_ms = int((time.perf_counter() - start) * 1000)
    status = ProgramStatus(
        program=provider.program,
        program_name=provider.program_name,
        alliance=provider.alliance,
        queried=True,
        succeeded=succeeded,
        duration_ms=duration_ms,
        error=error,
        offers_found=len(offers),
    )
    return offers, status


async def run_search(req: SearchRequest) -> SearchResponse:
    settings = get_settings()
    providers = get_providers(req.programs)
    timeout = httpx.Timeout(settings.http_timeout_seconds)
    limits = httpx.Limits(max_connections=20, max_keepalive_connections=10)

    all_offers: List[FlightOffer] = []
    statuses: List[ProgramStatus] = []
    links: List[ProviderLink] = []

    live_providers = [p for p in providers if p.implementation == "live"]

    async with httpx.AsyncClient(timeout=timeout, limits=limits, http2=False) as client:
        results = await asyncio.gather(
            *[_run_provider(p, client, req) for p in live_providers],
            return_exceptions=False,
        )

    for offers, status in results:
        all_offers.extend(offers)
        statuses.append(status)

    for p in providers:
        try:
            url = p.deep_link(
                req.origin, req.destination, req.depart_date, req.cabin, req.passengers
            )
        except Exception as e:
            logger.warning("deep_link failed for %s: %s", p.program, e)
            continue
        links.append(
            ProviderLink(
                program=p.program,
                program_name=p.program_name,
                alliance=p.alliance,
                implementation=p.implementation,
                url=url,
            )
        )

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
        provider_links=links,
    )
