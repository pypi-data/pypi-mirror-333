from dataclasses import dataclass
from typing import List, Optional, overload

from typing_extensions import TypeGuard


@dataclass
class FieldInfo:
    label: str
    position: int
    """1-indexed position of the field in the table"""


class TableRegion:
    """Represents a subset/region of a table

    It can represent the whole table, a row (whole row, or several cells of a
    row), one or several columns, or a cell (intersection of a single
    row and a column).

    See type narrowing functions `involves_single_row`, `involves_single_field`
    and `involves_single_cell`.

    Params:
        row_number:
            Number of the row to subset, 1 indexed, starting at the header. If None is
            provided, then the context covers all rows.
        fields_info:
            Specific fields (columns) to subset. If None is provided (or an
            empty List), then the context covers all fields.
    """

    def __init__(
        self,
        row_number: Optional[int] = None,
        fields_info: Optional[List[FieldInfo]] = None,
    ):
        self.row_number = row_number
        self.fields_info = fields_info

    @property
    def field_info(self) -> Optional[FieldInfo]:
        """Returns the field info if there is only one field, None otherwiser"""
        fields_info = self.fields_info
        if fields_info and len(fields_info) == 1:
            return fields_info[0]
        return None

    def __repr__(self) -> str:
        if involves_single_cell(self):
            return f"CellRegion(row={self.row_number}, field={self.field_info})"
        elif involves_single_row(self):
            if self.fields_info:
                return f"RowRegion(row={self.row_number}, fields={self.fields_info})"
            return f"WholeRow(row={self.row_number})"
        elif involves_single_field(self):
            return f"FieldRegion(field={self.field_info})"
        else:
            return "WholeTableRegion"


def involves_single_row(region) -> TypeGuard["RowRegion"]:
    """Checks whether a region is a whole row or contained inside a single row"""
    return region.row_number is not None


def involves_single_field(region) -> TypeGuard["SingleFieldRegion"]:
    """Checks whether a region is a all or a subset of a single field/column"""
    return region.fields_info and len(region.fields_info) == 1


def involves_single_cell(region) -> TypeGuard["CellRegion"]:
    """Checks whether a region is a single cell"""
    return involves_single_field(region) and involves_single_row(region)


# Following classes are used for type narrowing


@dataclass
class RowRegion(TableRegion):
    """A class for static typing purposes"""

    row_number: int
    fields_info: None

    @property
    @overload
    def field_info(self) -> None: ...


@dataclass
class SingleFieldRegion(TableRegion):
    """A class for static typing purposes"""

    row_number: Optional[int]
    fields_info: List[FieldInfo]

    @property
    @overload
    def field_info(self) -> FieldInfo: ...


@dataclass
class CellRegion(TableRegion):
    """A class for static typing purposes"""

    fields_info: List[FieldInfo]
    row_number: int

    @property
    @overload
    def field_info(self) -> FieldInfo: ...
