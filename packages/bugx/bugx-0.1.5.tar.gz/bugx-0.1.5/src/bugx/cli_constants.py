"""cli constants"""

from dataclasses import dataclass
from typing import ClassVar

from bugx import terminal_width
from bugx.__about__ import __version__, app_name, author, description, short_description


@dataclass
class CliApplication:
    """CLI Application params"""

    EPILOG: ClassVar[
        str
    ] = f"""
    {":pleading_face: : Please Maximize the terminal for Better Experience." if terminal_width <= 70 else ""}
    [bold yellow]Developed by {author} :sunglasses:.[/bold yellow]"""
    DESCRIPTION: ClassVar[str] = description if terminal_width >= 80 else short_description
    VERSION: ClassVar[str] = __version__
    APP_NAME: ClassVar[str] = app_name.title()


@dataclass
class SelectOption:
    """Select Option params"""

    SHORT_HELP: ClassVar[str] = "Prompts the users to select the Bugreports."

    EXAMPLES: ClassVar[
        str
    ] = f"""
    
 {app_name.title()} will prompts the user to select the files using Right/Left arrow to select/unselect, Up/Down to navigate.\
 Press ENTER after selecting the files.\n\n
   
 Examples:
 
     $ {app_name} select --display
     $ {app_name} select -d
     
     $ {app_name} select --all
     $ {app_name} select -a
     
 Recommended to use :  {app_name} select -d
    """

    DISPLAY_FLAG_HELP: ClassVar[str] = "Displays the output in the terminal."
    ALL_FLAG_HELP: ClassVar[str] = "Parses all Bugreports."


@dataclass
class ParseOption:
    """parse option"""

    SHORT_HELP: ClassVar[str] = "Allows user to drag and drop the Bugreports."
    EXAMPLES: ClassVar[
        str
    ] = f"""
    
 Allows the user to drag and drop the Bugreports.\n\n
   
 Examples:
 
     $ {app_name} parse --display
     $ {app_name} parse -d
     
     $ {app_name} select --all
     $ {app_name} select -a
     
 Recommended to use :  {app_name} parse -d
    """
    DISPLAY_FLAG_HELP: ClassVar[str] = "Displays the output in the terminal."


@dataclass
class WatchOption:
    """watch option"""

    SHORT_HELP: ClassVar[str] = "Looks for newly added Bugreports."
    EXAMPLES: ClassVar[
        str
    ] = f"""
    
 {app_name.title()} automatically looks for new bugreports in both Downloads & Documents folders.
 If a new bugreport added/downloaded/dropped into any of the two folders it will be automatically processed.\n\n
   
 Examples:
 
     $ {app_name} watch --display
     $ {app_name} watch -d

 Recommended to use :  {app_name} watch -d
    """
    DISPLAY_FLAG_HELP: ClassVar[str] = "Displays the output in the terminal."
