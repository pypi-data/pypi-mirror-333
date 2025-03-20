import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol

import frictionless
from frictionless import errors as frerrors

from .error_tags import Tag
from .error_types import ErrType
from .field import DEFAULT_FALSE_VALUES, DEFAULT_TRUE_VALUES, Field, FieldType
from .json import JSON
from .locale import Locale, Translation
from .options import Options
from .schema import Schema
from .table_region import (
    FieldInfo,
    TableRegion,
    involves_single_cell,
    involves_single_field,
    involves_single_row,
)

_BODY_TAGS = frozenset([Tag.BODY, Tag.CELL, Tag.CONTENT, Tag.ROW, Tag.TABLE])


@dataclass
class Constraint:
    violated_constraint: str
    constraint_value: Any


@dataclass
class Error:
    """Stores all information about data considered invalid

    It should be created in two steps. First initialize the error content with
    the `new` function, and then add context with the `with_context` method.
    Both methods can be chained. This two step initialization allows
    separation of concerns.

    Error content : the class stores information to explain the nature of the error
    to the user by means of a short title and a message. It also has a type to facilitate
    programmatic identification.

    Error context : additionnal information about where and in what conditions the error
    occurred is stored in this class as well. The `locale` property allows to
    translate the message if needed.
    """

    _title: str
    _message: str

    type: ErrType

    location: TableRegion = TableRegion(None, None)

    tags: List[Tag] = field(default_factory=list)

    # Context properties. See `with_context` method
    _field_info: Options = field(default_factory=Options)
    _validated_values: List[Any] = field(default_factory=list)
    _violated_constraint: Optional[Constraint] = None
    locale: Optional[Locale] = None

    @staticmethod
    def new(title: str, message: str, type: ErrType) -> "PartialError":
        """Define error context for the user

        Params:
            title:
                short human readable title, in Title Case (every word
                capitalized)
            message:
                description of why the value is invalid
            type:
                an error type, used as an identifier
        """
        return Error(title, message, type)

    def with_context(
        self,
        validated_values: List[Any] = [],
        location: TableRegion = TableRegion(),
        details: Options = Options(),
        violated_constraint: Optional[Constraint] = None,
        locale: Optional[Locale] = None,
    ) -> "Error":
        """Store information about the context in which the error occurred

        Parameters:
            validated_values:
                The value or values that triggered the error
            location:
                Where the error occurred.
                The location can be any region: a single cell, one or several rows or
                fields/columns, or the whole table.
            details:
                Details about the validator, e.g. validator options
            violated_constraint:
                Details about the violated constraint to provide in the case
                of an error associated to a Table Schema constraint
            locale:
                A locale that can be used for translations. None means no
                translation.
        """
        self._validated_values = validated_values

        self.location = location

        # Guess tags from location
        if involves_single_cell(location):
            self.tags = [Tag.BODY, Tag.TABLE, Tag.ROW, Tag.CELL]
        elif involves_single_row(location):
            if location.row_number == 1:
                self.tags = [Tag.BODY, Tag.TABLE, Tag.HEADER]
            else:
                self.tags = [Tag.BODY, Tag.TABLE, Tag.ROW]

        else:
            self.tags = [Tag.STRUCTURE]

        if details:
            self._field_info = details

        if violated_constraint:
            self._violated_constraint = violated_constraint

        if locale:
            self.locale = locale

        return self

    def with_no_context(self):
        """Explicit shortcut to tell that there is no context to attach to the Error"""
        return self.with_context()

    @property
    def message(self):
        if self.locale:
            _, message = translate_message(self, self.locale)
            if message != "":
                return message

        return self._message

    @property
    def title(self):
        if self.locale:
            title, _ = translate_message(self, self.locale)
            if title != "":
                return title

        return self._title

    @classmethod
    def from_frictionless(
        cls,
        frless_err: frictionless.Error,
        locale: Optional[Locale],
        schema: Optional[Schema] = None,
    ) -> "Error":
        err = cls.new(
            title=frless_err.title,
            message=frless_err.message,
            type=ErrType(frless_err.type),
        )

        context = TableRegion(None, None)
        validated_values = []
        details = {}
        violated_constraint = None

        if isinstance(frless_err, frerrors.RowError):
            context.row_number = frless_err.row_number

        if isinstance(frless_err, frerrors.CellError):
            validated_values.append(frless_err.cell)

        if isinstance(frless_err, frerrors.CellError) or isinstance(
            frless_err, frerrors.LabelError
        ):
            assert schema, "Please provide a schema to properly deal with Cell Errors"

            context.fields_info = [
                FieldInfo(frless_err.field_name, frless_err.field_number)
            ]

            field = Error._get_field(frless_err, schema)

            if isinstance(frless_err, frerrors.ConstraintError):
                violated_constraint_str = _extract_constraint_from_message(frless_err)
                constraint_value = (
                    field.get_constraint_value(violated_constraint_str)
                    if field and violated_constraint_str
                    else ""
                )
                violated_constraint = Constraint(
                    violated_constraint_str, constraint_value
                )

        if schema:
            field = Error._get_field(frless_err, schema)
            if field:
                details = {**details, **field.frless_field.to_dict()}

        err = err.with_context(
            validated_values, context, Options(details), violated_constraint, locale
        )
        err = _correct_schema_sync_bug(err)
        err._message = frless_err.message
        err._title = frless_err.title

        err.tags = [Tag(t) for t in frless_err.tags]

        return err

    def is_body_error(self) -> bool:
        """Classify the given error as 'body error' according to its tags."""
        tags = self.tags
        return bool(_BODY_TAGS & set(tags))

    def _to_frictionless(self) -> frictionless.Error:
        """Convert to frictionless.

        Depending on the error, it is transformed into one of CellError,
        RowError, or Error.
        """
        region = self.location
        if involves_single_cell(region):

            class CustomCellError(frerrors.CellError):
                """Custom error class"""

                type = self.type.value
                title = self.title
                tags = [t.value for t in self.tags]
                template = "{note}"
                description = ""

            return CustomCellError(
                note=self.message,
                cells=[],
                row_number=region.row_number,
                cell=self._validated_values[0],
                field_name=region.field_info.label,
                field_number=region.field_info.position,
            )

        elif involves_single_row(region):

            class CustomRowError(frerrors.RowError):
                """Custom error class"""

                type = self.type.value
                title = self.title
                tags = [t.value for t in self.tags]
                template = "{note}"
                description = ""

            return CustomRowError(
                note=self.message,
                cells=[],
                row_number=region.row_number,
            )

        else:

            class CustomError(frerrors.Error):
                type = self.type.value
                title = self.title
                tags = [t.value for t in self.tags]
                template = "{note}"
                description = ""

            return CustomError(note=self.message)

    @staticmethod
    def _get_field(error: frictionless.Error, schema: Schema) -> Optional[Field]:
        if isinstance(error, frerrors.CellError):
            label = error.field_name
            field = schema.find_field_in_schema(label)
        else:
            field = None
        return field

    def to_dict(self) -> Dict[str, JSON]:
        d = {
            "title": self.title,
            "message": self.message,
            "type": self.type.value,
            "tags": [tag.value for tag in self.tags],
        }

        location = self.location
        if involves_single_row(location):
            d["rowNumber"] = location.row_number

        if involves_single_field(location):
            field = location.field_info
            d["fieldName"] = field.label
            d["fieldNumber"] = field.position

        if len(self._validated_values) == 1:
            d["cell"] = self._validated_values[0]
        elif len(self._validated_values) > 1:
            d["cells"] = self._validated_values

        return d


