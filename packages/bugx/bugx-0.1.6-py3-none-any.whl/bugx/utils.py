"""utils"""

import sys
from typing import Literal, NoReturn

from bugx import console


class Prettier:
    """prettier"""

    def __init__(self, message: str):
        self.message: str = message

    @property
    def bold_yellow(self) -> str:
        """bold yellow"""
        return f"[bold yellow]{self.message}[/bold yellow]"

    @property
    def bold_green(self) -> str:
        """bold green"""
        return f"[bold green]{self.message}[/bold green]"

    @property
    def bold_red(self) -> str:
        """bold red"""
        return f"[bold red]{self.message}[/bold red]"

    def apply(self, weight: Literal["bold", "italic"], color: str) -> str:
        """apply"""
        return f"[{weight} {color}]{self.message}[/{weight} {color}]"


class Display:
    """Display"""

    def __init__(self):
        self.print = console.print

    def interrupt(self, message: str, app_exit: bool = True) -> NoReturn:
        """interrupt"""
        self.print(
            f":unamused: :{Prettier(message=f"Dude you Interrupted me. {message}").bold_yellow}"
        )
        if app_exit:
            sys.exit(2)

    def success(self, message: str) -> NoReturn:
        """success"""
        self.print(f":white_check_mark: :{Prettier(message=message).bold_green}")

    def error(self, message: str, app_exit: bool = False, new_line: bool = False) -> NoReturn:
        """error"""
        self.print(
            f"{"\n" if new_line else ""}:x: :{Prettier(message=message).bold_red}",
            new_line_start=new_line,
        )
        if app_exit:
            sys.exit(1)


if __name__ == "__main__":
    Display().error("mess")
