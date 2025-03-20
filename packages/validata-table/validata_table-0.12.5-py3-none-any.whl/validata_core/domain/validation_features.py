from dataclasses import dataclass
from pathlib import Path
from typing import List, Union

import frictionless
from frictionless import resources as frless_resources

import validata_core.domain.schema_features as schema_features
from validata_core.domain.check import (
    CheckInstance,
    CheckRepository,
    combine_repositories,
)
from validata_core.domain.fr_locale import FrLocale
from validata_core.domain.spi import (
    FileTableReader,
    LocalDescriptorFetcher,
    RemoteDescriptorFetcher,
    RemoteTableReader,
)
from validata_core.domain.table_resource import ResourceFeatures, TableResource
from validata_core.domain.types import (
    Error,
    ErrType,
    InlineArrayOfArrays,
    Locale,
    Report,
    Schema,
    SchemaDescriptor,
    Source,
    TypedException,
)
from validata_core.domain.warning_messages import iter_warnings
from validata_core.infrastructure.table_resource_readers import FrictionlessTableAdapter

VALIDATA_MAX_ROWS = 100000


class ValidationFeatures:
    """
    Features related to validation encapsulated inside a class to allow
    for dependency injection (local and remote data retrieval, additional
    checks)
    """

    def __init__(
        self,
        remote_descriptor_fetcher: RemoteDescriptorFetcher,
        local_descriptor_fetcher: LocalDescriptorFetcher,
        file_table_reader: FileTableReader,
        remote_table_reader: RemoteTableReader,
        custom_formats_repositories: List[CheckRepository],
    ):
        self._remote_content_fetcher = remote_descriptor_fetcher
        self._local_content_fetcher = local_descriptor_fetcher

        self._resource_service = ResourceFeatures(
            file_table_reader, remote_table_reader
        )

        consolidated_repository = combine_repositories(*custom_formats_repositories)
        self._custom_checks_repository = consolidated_repository

    def validate_schema(
        self,
        schema_descriptor: SchemaDescriptor,
    ) -> Report:
        """
        Raises:
          TypedException
        """
        return _FrictionlessValidation.validate_schema(schema_descriptor)

    def validate(
        self,
        source: Source,
        schema_descriptor: Union[SchemaDescriptor, str],
        ignore_header_case: bool = False,
        locale: Locale = FrLocale(),
        **options,
    ) -> Report:
        """
        Validate a `source` using a `schema` returning a validation report.

        Parameters:
          - `source` and `schema` can be access paths to local or remote files, or
        already parsed into python.
          - ignore_header_case: if True, changing the case of the header
            does not change the result.
          - locale: provide error translations. See the `Locale` Protocol for
            details.

        Raises:
          TypedException
        """

        resource: TableResource = self._resource_service.make_validata_resource(source)

        return self.validate_resource(
            resource,
            schema_descriptor,
            ignore_header_case,
            locale,
            **options,
        )

    def validate_resource(
        self,
        resource: TableResource,
        schema_descriptor: Union[SchemaDescriptor, str, Path],
        ignore_header_case: bool = False,
        locale: Locale = FrLocale(),
        **options,
    ) -> Report:
        """
        Validation function for a given `ValidataResource`.
        See `validate` for the documentation.

        Raises:
          TypedException
        """
        schema_validation_report = _FrictionlessValidation.validate_schema(
            schema_descriptor
        )

        if not schema_validation_report.valid:
            return schema_validation_report

        if isinstance(schema_descriptor, str) and schema_descriptor.startswith("http"):
            url: str = schema_descriptor
            schema_descriptor = schema_features.fetch_remote_descriptor(
                url, self._remote_content_fetcher
            )

        if isinstance(schema_descriptor, str) or isinstance(schema_descriptor, Path):
            schema_descriptor = schema_features.fetch_local_descriptor(
                schema_descriptor, self._local_content_fetcher
            )

        schema = schema_features.parse(schema_descriptor)

        # Build checks and related errors from schema
        custom_checks_result = self._build_custom_checks(schema)
        custom_checks_instances = custom_checks_result.check_instances

        report: Report = _FrictionlessValidation.validate(
            resource=resource,
            schema=schema,
            check_instances=custom_checks_instances,
            ignore_header_case=ignore_header_case,
            locale=locale,
        )

        report.add_errors(custom_checks_result.errors)
        report.add_warnings(custom_checks_result.warnings)

        return report

    def _build_custom_checks(self, schema: Schema) -> "_CustomChecksBuildingResult":
        """Build custom checks.

        If a custom check is not valid, a CheckError is created for this
        check. The other checks are then normally processed.

        The return value gathers all checks and check errors.

        A maximum row number check always applies, independently from the
        schema.
        """

        DEPRECATED_CHECKS = {
            "french-siret-value": "siret",
            "french-siren-value": "siren",
            "nomenclature-actes-value": "nomenclature-acte",
        }

        validation_checks: List[CheckInstance] = []
        check_errors = []
        check_warnings = []

        custom_checks = schema.get_custom_checks()
        for check_descriptor in custom_checks:
            if check_descriptor.name in DEPRECATED_CHECKS:
                deprecated_name = check_descriptor.name
                new_name = DEPRECATED_CHECKS[check_descriptor.name]

                check_descriptor.name = new_name
                check_warnings.append(
                    f"Le custom check '{deprecated_name}' est déprécié, veuillez utiliser '{new_name}' à la place dans le schéma."
                )
            try:
                check_instance = self._custom_checks_repository.create_instance(
                    check_descriptor
                )
            except Exception as e:
                check_errors.append(
                    Error.new(
                        "Erreur d'Initialisation du Custom Check",
                        f"Le custom check {check_descriptor.name} n'a pas pu être correctement initialisé : {e}",
                        ErrType.CHECK_ERROR,
                    ).with_no_context()
                )
                continue

            if not check_instance:
                check_errors.append(
                    Error.new(
                        "Custom Check Inconnu",
                        f"Tentative d'utilisation du custom check {check_descriptor.name}, qui n'est pas défini",
                        ErrType.CHECK_ERROR,
                    ).with_no_context()
                )
                continue

            validation_checks.append(check_instance)

        return _CustomChecksBuildingResult(
            validation_checks, check_errors, check_warnings
        )


