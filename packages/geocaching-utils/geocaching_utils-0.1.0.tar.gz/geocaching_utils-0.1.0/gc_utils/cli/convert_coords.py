"""
CLI command for coordinate conversion and distance calculation.
"""
import argparse
from gc_utils.utils import coordinates


def register_subcommand(subparsers):
    """Register the coords subcommand with the parser."""
    coords_parser = subparsers.add_parser(
        'coords',
        help='Convert coordinates and calculate distances'
    )

    coords_parser.add_argument(
        '--mode',
        choices=['convert', 'distance'],
        default='convert',
        help='Operation mode: convert coordinates or calculate distance'
    )

    coords_parser.add_argument(
        'coordinate_strings',
        nargs='+',
        help='Coordinate string(s) to process. Use one for conversion, two for distance calculation.'
    )

    coords_parser.add_argument(
        '--out-format',
        choices=['decimal', 'ddm', 'dms'],
        default='decimal',
        help='Output format for coordinate conversion: decimal (DD.DDDD), ddm (DD MM.MMM), or dms (DD MM SS.SSS)'
    )

    coords_parser.add_argument(
        '--unit',
        choices=['km', 'mi', 'nm'],
        default='km',
        help='Distance unit for distance calculations: kilometers (km), miles (mi), or nautical miles (nm)'
    )

    return coords_parser


def handle(args):
    """Handle the coords command."""
    try:
        mode = args.mode

        if mode == 'convert':
            if len(args.coordinate_strings) != 1:
                print("Error: Coordinate conversion requires exactly one coordinate")
                return 1

            # Parse the input coordinate
            lat, lon = coordinates.parse_coordinate(args.coordinate_strings[0])

            # Format the output according to the specified format
            formatted = coordinates.format_coordinate(
                lat, lon, format=args.out_format)

            print(formatted)

        elif mode == 'distance':
            if len(args.coordinate_strings) != 2:
                print("Error: Distance calculation requires exactly two coordinates")
                return 1

            # Parse the input coordinates
            coord1 = coordinates.parse_coordinate(args.coordinate_strings[0])
            coord2 = coordinates.parse_coordinate(args.coordinate_strings[1])

            # Calculate the distance
            dist = coordinates.distance(coord1, coord2, unit=args.unit)

            # Determine unit label
            unit_labels = {
                'km': 'kilometers',
                'mi': 'miles',
                'nm': 'nautical miles'
            }
            unit_label = unit_labels.get(args.unit, args.unit)

            print(f"Distance: {dist:.2f} {unit_label}")

        return 0
    except ValueError as e:
        print(f"Error: {str(e)}")
        return 1
