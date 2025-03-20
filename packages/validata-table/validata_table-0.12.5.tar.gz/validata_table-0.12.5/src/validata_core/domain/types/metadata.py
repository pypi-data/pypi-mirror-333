from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

import importlib_metadata
from dateutil import tz


@dataclass
class Metadata:
    version: str
    date: str

    to_dict = asdict


class AutoMetadata(Metadata):
    def __init__(self):
        version = get_version()
        tzFrance = tz.gettz("Europe/Paris")
        date = datetime.now(tzFrance).isoformat()
        super().__init__(version, date)


def metadata_or_default(m: Optional[Metadata]):
    """Provides automatic metadata if none is provided

    An AutoMetadata class should not be passed as a default argument, as
    python evaluates the default arguments once, and not at each function
    call.

    Instead, pass an optional Metadata and call this function for a default
    value.
    """
    if not m:
        return AutoMetadata()

    return m


def get_version() -> str:
    try:
        version = importlib_metadata.version("validata-table")
    except importlib_metadata.PackageNotFoundError:
        version = (
            "Numéro de version uniquement disponible si le package "
            "validata-table est installé"
        )
    return version
