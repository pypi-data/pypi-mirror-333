from pathlib import Path
from typing import List, Union

from frictionless import resources as frless_resources

from validata_core.domain.spi import FileTableReader, RemoteTableReader
from validata_core.domain.table_reader import TableReader
from validata_core.domain.types import ErrType, InlineData, Source, TypedException
from validata_core.domain.types.source import Header, InlineArrayOfArrays, Row
from validata_core.infrastructure.table_resource_readers import FrictionlessTableAdapter


class TableResource:
    """Base class to retrieve data and stats on tabular data"""

    def __init__(self, reader: TableReader):
        self._reader = reader

        header, rows = reader.read_header_and_rows()

        self._header: Header = header
        self._rows: List[Row] = rows

    @property
    def n_rows(self) -> int:
        return len(self._rows)

    @property
    def n_fields(self) -> int:
        return len(self._header)

    def source(self) -> str:
        return self._reader.source()

    def header(self) -> Header:
        return self._header

    def rows(self) -> List[Row]:
        return self._rows

    def to_inline_data(self) -> InlineArrayOfArrays:
        return [self.header()] + self.rows()


class ResourceFeatures:
    """Class for creating a TableResource for different sources.

    Allows for dependency injection of all external service providers (read
    local and remote files).
    """

    def __init__(
        self,
        file_table_reader: FileTableReader,
        remote_table_reader: RemoteTableReader,
    ):
        self._file_table_reader = file_table_reader
        self._remote_table_reader = remote_table_reader

    def make_validata_resource(self, source: Source) -> TableResource:
        """Detects the format of the source and creates the Validata Resource
        accordingly

        Raises:
          TypedException
        """
        if not isinstance(source, str) and not isinstance(source, Path):
            return self.from_inline_data(source)

        if isinstance(source, str) and source.startswith("http"):
            url = source
            return self.from_remote_file(url)
        else:
            path = source
            with open(path, "rb") as f:
                content: bytes = f.read()
            return self.from_file_content(path, content)

    def from_file_content(
        self, filename: Union[str, Path], content: bytes
    ) -> TableResource:
        """
        Creates a TableResource from file content provided as bytes

        Raises:
          TypedException: an error occurred while reading data
        """

        return TableResource(self._file_table_reader.make(str(filename), content))

    def from_remote_file(self, url: str) -> TableResource:
        """
        Raises:
          TypedException
        """

        return TableResource(self._remote_table_reader.make(url))

    def from_inline_data(self, data: InlineData) -> TableResource:
        """
        Creates a TableResource from inline data. See `InlineData` type for
        exected data format.

        Raises:
          TypedException
        """
        try:
            frless_resource = frless_resources.TableResource(data)
        except Exception as e:
            raise TypedException.new(ErrType.SOURCE_ERROR, str(e))

        return TableResource(FrictionlessTableAdapter(frless_resource))