class PartialError(Protocol):
    """Class used mostly for typing. A partial Error is an error that already has content,
    but still needs to have some context provided to be complete. See the
    `Error.with_context` and `Error.with_no_context` documentations.

    It allows for the separation of concerns, but with static typing ensuring
    that both content and context must be specified for the error to be complete.
    """

    def with_context(
        self,
        validated_values: List[Any] = [],
        location: TableRegion = TableRegion(),
        details: Options = Options(),
        violated_constraint: Optional[Constraint] = None,
        locale: Optional[Locale] = None,
    ) -> Error: ...

    def with_no_context(self) -> Error: ...


CONSTRAINT_RE = re.compile(r'^constraint "([^"]+)" is .*$')
ARRAY_CONSTRAINT_RE = re.compile(r'^array item constraint "([^"]+)" is .*$')


def _extract_constraint_from_message(err: frerrors.Error) -> str:
    m = CONSTRAINT_RE.match(err.note) or ARRAY_CONSTRAINT_RE.match(err.note)

    return m[1] if m else ""


def translate_message(err: Error, locale: Locale) -> Translation:
    """Translate an error message with a locale

    If for whatever reason the translation is not possible, return an
    empty translation `("", "")` to use the original message
    """
    if err.type == ErrType.EXTRA_CELL:
        return locale.extra_cell()

    elif err.type == ErrType.TYPE_ERROR:
        assert len(err._validated_values) == 1
        cell_value = err._validated_values[0]

        return _type_error(cell_value, err._field_info, locale)

    elif err.type == ErrType.CONSTRAINT_ERROR:
        assert len(err._validated_values) == 1
        assert err._violated_constraint
        cell_value = err._validated_values[0]

        return _constraint_error(
            err._violated_constraint.violated_constraint,
            err._violated_constraint.constraint_value,
            cell_value,
            err._field_info,
            locale,
        )

    elif err.type == ErrType.MISSING_CELL:
        return locale.missing_cell()

    elif err.type == ErrType.UNIQUE_ERROR:
        return locale.unique_error()

    elif err.type == ErrType.TRUNCATED_VALUE:
        return locale.truncated_value()

    elif err.type == ErrType.FORBIDDEN_VALUE:
        return locale.forbidden_value()

    elif err.type == ErrType.SEQUENTIAL_VALUE:
        return locale.sequential_value()

    elif err.type == ErrType.ASCII_VALUE:
        return locale.ascii_value()

    elif err.type == ErrType.BLANK_HEADER:
        return locale.blank_header()

    elif err.type == ErrType.DUPLICATE_LABEL:
        return locale.duplicate_labels()

    elif err.type == ErrType.MISSING_LABEL:
        assert involves_single_field(err.location)
        expected_label = err.location.field_info.label
        if expected_label:
            return locale.missing_label(expected_label)

    # Resource errors
    elif err.type == ErrType.ENCODING_ERROR:
        return locale.encoding()

    # Row errors
    elif err.type == ErrType.BLANK_ROW:
        return locale.blank_row()

    elif err.type == ErrType.PRIMARY_KEY:
        return locale.primary_key()

    elif err.type == ErrType.FOREIGN_KEY:
        return locale.foreign_key()

    elif err.type == ErrType.DUPLICATE_ROW:
        return locale.duplicate_row()

    elif err.type == ErrType.ROW_CONSTRAINT:
        return locale.row_constraint()

    return "", ""


