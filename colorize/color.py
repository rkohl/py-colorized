from __future__ import annotations

from dataclasses import dataclass, field

from coloraide import Color as CAColor

from colorize.types import WCAG, Colors, ColorTheme, Harmonics, HexColor, Palettes


@dataclass(frozen=True)
class Colorize:
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
    amount = self._clamp_amount(amount)

    c = self._color.clone()
    c["l"] *= 1 - amount

    return self._from_ca(c)

  def lighten(self, amount: float) -> Colorize:
    amount = self._clamp_amount(amount)

    c = self._color.clone()
    c["l"] += (1 - c["l"]) * amount
    c["l"] = min(1.0, c["l"])

    return self._from_ca(c)

  def saturate(self, amount: float) -> Colorize:
    amount = self._clamp_amount(amount)

    c = self._color.clone()
    c["c"] *= 1 + amount

    return self._from_ca(c)

  def desaturate(self, amount: float) -> Colorize:
    amount = self._clamp_amount(amount)

    c = self._color.clone()
    c["c"] *= 1 - amount

    return self._from_ca(c)

  def tint(self, amount: float) -> Colorize:
    amount = self._clamp_amount(amount)

    return self._from_ca(self._color.mix(CAColor("#FFFFFF"), amount, space="oklch"))

  def shade(self, amount: float) -> Colorize:
    amount = self._clamp_amount(amount)

    return self._from_ca(self._color.mix(CAColor("#000000"), amount, space="oklch"))

  def tints(self, count: int = 5) -> Colors:
    if count <= 0:
      raise ValueError("count must be greater than zero")
    return [self.tint(i / count) for i in range(1, count + 1)]

  def shades(self, count: int = 5) -> Colors:
    if count <= 0:
      raise ValueError("count must be greater than zero")
    return [self.shade(i / count) for i in range(1, count + 1)]

  def alpha(self, opacity: float = 1.0) -> str:
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
    return self._color.contrast(other._color if other else CAColor("#FFFFFF"))

  def wcag(self, other: Colorize | None = None) -> WCAG:
    return WCAG(self, other)

  # ------------------------------------------------------------
  # PALETTE/THEME
  # ------------------------------------------------------------

  @property
  def palette(self) -> Palettes.Full:
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
    return ColorTheme(
      primary=self,
      primary_text=self.wcag().best_text_color(),
      complement=self.harmonies.complement,
      analogous=self.harmonies.analogous(),
      triadic=self.harmonies.triadic,
      split_complementary=self.harmonies.split_complementary(),
      palette=self.palette,
    )
