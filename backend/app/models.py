from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class CachedSearch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cache_key: str = Field(index=True, unique=True)
    origin: str = Field(index=True)
    destination: str = Field(index=True)
    depart_date: str = Field(index=True)
    cabin: str = Field(index=True)
    passengers: int = 1
    payload_json: str
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    expires_at: datetime = Field(index=True)
