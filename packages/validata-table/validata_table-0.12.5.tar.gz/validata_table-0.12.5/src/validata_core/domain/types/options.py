from typing import Any, Dict, Optional, Type, TypeVar

from validata_core.domain.dict_parser import DictParser

T = TypeVar("T")


class Options(DictParser):
    """Options deals with secure access to a Validator's parameters"""

    def __init__(self, data: Dict[str, Any] = {}):
        super().__init__(data)
        self._defaults = {}

    def declare(self, option: str, type: Type[T], default: Optional[T] = None) -> T:
        """Declares an expected option

        Any option without default is considered required.

        Declaring an option is actually nothing more than trying to
        extract it with parent `DictParser.get`. However, this alias' name is more
        natural when the option is extracted to be stored inside the Validator
        object with a proper type. It suggests that the errors should not be
        directly handled, which is the case.

        Raises:
            - KeyError
            - TypeError
        """
        return super().get(option, type, default)
