from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Self

from .._util import Serializable


@dataclass(frozen=True, slots=True)
class HexColor(Serializable):
  """An immutable, normalized hexadecimal color value.

  Attributes:
    `hex`: The normalized hexadecimal color value.

  Methods:
    `from_rgb`: Create a HexColor from RGB or RGBA values.
    `to_rgb`: Convert the HexColor to an RGB tuple.
    `to_rgba`: Convert the HexColor to an RGBA tuple.
    `has_alpha`: Check if the HexColor includes an alpha channel.

  Protocol:
    `serialize`: A property that returns a dictionary representation of the object.
  """

  _PATTERN = re.compile(r"^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")

  _value: str

  def __init__(self, value: str) -> None:
    value = value.strip()
    digits = value[1:] if value.startswith("#") else value

    if not self._PATTERN.fullmatch(digits):
      raise ValueError("hex color must contain 3, 4, 6, or 8 hexadecimal digits")

    if len(digits) in (3, 4):
      digits = "".join(character * 2 for character in digits)

    object.__setattr__(self, "_value", f"#{digits.lower()}")

  @classmethod
  def from_rgb(cls, red: int, green: int, blue: int, alpha: int | None = None) -> Self:
    """
    Create a HexColor from RGB or RGBA values.
    """
    channels = (red, green, blue) if alpha is None else (red, green, blue, alpha)

    if any(isinstance(channel, bool) or not isinstance(channel, int) or not 0 <= channel <= 255 for channel in channels):
      raise ValueError("color channels must be integers from 0 to 255")

    return cls("#" + "".join(f"{channel:02x}" for channel in channels))

  @property
  def hex(self) -> str:
    """
    Get the normalized hexadecimal color value.
    """
    return self._value

  @property
  def has_alpha(self) -> bool:
    """
    Check if the HexColor includes an alpha channel.
    """
    return len(self._value) == 9

  def to_rgb(self) -> tuple[int, int, int]:
    """
    Convert the HexColor to an RGB tuple.
    """
    return (
      int(self._value[1:3], 16),
      int(self._value[3:5], 16),
      int(self._value[5:7], 16),
    )

  def to_rgba(self) -> tuple[int, int, int, int]:
    alpha = int(self._value[7:9], 16) if self.has_alpha else 255
    return *self.to_rgb(), alpha

  def __str__(self) -> str:
    return self._value

  @property
  def __call__(self) -> str:
    return self._value
