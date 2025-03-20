"""
This module provides the `Check` and `CheckRepository` classes, which are
utilities for adding new custom check capabilities to the validation service.

A `Check` wraps the validation logic from a Validator (see
validator.py) into a full-blown check, with support and sensible default
behavior for missing columns and options. To be operational, a check needs to
be instantiated into a `CheckInstance` by providing all concrete information
(specific options, on what column to apply the check, etc.). The
`CheckInstance` can then be converted into a `frictionless.Check`.

A `CheckRepository` is a collection of `Check`s.
"""

import inspect
from dataclasses import dataclass
from typing import (
    Callable,
    List,
    Literal,
    Optional,
    Protocol,
    Sequence,
    Set,
    Type,
    Union,
    overload,
)

import attrs
import frictionless

import validata_core.domain.utils as utils
from validata_core.domain.types import (
    CheckDescriptor,
    Error,
    FieldInfo,
    PartialError,
    TableRegion,
)
from validata_core.domain.validator import FieldValue, Validator


@dataclass(frozen=True)
class FieldParam:
    """A FieldParam is a specific check parameter, that refers to one or
    multiple field names of the data.

    Specifying the parameter to represent a single field (`holds_multiple=False`) sets the expectation
    that its value is a string (the field name). If it represents multiple
    fields (`holds_multiple=True`), then its value is expected to be a list of strings (the field names).
    """

    name: str
    holds_multiple: bool = False


MissingFieldsHandler = Callable[
    [Sequence[Union[str, List[str]]], List[str]], Optional[PartialError]
]


def default_missing_fields_handler(
    expected_fields, observed_fields
) -> Optional[PartialError]:
    return None


class Check:
    """
    A base class for defining new validation capabilities, in addition to the Table Schema
    specification, by wrapping a Validator class.

    As rows are validated independently, its perimeter is limited to validation that can
    apply in the context of a single row of data.

    Before validating any data, a specific check instance must first be
    created (method `create_instance`) with schema provided options and parameters.
    """

    def __init__(
        self,
        name: str,
        validator_class: Type[Validator],
        field_params: List[Union[str, FieldParam]] = ["column"],
        skip_if_missing_values: bool = True,
        missing_fields_handler: MissingFieldsHandler = default_missing_fields_handler,
    ):
        """
        By default, validation errors are created on the cell of the first field (in the order of `field_params`).

        Params:
            - name:
                A name that can be used as an identifier to refer to the
                check. Usually in kebab case.

            - validator_class:
                Class that holds the validation logic

                Values to be validated are extracted from the data given the
                `field_params` value, and presented in the same order. If any
                field is missing, it is treated as a missing value (value = `None`)

                By default, any missing value skips the validation, see
                `skip_if_missing_values`.

            - field_params:
                Parameters that hold the names of the fields to be validated.

                Each parameter stores a single name of field, except for the
                last one that can also store a list of fields (using a
                `FieldParam`).

            - skip_if_missing_values:
                If True, if a value being passed to the `validator_class.validate`
                method is missing from the current row, then skip the row
                validation.

                This is a sensible behavior if the check cannot be performed
                in case of missing values. It is the responsibility of the
                Table Schema `required` keyword to determine requiredness.
                Disable if the check's concern is specifically about requiredness.

            - missing_fields_handler:
                Optional missing fields handling, if something more complex
                than the default behavior is needed (default behavior: any
                missing field is treated as a missing value).
                The handler is a function, that takes two inputs : the expected fields and
                the observed fields, and can return an error if needed (None
                otherwise). No need to set the error context which will
                automatically set.

        """
        self.name = name

        self.skip_if_missing_values = skip_if_missing_values

        self._validator_class = validator_class
        self._field_params: List[Union[str, FieldParam]] = field_params

        self._missing_fields_handler = missing_fields_handler

        validate_signature = inspect.signature(self._validator_class.validate)

        assert (
            len(field_params) == len(validate_signature.parameters) - 1
        ), f"""
            length of field_params ({field_params}) should match the number of
            parameters of validate method signature, `self` aside
            ({str(validate_signature)})
            """

    def create_instance(self, check_descriptor: CheckDescriptor) -> "CheckInstance":
        """
        Raises:
            Exception: something went wrong during check instantiation. This
            could be for instance an option or a field parameter missing (`KeyError`) or of wrong type
            (`TypeError`).
        """
        return CheckInstance(self, check_descriptor)


