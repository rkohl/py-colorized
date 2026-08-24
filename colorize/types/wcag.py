from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .._util import Serializable

if TYPE_CHECKING:
  from colorize.color import Colorize


class WCAG(Serializable):
  """
  A class representing the Web Content Accessibility Guidelines (WCAG) for color contrast ratios.

  **Properties:**
    - `ratio`: The contrast ratio between two colors.
    - `rating`: The WCAG rating for the color contrast ratio.
    - `is_light`: Whether the color is considered light.
    - `is_dark`: Whether the color is considered dark.

  **Methods:**
    - `ratio`: Returns the contrast ratio between the two colors.
    - `is_light`: Returns True if the color is considered light.
    - `is_dark`: Returns True if the color is considered dark.
    - `contrasting`: Returns the contrast ratio between the color and another color.
    - `best_text_color`: Returns the best text color (light or dark) for readability
    - `shade`: Returns a shade of the color that has the highest contrast ratio with a reference color.

  **Protocol:**
    - `serialize`: A property that returns a dictionary representation of the object.
  """

  def __init__(self, color: Colorize, *, compared: Colorize | None = None) -> None:
    from colorize.color import Colorize

    self._color: Colorize = color
    self._compare: Colorize = Colorize("#FFFFFF") if compared is None else compared

  @property
  def ratio(self) -> float:
    return self._color._color.contrast(self._compare._color)

  @property
  def is_light(self) -> bool:
    return self._color.lightness > 0.6

  @property
  def is_dark(self) -> bool:
    return not self.is_light

  def contrasting(self, other: Colorize) -> float:
    return self._color._color.contrast(other._color)

  def best_text_color(self, *, light: Colorize | None = None, dark: Colorize | None = None) -> Colorize:
    from colorize.color import Colorize

    if light is None:
      light = Colorize("#FFFFFF")
    if dark is None:
      dark = Colorize("#000000")

    return dark if self.contrasting(dark) > self.contrasting(light) else light

  def shade(self, reference: Colorize | None = None, steps: int = 9) -> Colorize:
    if steps <= 0:
      raise ValueError("steps must be greater than zero")

    base = reference or self._color

    # Generate candidates
    tints = self._color.tints(steps)
    shades = self._color.shades(steps)

    candidates = tints + shades

    # Score by WCAG contrast vs base color
    scored = [(c, c.contrast_ratio(base)) for c in candidates]

    # Pick highest contrast
    best_color, _ = max(scored, key=lambda x: x[1])

    return best_color

  @property
  def rating(self) -> Rating:
    return Rating(
      ratio=round(self.ratio, 2),
      aa=Level(
        normal=self.ratio >= 4.5,
        large=self.ratio >= 3.0,
      ),
      aaa=Level(
        normal=self.ratio >= 7.0,
        large=self.ratio >= 4.5,
      ),
    )


@dataclass(frozen=True)
class Level(Serializable):
  """
  A class representing the Level rating for color contrast ratios.

  ***Level AA***:
    - *Normal text*: Minimum contrast ratio of 4.5:1
    - *Large text*: Minimum contrast ratio of 3:1

  ***Level AAA***:
    - *Normal text*: Minimum contrast ratio of 7:1
    - *Large text*: Minimum contrast ratio of 4.5:1
  Attributes:
    `normal`: Whether the contrast ratio meets the normal standard.
    `large`: Whether the contrast ratio meets the large standard.

  Protocol:
    `serialize`: A property that returns a dictionary representation of the object.
  """

  normal: bool = False
  large: bool = False


@dataclass(frozen=True)
class Rating(Serializable):
  """
  A WCAG rating for a color contrast ratio.

  ***WCAG Rating***

  Measures contrast ratios
  between text and backgrounds to ensure readability for
  people with low vision.


  **Attributes:**
    - `ratio`: The contrast ratio.
    - `aa`: The Level AA rating.
    - `aaa`: The Level AAA rating.

  **Protocol**:
    - `serialize`: A property that returns a dictionary representation of the object.
  """

  ratio: float
  aa: Level
  aaa: Level
