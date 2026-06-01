from __future__ import annotations

from typing import Dict, List

from .base import Provider
from .aeroplan import AeroplanProvider
from .alaska import AlaskaProvider
from .american import AmericanProvider
from .ana import ANAProvider
from .british_airways import BritishAirwaysProvider
from .delta import DeltaProvider
from .flying_blue import FlyingBlueProvider
from .lufthansa import LufthansaProvider
from .turkish import TurkishProvider
from .united import UnitedProvider
from .virgin_atlantic import VirginAtlanticProvider


_PROVIDER_INSTANCES: List[Provider] = [
    AeroplanProvider(),
    BritishAirwaysProvider(),
    AlaskaProvider(),
    UnitedProvider(),
    AmericanProvider(),
    FlyingBlueProvider(),
    VirginAtlanticProvider(),
    DeltaProvider(),
    LufthansaProvider(),
    TurkishProvider(),
    ANAProvider(),
]

PROVIDERS: Dict[str, Provider] = {p.program: p for p in _PROVIDER_INSTANCES}


def get_providers(program_keys: List[str] | None = None) -> List[Provider]:
    if not program_keys:
        return list(PROVIDERS.values())
    return [PROVIDERS[k] for k in program_keys if k in PROVIDERS]