class CheckInstance:
    """
    A check instance has, in addition to a check, a set of use-case specific parameters /
    options to describe how the check should be applied. These options are usually derived
    from the schema.
    """

    def __init__(
        self,
        check: Check,
        check_descriptor: CheckDescriptor,
    ):
        self.check = check
        self.options = check_descriptor.params
        self.column = check_descriptor.column

        validator = self.check._validator_class(check_descriptor.params)
        self._validator = validator

        fields = []

        # Identify data fields associated with the check
        for field_param in self.check._field_params:
            if isinstance(field_param, str):
                field_param = FieldParam(field_param)

            _type = List[str] if field_param.holds_multiple else str

            if field_param.name == "column":
                if not check_descriptor.column:
                    raise KeyError
                field = check_descriptor.column
            else:
                field = check_descriptor.params.get(field_param.name, _type)
            fields.append(field)

        self._fields = fields

        self._check_stopped: bool = False

    def _validate_fields(self, fields: List[str]) -> Optional[Error]:
        """Handle missing fields if needed"""
        err = self.check._missing_fields_handler(self.get_fields(), fields)
        if err is not None:
            err = err.with_context(
                validated_values=fields, location=TableRegion(row_number=1)
            )

        return err

    def to_frictionless_check(self) -> frictionless.Check:
        """Converts the check to a format compatible with frictionless"""
        return _FrictionlessCheckAdapter(self)

    def _validate_row(self, row: frictionless.Row) -> Optional[Error]:
        """
        If check does not apply, or row is valid, returns None
        """

        field_values = self._extract_values_from_row(row)

        if self.check.skip_if_missing_values:
            if any(
                field_value.value is None for field_value in utils.flatten(field_values)
            ):
                return None

        err = self._validator.validate(*field_values)

        if err:
            fields = self.get_fields(flatten=True)
            # If "column" parameter is set, then associate the error to it.
            # Otherwise, issue a row errors
            fields_that_errors = [self.column] if self.column else fields

            field_positions = [
                i + 1
                for i, field in enumerate(row.fields)
                if field.name in fields_that_errors
            ]

            if not field_positions:
                context = TableRegion(row.row_number)
            else:
                context = TableRegion(
                    row.row_number,
                    [
                        FieldInfo(f, pos)
                        for f, pos in zip(fields_that_errors, field_positions)
                    ],
                )
            err = err.with_context(
                location=context,
                validated_values=[v.value for v in utils.flatten(field_values)],
            )

            return err

    def _extract_values_from_row(
        self, row
    ) -> List[Union[FieldValue, List[FieldValue]]]:
        """Extracts values associated to their field names. Missing fields are treated as
        missing values.
        """
        values = []

        for field_labels_data in self._fields:
            if isinstance(field_labels_data, list):
                field_labels = field_labels_data
                values.append(
                    [
                        FieldValue(row.get(field_label, None), field_label)
                        for field_label in field_labels
                    ]
                )
            else:
                field_label = field_labels_data
                values.append(FieldValue(row.get(field_label, None), field_label))

        return values

    def _build_context(self, row: frictionless.Row, field_label: str) -> TableRegion:
        field_info: Optional[FieldInfo] = None
        try:
            index = row.field_names.index(field_label)
            field_position = index + 1  # field number is 1-indexed
            field_info = FieldInfo(field_label, field_position)
        except ValueError:
            pass

        return TableRegion(row.row_number, [field_info] if field_info else None)

    # Overloads are to properly type get_fields output depending on `flatten` value
    @overload
    def get_fields(self, flatten: Literal[True]) -> Sequence[str]: ...

    @overload
    def get_fields(self, flatten: bool) -> Sequence[Union[str, List[str]]]: ...

    @overload
    def get_fields(self) -> Sequence[Union[str, List[str]]]: ...

    def get_fields(self, flatten: bool = False) -> Sequence[Union[str, List[str]]]:
        """Returns all fields. Each parameter can be associated to one field
        (type `str`) or multiple fields (type `List[str]`). In the second
        case, by default, the fields are returned as a nested list, that can
        be flattened with `flatten=True`.
        """
        if flatten:
            return utils.flatten(self._fields)
        return self._fields


@attrs.define(kw_only=True, repr=False)
class _FrictionlessCheckAdapter(frictionless.Check):
    """Adapts validata.check to expected frictionless.Check interface"""

    type = "check"

    Errors = []

    def __init__(
        self,
        check_instance: CheckInstance,
    ):
        self._check_instance = check_instance

    def validate_row(self, row):
        if not self._check_instance or self._check_instance._check_stopped:
            return []

        fields = list(row.keys())
        error = self._check_instance._validate_fields(fields)
        if error:
            frless_error = error._to_frictionless()
            self.Errors.append(frless_error.__class__)
            self._check_instance._check_stopped = True
            return [frless_error]

        error = self._check_instance._validate_row(row)
        if error:
            frless_error = error._to_frictionless()
            self.Errors.append(frless_error.__class__)

            return [frless_error]

        return []

    @classmethod
    def metadata_select_class(cls, type: Optional[str]):
        return cls


class CheckRepository(Protocol):
    """Interface for declaring a collection of custom checks"""

    def ls(self) -> Set[str]:
        """Returns a list of valid check names"""
        ...

    def create_instance(self, check: CheckDescriptor) -> Optional[CheckInstance]:
        """Creates check instance matching the input check information

        Returns None if the check name is not part of the catalog
        Raises an exception if the `check_params` are not formatted as
        expected for the given check.
        """
        ...


def new_check_repository(checks: Sequence[Check]):
    """Helper function that creates a repository from checks"""

    class BaseCheckRepository(CheckRepository):
        def __init__(self, checks):
            self._checks_by_name = {check.name: check for check in checks}

        def ls(self):
            return {check.name for check in checks}

        def create_instance(self, check):
            if check.name not in self.ls():
                return None

            return self._checks_by_name[check.name].create_instance(check)

    return BaseCheckRepository(checks)


def combine_repositories(
    *repositories: CheckRepository,
) -> CheckRepository:
    """Combine multiple repositories into a single one. If multiple checks
    have the same name, then the latter will be shadowed by the first
    encountered.
    """

    class CombinedRepository(CheckRepository):
        def ls(self) -> Set[str]:
            all_ls = set()
            for repository in repositories:
                all_ls.union(repository.ls())
            return all_ls

        def create_instance(self, check: CheckDescriptor) -> Optional[CheckInstance]:
            for repository in repositories:
                if check.name in repository.ls():
                    return repository.create_instance(check)

            return None

    return CombinedRepository()
