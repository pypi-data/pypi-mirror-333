import re

from hakisto import logger
from imuthes import DisplayColumn, DisplayTable


class CliCrudMixin:
    """Mixin to provide CRUD functionality"""

    CLI_LIST_COLUMNS__ = []
    CLI_LIST_FILTER__ = tuple()

    @classmethod
    def cli_crud_list__(cls, session, show_internal, **kwargs) -> DisplayTable:
        logger.debug(kwargs)
        logger.debug(f"show_internal: {show_internal}")
        if "regex" in kwargs:
            if kwargs.pop("regex"):
                kwargs["search"] = re.compile(input("Regular Expression (RegEx): "))
        columns_to_include = cls.CLI_LIST_COLUMNS__[:]
        if show_internal:
            columns_to_include.insert(0, DisplayColumn("id", ">", header="ID"))
            # noinspection PyUnresolvedReferences
            if "default_flag_" in cls.get_columns__():
                columns_to_include.append(DisplayColumn("default_flag_", header="Default Record"))
            # noinspection PyUnresolvedReferences
            if "system_flag_" in cls.get_columns__():
                columns_to_include.append(DisplayColumn("system_flag_", header="System Use"))
        display_table = DisplayTable(*columns_to_include)

        # noinspection PyUnresolvedReferences
        for row in cls.get__(
            session=session,
            search__=kwargs.pop("search", None),
            statuses__=(k for k, v in kwargs.items() if v is True),
            **{i.column: kwargs[i.name] for i in cls.CLI_LIST_FILTER__ if kwargs[i.name]},
        ):
            if not show_internal and getattr(row, "system_flag_", False):
                continue
            display_table.append(row)

        return display_table
