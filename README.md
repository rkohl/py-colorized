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
print(brand.complement())  # #865815
print(brand.best_text_color())  # #ffffff
print(brand.alpha(0.5))  # #33669980

palette = brand.generate_palette()
print(palette[500])  # #336699

rating = brand.wcag_rating(Colorize("#ffffff"))
print(rating.AA_normal)  # True
```

Adjustment amounts are clamped to the inclusive range `0.0` to `1.0`. Methods
return new `Colorize` values and leave the original unchanged. Three- and
six-digit hex values are supported, as are four- and eight-digit values with an
alpha channel.

## Development

Run the verification checks from the project root:

```bash
python -m pytest
ruff check .
ruff format --check .
```
