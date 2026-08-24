import math

import pytest

from colorize import Colorize, ColorTheme, HexColor, Palettes
from colorize.types import Colors, Level, Rating


def hue_distance(left: float, right: float) -> float:
  return abs((left - right + 180) % 360 - 180)


class TestConstruction:
  def test_public_namespace_exposes_hex_color(self) -> None:
    assert HexColor("#abc") == Colorize("#abc").hex

  def test_color_collection_alias_is_safe_to_inspect(self) -> None:
    assert Colors.__value__ == list["Colorize"]

  def test_normalizes_short_hex_and_whitespace(self) -> None:
    color = Colorize("  abc  ")

    assert str(color.hex) == "#aabbcc"
    assert str(color) == "#aabbcc"
    assert repr(color) == "Colorize('#aabbcc')"

  def test_invalid_color_raises_value_error(self) -> None:
    with pytest.raises(ValueError):
      Colorize("not-a-color")

  def test_equivalent_colors_are_equal_and_hashable(self) -> None:
    short = Colorize("#fff")
    long = Colorize("#ffffff")

    assert short == long
    assert hash(short) == hash(long)
    assert len({short, long}) == 1

  def test_exposes_oklch_components(self) -> None:
    color = Colorize("#336699")

    assert color.oklch == Palettes.Oklch(color.lightness, color.chroma, color.hue)
    assert 0 <= color.lightness <= 1
    assert color.chroma >= 0
    assert 0 <= color.hue < 360


class TestAdjustments:
  @pytest.mark.parametrize(
    ("method", "endpoint"),
    [
      ("lighten", "#ffffff"),
      ("darken", "#000000"),
      ("desaturate", "#777777"),
      ("tint", "#ffffff"),
      ("shade", "#000000"),
    ],
  )
  def test_full_adjustments_reach_expected_endpoint(self, method: str, endpoint: str) -> None:
    result = getattr(Colorize("#777777"), method)(1)

    assert result == Colorize(endpoint)

  @pytest.mark.parametrize("method", ["lighten", "darken", "saturate", "desaturate", "tint", "shade"])
  def test_adjustment_amounts_are_clamped(self, method: str) -> None:
    color = Colorize("#336699")

    assert getattr(color, method)(-1) == getattr(color, method)(0)
    assert getattr(color, method)(2) == getattr(color, method)(1)

  def test_adjustments_return_new_colors(self) -> None:
    color = Colorize("#336699")

    assert color.lighten(0.25) is not color
    assert color == Colorize("#336699")

  def test_rotate_hue_wraps_around_color_wheel(self) -> None:
    color = Colorize("#336699")

    assert hue_distance(color.rotate_hue(390).hue, color.rotate_hue(30).hue) < 1

  def test_alpha_replaces_existing_alpha_channel(self) -> None:
    color = Colorize("#33669940")

    assert color.alpha(0.5) == "#33669980"
    assert color.alpha(-1) == "#33669900"
    assert color.alpha(2) == "#336699ff"


class TestCollectionsAndHarmonies:
  @pytest.mark.parametrize("method", ["tints", "shades"])
  def test_gradient_count_and_endpoint(self, method: str) -> None:
    colors = getattr(Colorize("#336699"), method)(4)

    assert len(colors) == 4
    assert colors[-1] == Colorize("#ffffff" if method == "tints" else "#000000")

  @pytest.mark.parametrize("method", ["tints", "shades"])
  def test_gradient_rejects_non_positive_count(self, method: str) -> None:
    with pytest.raises(ValueError, match="count must be greater than zero"):
      getattr(Colorize("#336699"), method)(0)

  def test_harmonies_include_base_color_and_expected_hue_offsets(self) -> None:
    color = Colorize("#336699")
    complement = color.harmonies.complement
    analogous = color.harmonies.analogous()
    triadic = color.harmonies.triadic
    split = color.harmonies.split_complementary()

    assert hue_distance(complement.hue, (color.hue + 180) % 360) < 1
    assert analogous.secondary is color
    assert triadic.primary is color
    assert split.primary is color
    assert hue_distance(triadic.secondary.hue, (color.hue + 120) % 360) < 1
    assert hue_distance(triadic.tertiary.hue, (color.hue + 240) % 360) < 1

  def test_monochromatic_scale_preserves_order_and_size(self) -> None:
    colors = Colorize("#336699").harmonies.monochromatic(5)

    assert len(colors) == 5
    assert [color.lightness for color in colors] == sorted(color.lightness for color in colors)

  def test_monochromatic_scale_requires_at_least_two_colors(self) -> None:
    with pytest.raises(ValueError, match="count must be at least two"):
      Colorize("#336699").harmonies.monochromatic(1)


