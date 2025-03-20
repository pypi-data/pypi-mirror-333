"""
Utilities for handling coordinates - parsing, formatting, and distance calculations.
"""
import re
import math


def parse_coordinate(coord_string):
    """
    Parse a coordinate string into decimal latitude and longitude.
    Supports formats like:
    - N 47° 36.123 W 122° 19.456
    - 47° 36.123' N, 122° 19.456' W
    - 47.602050, -122.324194

    Args:
        coord_string (str): The coordinate string to parse

    Returns:
        tuple: (latitude, longitude) in decimal degrees
    """
    # First check if it's already in decimal format
    decimal_pattern = r'(-?\d+\.\d+)[,\s]+(-?\d+\.\d+)'
    decimal_match = re.search(decimal_pattern, coord_string)
    if decimal_match:
        return float(decimal_match.group(1)), float(decimal_match.group(2))

    # Match degrees-minutes-seconds (DMS) format
    dms_pattern = r'([NS])\s*(\d+)[°\s]+(\d+)[\'′\s]+(\d+\.?\d*)[\"\″]?\s*,?\s*([EW])\s*(\d+)[°\s]+(\d+)[\'′\s]+(\d+\.?\d*)[\"\″]?'
    dms_match = re.search(dms_pattern, coord_string, re.IGNORECASE)
    if dms_match:
        lat_dir, lat_deg, lat_min, lat_sec, lon_dir, lon_deg, lon_min, lon_sec = dms_match.groups()
        latitude = float(lat_deg) + float(lat_min) / 60 + float(lat_sec) / 3600
        longitude = float(lon_deg) + float(lon_min) / \
            60 + float(lon_sec) / 3600

        if lat_dir.upper() == 'S':
            latitude = -latitude
        if lon_dir.upper() == 'W':
            longitude = -longitude

        return latitude, longitude

    # Match degrees-decimal minutes (DDM) format, common in geocaching
    ddm_pattern = r'([NS])\s*(\d+)[°\s]+(\d+\.?\d*)[\'\s]+([EW])\s*(\d+)[°\s]+(\d+\.?\d*)[\'\s]+'
    ddm_match = re.search(ddm_pattern, coord_string, re.IGNORECASE)
    if ddm_match:
        lat_dir, lat_deg, lat_min, lon_dir, lon_deg, lon_min = ddm_match.groups()
        latitude = float(lat_deg) + float(lat_min) / 60
        longitude = float(lon_deg) + float(lon_min) / 60

        if lat_dir.upper() == 'S':
            latitude = -latitude
        if lon_dir.upper() == 'W':
            longitude = -longitude

        return latitude, longitude

    # Alternative DDM pattern without apostrophes
    alt_ddm_pattern = r'([NS])\s*(\d+)[°\s]+(\d+\.?\d*)\s+([EW])\s*(\d+)[°\s]+(\d+\.?\d*)'
    alt_ddm_match = re.search(alt_ddm_pattern, coord_string, re.IGNORECASE)
    if alt_ddm_match:
        lat_dir, lat_deg, lat_min, lon_dir, lon_deg, lon_min = alt_ddm_match.groups()
        latitude = float(lat_deg) + float(lat_min) / 60
        longitude = float(lon_deg) + float(lon_min) / 60

        if lat_dir.upper() == 'S':
            latitude = -latitude
        if lon_dir.upper() == 'W':
            longitude = -longitude

        return latitude, longitude

    # If all patterns fail
    raise ValueError(f"Could not parse coordinate string: {coord_string}")


def format_coordinate(latitude, longitude, format="ddm"):
    """
    Format decimal coordinates into a user-friendly string.

    Args:
        latitude (float): Decimal latitude
        longitude (float): Decimal longitude
        format (str, optional): Output format ('decimal', 'ddm', or 'dms'). Defaults to "ddm".

    Returns:
        str: Formatted coordinate string
    """
    if format == "decimal":
        return f"{latitude:.6f}, {longitude:.6f}"

    lat_dir = "N" if latitude >= 0 else "S"
    lon_dir = "E" if longitude >= 0 else "W"

    lat_abs = abs(latitude)
    lon_abs = abs(longitude)

    lat_deg = int(lat_abs)
    lon_deg = int(lon_abs)

    if format == "ddm":
        lat_min = (lat_abs - lat_deg) * 60
        lon_min = (lon_abs - lon_deg) * 60
        return f"{lat_dir} {lat_deg}° {lat_min:.3f}' {lon_dir} {lon_deg}° {lon_min:.3f}'"

    elif format == "dms":
        lat_min = int((lat_abs - lat_deg) * 60)
        lon_min = int((lon_abs - lon_deg) * 60)

        lat_sec = ((lat_abs - lat_deg) * 60 - lat_min) * 60
        lon_sec = ((lon_abs - lon_deg) * 60 - lon_min) * 60

        return f"{lat_dir} {lat_deg}° {lat_min}' {lat_sec:.3f}\" {lon_dir} {lon_deg}° {lon_min}' {lon_sec:.3f}\""

    else:
        raise ValueError(f"Unsupported format: {format}")


def distance(coord1, coord2, unit="km"):
    """
    Calculate the great-circle distance between two coordinates using the Haversine formula.

    Args:
        coord1 (tuple): (latitude, longitude) of first point
        coord2 (tuple): (latitude, longitude) of second point
        unit (str, optional): Unit of distance ('km', 'mi', or 'nm'). Defaults to "km".

    Returns:
        float: Distance between the two points in the specified unit
    """
    # Earth radius in kilometers
    R = 6371.0

    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance_km = R * c

    if unit == "km":
        return distance_km
    elif unit == "mi":
        return distance_km * 0.621371
    elif unit == "nm":  # Nautical miles
        return distance_km * 0.539957
    else:
        raise ValueError(f"Unsupported unit: {unit}")


def project_waypoint(latitude, longitude, distance, bearing, unit="km"):
    """
    Calculate a new waypoint given a starting point, distance, and bearing.

    Args:
        latitude (float): Starting latitude in decimal degrees
        longitude (float): Starting longitude in decimal degrees
        distance (float): Distance to travel
        bearing (float): Bearing in degrees (0 = North, 90 = East, etc.)
        unit (str, optional): Unit of distance ('km', 'mi', or 'nm'). Defaults to "km".

    Returns:
        tuple: (latitude, longitude) of the destination point
    """
    # Convert distance to kilometers if necessary
    if unit == "mi":
        distance = distance * 1.60934
    elif unit == "nm":
        distance = distance * 1.852

    # Earth radius in kilometers
    R = 6371.0

    # Convert to radians
    lat1 = math.radians(latitude)
    lon1 = math.radians(longitude)
    bearing_rad = math.radians(bearing)

    # Angular distance
    ang_dist = distance / R

    # Calculate the destination point
    lat2 = math.asin(math.sin(lat1) * math.cos(ang_dist) +
                     math.cos(lat1) * math.sin(ang_dist) * math.cos(bearing_rad))

    lon2 = lon1 + math.atan2(math.sin(bearing_rad) * math.sin(ang_dist) * math.cos(lat1),
                             math.cos(ang_dist) - math.sin(lat1) * math.sin(lat2))

    # Convert back to degrees
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    return (lat2, lon2)
