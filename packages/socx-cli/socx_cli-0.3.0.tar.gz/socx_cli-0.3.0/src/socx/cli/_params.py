import logging
from functools import partial

import rich_click as click

from . import _cli

socx = partial(
    click.command,
    "socx",
    cls=_cli.CmdLine,
    no_args_is_help=True,
    invoke_without_command=True,
)

help_ = partial(click.help_option, "--help", "-h")

debug = partial(
    click.option,
    "--debug",
    "-d",
    envvar="SOCX_DEBUG",
    type=click.BOOL,
    default=False,
    is_flag=True,
    show_envvar=True,
    show_default=True,
    expose_value=True,
    help="Run in debug mode.",
)

verbosity = partial(
    click.option,
    "--verbosity",
    "-v",
    nargs=1,
    envvar="SOCX_VERBOSITY",
    default="INFO",
    type=click.Choice(
        logging.getLevelNamesMapping().keys(),
        case_sensitive=False,
    ),
    show_envvar=True,
    show_choices=True,
    show_default=True,
    expose_value=True,
    help="set the logging verbosity to the specified level.",
)

configure = partial(
    click.option,
    "--configure/--no-configure",
    type=click.BOOL,
    default=True,
    is_flag=True,
    show_envvar=True,
    show_default=True,
    expose_value=True,
    help="Load/Don't-Load local user configuration overrides.",
)
