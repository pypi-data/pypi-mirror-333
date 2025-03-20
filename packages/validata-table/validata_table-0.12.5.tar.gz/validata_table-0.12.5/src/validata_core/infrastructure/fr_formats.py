import inspect
import re
from dataclasses import dataclass
from typing import Any, Dict, Set

from frformat import all_formats

from validata_core.domain.check import Check, CheckRepository
from validata_core.domain.types import CheckDescriptor, Error, ErrType
from validata_core.domain.validator import Validator, single_value


class FrFormatsRepository(CheckRepository):
    """Repository of all checks built from `frformat` dependency.

    See parent class for general information.
    """

    def __init__(self):
        self._formats = {
            _pascal_to_kebab_case(format.__name__): format for format in all_formats
        }

    def ls(self) -> Set[str]:
        return set(self._formats.keys())

    def create_instance(self, check: CheckDescriptor):
        if check.name not in self.ls():
            return None

        if not check.column:
            raise Exception("Internal error")

        frformat_title = check.name.replace("-", " ").title()
        format_cls = self._formats[check.name]

        class FrFormatAdapter(Validator):
            def __init__(self, options):
                keyword_match = _match_kwargs(format_cls.__init__, check.params._data)

                missing = keyword_match.missing_params
                if missing:
                    raise Exception(
                        "Paramètre obligatoire manquant dans le custom check"
                        f"{format_cls.metadata.name} (`{check.name}`) : {', '.join(missing)}. "
                        "Veuillez corriger le schéma."
                    )

                self._frformat_instance = format_cls(**keyword_match.valid_kwargs)

            @single_value
            def validate(self, value: Any):
                valid: bool = True
                message: str = ""

                if hasattr(
                    self._frformat_instance, "is_valid_with_details"
                ) and callable(
                    getattr(self._frformat_instance, "is_valid_with_details")
                ):
                    valid, details = self._frformat_instance.is_valid_with_details(
                        value
                    )
                    if not valid:
                        message = ", ".join(details)
                else:
                    valid = self._frformat_instance.is_valid(value)
                    message = (
                        f"La valeur n'est pas conforme au format {frformat_title}."
                    )

                if not valid:
                    return Error.new(
                        "Format Invalide",
                        message,
                        ErrType.CUSTOM_CHECK_ERROR,
                    )

        return Check(frformat_title, FrFormatAdapter).create_instance(check)


@dataclass
class _KwargsData:
    """See documentation of _match_kwargs"""

    valid_kwargs: Dict[str, Any]
    missing_params: set[str]


def _match_kwargs(func, kwargs: Dict[str, Any]) -> _KwargsData:
    """
    Try to match `kwargs` with the expected keywords of `func`, with two
    return values:

    - "valid_kwargs" holds keys that are valid keywords of `func`
    the signature of `func`

    - "missing_params" are the required `func` keyword parameters that are missing from `kwargs`
    """
    signature = inspect.signature(func)
    params = signature.parameters

    valid_kwargs = {k: v for k, v in kwargs.items() if k in params}

    required_params = {
        name
        for name, param in params.items()
        if param.default == inspect.Parameter.empty
        and param.kind
        in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY)
        and name != "self"
    }
    missing_params = required_params - valid_kwargs.keys()

    return _KwargsData(valid_kwargs, missing_params)


def _pascal_to_kebab_case(name):
    """Not flawless, but avoids a dependency"""
    name = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1-\2", name).lower()
