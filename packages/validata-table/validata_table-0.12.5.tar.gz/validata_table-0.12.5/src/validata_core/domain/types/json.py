from typing import Dict, List, Union

JSONPrimitive = Union[str, int, bool, float, None]
JSON = Union[Dict[str, "JSON"], List["JSON"], JSONPrimitive]
