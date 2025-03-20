from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import frictionless

from .check_descriptor import CheckDescriptor
from .error_types import ErrType
from .field import Field
from .json import JSON
from .typed_exception import TypedException

SchemaDescriptor = Dict[str, JSON]


@dataclass
class Schema:
    descriptor: SchemaDescriptor
    fields: List[Field]
    custom_checks: List[CheckDescriptor]

    @classmethod
    def from_descriptor(cls, descriptor: SchemaDescriptor) -> Schema:
        try:
            schema = frictionless.Schema.from_descriptor(descriptor)
        except frictionless.FrictionlessException as e:
            raise TypedException(
                message=f"An error occurred while parsing the schema descriptor: { e }",
                type=ErrType.SCHEMA_ERROR,
            )

        fields = [Field.from_frictionless(f) for f in schema.fields]

        custom_checks: List[CheckDescriptor] = []

        custom_checks.extend(cls._from_custom_checks_prop(descriptor))
        custom_checks.extend(cls._from_field_custom_check(fields))

        return cls(
            descriptor,
            fields,
            custom_checks,
        )

    def get_custom_checks(self) -> List[CheckDescriptor]:
        return self.custom_checks

    @classmethod
    def _from_custom_checks_prop(
        cls, descriptor: SchemaDescriptor
    ) -> List[CheckDescriptor]:
        """Custom checks may be defined inside a top level `custom_checks`
        property

        This function verifies that if it exists, this property has the expected format, but not if the checks
        actually refer to existing checks.
        """

        if "custom_checks" not in descriptor:
            return []

        checks_descriptor = descriptor["custom_checks"]

        if not isinstance(checks_descriptor, List):
            raise TypedException(
                message='The "custom_checks" property expects a JSON array. Got:\n{checks_descriptor}',
                type=ErrType.CHECK_ERROR,
            )

        custom_checks: List[CheckDescriptor] = []

        for check in checks_descriptor:
            if not isinstance(check, Dict):
                raise TypedException(
                    message=f'Each element of the "custom_checks" array is expected to be a JSON object. Got:\n{check}',
                    type=ErrType.CHECK_ERROR,
                )

            if "name" not in check:
                raise TypedException(
                    message=f'Each element custom check is expected to have a "name" property. Got:\n{check}',
                    type=ErrType.CHECK_ERROR,
                )

            if not isinstance(check["name"], str):
                raise TypedException(
                    message=f'The "name" property of a custom check is expected to be a string. Got:\n{check["name"]}',
                    type=ErrType.CHECK_ERROR,
                )

            if "params" not in check:
                raise TypedException(
                    message=f'Each element custom check is expected to have a "params" property. Got:\n{check}',
                    type=ErrType.CHECK_ERROR,
                )

            if not isinstance(check["params"], Dict):
                raise TypedException(
                    message=f'The "params" property of a custom check is expected to be a JSON object. Got:\n{check["params"]}',
                    type=ErrType.CHECK_ERROR,
                )

            column = None

            if "column" in check["params"]:
                if not isinstance(check["params"]["column"], str):
                    raise TypedException(
                        message=f'The "params.column" property of a custom check is expected to be a valid string (column name). Got:\n{check["params"]["column"]}',
                        type=ErrType.CHECK_ERROR,
                    )
                column = check["params"]["column"]

            custom_checks.append(
                CheckDescriptor(check["name"], column, check["params"])
            )

        return custom_checks

    @classmethod
    def _from_field_custom_check(cls, fields: List[Field]):
        """Custom_checks_may be defined inside a field with the `customCheck`
        property"""
        custom_checks: List[CheckDescriptor] = []

        for field in fields:
            if not field.custom_check:
                continue
            custom_checks.append(field.custom_check)

        return custom_checks

    def get_fields(self) -> List[Field]:
        return self.fields

    def find_field_in_schema(self, field_name: str) -> Optional[Field]:
        return next(
            (field for field in self.fields if field.name == field_name),
            None,
        )
