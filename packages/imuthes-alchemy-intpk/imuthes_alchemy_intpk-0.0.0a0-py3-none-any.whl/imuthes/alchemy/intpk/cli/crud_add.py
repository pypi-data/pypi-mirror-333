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


def add_command(click_group: click.Group, table_class):

    @click_group.command(name="add", short_help=f"Add '{table_class.display_name__}'")
    @click.pass_context
    def cmd(ctx, **kwargs):
        kwargs = {k: v for k, v in kwargs.items() if v}
        with Session(ctx.obj["engine"]) as session:
            record = table_class(**kwargs)
            session.add(record)
            session.commit()
            logger.success(f"{record!r}")

    short = set(" hv")
    for i in table_class.CLI_ADD_COLUMNS__:
        kwargs = {}
        if not i.empty_ok:
            kwargs["prompt"] = i.description
            kwargs["required"] = True
        cmd.params.append(
            click.Option(get_dynamic_param_decls(short=short, name=i.name), help=f"{i.description}", **kwargs)
        )
