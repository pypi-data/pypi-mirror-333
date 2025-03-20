from pathlib import Path
from typing import Union

from validata_core.domain.spi import LocalDescriptorFetcher, RemoteDescriptorFetcher
from validata_core.domain.types import Schema, SchemaDescriptor


def fetch_remote_descriptor(
    url: str, remote_content_fetcher: RemoteDescriptorFetcher
) -> SchemaDescriptor:
    """
    Raises:
        TypedException
    """
    return remote_content_fetcher.fetch(url)


def fetch_local_descriptor(
    filepath: Union[str, Path], local_content_fetcher: LocalDescriptorFetcher
) -> SchemaDescriptor:
    return local_content_fetcher.fetch(filepath)


def parse(descriptor: SchemaDescriptor) -> Schema:
    return Schema.from_descriptor(descriptor)
