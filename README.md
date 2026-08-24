# Py Colorized

Py Colorized is a small, typed Python library for manipulating colors in the OKLCH
color space. It provides immutable color values, lightness and saturation
adjustments, color harmonies, WCAG contrast helpers, and palette/theme
generation.

## Requirements

- Python 3.12 or newer

## Installation

Install the package from this repository:

```bash
python -m pip install py-colorized
```

## Usage

```python
from colorized import Colorize

brand = Colorize("#336699")

print(brand.lighten(0.2))  # #5084b9
print(brand.harmonies.complement)  # #865815
print(brand.wcag().best_text_color())  # #ffffff
print(brand.alpha(0.5))  # #33669980

palette = brand.palette
print(palette[500])  # #336699

rating = brand.wcag(contrasting_with=Colorize("#ffffff")).rating
print(rating.aa.normal)  # True
```

Operations can be chained to build more complex adjustments:

```python
brand = Colorize("#336699")

print(brand.tint(0.2).lighten(0.4))  # #8bb6e2
print(brand.lighten(0.4).alpha(0.5))  # #6ea3da80
```

## Adjustment values

Adjustment values are proportions from `0.0` to `1.0`. For example,
`brand.lighten(0.2)` lightens the color by 20%, moving its OKLCH lightness 20%
of the remaining distance toward white.

- `darken(0.2)` reduces the current lightness by 20%.
- `saturate(0.2)` increases the current chroma by 20%.
- `desaturate(0.2)` reduces the current chroma by 20%.
- `tint(0.2)` mixes in 20% white, while `shade(0.2)` mixes in 20% black.
- `alpha(0.5)` sets the color to 50% opacity.

Values outside the supported range are clamped: negative values become `0.0`,
and values greater than `1.0` become `1.0`. Adjustment methods return new
`Colorize` values and leave the original unchanged.

Three- and six-digit hex values are supported, as are four- and eight-digit
values with an alpha channel.

## HexColor

`HexColor` is the immutable, normalized hexadecimal value stored in
`Colorize.hex`. It supports RGB/RGBA conversion and detects whether an alpha
channel is present.

```python
from colorized import HexColor, Palettes

color = HexColor("abc8")

print(color)  # #aabbcc88
print(color.has_alpha)  # True
print(color.to_rgb().rgb)  # [170, 187, 204]
print(color.to_rgba().rgba)  # [170, 187, 204, 136]

green = HexColor.from_rgb(red=0, green=128, blue=0)
print(green)  # #008000

transparent_blue = HexColor.from_rgb(Palettes.RGBA(red=51, green=102, blue=153, alpha=128))
print(transparent_blue)  # #33669980
```

## Returned types

`Colorize` uses typed model objects where a result has named components. The
palette models are available through `Palettes`; lower-level helper types are
available from `colorized.types`.

| API | Return type | Description |
| --- | --- | --- |
| `color.hex` | `HexColor` | Normalized hexadecimal value |
| `HexColor.to_rgb()` | `Palettes.RGB` | Named red, green, and blue channels |
| `HexColor.to_rgba()` | `Palettes.RGBA` | Named red, green, blue, and alpha channels |
| `color.oklch` | `Palettes.Oklch` | Named `lightness`, `chroma`, and `hue` values |
| `color.oklch.values` | `list[float]` | OKLCH components in lightness, chroma, hue order |
| `color.lightness`, `color.chroma`, `color.hue` | `float` | Individual OKLCH components |
| `rotate_hue()`, `darken()`, `lighten()` | `Colorize` | Adjusted immutable color |
| `saturate()`, `desaturate()`, `tint()`, `shade()` | `Colorize` | Adjusted immutable color |
| `tints()`, `shades()` | `list[Colorize]` | Generated color scale |
| `alpha()` | `str` | Eight-digit hexadecimal string with alpha |
| `harmonies` | `Harmonics` | Harmony generator for the color |
| `harmonies.complement` | `Colorize` | Complementary color |
| `harmonies.analogous()`, `harmonies.triadic` | `Palettes.Triadic` | Named three-color palette |
| `harmonies.split_complementary()` | `Palettes.Triadic` | Named split-complementary palette |
| `dual.colors`, `triadic.colors` | `list[Colorize]` | Palette colors in field order |
| `quadratic.colors` | `list[Colorize]` | Four palette colors in field order |
| `harmonies.monochromatic()` | `list[Colorize]` | Monochromatic color scale |
| `contrast_ratio()` | `float` | Contrast ratio against another color, or white by default |
| `wcag(contrasting_with=...)` | `WCAG` | Accessibility helper using the provided color, or white by default |
| `wcag().rating` | `Rating` | Ratio with `aa` and `aaa` `Level` results |
| `wcag().best_text_color()`, `wcag().shade()` | `Colorize` | Contrast-selected color |
| `palette` | `dict[int, Colorize]` | Palette keyed by stops from `50` through `950` |
| `theme` | `ColorTheme` | Complete generated color theme |

Palette results expose both named fields and ordered list helpers:

```python
from colorized import Colorize, Palettes
from colorized.types import Harmonics, Level, Rating, WCAG

brand = Colorize("#336699")

oklch: Palettes.Oklch = brand.oklch
harmonies: Harmonics = brand.harmonies
analogous: Palettes.Triadic = harmonies.analogous()
wcag: WCAG = brand.wcag(contrasting_with=Colorize("#ffffff"))
rating: Rating = wcag.rating
theme = brand.theme

print(oklch.lightness)
assert oklch.values == [oklch.lightness, oklch.chroma, oklch.hue]
print(analogous.primary, analogous.secondary, analogous.tertiary)
assert analogous.colors == [analogous.primary, analogous.secondary, analogous.tertiary]
print(rating.aa == Level(normal=True, large=True))  # True
print(theme.primary)  # #336699
```

Use `.serialize` to convert colors, harmonies, RGB values, palettes, WCAG
ratings, and themes to built-in Python values:

```python
data = brand.serialize

print(data["hex"])  # #336699
print(data["alpha"])  # False
print(data["lightness"])  # 0.4993144558452082
print(data["chroma"])  # 0.09866437712418324
print(data["hue"])  # 250.4330574201755

print(brand.harmonies.serialize["complement"])
# {"hex": "#865815" ... }
```

```json
{
  "hex": "#336699",
  "alpha": False,
  "lightness": 0.4993144558452082,
  "chroma": 0.09866437712418324,
  "hue": 250.4330574201755
}
```

## Tests

Run the verification checks from the project root:

```bash
python -m pytest
```
