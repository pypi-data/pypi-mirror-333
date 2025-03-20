"""
Geometric calculation utilities for coordinates.

This module provides functions for performing geometric calculations on coordinates,
such as finding circumcenters, centroids, triangulation, and other spatial operations
useful for geocaching puzzles and challenges.
"""
import math
from typing import Tuple, List, Optional
from gc_utils.utils.coordinates import distance, format_coordinate


def circumcenter(point1: Tuple[float, float],
                 point2: Tuple[float, float],
                 point3: Tuple[float, float]) -> Tuple[float, float]:
    """
    Calculate the circumcenter of a triangle defined by three points.

    The circumcenter is the center of a circle that passes through all three points.

    Args:
        point1 (tuple): (latitude, longitude) of first point
        point2 (tuple): (latitude, longitude) of second point
        point3 (tuple): (latitude, longitude) of third point

    Returns:
        tuple: (latitude, longitude) of the circumcenter

    Raises:
        ValueError: If the points are collinear (lie on a straight line)
    """
    # Convert to radians for calculation
    # Note: We're using a plane approximation for simplicity
    # For more accuracy with large distances, a spherical triangle solution would be needed

    # Extract coordinates
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    # Check if points are collinear
    area = 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if math.isclose(area, 0, abs_tol=1e-10):
        raise ValueError(
            "The three points are collinear (lie on a straight line)")

    # Calculate circumcenter
    # Using the formula from computational geometry
    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

    ux = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2)
          * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / d
    uy = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2)
          * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / d

    return (ux, uy)


def circumradius(point1: Tuple[float, float],
                 point2: Tuple[float, float],
                 point3: Tuple[float, float],
                 unit: str = "km") -> float:
    """
    Calculate the radius of the circumcircle of a triangle.

    Args:
        point1 (tuple): (latitude, longitude) of first point
        point2 (tuple): (latitude, longitude) of second point
        point3 (tuple): (latitude, longitude) of third point
        unit (str, optional): Unit of distance ('km', 'mi', or 'nm'). Defaults to "km".

    Returns:
        float: Radius of the circumcircle in the specified unit
    """
    center = circumcenter(point1, point2, point3)
    # Calculate the distance from the center to any of the three points
    return distance(center, point1, unit=unit)


def centroid(points: List[Tuple[float, float]]) -> Tuple[float, float]:
    """
    Calculate the centroid (center of mass) of a set of points.

    Args:
        points (list): List of (latitude, longitude) tuples

    Returns:
        tuple: (latitude, longitude) of the centroid

    Raises:
        ValueError: If the list of points is empty
    """
    if not points:
        raise ValueError(
            "Cannot calculate centroid of an empty list of points")

    # Calculate the average of coordinates
    sum_lat = sum(p[0] for p in points)
    sum_lon = sum(p[1] for p in points)

    return (sum_lat / len(points), sum_lon / len(points))


def midpoint(point1: Tuple[float, float], point2: Tuple[float, float]) -> Tuple[float, float]:
    """
    Calculate the midpoint between two points.

    Args:
        point1 (tuple): (latitude, longitude) of first point
        point2 (tuple): (latitude, longitude) of second point

    Returns:
        tuple: (latitude, longitude) of the midpoint
    """
    # Simple average for midpoint
    return ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)


def bounding_box(points: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """
    Calculate the bounding box for a set of points.

    Args:
        points (list): List of (latitude, longitude) tuples

    Returns:
        tuple: ((min_lat, min_lon), (max_lat, max_lon)) defining the bounding box

    Raises:
        ValueError: If the list of points is empty
    """
    if not points:
        raise ValueError(
            "Cannot calculate bounding box of an empty list of points")

    min_lat = min(p[0] for p in points)
    max_lat = max(p[0] for p in points)
    min_lon = min(p[1] for p in points)
    max_lon = max(p[1] for p in points)

    return ((min_lat, min_lon), (max_lat, max_lon))


def is_point_inside_polygon(point: Tuple[float, float],
                            polygon: List[Tuple[float, float]]) -> bool:
    """
    Check if a point is inside a polygon using the ray casting algorithm.

    Args:
        point (tuple): (latitude, longitude) of the point to check
        polygon (list): List of (latitude, longitude) tuples defining the polygon vertices

    Returns:
        bool: True if the point is inside the polygon, False otherwise
    """
    if len(polygon) < 3:
        return False

    # Ray casting algorithm
    x, y = point
    inside = False

    j = len(polygon) - 1
    for i in range(len(polygon)):
        xi, yi = polygon[i]
        xj, yj = polygon[j]

        intersect = ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / (yj - yi) + xi)
        if intersect:
            inside = not inside

        j = i

    return inside


