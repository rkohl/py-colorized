from __future__ import annotations

from dataclasses import dataclass

from colorize.color import Colorize

from .._util import Serializable
from .palette import Full, Triadic


@dataclass(frozen=True)
class ColorTheme(Serializable):
  """
  A color theme with a primary color, a primary text color, a complement color, an
  analogous palette, a triadic palette, a split complementary palette, and a full palette.

  Attributes:
    `primary`: The primary color.
    `primary_text`: The primary text color.
    `complement`: The complement color.
    `analogous`: The analogous palette.
    `triadic`: The triadic palette.
    `split_complementary`: The split complementary palette.
    `palette`: The full palette.

  Protocol:
    `serialize`: A property that returns a dictionary representation of the object.
  """

  primary: Colorize
  primary_text: Colorize
  complement: Colorize
  analogous: Triadic
  triadic: Triadic
  split_complementary: Triadic
  palette: Full
