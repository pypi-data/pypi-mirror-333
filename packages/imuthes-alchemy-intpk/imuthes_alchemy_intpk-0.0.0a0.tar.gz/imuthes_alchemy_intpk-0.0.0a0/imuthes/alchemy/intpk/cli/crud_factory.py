from itertools import chain

import click
from click_default_group import DefaultGroup

from .crud_list import list_command
from .crud_activate import activate_command
from .crud_deactivate import deactivate_command
from .crud_change import change_command
from .crud_add import add_command


def table_command(table_class):
    # noinspection PyUnusedLocal
    @click.group(
        name=table_class.__tablename__.replace("_", "-"),
        short_help=table_class.display_name__,
        cls=DefaultGroup,
        default="list",
        default_if_no_args=True,
    )
    @click.pass_context
    def grp(ctx):
        pass

    if table_class.CLI_LIST_COLUMNS__:
        list_command(click_group=grp, table_class=table_class)

    if hasattr(table_class, "CLI_ADD_COLUMNS__"):
        add_command(click_group=grp, table_class=table_class)

    if hasattr(table_class, "CLI_CHANGE_COLUMNS__"):
        change_command(click_group=grp, table_class=table_class)

    if hasattr(table_class, "STATUS__"):
        status_targets = set(chain(*[i for i in table_class.STATUS__.values()]))
        if "ACTIVE" in status_targets:
            activate_command(click_group=grp, table_class=table_class)
        if "INACTIVE" in status_targets:
            deactivate_command(click_group=grp, table_class=table_class)

    return grp
