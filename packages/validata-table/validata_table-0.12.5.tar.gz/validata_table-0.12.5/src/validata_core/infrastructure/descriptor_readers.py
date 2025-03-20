import json
from pathlib import Path
from typing import Protocol, Union

import requests

from validata_core.domain.spi import LocalDescriptorFetcher, RemoteDescriptorFetcher
from validata_core.domain.types import ErrType, SchemaDescriptor, TypedException


class _ContentReader(Protocol):
    """ContentReader is an interface to classes that reads content at a given
    path"""

    def read(self, path: str) -> str: ...


class _RemoteContentReader(_ContentReader):
    """Reads remote content"""

    def read(self, path: str) -> str:
        response = requests.get(path)
        return response.text


class _LocalContentReader(_ContentReader):
    """Reads content of local file"""

    def read(self, path: str) -> str:
        with open(path) as f:
            content = f.read()
        return content


class _DescriptorFetcher:
    """Generic fetcher that deals with errors and JSON parsing"""

    _content_reader: _ContentReader
    _err_type: ErrType

    def _fetch(self, path: str) -> SchemaDescriptor:
        try:
            content = self._content_reader.read(path)
        except Exception as e:
            raise TypedException.new(self._err_type, str(e))

        schema_descriptor = _parse_json(content)
        return schema_descriptor


class LocalDescriptorReader(_DescriptorFetcher, LocalDescriptorFetcher):
    _content_reader = _LocalContentReader()
    _err_type = ErrType.LOCAL_SOURCE_ERROR

    def fetch(self, filepath: Union[str, Path]) -> SchemaDescriptor:
        return super()._fetch(str(filepath))


class RemoteDescriptorReader(_DescriptorFetcher, RemoteDescriptorFetcher):
    _content_reader = _RemoteContentReader()
    _err_type = ErrType.REMOTE_SOURCE_ERROR

    def fetch(self, url: str) -> SchemaDescriptor:
        return super()._fetch(url)


def _parse_json(content: str) -> SchemaDescriptor:
    """A simple json parsing utility functon with error handling"""
    try:
        schema_descriptor = json.loads(content)
    except Exception as e:
        raise TypedException.new(ErrType.JSON_FORMAT_ERROR, str(e))
    return schema_descriptor
