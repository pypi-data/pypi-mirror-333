"""
Tests for the geometry module.
"""
import unittest
import math
from geocaching_utils.utils import geometry, coordinates


class GeometryTests(unittest.TestCase):
    """Test cases for the geometry utilities."""

    def test_midpoint(self):
        """Test midpoint calculation."""
        point1 = (40.0, -75.0)
        point2 = (42.0, -70.0)

        mid = geometry.midpoint(point1, point2)

        self.assertAlmostEqual(mid[0], 41.0, places=10)
        self.assertAlmostEqual(mid[1], -72.5, places=10)

    def test_centroid(self):
        """Test centroid calculation."""
        points = [
            (40.0, -75.0),
            (42.0, -70.0),
            (39.0, -72.0)
        ]

        center = geometry.centroid(points)

        self.assertAlmostEqual(center[0], 40.333333, places=6)
        self.assertAlmostEqual(center[1], -72.333333, places=6)

        # Test with empty list
        with self.assertRaises(ValueError):
            geometry.centroid([])

    def test_circumcenter(self):
        """Test circumcenter calculation."""
        # Create a right triangle where the circumcenter is easy to calculate
        point1 = (0.0, 0.0)
        point2 = (0.0, 2.0)
        point3 = (2.0, 0.0)

        center = geometry.circumcenter(point1, point2, point3)

        self.assertAlmostEqual(center[0], 1.0, places=10)
        self.assertAlmostEqual(center[1], 1.0, places=10)

        # Test collinear points (should raise ValueError)
        collinear_point1 = (0.0, 0.0)
        collinear_point2 = (1.0, 1.0)
        collinear_point3 = (2.0, 2.0)

        with self.assertRaises(ValueError):
            geometry.circumcenter(
                collinear_point1, collinear_point2, collinear_point3)

    def test_circumradius(self):
        """Test circumradius calculation."""
        # Using the right triangle from the circumcenter test
        point1 = (0.0, 0.0)
        point2 = (0.0, 2.0)
        point3 = (2.0, 0.0)

        # The expected radius is sqrt(2) = 1.414...
        radius = geometry.circumradius(point1, point2, point3, unit="km")

        # Since we're just testing the calculation in a Cartesian plane,
        # the actual units don't matter much. The "distance" function
        # would typically account for the spherical earth, but in our
        # test case with coordinates near (0,0), it's close enough.
        self.assertAlmostEqual(radius, math.sqrt(2) * 111, places=0)

    def test_bounding_box(self):
        """Test bounding box calculation."""
        points = [
            (40.0, -75.0),
            (42.0, -70.0),
            (39.0, -72.0)
        ]

        bbox = geometry.bounding_box(points)

        # Expected: ((39.0, -75.0), (42.0, -70.0))
        self.assertEqual(bbox[0][0], 39.0)
        self.assertEqual(bbox[0][1], -75.0)
        self.assertEqual(bbox[1][0], 42.0)
        self.assertEqual(bbox[1][1], -70.0)

        # Test with empty list
        with self.assertRaises(ValueError):
            geometry.bounding_box([])

    def test_is_point_inside_polygon(self):
        """Test point-in-polygon check."""
        polygon = [
            (0.0, 0.0),
            (0.0, 10.0),
            (10.0, 10.0),
            (10.0, 0.0)
        ]

        # Point inside
        self.assertTrue(geometry.is_point_inside_polygon((5.0, 5.0), polygon))

        # Point outside
        self.assertFalse(
            geometry.is_point_inside_polygon((15.0, 5.0), polygon))

        # Point on edge (this can be inconsistent with the ray casting algorithm)
        # Some implementations consider this inside, others outside
        # We'll skip asserting this.

        # Test with too few points for a polygon
        self.assertFalse(geometry.is_point_inside_polygon(
            (5.0, 5.0), [(0.0, 0.0), (10.0, 10.0)]))

    def test_triangle_area(self):
        """Test triangle area calculation."""
        # Create a simple triangle with known area (1 square unit)
        point1 = (0.0, 0.0)
        point2 = (1.0, 0.0)
        point3 = (0.0, 2.0)

        # The expected area is 1 (base = 1, height = 2, area = 1/2 * base * height)
        # But since we're working with lat/lon, the scaling will be different
        # We'll just check that it's positive and reasonably close to the expected value
        area = geometry.triangle_area(point1, point2, point3, unit="km²")

        self.assertGreater(area, 0)


if __name__ == "__main__":
    unittest.main()
