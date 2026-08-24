from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from colorize.color import Colorize

type Colors = list["Colorize"]
"""
Represents a list of colors.
"""
