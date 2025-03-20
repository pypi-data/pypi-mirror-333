import json
import pathlib
import re
import sys

import click
from click_default_group import DefaultGroup
from hakisto import logger

from imuthes import DisplayColumn, DisplayTable
from imuthes.alchemy import Deferrer
from imuthes.alchemy.engine import get_engine
from sqlalchemy.orm import Session

from ..exceptions import StatusChangeNotPermittedError


def activate_command(click_group: click.Group, table_class):

    @click_group.command(name="activate", short_help=f"Activate '{table_class.display_name__}'")
    @click.pass_context
    def cmd(ctx, **kwargs):
        logger.debug(kwargs)
        with Session(ctx.obj["engine"]) as session:
            row = table_class.get__(session=session, requirement__="1", **kwargs)
            try:
                row.change_status__("ACTIVE")
            except StatusChangeNotPermittedError as e:
                logger.error(str(e))
                sys.exit(-1)
            session.commit()
            logger.success(f"Activated {row}")

    for i in table_class.get_unique_constraint__():
        cmd.params.append(click.Argument((i.name,)))
