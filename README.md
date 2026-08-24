# Colorize

Colorize is a small, typed Python library for manipulating colors in the OKLCH
color space. It provides immutable color values, lightness and saturation
adjustments, color harmonies, WCAG contrast helpers, and palette/theme
generation.

## Requirements

- Python 3.12 or newer
- `coloraide`

## Installation

Install the package from this repository:

```bash
python -m pip install .
```

For local development, install the test and lint tools too:

```bash
python -m pip install -e '.[dev]'
```

## Usage

```python
from colorize import Colorize

brand = Colorize("#336699")

print(brand.lighten(0.2))  # #5084b9
print(brand.harmonies.complement)  # #865815
print(brand.wcag().best_text_color())  # #ffffff
print(brand.alpha(0.5))  # #33669980

palette = brand.palette
print(palette[500])  # #336699

rating = brand.wcag(Colorize("#ffffff")).rating
print(rating.aa.normal)  # True
```

Operations can be chained to build more complex adjustments:

```python
brand = Colorize("#336699")

print(brand.tint(0.2).lighten(0.4))  # #8bb6e2
print(brand.lighten(0.4).alpha(0.5))  # #6ea3da80
```

Adjustment amounts are clamped to the inclusive range `0.0` to `1.0`. Methods
return new `Colorize` values and leave the original unchanged. Three- and
six-digit hex values are supported, as are four- and eight-digit values with an
alpha channel.

## HexColor

`HexColor` is the immutable, normalized hexadecimal value stored in
`Colorize.hex`. It supports RGB/RGBA conversion and detects whether an alpha
channel is present.

```python
from colorize import HexColor, Palettes

color = HexColor("abc8")

print(color)  # #aabbcc88
print(color.has_alpha)  # True
print(color.to_rgb().rgb)  # [170, 187, 204]
print(color.to_rgba().rgba)  # [170, 187, 204, 136]

green = HexColor.from_rgb(red=0, green=128, blue=0)
print(green)  # #008000

transparent_blue = HexColor.from_rgb(
    Palettes.RGBA(red=51, green=102, blue=153, alpha=128)
)
print(transparent_blue)  # #33669980
```

## Returned types

`Colorize` uses typed model objects where a result has named components. The
palette models are available through `Palettes`; lower-level helper types are
available from `colorize.types`.

| API | Return type | Description |
| --- | --- | --- |
| `color.hex` | `HexColor` | Normalized hexadecimal value |
| `HexColor.to_rgb()` | `Palettes.RGB` | Named red, green, and blue channels |
| `HexColor.to_rgba()` | `Palettes.RGBA` | Named red, green, blue, and alpha channels |
| `color.oklch` | `Palettes.Oklch` | Named `lightness`, `chroma`, and `hue` values |
| `color.lightness`, `color.chroma`, `color.hue` | `float` | Individual OKLCH components |
| `rotate_hue()`, `darken()`, `lighten()` | `Colorize` | Adjusted immutable color |
| `saturate()`, `desaturate()`, `tint()`, `shade()` | `Colorize` | Adjusted immutable color |
| `tints()`, `shades()` | `list[Colorize]` | Generated color scale |
| `alpha()` | `str` | Eight-digit hexadecimal string with alpha |
| `harmonies` | `Harmonics` | Harmony generator for the color |
| `harmonies.complement` | `Colorize` | Complementary color |
| `harmonies.analogous()`, `harmonies.triadic` | `Palettes.Triadic` | Named three-color palette |
| `harmonies.split_complementary()` | `Palettes.Triadic` | Named split-complementary palette |
| `harmonies.monochromatic()` | `list[Colorize]` | Monochromatic color scale |
| `contrast_ratio()` | `float` | WCAG contrast ratio |
| `wcag()` | `WCAG` | Contrast and accessibility helper |
| `wcag().rating` | `Rating` | Ratio with `aa` and `aaa` `Level` results |
| `wcag().best_text_color()`, `wcag().shade()` | `Colorize` | Contrast-selected color |
| `palette` | `dict[int, Colorize]` | Palette keyed by stops from `50` through `950` |
| `theme` | `ColorTheme` | Complete generated color theme |

Palette results expose named fields rather than tuple indexes:

```python
from colorize import Colorize, Palettes
from colorize.types import Harmonics, Level, Rating, WCAG

brand = Colorize("#336699")

oklch: Palettes.Oklch = brand.oklch
harmonies: Harmonics = brand.harmonies
analogous: Palettes.Triadic = harmonies.analogous()
wcag: WCAG = brand.wcag(Colorize("#ffffff"))
rating: Rating = wcag.rating
theme = brand.theme

print(oklch.lightness)
print(analogous.primary, analogous.secondary, analogous.tertiary)
print(rating.aa == Level(normal=True, large=True))  # True
print(theme.primary)  # #336699
```

The `RGB`, palette, WCAG rating, and theme models implement the `Serializable`
protocol and expose a `.serialize` property for conversion to built-in Python
values.

## Development

Run the verification checks from the project root:

```bash
python -m pytest
```
