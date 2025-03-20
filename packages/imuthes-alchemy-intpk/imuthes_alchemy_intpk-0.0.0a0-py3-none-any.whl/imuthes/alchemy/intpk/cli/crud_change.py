import json
import pathlib
import re

import click
from click_default_group import DefaultGroup
from sqlalchemy.testing.plugin.plugin_base import requirements

from hakisto import logger

from imuthes import DisplayColumn, DisplayTable
from imuthes.alchemy import Deferrer
from imuthes.alchemy.engine import get_engine
from sqlalchemy.orm import Session

from imuthes.alchemy.intpk import FilterColumn
from .get_dynamic_param_decls import get_dynamic_param_decls


def change_command(click_group: click.Group, table_class):

    @click_group.command(name="change", short_help=f"Change '{table_class.display_name__}'")
    @click.pass_context
    def cmd(ctx, **kwargs):
        logger.debug(kwargs)
        pk = {}
        for i in table_class.get_unique_constraint__():
            pk[i.name] = kwargs.pop(i.name)
        with Session(ctx.obj["engine"]) as session:
            record = table_class.get__(session=session, requirement__="1", **pk)
            for i in table_class.CLI_CHANGE_COLUMNS__:
                if kwargs[i.name] is not None and (i.empty_ok or kwargs[i.name]):
                    setattr(record, i.name, kwargs[i.name])
            session.commit()
            logger.success(f"{record!r}")

    for i in table_class.get_unique_constraint__():
        cmd.params.append(click.Argument((i.name,)))

    short = set(" hv")
    for i in table_class.CLI_CHANGE_COLUMNS__:
        cmd.params.append(click.Option(get_dynamic_param_decls(short=short, name=i.name), help=f"new {i.description}"))