def _type_error(cell_value: Any, details: Options, locale: Locale) -> Translation:
    """Return french name and french message related to
    'type' frictionless error.

    If some details are missing of wrong type, then the data does not meet the
    expectations of a type error and raise an error.
    """

    try:
        field_type_str: str = details.get("type", str)
        field_type: FieldType = FieldType(field_type_str)

    except Exception:
        return ("", "")

    if field_type == FieldType.STRING:
        str_format = details.get("format", str, "default")
        return locale.string_type(str_format)

    elif field_type == FieldType.NUMBER:
        return locale.number_type(cell_value)

    elif field_type == FieldType.INTEGER:
        return locale.integer_type(cell_value)

    elif field_type == FieldType.BOOLEAN:
        true_values = details.get("trueValues", List[str], DEFAULT_TRUE_VALUES)
        false_values = details.get("falseValues", List[str], DEFAULT_FALSE_VALUES)
        return locale.boolean_type(true_values, false_values)

    elif field_type == FieldType.OBJECT:
        return "", ""

    elif field_type == FieldType.ARRAY:
        return locale.array_type()

    elif field_type == FieldType.LIST:
        # delimiter = details.get("delimiter", str, ",")
        # item_type = details.get("itemType", str, "any")
        # return locale.list_type(delimiter, item_type)
        return "", ""

    elif field_type == FieldType.DATE:
        date_format = details.get("format", str, "default")
        return locale.date_type(cell_value, date_format)

    elif field_type == FieldType.TIME:
        return "", ""

    elif field_type == FieldType.DATETIME:
        return "", ""

    elif field_type == FieldType.YEAR:
        return locale.year_type(cell_value)

    elif field_type == FieldType.YEARMONTH:
        return "", ""

    elif field_type == FieldType.DURATION:
        return "", ""

    elif field_type == FieldType.GEOPOINT:
        return "", ""

    elif field_type == FieldType.GEOJSON:
        return "", ""

    elif field_type == FieldType.ANY:
        return "", ""

    return (
        "Type non supporté",
        f"Type non supporté ou paramètre manquant : {field_type.value}",
    )


def _constraint_error(
    violated_constraint: str,
    constraint_value: Any,
    validated_value: Any,
    details: Options,
    locale: Locale,
) -> Translation:
    """Return french message related to 'constraint' frictionless error."""

    if violated_constraint == "required":
        return locale.required()

    if violated_constraint == "unique":
        return locale.unique()

    if violated_constraint == "minLength":
        return locale.min_length(validated_value, constraint_value)

    if violated_constraint == "maxLength":
        return locale.max_length(validated_value, constraint_value)

    if violated_constraint == "minimun":
        return locale.minimum(validated_value, constraint_value)

    if violated_constraint == "maximum":
        return locale.maximum(validated_value, constraint_value)

    if violated_constraint == "pattern":
        example = details.get("example", str, default="")
        return locale.pattern(validated_value, example, constraint_value)

    if violated_constraint == "enum":
        return locale.enum(constraint_value)

    return "", ""


def _correct_schema_sync_bug(err: Error) -> Error:
    """With the `schema_sync` option, an untyped error can be returned. This
    function corrects the error type.

    This is an upstream bug, related to https://github.com/frictionlessdata/frictionless-py/issues/1339
    """
    if err._message == '"schema_sync" requires unique labels in the header':
        err.type = ErrType.DUPLICATE_LABEL
    return err
