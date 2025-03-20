"""
Tests for the coordinates module.
"""
import unittest
from gc_utils.utils import coordinates


class CoordinateTests(unittest.TestCase):
    """Test cases for the coordinate utilities."""

    def test_parse_coordinate(self):
        """Test coordinate parsing."""
        # Test decimal format
        lat, lon = coordinates.parse_coordinate("47.602050, -122.324194")
        self.assertAlmostEqual(lat, 47.602050, places=6)
        self.assertAlmostEqual(lon, -122.324194, places=6)

        # Test degrees-minutes format (DDM)
        lat, lon = coordinates.parse_coordinate("N 47° 36.123 W 122° 19.456")
        self.assertAlmostEqual(lat, 47.60205, places=5)
        self.assertAlmostEqual(lon, -122.32427, places=5)

    def test_format_coordinate(self):
        """Test coordinate formatting."""
        # Test decimal format
        formatted = coordinates.format_coordinate(
            47.602050, -122.324194, format="decimal")
        self.assertEqual(formatted, "47.602050, -122.324194")

        # Test DDM format (degrees, decimal minutes)
        formatted = coordinates.format_coordinate(
            47.602050, -122.324194, format="ddm")
        self.assertIn("N 47°", formatted)
        self.assertIn("W 122°", formatted)

    def test_distance(self):
        """Test distance calculation."""
        # Test distance between Seattle and New York (approx.)
        seattle = (47.6062, -122.3321)
        new_york = (40.7128, -74.0060)

        # Distance in kilometers
        distance_km = coordinates.distance(seattle, new_york, unit="km")
        self.assertTrue(3700 < distance_km < 3900)  # Roughly 3800 km

        # Distance in miles
        distance_mi = coordinates.distance(seattle, new_york, unit="mi")
        self.assertTrue(2300 < distance_mi < 2500)  # Roughly 2400 mi


if __name__ == "__main__":
    unittest.main()
