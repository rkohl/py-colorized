import pytest

from colorize.types.hex import HexColor


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
  color = HexColor.from_rgb(51, 102, 153, 128)

  assert color == HexColor("#33669980")
  assert color.to_rgb() == (51, 102, 153)
  assert color.to_rgba() == (51, 102, 153, 128)
