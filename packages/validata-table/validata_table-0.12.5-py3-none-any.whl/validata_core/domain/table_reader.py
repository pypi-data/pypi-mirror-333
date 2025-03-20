from typing import Protocol, Tuple

from validata_core.domain.types import Header, Row


class TableReader(Protocol):
    """Interface for a service that knows how to read a table for specific sources"""

    def read_header_and_rows(self) -> Tuple[Header, list[Row]]: ...

    def source(self) -> str: ...
