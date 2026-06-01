from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional

from sqlmodel import Session, select

from .config import get_settings
from .models import CachedSearch
from .schemas import SearchRequest, SearchResponse


def make_cache_key(req: SearchRequest) -> str:
    raw = json.dumps(
        {
            "o": req.origin,
            "d": req.destination,
            "dt": req.depart_date.isoformat(),
            "c": req.cabin,
            "p": req.passengers,
            "pr": sorted(req.programs) if req.programs else None,
        },
        sort_keys=True,
    )
    return hashlib.sha256(raw.encode()).hexdigest()


def read_cache(session: Session, req: SearchRequest) -> Optional[SearchResponse]:
    key = make_cache_key(req)
    stmt = select(CachedSearch).where(CachedSearch.cache_key == key)
    row = session.exec(stmt).first()
    if not row:
        return None
    if row.expires_at < datetime.utcnow():
        return None
    payload = json.loads(row.payload_json)
    payload["cached"] = True
    return SearchResponse.model_validate(payload)


def write_cache(session: Session, req: SearchRequest, resp: SearchResponse) -> None:
    settings = get_settings()
    key = make_cache_key(req)
    now = datetime.utcnow()
    expires = now + timedelta(minutes=settings.cache_ttl_minutes)
    stmt = select(CachedSearch).where(CachedSearch.cache_key == key)
    existing = session.exec(stmt).first()
    payload = resp.model_copy(update={"cached": False}).model_dump()
    if existing:
        existing.payload_json = json.dumps(payload)
        existing.created_at = now
        existing.expires_at = expires
        session.add(existing)
    else:
        session.add(
            CachedSearch(
                cache_key=key,
                origin=req.origin,
                destination=req.destination,
                depart_date=req.depart_date.isoformat(),
                cabin=req.cabin,
                passengers=req.passengers,
                payload_json=json.dumps(payload),
                created_at=now,
                expires_at=expires,
            )
        )
    session.commit()
