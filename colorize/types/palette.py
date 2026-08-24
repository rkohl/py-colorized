from __future__ import annotations

from dataclasses import dataclass

from colorize.color import Colorize

from .._util import Serializable


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
type Full = dict[int, Colorize]
