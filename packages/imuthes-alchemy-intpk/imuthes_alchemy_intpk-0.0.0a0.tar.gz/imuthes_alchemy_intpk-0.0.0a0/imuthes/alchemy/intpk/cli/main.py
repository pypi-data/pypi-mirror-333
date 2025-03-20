import click

from hakisto import logger
from hakisto._click.file import hakisto_file
from hakisto._click import hakisto_process_severity, hakisto_process_file
from hakisto._click.severity import hakisto_severity

from .crud_factory import table_command
from .. import Status
from ... import get_engine


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@hakisto_severity()
@hakisto_file()
@click.pass_context
def main(ctx, log_severity, log_file):
    """Imuthes Database with Integer Primary Key"""
    hakisto_process_severity(log_severity)
    hakisto_process_file(log_file)
    ctx.ensure_object(dict)
    ctx.obj["engine"] = get_engine("sqlite:///sandbox.db")


@main.command()
@click.pass_context
def create_database(ctx):
    """Create Database and populate with default content"""
    from ... import Deferrer
    from .. import Base

    logger.info(f"Creating database at »{ctx.obj['engine'].url}«")
    deferrer = Deferrer()
    Base.metadata.create_all(ctx.obj["engine"])
    deferrer.execute(ctx.obj["engine"])


main.add_command(table_command(Status))
