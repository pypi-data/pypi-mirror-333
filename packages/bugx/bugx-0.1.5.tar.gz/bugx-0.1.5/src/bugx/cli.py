"""cli"""

import subprocess
from functools import wraps
from typing import Annotated, Any

import click
import typer
from typer.core import TyperGroup as TyperGroupBase

from bugx.bugreport_extractor import for_cli
from bugx.cli_constants import CliApplication, SelectOption, WatchOption
from bugx.utils import Display, console
from bugx.watcher import watcher

display = Display()


class TyperGroup(TyperGroupBase):
    """Custom TyperGroup class."""

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)

    def get_usage(self, ctx: click.Context) -> str:
        """Override get_usage."""
        usage: str = super().get_usage(ctx)
        message: str = f"{CliApplication.DESCRIPTION}\n\n{usage}"
        return message


app = typer.Typer(
    name=CliApplication.APP_NAME,
    epilog=CliApplication.EPILOG,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
    add_completion=True,
    invoke_without_command=True,
    rich_markup_mode="rich",
    cls=TyperGroup,
)


def version_callback(value: bool) -> None:
    """Version callback"""
    if value:
        console.print(f":sparkles: {CliApplication.APP_NAME} version {CliApplication.VERSION}")
        raise typer.Exit()


@app.callback(short_help="Prints the Version and Changelog.", epilog=CliApplication.EPILOG)
def cli_version(
    display_version: Annotated[
        bool, typer.Option("--version", "-v", help="Prints the Version and Changelog.",is_eager=True)
    ] = False,
) -> None:
    if display_version:
        version_callback(value=True)


def docstring(*examples):
    """docstring decorator"""

    def decorator(obj):
        if obj.__doc__:
            obj.__doc__ = obj.__doc__.format(*examples)
        return obj

    return decorator


def run_with(interrupt_message: str):
    """run with decorator"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt as run_with_interrupt:
                if not run_with_interrupt.args:
                    display.interrupt(message=interrupt_message)
                else:
                    display.interrupt(
                        message=f"{interrupt_message if not run_with_interrupt.args[0].args  else run_with_interrupt}"
                    )
            except (
                subprocess.CalledProcessError,
                ValueError,
                TypeError,
                AttributeError,
            ) as run_with_error:
                display.error(message=f"{func.__name__}: {run_with_error}")

        return wrapper

    return decorator


@app.command(
    name="select",
    rich_help_panel="Commands",
    epilog=CliApplication.EPILOG,
    short_help=SelectOption.SHORT_HELP,
    help=SelectOption.EXAMPLES,
)
# @docstring(SelectOption.EXAMPLES)
@run_with(interrupt_message="While running select operation.")
def select(
    select_all: Annotated[
        bool, typer.Option("--all", "-a", help=SelectOption.ALL_FLAG_HELP)
    ] = False,
    to_display: Annotated[
        bool,
        typer.Option("--display", "-d", help=SelectOption.DISPLAY_FLAG_HELP),
    ] = False,
    _: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            help="Show version information",
            callback=version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    """Prompts the user to select the bugreports."""
    for_cli(override=to_display, select_all=select_all)


@app.command(
    name="watch",
    rich_help_panel="Commands",
    epilog=CliApplication.EPILOG,
    help=WatchOption.EXAMPLES,
    short_help=WatchOption.SHORT_HELP,
)
@run_with(interrupt_message="While running watch operation.")
def watch(
    to_display: Annotated[
        bool,
        typer.Option("--display", "-d", help=WatchOption.DISPLAY_FLAG_HELP),
    ] = False,
    _: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            help="Show version information",
            callback=version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    """looks for bugreports."""
    watcher(override=to_display)


if __name__ == "__main__":
    app()
