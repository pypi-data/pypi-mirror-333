![logo](https://github.com/spectraldecomp/geocaching-utils/blob/main/geocaching_utils/data/public/geocaching-utils-logo.png)
---
geocaching-utils is a Python package offering a suite of tools for Geocaching puzzle creation/solving and GIS-related tasks.

## Features

- **Cipher Utilities**: Decode various ciphers commonly used in geocaching puzzles
  - Caesar cipher (including ROT13)
  - Vigenère cipher
  - Atbash cipher
  - Morse code

- **Coordinate Utilities**:
  - Parse coordinates in different formats (decimal, DDM, DMS)
  - Convert between coordinate formats
  - Calculate distance between coordinates
  - Project waypoints given distance and bearing

- **Geometry Utilities**:
  - Calculate circumcenter of three coordinates
  - Find centroid of multiple points
  - Calculate midpoint between two coordinates
  - Determine triangle area
  - Generate bounding boxes
  - Check if a point is inside a polygon

- **Puzzle Helpers**:
  - Anagram solving
  - ASCII/text conversion
  - Number/letter conversion
  - Text manipulation

## Installation

### PyPI Installation (Recommended)

```bash
# Install directly from PyPI
pip install geocaching-utils
```

### Manual Installation from Source

```bash
# Install from the repository
git clone https://github.com/spectraldecomp/geocaching-utils.git
cd geocaching-utils
pip install -e .
```

## CLI Usage

geocaching-utils provides a command-line interface named `gc-utils` for quick access to common functions. All of the commands use `--mode` to specify the operation:

### Decode Ciphers

```bash
# Caesar cipher (ROT13 by default)
gc-utils cipher --mode caesar "Urer vf n fvzcyr grkg"

# Caesar with specific shift
gc-utils cipher --mode caesar --shift 3 "Khoor, zruog!"

# Vigenère cipher
gc-utils cipher --mode vigenere --key "geocache" "Vcswymcmwz kc h ztwfvl"

# Morse code
gc-utils cipher --mode morse ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
```

### Coordinates and Distance Operations

```bash
# Convert to decimal format (default)
gc-utils coords --mode convert "N 47° 36.123 W 122° 19.456"

# Convert to DMS format
gc-utils coords --mode convert --out-format dms "47.602050, -122.324194"

# Calculate distance between two points (in km by default)
gc-utils coords --mode distance "N 47° 36.123 W 122° 19.456" "N 40° 42.768 W 074° 00.360"

# Calculate distance in miles
gc-utils coords --mode distance --unit mi "47.602050, -122.324194" "40.712800, -74.006000"
```

### Geometric Calculations

```bash
# Find the circumcenter (center of a circle passing through three points)
gc-utils geometry --mode circumcenter "N 47° 36.123 W 122° 19.456" "N 46° 12.345 W 121° 54.321" "N 48° 30.456 W 123° 45.789"

# Calculate the circumcenter and its radius
gc-utils geometry --mode circumcenter --radius --unit mi "N 47° 36.123 W 122° 19.456" "N 46° 12.345 W 121° 54.321" "N 48° 30.456 W 123° 45.789"

# Find the centroid (center of mass) of multiple coordinates
gc-utils geometry --mode centroid "N 47° 36.123 W 122° 19.456" "N 46° 12.345 W 121° 54.321" "N 48° 30.456 W 123° 45.789"

# Calculate the midpoint between two coordinates
gc-utils geometry --mode midpoint "N 47° 36.123 W 122° 19.456" "N 48° 30.456 W 123° 45.789"

# Calculate the area of a triangle
gc-utils geometry --mode triangle-area --unit km² "N 47° 36.123 W 122° 19.456" "N 46° 12.345 W 121° 54.321" "N 48° 30.456 W 123° 45.789"

# Find the bounding box of a set of coordinates
gc-utils geometry --mode bounding-box "N 47° 36.123 W 122° 19.456" "N 46° 12.345 W 121° 54.321" "N 48° 30.456 W 123° 45.789"
```

### Puzzle Tools

```bash
# Convert ASCII values to text
gc-utils tools --mode ascii-to-text "72 101 108 108 111"

# Convert text to ASCII values
gc-utils tools --mode text-to-ascii "Hello"

# Solve anagrams
gc-utils tools --mode anagram "listen"

# Convert between letters and numbers (A=1, B=2, etc.)
gc-utils tools --mode a1z26 "ABC" --direction to-numbers
gc-utils tools --mode a1z26 "1 2 3" --direction to-letters

# Reverse text
gc-utils tools --mode reverse "Hello World"
gc-utils tools --mode reverse "Hello World" --words-only
```

## Python API Usage

You can also use geocaching-Utils as a Python library:

```python
from geocaching_utils.utils import ciphers, coordinates, puzzle_helpers, geometry

# Decode a cipher
decoded = ciphers.caesar_decode("Uryyb, jbeyq!", shift=13)
print(decoded)  # "Hello, world!"

# Decode a Vigenère cipher
decoded = ciphers.vigenere_decode("Jevpq, uyvnd!", key="key")
print(decoded)  # "Hello, world!"

# Parse and format coordinates
lat, lon = coordinates.parse_coordinate("N 47° 36.123 W 122° 19.456")
formatted = coordinates.format_coordinate(lat, lon, format="dms")
print(formatted)  # "N 47° 36' 7.380" W 122° 19' 27.360""

# Calculate distance
seattle = (47.6062, -122.3321)
new_york = (40.7128, -74.0060)
distance = coordinates.distance(seattle, new_york, unit="mi")
print(f"Distance: {distance:.2f} miles")

# Use puzzle helpers
ascii_text = puzzle_helpers.ascii_to_text([72, 101, 108, 108, 111])
print(ascii_text)  # "Hello"

# Convert numbers to letters
letters = puzzle_helpers.number_to_letter([1, 2, 3])
print(letters)  # "ABC"

# Convert letters to numbers
numbers = puzzle_helpers.letter_to_number("ABC")
print(numbers)  # [1, 2, 3]

anagrams = puzzle_helpers.anagram_solver("listen")
print(anagrams)  # Includes "silent", etc.

# Use geometry functions
triangle_points = [(47.6062, -122.3321), (46.1234, -121.5432), (48.3045, -123.4578)]
center = geometry.circumcenter(*triangle_points)
radius = geometry.circumradius(*triangle_points, unit="km")
print(f"Circumcenter: {center}, Radius: {radius:.2f} km")

# Find centroid of multiple points
coords = [(47.6062, -122.3321), (46.1234, -121.5432), (48.3045, -123.4578), (45.5231, -122.6765)]
center_point = geometry.centroid(coords)
print(f"Centroid: {geometry.format_point(center_point)}")
```

## Testing

Run the tests with pytest:

```bash
cd geocaching-utils
pytest tests/
```

The test suite includes comprehensive tests for all functions with diverse test cases, including:
- Ciphers: Tests for Caesar, Vigenère, and Morse code decoding
- Coordinates: Tests for parsing various coordinate formats and distance calculations
- Geometry: Tests for various geometric operations like midpoint, centroid, and circumcenter calculations
- Puzzle Helpers: Tests for text manipulation, ASCII conversion, and number/letter conversion

## License

This project is licensed under the MIT License - see the LICENSE file for details.
