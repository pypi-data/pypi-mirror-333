import click
from sqlalchemy.orm import Session

from hakisto import logger
from .get_dynamic_param_decls import get_dynamic_param_decls


def list_command(click_group: click.Group, table_class):
    @click_group.command(name="list", short_help=f"List content of '{table_class.display_name__}'")
    @click.option("--show-internal", is_flag=True, help="Show columns and records used internally (usually hidden)")
    @click.option("--markdown", is_flag=True, help="Show as Markdown")
    @click.pass_context
    def cmd(ctx, show_internal, markdown, **kwargs):
        logger.debug(f"markdown: {markdown}")
        with Session(ctx.obj["engine"]) as session:
            display_table = table_class.cli_crud_list__(session=session, show_internal=show_internal, **kwargs)

            if markdown:
                print(display_table.markdown())
            else:
                print(display_table.ascii())

            logger.info(f"Found {len(display_table)} records")

    if hasattr(table_class, "search__"):
        cmd.params.append(click.Argument(("search",), required=False))
        cmd.params.append(click.Option(("--regex",), is_flag=True, help="Prompt for Regular Expression (RegEx)"))

    short = set(" hv")

    for i in getattr(table_class, "STATUS__", tuple()):
        name = i.lower().replace(" ", "-")
        cmd.params.append(
            click.Option(get_dynamic_param_decls(short=short, name=name), is_flag=True, help=f"with status {i}")
        )

    for i in table_class.CLI_LIST_FILTER__:
        cmd.params.append(
            click.Option(get_dynamic_param_decls(short=short, name=i.name), help=f"filter by {i.description}")
        )
