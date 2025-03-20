from enum import Enum


class Tag(Enum):
    CELL = "#cell"
    CONTENT = "#content"
    ROW = "#row"
    TABLE = "#table"
    HEADER = "#header"
    LABEL = "#label"
    FILE = "#file"

    # Custom ones
    STRUCTURE = "#structure"
    BODY = "#body"

    def __repr__(self):
        return str(self)
