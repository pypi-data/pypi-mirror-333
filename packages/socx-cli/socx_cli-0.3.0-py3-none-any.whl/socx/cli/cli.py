from __future__ import annotations

import logging

from trogon import tui
import rich_click as click

from . import _params
from ..log import set_level
from ..config import settings
from ..config import reconfigure
from ..config import USER_CONFIG_DIR


@tui()
@_params.socx()
@_params.debug()
@_params.verbosity()
@_params.configure()
def cli(**options) -> None:
    """System on chip verification and tooling infrastructure."""
    settings.update({"cli": options})
    if settings.cli.debug:
        settings.cli.verbosity = logging.getLevelName(logging.DEBUG)
    set_level(settings.cli.verbosity)
    if settings.cli.configure:
        reconfigure(USER_CONFIG_DIR / "*.toml", [], ["*.toml"])
    ctx: click.Context = click.get_current_context()
    if ctx.invoked_subcommand is None:
        formatter = ctx.make_formatter()
        cli.format_help(ctx, formatter)
