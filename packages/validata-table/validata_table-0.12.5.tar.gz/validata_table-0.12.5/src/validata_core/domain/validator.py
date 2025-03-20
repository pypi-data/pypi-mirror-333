"""
This module provides utilities to define validation logic for custom checks.

For that purpose it introduces the `Validator` class.

A `Validator` needs to be wrapped by a `Check` to be used by a validation
service.
"""

from abc import ABC
from dataclasses import dataclass
from functools import wraps
from typing import Callable, Generic, Optional, Protocol, TypeVar

from validata_core.domain.types import Options, PartialError

T = TypeVar("T")


@dataclass(frozen=True)
class FieldValue(Generic[T]):
    """Stores a field label along its value

    The field label allows for more explicit error messages, by differenciating the
    values with their label.
    """

    value: T
    label: str


class Validator(Protocol):
    """An interface to define validation logic for field-based custom check

    The `validate` method implements the validation logic.

    The validator can take options, which can be declared inside
    the `__init__` function, like follows:

    ```
    self._my_option = options.declare("my_option", int, default = 0)
    ```

    Any missing / wrongly typed option in the input data will be
    handled by the caller. If this validation is not sufficient, additionnal
    valdiation can be performed in `__init__`, and throw an Exception if options are invalid.
    """

    def __init__(self, options: Options):
        pass

    validate: Callable[..., Optional[PartialError]]
    """Takes FieldValues (each argument stores a `FieldValue` or a
    `List[FieldValue]`) and issues an Error if validation fails.

    The error is only partially defined as the validator has no information
    about the validation context, which is dealt by the `Check` class.

    See the `single_value` decorator for a simplified signature for single
    value validation.
    """


class BaseValidator(ABC, Validator):
    """A base implementation with no option"""

    def __init__(self, options: Options):
        pass


def single_value(method):
    """A decorator to simplify single value validators

    This decorator, applied to the `validator` method of a `Validator`, allows
    to directly have the value as argument, instead of a `FieldValue` (value +
    label).

    Indeed, single value validation does not need to differentiate values (as there is
    only one), so dropping the label simplifies the method signature.
    """

    @wraps(method)
    def inner_validate(self, labeled_value: FieldValue) -> Optional[PartialError]:
        return method(self, labeled_value.value)

    return inner_validate
