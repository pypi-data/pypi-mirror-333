from dataclasses import dataclass
from typing import Dict, Optional

from .json import JSON
from .options import Options


@dataclass
class CheckDescriptor:
    """
    Descriptor-like information of an additional data check that extends Table Schema
    specification.

    This descriptor is actually never encountered like this in the schema, but
    brings together the two supported ways of defining a custom check (as a
    field property, or in a top level property).
    """

    name: str

    column: Optional[str]
    """
    Holds the name of the column for checks that are performed on a single
    column.

    For checks that are performed on multiple columns, holds the name of the
    column to which associate a cell error. If undefined, any error will be
    a RowError.

    Other column names are stored in the `params` properties, as there is no
    standard way to define them.
    """

    params: Options

    def __init__(self, name, column, params: Dict[str, JSON]):
        self.name = name
        self.column = column
        self.params = Options(params)
