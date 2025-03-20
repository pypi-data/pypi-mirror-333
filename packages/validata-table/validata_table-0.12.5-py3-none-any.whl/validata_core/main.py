import functools
from typing import Callable

from validata_core.custom_checks import validata_check_repository
from validata_core.domain.schema_features import fetch_remote_descriptor
from validata_core.domain.table_resource import ResourceFeatures
from validata_core.domain.types import Report, SchemaDescriptor
from validata_core.domain.validation_features import ValidationFeatures
from validata_core.infrastructure.descriptor_readers import (
    LocalDescriptorReader,
    RemoteDescriptorReader,
)
from validata_core.infrastructure.fr_formats import FrFormatsRepository
from validata_core.infrastructure.table_resource_readers import (
    FrictionlessFileReader,
    FrictionlessRemoteReader,
)

# Resources dependency injection

resource_service = ResourceFeatures(
    FrictionlessFileReader(),
    FrictionlessRemoteReader(),
)

# Validation

remote_decriptor_fetcher = RemoteDescriptorReader()
local_descriptor_fetcher = LocalDescriptorReader()
checks_repository = [FrFormatsRepository(), validata_check_repository]

validation_service = ValidationFeatures(
    RemoteDescriptorReader(),
    LocalDescriptorReader(),
    FrictionlessFileReader(),
    FrictionlessRemoteReader(),
    checks_repository,
)

ValidateSignature = Callable[..., Report]

validate: ValidateSignature = functools.partial(
    validation_service.validate.__func__,  # type: ignore
    validation_service,
)
validate_schema = functools.partial(
    validation_service.validate_schema.__func__,  # type: ignore
    validation_service,
)

# Schema


def fetch_remote_schema(url: str) -> SchemaDescriptor:
    return fetch_remote_descriptor(url, remote_decriptor_fetcher)
