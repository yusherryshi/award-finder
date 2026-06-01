from __future__ import annotations

from typing import List

from fastapi import APIRouter

from ..airports import AIRPORTS
from ..providers.registry import PROVIDERS
from ..schemas import ProgramInfo

router = APIRouter(prefix="/api", tags=["meta"])


@router.get("/programs", response_model=List[ProgramInfo])
def list_programs() -> List[ProgramInfo]:
    return [
        ProgramInfo(
            program=p.program,
            program_name=p.program_name,
            alliance=p.alliance,
            implementation=p.implementation,
            notes=p.notes,
        )
        for p in PROVIDERS.values()
    ]


@router.get("/airports")
def list_airports():
    return [
        {"iata": code, **info}
        for code, info in sorted(AIRPORTS.items())
    ]
