from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from colorized.color import Colorize

type Colors = list["Colorize"]
"""
Represents a list of colors.
"""
