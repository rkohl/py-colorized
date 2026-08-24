from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from coloraide import Color as CAColor

from .._util import Serializable
from .color import Colors
from .palette import Triadic

if TYPE_CHECKING:
  from colorize.color import Colorize


@dataclass(frozen=True)
class Harmonics(Serializable):
  """Generate harmonies derived from a base color.

  Attributes:
    complement: The color opposite the base color on the color wheel.
    triadic: A three-color palette spaced evenly around the color wheel.

  Methods:
    analogous: Return the base color and its two analogous colors.
    split_complementary: Return a split-complementary three-color palette.
    monochromatic: Return colors with increasing lightness.
  """

  _color: Colorize

  @property
  def complement(self) -> Colorize:
    return self._color.rotate_hue(180)

  def analogous(self, angle: float = 30) -> Triadic:
    return Triadic(
      self._color.rotate_hue(-angle),
      self._color,
      self._color.rotate_hue(angle),
    )

  @property
  def triadic(self) -> Triadic:
    return Triadic(
      self._color,
      self._color.rotate_hue(120),
      self._color.rotate_hue(240),
    )

  def split_complementary(self, angle: float = 30) -> Triadic:
    return Triadic(
      self._color,
      self._color.rotate_hue(180 - angle),
      self._color.rotate_hue(180 + angle),
    )

  def monochromatic(self, count: int = 7) -> Colors:
    """Return ``count`` colors with increasing lightness."""

    if count < 2:
      raise ValueError("count must be at least two")
    return [
      self._color._from_ca(
        CAColor(
          "oklch",
          [
            0.15 + (i / (count - 1)) * 0.75,
            self._color.chroma,
            self._color.hue,
          ],
        )
      )
      for i in range(count)
    ]
