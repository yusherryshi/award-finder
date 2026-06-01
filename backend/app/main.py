from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .db import init_db
from .routers import programs, search

settings = get_settings()
logging.basicConfig(level=settings.log_level)

app = FastAPI(title="Award Finder", version="0.1.0")

_origins = settings.cors_origin_list
_allow_all = "*" in _origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if _allow_all else _origins,
    allow_credentials=False if _allow_all else True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/")
def root():
    return {"service": "award-finder", "ok": True}


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


app.include_router(search.router)
app.include_router(programs.router)
