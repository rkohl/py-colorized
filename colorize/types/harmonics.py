from colorize.color import CAColor, Colorize

from .color import Colors
from .palette import Triadic


# @dataclass(frozen=True)
class Harmonics:
  _color: Colorize
  """
  A collection of color harmonics.

  Attributes:
    `complement`: The complement color.
    `analogous`: The analogous palette.
    `triadic`: The triadic palette.
    `split_complementary`: The split complementary palette.
    `tetradic`: The tetradic palette.
  """

  def __init__(self, color: Colorize):
    self._color = color

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
