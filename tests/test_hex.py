import pytest

from colorized import Palettes
from colorized.types.hex import HexColor


def test_normalizes_hex_values() -> None:
  assert str(HexColor(" ABC ")) == "#aabbcc"
  assert str(HexColor("#abcd")) == "#aabbccdd"


def test_rejects_invalid_hex_values() -> None:
  with pytest.raises(ValueError, match="3, 4, 6, or 8"):
    HexColor("#12")


def test_equivalent_hex_values_compare_equal() -> None:
  short = HexColor("#fff")
  long = HexColor("#ffffff")

  assert short == long
  assert hash(short) == hash(long)


def test_converts_rgb_values() -> None:
  rgba = Palettes.RGBA(red=51, green=102, blue=153, alpha=128)
  color = HexColor.from_rgb(rgba)

  assert color == HexColor("#33669980")
  assert color.to_rgb() == Palettes.RGB(red=51, green=102, blue=153)
  assert color.to_rgba() == rgba
