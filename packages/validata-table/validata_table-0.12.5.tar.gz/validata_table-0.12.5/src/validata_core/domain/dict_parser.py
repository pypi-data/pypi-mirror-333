from typing import (
    Any,
    Dict,
    Iterator,
    Optional,
    Tuple,
    Type,
    TypeVar,
    cast,
    get_args,
    get_origin,
)

T = TypeVar("T")


class DictParser:
    """The dict parser allows to extract from a dict a value if it matches
    exactly an expected type. It is read-only.

    """

    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def get(self, key: str, expected_type: Type[T], default: Optional[T] = None) -> T:
        """
        Raises:
           KeyError: missing key
           TypeError: the value could not be casted to the expected_type
        """
        if key not in self._data:
            if default is None:
                raise KeyError(
                    f"Key '{key}' is missing and no default value is provided."
                )
            value = default
        else:
            value = self._data[key]

            # Type check with support for lists, e.g. List[str]
            origin_type = get_origin(expected_type)
            args_type = get_args(expected_type)

            if origin_type is not None:
                if not isinstance(value, origin_type):
                    raise TypeError(
                        f"Key '{key}' has type {type(value).__name__}, expected {origin_type.__name__}."
                    )
                if args_type:
                    if origin_type is list and not all(
                        isinstance(item, args_type[0]) for item in value
                    ):
                        raise TypeError(
                            f"Key '{key}' contains elements of incorrect type."
                        )

            elif not isinstance(value, expected_type):
                raise TypeError(
                    f"Key '{key}' has type {type(value).__name__}, expected {expected_type.__name__}."
                )

        return cast(T, value)

    def __iter__(self) -> Iterator[str]:
        """Return an iterator over the keys of the dictionary."""
        return iter(self._data)

    def items(self) -> Iterator[Tuple[str, Any]]:
        """Return an iterator over the items (key-value pairs) of the dictionary."""
        return iter(self._data.items())

    def keys(self) -> Iterator[str]:
        """Return an iterator over the keys of the dictionary."""
        return iter(self._data.keys())

    def values(self) -> Iterator[Any]:
        """Return an iterator over the values of the dictionary."""
        return iter(self._data.values())

    def __repr__(self):
        return self._data.__repr__()
