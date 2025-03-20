from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

import frictionless
import frictionless.fields as frfields

from .check_descriptor import CheckDescriptor
from .error_types import ErrType
from .typed_exception import TypedException


class FieldType(Enum):
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    OBJECT = "object"
    ARRAY = "array"
    LIST = "list"
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"
    YEAR = "year"
    YEARMONTH = "yearmonth"
    DURATION = "duration"
    GEOPOINT = "geopoint"
    GEOJSON = "geojson"
    ANY = "any"

    @classmethod
    def _missing_(cls, value):
        raise TypedException(
            "%r is not a valid field type. Valid types: %s"
            % (
                value,
                ", ".join([repr(m.value) for m in cls]),
            ),
            ErrType.FIELD_ERROR,
        )


@dataclass
class Field:
    type: FieldType
    format: str
    frless_field: frictionless.Field

    _CUSTOM_CHECK_PROP = "customCheck"  # If changed, docs need to be updated as well
    """Name of the field descriptor property  that holds information about a custom
    check.
    """

    @classmethod
    def from_frictionless(cls, field: frictionless.Field) -> "Field":
        field_type_enum = FieldType(field.type)
        return Field(field_type_enum, field.format, field)

    @property
    def custom_check(self) -> Optional[CheckDescriptor]:
        """Custom checks can be defined directly inside the field descriptor
        with a "customCheck" property.

        This retrieves this custom check or returns None if none is defined.
        """
        descriptor = self.frless_field.to_descriptor()

        if self._CUSTOM_CHECK_PROP not in descriptor:
            return None

        fr_format_descriptor = descriptor[self._CUSTOM_CHECK_PROP]

        if isinstance(fr_format_descriptor, str):
            return CheckDescriptor(fr_format_descriptor, self.name, {})

        else:
            return CheckDescriptor(
                fr_format_descriptor["name"],
                self.name,
                {k: v for k, v in fr_format_descriptor.items() if k != "name"},
            )

    @property
    def name(self) -> str:
        return self.frless_field.name

    @property
    def example(self) -> Optional[str]:
        return self.frless_field.example

    def get_true_values(self):
        if isinstance(self.frless_field, frfields.boolean.BooleanField):
            true_values = (
                self.frless_field.true_values
                if self.frless_field.true_values
                else ["true"]
            )
            return true_values
        return None

    def get_false_values(self):
        if isinstance(self.frless_field, frfields.boolean.BooleanField):
            false_values = (
                self.frless_field.false_values
                if self.frless_field.false_values
                else ["false"]
            )
            return false_values
        return None

    def _get_array_item_constraint(self, violated_constraint: str):
        assert isinstance(self.frless_field, frfields.array.ArrayField)
        assert self.frless_field.array_item is not None
        return self.frless_field.array_item["constraints"][violated_constraint]

    def _get_constraint(self, violated_constraint: str):
        return self.frless_field.constraints[violated_constraint]

    def get_constraint_value(self, violated_constraint: str) -> Any:
        """Extract and return constraint value from a field constraints"""

        if self.type == FieldType.ARRAY:
            return self._get_array_item_constraint(violated_constraint)

        else:
            return self._get_constraint(violated_constraint)


DEFAULT_TRUE_VALUES = ["true", "True", "TRUE", "1"]
DEFAULT_FALSE_VALUES = ["false", "False", "FALSE", "0"]