@dataclass
class _CustomChecksBuildingResult:
    """Stores check instances along possible errors or warnings that occurred
    during the building process of the custom checks"""

    check_instances: List[CheckInstance]
    errors: List[Error]
    warnings: List[str]


class _FrictionlessValidation:
    """
    This class wraps frictionless validation features.

    Its API offers a way to validate Validata objects without knowing about
    frictionless, nor operating explicit transformations on objects.
    """

    @classmethod
    def validate(
        cls,
        resource: TableResource,
        schema: Schema,
        check_instances: List[CheckInstance],
        ignore_header_case: bool,
        locale: Locale,
    ) -> Report:
        frless_schema = frictionless.Schema.from_descriptor(schema.descriptor)

        original_schema = frless_schema.to_copy()

        consolidated_resource = cls._consolidate_to_frless_resource(
            resource, frless_schema, ignore_header_case
        )

        frless_checks = [cls._max_rows_check(VALIDATA_MAX_ROWS)] + [
            c.to_frictionless_check() for c in check_instances
        ]

        source_header = None

        try:
            report = frictionless.validate(
                source=consolidated_resource, checks=frless_checks
            )
        except Exception as e:
            report = frictionless.Report.from_validation(
                errors=[
                    frictionless.Error(
                        note=f"frictionless encountered an unexpected error. This is likely an internal error  (error message: {str(e)})."
                    )
                ]
            )

        if report.tasks:
            try:
                # `consolidated_resource.header` returns header in wrong order
                # in case of missing fields.
                # We use our own method instead
                source_header, _ = FrictionlessTableAdapter(
                    consolidated_resource
                ).read_header_and_rows()
            except TypedException:
                source_header = None

        required_field_names = cls._extract_required_field_names(frless_schema)

        for table in report.tasks:
            # Add warnings

            if source_header:
                table.warnings = list(
                    iter_warnings(
                        source_header,
                        required_field_names,
                        original_schema,
                        ignore_header_case,
                    )
                )
                table.stats["warnings"] += len(table.warnings)
                report.stats["warnings"] += len(table.warnings)
                report.warnings += table.warnings

        return Report.from_frictionless_report(report, locale, schema, resource.n_rows)

    @classmethod
    def validate_schema(cls, schema_descriptor: Union[SchemaDescriptor, str, Path]):
        try:
            if isinstance(schema_descriptor, Path):
                schema_descriptor = str(schema_descriptor)
            frictionless.Schema.from_descriptor(schema_descriptor)
        except frictionless.FrictionlessException as exception:
            errors = exception.reasons if exception.reasons else [exception.error]
            return Report.from_frictionless_report(
                frictionless.Report.from_validation(errors=errors), None, None, 0
            )

        frictionless_report = frictionless.validate(schema_descriptor, type="schema")
        return Report.from_frictionless_report(frictionless_report, None, None, 0)

    @staticmethod
    def _consolidate_to_frless_resource(
        resource: TableResource,
        schema: frictionless.Schema,
        ignore_header_case: bool,
    ) -> frless_resources.TableResource:
        resource_data: InlineArrayOfArrays = [resource.header()] + resource.rows()

        # Merge options to pass to frictionless
        frless_table = frless_resources.TableResource(
            resource_data,
            schema=schema,
            dialect=frictionless.Dialect(header_case=not ignore_header_case),
            detector=frictionless.Detector(schema_sync=True),
        )

        return frless_table

    @staticmethod
    def _extract_required_field_names(
        schema: frictionless.Schema,
    ) -> list[str]:
        return [
            field.name
            for field in schema.fields
            if field.constraints
            and "required" in field.constraints
            and field.constraints["required"]
        ]

    @staticmethod
    def _max_rows_check(max_rows) -> frictionless.Check:
        return frictionless.Check.from_descriptor(
            {"type": "table-dimensions", "maxRows": max_rows}
        )
