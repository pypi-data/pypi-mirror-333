from pathlib import Path
from typing import Protocol, Union

from validata_core.domain.table_reader import TableReader
from validata_core.domain.types import Schema, SchemaDescriptor, TypedException


class FileTableReader(Protocol):
    def make(self, filename: str, content: bytes) -> TableReader: ...


class RemoteTableReader(Protocol):
    def make(self, url: str) -> TableReader: ...


class TableSchemaService(Protocol):
    """Service provider interface for dealing with table schema specification"""

    def parse(self, descriptor: SchemaDescriptor) -> Union[Schema, TypedException]:
        """Parses a standard table schema descriptor into a Schema object

        All specificities of the profile (as opposed to the standard
        specification) are ignored
        """
        ...


class RemoteDescriptorFetcher(Protocol):
    def fetch(self, url: str) -> SchemaDescriptor: ...


class LocalDescriptorFetcher(Protocol):
    def fetch(self, filepath: Union[str, Path]) -> SchemaDescriptor: ...
