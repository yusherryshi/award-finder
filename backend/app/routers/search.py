from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..cache import read_cache, write_cache
from ..db import get_session
from ..schemas import SearchRequest, SearchResponse
from ..services.search_service import run_search

router = APIRouter(prefix="/api", tags=["search"])


@router.post("/search", response_model=SearchResponse)
async def search(req: SearchRequest, session: Session = Depends(get_session)) -> SearchResponse:
    cached = read_cache(session, req)
    if cached is not None:
        return cached
    resp = await run_search(req)
    write_cache(session, req, resp)
    return resp
