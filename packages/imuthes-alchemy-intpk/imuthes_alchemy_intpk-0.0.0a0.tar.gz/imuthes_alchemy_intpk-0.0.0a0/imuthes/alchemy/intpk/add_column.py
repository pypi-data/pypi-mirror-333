class AddColumn:

    def __init__(
        self,
        name: str,
        description: str = None,
        column: str = None,
        empty_ok: bool = True,
    ) -> None:
        self.name = name
        self.column = column or name
        self.description = description or name
        self.empty_ok = empty_ok
