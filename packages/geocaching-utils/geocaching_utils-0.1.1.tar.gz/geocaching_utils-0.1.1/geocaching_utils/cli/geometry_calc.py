"""
CLI command for geometric calculations on coordinates.
"""
import argparse
from geocaching_utils.utils import coordinates, geometry


def register_subcommand(subparsers):
    """Register the geometry subcommand with the parser."""
    geometry_parser = subparsers.add_parser(
        'geometry',
        help='Perform geometric calculations on coordinates'
    )

    # Add mode argument instead of subcommands
    geometry_parser.add_argument(
        '--mode',
        required=True,
        choices=['circumcenter', 'centroid', 'midpoint',
                 'triangle-area', 'bounding-box'],
        help='Geometric operation to perform'
    )

    # Arguments for all modes
    geometry_parser.add_argument(
        'points',
        nargs='+',
        help='Coordinates for geometric calculation (e.g., "N 47° 36.123 W 122° 19.456")'
    )

    # Format for output coordinates
    geometry_parser.add_argument(
        '--format',
        choices=['decimal', 'ddm', 'dms'],
        default='decimal',
        help='Output format for coordinates'
    )

    # Circumcenter specific arguments
    geometry_parser.add_argument(
        '--radius',
        action='store_true',
        help='Calculate and display the circumradius (for circumcenter mode)'
    )

    # Unit arguments for distance/area calculations
    geometry_parser.add_argument(
        '--unit',
        help='Unit for measurements: km/mi/nm for distances, km²/mi²/nm² for areas'
    )

    return geometry_parser


def handle(args):
    """Handle the geometry command."""
    mode = args.mode

    try:
        if mode == 'circumcenter':
            if len(args.points) != 3:
                raise ValueError(
                    "Circumcenter calculation requires exactly 3 points")

            # Parse the three points
            point1 = coordinates.parse_coordinate(args.points[0])
            point2 = coordinates.parse_coordinate(args.points[1])
            point3 = coordinates.parse_coordinate(args.points[2])

            # Calculate the circumcenter
            center = geometry.circumcenter(point1, point2, point3)

            # Format the output - unpack the tuple for format_coordinate
            formatted_center = coordinates.format_coordinate(
                center[0], center[1], format=args.format)
            print(f"Circumcenter: {formatted_center}")

            # Calculate and display the circumradius if requested
            if args.radius:
                unit = args.unit if args.unit else 'km'
                if unit not in ['km', 'mi', 'nm']:
                    unit = 'km'
                radius = geometry.circumradius(
                    point1, point2, point3, unit=unit)
                print(f"Circumradius: {radius:.3f} {unit}")

        elif mode == 'centroid':
            # Parse all points
            points = [coordinates.parse_coordinate(p) for p in args.points]

            # Calculate the centroid
            center = geometry.centroid(points)

            # Format the output - unpack the tuple for format_coordinate
            formatted_center = coordinates.format_coordinate(
                center[0], center[1], format=args.format)
            print(f"Centroid: {formatted_center}")

        elif mode == 'midpoint':
            if len(args.points) != 2:
                raise ValueError(
                    "Midpoint calculation requires exactly 2 points")

            # Parse the two points
            point1 = coordinates.parse_coordinate(args.points[0])
            point2 = coordinates.parse_coordinate(args.points[1])

            # Calculate the midpoint
            mid = geometry.midpoint(point1, point2)

            # Format the output - unpack the tuple for format_coordinate
            formatted_mid = coordinates.format_coordinate(
                mid[0], mid[1], format=args.format)
            print(f"Midpoint: {formatted_mid}")

        elif mode == 'triangle-area':
            if len(args.points) != 3:
                raise ValueError(
                    "Triangle area calculation requires exactly 3 points")

            # Parse the three points
            point1 = coordinates.parse_coordinate(args.points[0])
            point2 = coordinates.parse_coordinate(args.points[1])
            point3 = coordinates.parse_coordinate(args.points[2])

            # Default unit if not specified
            unit = args.unit if args.unit else 'km²'
            if unit not in ['km²', 'mi²', 'nm²']:
                unit = 'km²'

            # Calculate the area
            area = geometry.triangle_area(
                point1, point2, point3, unit=unit)

            # Output the result
            print(f"Triangle area: {area:.6f} {unit}")

        elif mode == 'bounding-box':
            # Parse all points
            points = [coordinates.parse_coordinate(p) for p in args.points]

            # Calculate the bounding box
            (min_lat, min_lon), (max_lat, max_lon) = geometry.bounding_box(points)

            # Format the coordinates - unpack the tuples for format_coordinate
            min_point = coordinates.format_coordinate(
                min_lat, min_lon, format=args.format)
            max_point = coordinates.format_coordinate(
                max_lat, max_lon, format=args.format)

            # Output the result
            print(f"Bounding Box:")
            print(f"  Southwest corner: {min_point}")
            print(f"  Northeast corner: {max_point}")

        return 0

    except ValueError as e:
        print(f"Error: {str(e)}")
        return 1
