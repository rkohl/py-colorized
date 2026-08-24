from __future__ import annotations

from dataclasses import dataclass, field

from coloraide import Color as CAColor

from colorized.types import WCAG, Colors, ColorTheme, Harmonics, HexColor, Palettes

from ._util import Data, Serializable


@dataclass(frozen=True)
class Colorize(Serializable):
  """An immutable hexadecimal color backed by the OKLCH color space.

  ``Colorize`` normalizes hexadecimal input and exposes operations for color
  adjustment, harmony generation, contrast evaluation, and palette/theme
  generation. Operations return new values and never mutate the source color.

  Attributes:
    hex: The normalized hexadecimal value.
  """

  hex: HexColor
  _color: CAColor = field(repr=False, compare=False, hash=False)

  def __init__(self, hex: HexColor | str):
    _hex = hex if isinstance(hex, HexColor) else HexColor(hex)

    # Convert once into OKLCH
    ca = CAColor(_hex.hex).convert("oklch")

    object.__setattr__(self, "hex", _hex)
    object.__setattr__(self, "_color", ca)

  @classmethod
  def _from_ca(cls, color: CAColor) -> Colorize:
    return cls(color.convert("srgb").to_string(hex=True))

  def __str__(self) -> str:
    return self.hex.hex

  def __repr__(self) -> str:
    return f"Colorize('{self.hex}')"

  @property
  def oklch(self) -> Palettes.Oklch:
    """
    Return the color in OKLCH color space.
    """

    lightness, chroma, hue = self._color.coords()
    return Palettes.Oklch(lightness, chroma, hue)

  @property
  def lightness(self) -> float:
    return self.oklch.lightness

  @property
  def chroma(self) -> float:
    return self.oklch.chroma

  @property
  def hue(self) -> float:
    return self.oklch.hue

  @staticmethod
  def _clamp_amount(amount: float) -> float:
    """
    Normalize an amount to the range 0.0 - 1.0.
    """
    return max(0.0, min(1.0, float(amount)))

  def rotate_hue(self, degrees: float) -> Colorize:
    c = self._color.clone()
    c["h"] = (c["h"] + degrees) % 360
    return self._from_ca(c)

  def darken(self, amount: float) -> Colorize:
    """
    Darken the color by a given amount.
    Example: ``color.darken(0.2)`` will darken the color by 20%.

    Args:
      - `amount` (float): The amount to darken the color, in the range 0.0 to 1.0.
    """
    amount = self._clamp_amount(amount)

    c = self._color.clone()
    c["l"] *= 1 - amount

    return self._from_ca(c)

  def lighten(self, amount: float) -> Colorize:
    """
    Lighten the color by a given amount.
    Example: ``color.lighten(0.2)`` will lighten the color by 20%.

    Args:
      - `amount` (float): The amount to lighten the color, in the range
        0.0 to 1.0.
    """

    amount = self._clamp_amount(amount)

    c = self._color.clone()
    c["l"] += (1 - c["l"]) * amount
    c["l"] = min(1.0, c["l"])

    return self._from_ca(c)

  def saturate(self, amount: float) -> Colorize:
    """
    Saturate the color by a given amount.
    Example: ``color.saturate(0.2)`` will saturate the color
    by 20%.

    Args:
      - `amount` (float): The amount to saturate the color, in the range
        0.0 to 1.0.
    """
    amount = self._clamp_amount(amount)

    c = self._color.clone()
    c["c"] *= 1 + amount

    return self._from_ca(c)

  def desaturate(self, amount: float) -> Colorize:
    """
    Desaturate the color by a given amount.
    Example: ``color.desaturate(0.2)`` will desaturate the
    color by 20%.

    Args:
      - `amount` (float): The amount to desaturate the color, in the
        range 0.0 to 1.0.
    """
    amount = self._clamp_amount(amount)

    c = self._color.clone()
    c["c"] *= 1 - amount

    return self._from_ca(c)

  def tint(self, amount: float) -> Colorize:
    """
    Tint the color by a given amount.
    Example: ``color.tint(0.2)`` will tint the color by 20%.

    Args:
      - `amount` (float): The amount to tint the color, in the range
        0.0 to 1.0.
    """
    amount = self._clamp_amount(amount)

    return self._from_ca(self._color.mix(CAColor("#FFFFFF"), amount, space="oklch"))

  def shade(self, amount: float) -> Colorize:
    """
    Shade the color by a given amount.
    Example: ``color.shade(0.2)`` will shade the color by 20%.

    Args:
      - `amount` (float): The amount to shade the color, in the range
        0.0 to 1.0.
    """
    amount = self._clamp_amount(amount)

    return self._from_ca(self._color.mix(CAColor("#000000"), amount, space="oklch"))

  def tints(self, count: int = 5) -> Colors:
    """
    Generate a list of tints of the color.
    """

    if count <= 0:
      raise ValueError("count must be greater than zero")
    return [self.tint(i / count) for i in range(1, count + 1)]

  def shades(self, count: int = 5) -> Colors:
    """
    Generate a list of shades of the color.
    """

    if count <= 0:
      raise ValueError("count must be greater than zero")
    return [self.shade(i / count) for i in range(1, count + 1)]

  def alpha(self, opacity: float = 1.0) -> str:
    """
    Return the color as a hexadecimal string with an alpha channel.
    Example: ``color.alpha(0.5)`` will return the color as a hexadecimal
    string with 50% opacity.

    Args:
      - `opacity` (float): The opacity of the color, in the range 0
        to 1.0. Defaults to 1.0 (fully opaque).
    """

    opacity = self._clamp_amount(opacity)

    color = self._color.clone()
    color["alpha"] = opacity

    return color.convert("srgb").to_string(hex=True, alpha=True)

  # ------------------------------------------------------------
  # HARMONIES
  # ------------------------------------------------------------

  @property
  def harmonies(self) -> Harmonics:
    """
    Get the color harmonics.
    """
    return Harmonics(self)

  # ------------------------------------------------------------
  # CONTRAST / WCAG
  # ------------------------------------------------------------

  def contrast_ratio(self, other: Colorize | None = None) -> float:
    """
    Get the contrast ratio between this color and another color.
    If no other color is provided, the contrast ratio is calculated against white.
    """

    return self._color.contrast(other._color if other else CAColor("#FFFFFF"))

  def wcag(self, *, contrasting_with: Colorize | None = None) -> WCAG:
    """
    Get the WCAG contrast ratio and compliance level for this
    color against another color.
    If no other color is provided, the contrast ratio is
    calculated against white.
    """
    return WCAG(self, compared=contrasting_with)

  # ------------------------------------------------------------
  # PALETTE/THEME
  # ------------------------------------------------------------

  @property
  def palette(self) -> Palettes.Full:
    """Generate the standard lightness palette for this color."""

    hue = self.hue
    chroma = self.chroma

    stops = {
      50: 0.97,
      100: 0.94,
      200: 0.88,
      300: 0.80,
      400: 0.70,
      500: self.lightness,
      600: 0.58,
      700: 0.48,
      800: 0.38,
      900: 0.28,
      950: 0.18,
    }

    return {k: self._from_ca(CAColor("oklch", [l, chroma, hue])) for k, l in stops.items()}

  @property
  def theme(self) -> ColorTheme:
    """Generate a theme derived from this color."""

    return ColorTheme(
      primary=self,
      primary_text=self.wcag().best_text_color(),
      complement=self.harmonies.complement,
      analogous=self.harmonies.analogous(),
      triadic=self.harmonies.triadic,
      split_complementary=self.harmonies.split_complementary(),
      palette=self.palette,
    )

  @property
  def serialize(self) -> Data:
    """Return the color values as built-in Python data."""
    return {
      "hex": self.hex.hex,
      "alpha": self.hex.has_alpha,
      "lightness": self.lightness,
      "chroma": self.chroma,
      "hue": self.hue,
    }

  @property
  def _serialize_reference(self) -> Data:
    """Return the compact representation used when nested in other values."""
    return {"hex": self.hex.serialize}
