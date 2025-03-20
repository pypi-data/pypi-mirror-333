from typing import NamedTuple


class ChangeColumn(NamedTuple):
    name: str
    description: str
    empty_ok: bool = True
