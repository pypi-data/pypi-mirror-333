from pathlib import Path
from typing import Any, List, Optional, Sequence, Tuple

import frictionless
import requests
from frictionless import formats as frless_formats
from frictionless import resources as frless_resources

from validata_core.domain.spi import FileTableReader, RemoteTableReader
from validata_core.domain.types import Error, ErrType, Header, Row, TypedException


class FrictionlessFileReader(FileTableReader):
    def make(self, filename, content):
        return FrictionlessTableAdapter(
            _LocalTable(filename, content).make_table_resource()
        )


class FrictionlessRemoteReader(RemoteTableReader):
    def make(self, url):
        return FrictionlessTableAdapter(_RemoteTable(url).make_table_resource())


class FrictionlessTableAdapter:
    """Converts a `frictionless.resources.TableResource` to a `TableReader` interface (needed to create a `validata.TableResource`)"""

    def __init__(self, frless_table: frless_resources.TableResource):
        self._frless_table = frless_table

    def read_header_and_rows(self) -> Tuple[Header, List[Row]]:
        try:
            with self._frless_table as open_resource:
                if open_resource.cell_stream is None:
                    raise ValueError("impossible de lire le contenu")

                lines: List[Sequence[Any]] = list(open_resource.read_cells())

                if not lines:
                    raise ValueError("contenu vide")

                header: Header = lines[0]
                rows: List[Row] = lines[1:]

                # Fix BOM issue on first field name
                BOM_UTF8 = "\ufeff"

                if header and header[0].startswith(BOM_UTF8):
                    header: Header = [header[0].replace(BOM_UTF8, "")] + list(
                        header[1:]
                    )

            return header, rows

        except ValueError as value_error:
            raise TypedException(
                message=value_error.args[0], type=ErrType.SOURCE_ERROR
            ) from value_error

        except frictionless.exception.FrictionlessException as exception:
            validata_error = Error.from_frictionless(exception.error, None)
            raise TypedException(
                message=validata_error.message, type=ErrType.SOURCE_ERROR
            ) from exception

    def source(self) -> str:
        return self._frless_table.path or "inline"

    @staticmethod
    def is_supported_type(extension: str) -> bool:
        if extension and extension[0] != ".":
            extension = "." + extension
        return extension in (".csv", ".tsv", ".ods", ".xls", ".xlsx")


class _RemoteTable:
    """Builds a frless_resources.TableResource from an url poiting to a remote
    file, with desired default behavior"""

    def __init__(self, url: str):
        self.url = url

    def make_table_resource(self) -> frless_resources.TableResource:
        """
        Raises:
            TypedException[FORMAT_ERROR]: unsupported data format
            TypedException[SOURCE_ERROR]: unable to read data
        """
        # Frictionless has limitations with automatic format detection
        # See:
        # - https://github.com/frictionlessdata/frictionless-py/issues/1646
        # - https://github.com/frictionlessdata/frictionless-py/issues/1653
        # So we infer the format by ourselves
        default_format = "csv"
        _format = default_format

        extension_format = self._guess_format_from_extension()
        if extension_format:
            _format = extension_format
        else:
            content_type_header = self._guess_format_from_content_type_header()
            if content_type_header:
                _format = content_type_header

        if not FrictionlessTableAdapter.is_supported_type(_format):
            raise TypedException.new(ErrType.FORMAT_ERROR, _format)

        try:
            return frless_resources.TableResource(self.url, **_make_options(_format))
        except Exception as e:
            raise TypedException.new(ErrType.SOURCE_ERROR, str(e))

    def _get_content_type_header(self) -> Optional[str]:
        """Makes a HTTP HEAD request to the resource URL and returns the
        "Content-Type" header, or None if is missing"""

    def _guess_format_from_extension(self) -> str:
        """Looks at the file extension to derive a format"""
        suffix = Path(self.url).suffix

        if suffix.startswith("."):
            return suffix[1:]
        return ""

    def _guess_format_from_content_type_header(self) -> str:
        """Looks at the Content-Type header to derive a format.

        Supported formats are "csv", "xls" and "xlsx" (with their standard
        Content-Types).

        Retrieves the header with a HTTP HEAD request.

        Returns an empty string if the request fails, if the header is
        missing, or if its value is not supported yet.
        """

        try:
            response = requests.head(self.url)

            content_type = response.headers.get("Content-Type")
        except requests.RequestException:
            content_type = None

        if content_type is None:
            return ""

        if content_type.startswith("text/csv"):
            return "csv"

        elif content_type.startswith("application/vnd.ms-excel"):
            return "xls"

        elif content_type.startswith("application/vnd.openxmlformats"):
            return "xlsx"

        return ""


class _LocalTable:
    """Builds a frless_resources.TableResource from a file content, with desired default behavior"""

    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self.content = content

    def make_table_resource(self) -> frless_resources.TableResource:
        _format = ""
        file_ext = Path(self.filename).suffix.lower()
        if file_ext:
            _format = file_ext[1:]

        if not FrictionlessTableAdapter.is_supported_type(_format):
            raise TypedException.new(ErrType.FORMAT_ERROR, _format)

        try:
            return frless_resources.TableResource(
                self.content, **_make_options(_format)
            )
        except Exception as e:
            raise TypedException.new(ErrType.SOURCE_ERROR, str(e))


def _make_options(format: str) -> dict:
    control_option = (
        {"control": frless_formats.ExcelControl(preserve_formatting=True)}
        if format == "xlsx"
        else {}
    )

    def detect_encoding(buffer: bytes) -> str:
        """Try to decode using utf-8 first, fallback on frictionless helper function."""
        try:
            buffer.decode("utf-8")
            return "utf-8"
        except UnicodeDecodeError:
            encoding = frictionless.Detector().detect_encoding(buffer)
            return encoding.lower()

    return {
        "format": format,
        **control_option,
        "detector": frictionless.Detector(encoding_function=detect_encoding),
    }
