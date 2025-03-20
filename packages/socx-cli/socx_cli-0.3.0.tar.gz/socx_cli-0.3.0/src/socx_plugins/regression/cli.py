import rich_click as click

from socx_plugins.regression import _params


@click.group("rgr")
def cli():
    """Perform various regression related actions."""


@cli.command()
@_params.input()
@_params.output()
def run(input, output):  # noqa: A002
    """Run a regression from a file of 'socrun' commands."""
    import uvloop
    from socx_plugins.regression._cli import _run_from_file

    uvloop.run(_run_from_file(input, output))


@cli.command()
@_params.input()
@_params.output()
def rrfh(input, output):  # noqa: A002
    """Command alias for rerun-failure-history."""
    import uvloop
    from socx_plugins.regression._cli import _run_from_file

    uvloop.run(_run_from_file(input, output))


@cli.command()
@_params.input()
@_params.output()
def rerun_failure_history(input, output):  # noqa: A002
    """Rerun failed tests from all past regressions."""
    import uvloop
    from socx_plugins.regression._cli import _run_from_file

    uvloop.run(_run_from_file(input, output))