class TestContrastAndGeneratedOutput:
  def test_black_and_white_have_maximum_wcag_contrast(self) -> None:
    black = Colorize("#000000")
    white = Colorize("#ffffff")

    assert black.contrast_ratio(white) == pytest.approx(21)
    assert black.wcag(contrasting_with=white).rating == Rating(
      ratio=21.0,
      aa=Level(normal=True, large=True),
      aaa=Level(normal=True, large=True),
    )

  @pytest.mark.parametrize(("background", "expected"), [("#000000", "#ffffff"), ("#ffffff", "#000000")])
  def test_best_text_color_maximizes_contrast(self, background: str, expected: str) -> None:
    assert Colorize(background).wcag().best_text_color() == Colorize(expected)

  def test_light_and_dark_are_complementary_classifications(self) -> None:
    for color in (Colorize("#000000"), Colorize("#ffffff"), Colorize("#336699")):
      assert color.wcag().is_light is not color.wcag().is_dark

  def test_contrast_shade_selects_best_generated_candidate(self) -> None:
    color = Colorize("#336699")
    result = color.wcag().shade(steps=5)
    candidates = color.tints(5) + color.shades(5)

    assert result in candidates
    assert result.contrast_ratio(color) == max(candidate.contrast_ratio(color) for candidate in candidates)

  def test_contrast_shade_rejects_non_positive_steps(self) -> None:
    with pytest.raises(ValueError, match="steps must be greater than zero"):
      Colorize("#336699").wcag().shade(steps=0)

  def test_palette_has_standard_stops_and_preserves_base_at_500(self) -> None:
    color = Colorize("#336699")
    palette = color.palette

    assert list(palette) == [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]
    assert palette[500] == color

  def test_theme_contains_coherent_generated_values(self) -> None:
    color = Colorize("#336699")
    theme = color.theme

    assert isinstance(theme, ColorTheme)
    assert theme.primary is color
    assert theme.primary_text == color.wcag().best_text_color()
    assert theme.palette[500] == color

  def test_theme_serializes_nested_colors_without_recursion(self) -> None:
    serialized = Colorize("#336699").theme.serialize

    assert serialized["primary"] == {"hex": {"hex": "#336699", "has_alpha": False}}
    assert serialized["palette"][500] == serialized["primary"]

  def test_color_and_harmonies_serialize_without_recursion(self) -> None:
    color = Colorize("#336699")

    serialized = color.serialize

    assert serialized == {
      "hex": "#336699",
      "alpha": False,
      "lightness": color.lightness,
      "chroma": color.chroma,
      "hue": color.hue,
    }
    assert color.harmonies.serialize["complement"] == color.harmonies.complement._serialize_reference

  def test_palette_models_are_available_from_public_namespace(self) -> None:
    primary = Colorize("#336699")
    secondary = primary.harmonies.complement
    palette = Palettes.Dual(primary, secondary)

    assert palette == Palettes.DualPalette(primary=primary, secondary=secondary)

  def test_achromatic_hue_is_undefined(self) -> None:
    assert math.isnan(Colorize("#000000").hue)