def triangle_area(point1: Tuple[float, float],
                  point2: Tuple[float, float],
                  point3: Tuple[float, float],
                  unit: str = "km²") -> float:
    """
    Calculate the approximate area of a triangle on Earth's surface.

    This uses Heron's formula and approximates the distances using the haversine formula.
    For very large triangles, this approximation may not be accurate.

    Args:
        point1 (tuple): (latitude, longitude) of first point
        point2 (tuple): (latitude, longitude) of second point
        point3 (tuple): (latitude, longitude) of third point
        unit (str, optional): Unit of area ('km²', 'mi²', or 'nm²'). Defaults to "km²".

    Returns:
        float: Area of the triangle in the specified unit
    """
    # Calculate the lengths of the three sides using the distance function
    a = distance(point1, point2, unit=unit.replace('²', ''))
    b = distance(point2, point3, unit=unit.replace('²', ''))
    c = distance(point3, point1, unit=unit.replace('²', ''))

    # Use Heron's formula to calculate the area
    s = (a + b + c) / 2  # Semi-perimeter
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))

    return area


def orthocenter(point1: Tuple[float, float],
                point2: Tuple[float, float],
                point3: Tuple[float, float]) -> Tuple[float, float]:
    """
    Calculate the orthocenter of a triangle.

    The orthocenter is the point where the three altitudes of a triangle intersect.

    Args:
        point1 (tuple): (latitude, longitude) of first point
        point2 (tuple): (latitude, longitude) of second point
        point3 (tuple): (latitude, longitude) of third point

    Returns:
        tuple: (latitude, longitude) of the orthocenter
    """
    # Extract coordinates
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    # Calculate the slopes of the sides
    # Handle vertical lines (infinite slope)
    if x2 == x3:
        m1 = 0  # Perpendicular to vertical is horizontal
    else:
        m1 = -(x3 - x2) / (y3 - y2) if y3 != y2 else float('inf')

    if x1 == x3:
        m2 = 0
    else:
        m2 = -(x1 - x3) / (y1 - y3) if y1 != y3 else float('inf')

    if x1 == x2:
        m3 = 0
    else:
        m3 = -(x1 - x2) / (y1 - y2) if y1 != y2 else float('inf')

    # Calculate the points on the opposite sides
    if m1 == float('inf'):
        x4, y4 = x1, y1
    else:
        y4 = y1
        x4 = x1 + (y4 - y1) / m1 if m1 != 0 else x1

    if m2 == float('inf'):
        x5, y5 = x2, y2
    else:
        y5 = y2
        x5 = x2 + (y5 - y2) / m2 if m2 != 0 else x2

    if m3 == float('inf'):
        x6, y6 = x3, y3
    else:
        y6 = y3
        x6 = x3 + (y6 - y3) / m3 if m3 != 0 else x3

    # Now find where these lines intersect
    # For simplicity, we'll use the intersection of the first two altitudes
    # Define the lines in y = mx + b form
    b1 = y1 - m1 * x1
    b2 = y2 - m2 * x2

    # Handle special cases for vertical and horizontal lines
    if m1 == float('inf'):
        x = x1
        y = m2 * x + b2
    elif m2 == float('inf'):
        x = x2
        y = m1 * x + b1
    elif m1 == 0:
        y = y1
        x = (y - b2) / m2 if m2 != 0 else x2
    elif m2 == 0:
        y = y2
        x = (y - b1) / m1 if m1 != 0 else x1
    else:
        # Find intersection
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1

    return (x, y)
