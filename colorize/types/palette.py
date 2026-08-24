from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .._util import Serializable

if TYPE_CHECKING:
  from colorize.color import Colorize


@dataclass(frozen=True)
class RGB(Serializable):
  """
  A color in the RGB color space.

  Attributes:
    `red`: The red value.
    `green`: The green value.
    `blue`: The blue value.
    `alpha`: The alpha value.

  Protocol:
    `serialize`: A property that returns a dictionary representation of the object.
  """

  red: int
  green: int
  blue: int
  alpha: int = 255

  @property
  def has_alpha(self) -> bool:
    """
    Check if the color has an alpha channel.
    """
    return self.alpha < 255

  @property
  def rgb(self) -> list[int]:
    """
    Return the color as an RGB list.
    """
    return [self.red, self.green, self.blue]

  @property
  def rgba(self) -> list[int]:
    """
    Return the color as an RGBA list.
    """
    return [self.red, self.green, self.blue, self.alpha]


@dataclass(frozen=True)
class DualPalette(Serializable):
  """
  A palette with two colors.

  Attributes:
    `primary`: The primary color.
    `secondary`: The secondary color.

  Protocol:
    `serialize`: A property that returns a dictionary representation of the object.
  """

  primary: Colorize
  secondary: Colorize


@dataclass(frozen=True)
class TriadicPalette(Serializable):
  """
  A palette with three colors.

  Attributes:
    `primary`: The primary color.
    `secondary`: The secondary color.
    `tertiary`: The tertiary color.
  Protocol:
    `serialize`: A property that returns a dictionary representation of the object.
  """

  primary: Colorize
  secondary: Colorize
  tertiary: Colorize


@dataclass(frozen=True)
class OklchPalette(Serializable):
  """
  A palette in the OKLCH color space.

  Attributes:
    `lightness`: The lightness value.
    `chroma`: The chroma value.
    `hue`: The hue value.

  Protocol:
    `serialize`: A property that returns a dictionary representation of the object.
  """

  lightness: float
  chroma: float
  hue: float


@dataclass(frozen=True)
class QuadraticPalette(Serializable):
  """
  A palette with four colors.

  Attributes:
    `primary`: The primary color.
    `secondary`: The secondary color.
    `tertiary`: The tertiary color.
    `quaternary`: The quaternary color.

  Protocol:
    `serialize`: A property that returns a dictionary representation of the object.
  """

  primary: Colorize
  secondary: Colorize
  tertiary: Colorize
  quaternary: Colorize


Dual = DualPalette
Triadic = TriadicPalette
Quadratic = QuadraticPalette
Oklch = OklchPalette
RGBA = RGB
type Full = dict[int, Colorize]
