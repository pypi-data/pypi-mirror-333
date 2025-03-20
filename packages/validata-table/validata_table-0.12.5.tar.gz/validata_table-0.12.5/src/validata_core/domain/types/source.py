from pathlib import Path
from typing import Dict, List, Sequence, Union

from validata_core.domain.types.json import JSONPrimitive

CellValue = JSONPrimitive

Row = Sequence[CellValue]
Header = Sequence[str]  # a Header is a Row
InlineArrayOfArrays = Sequence[Row]

# Each object has headers as properties
InlineArrayOfObjects = List[Dict[str, CellValue]]

InlineData = Union[
    InlineArrayOfArrays,
    InlineArrayOfObjects,
]

PathSource = Union[str, Path]

Source = Union[PathSource, InlineData]
