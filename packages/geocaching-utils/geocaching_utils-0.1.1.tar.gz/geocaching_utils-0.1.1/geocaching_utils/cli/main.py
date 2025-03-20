"""
Main CLI entry point for gc-utils.
"""
import argparse
import sys
import importlib
from geocaching_utils import __version__


def main():
    """Main CLI entry point for gc-utils."""
    parser = argparse.ArgumentParser(
        prog="gc-utils",
        description="Geocaching puzzle utilities and tools"
    )

    parser.add_argument('--version', action='version',
                        version=f'gc-utils {__version__}')

    subparsers = parser.add_subparsers(
        dest='command', help='Available commands')

    # Define a mapping between CLI commands and module names
    command_to_module = {
        'cipher': 'decode_cipher',
        'coords': 'convert_coords',
        'tools': 'puzzle_tools',
        'geometry': 'geometry_calc'
    }

    # Import all modules using the mapping
    for command, module_name in command_to_module.items():
        try:
            # Import the module
            module = importlib.import_module(
                f'geocaching_utils.cli.{module_name}')
            # Register its subcommand
            if hasattr(module, 'register_subcommand'):
                module.register_subcommand(subparsers)
        except ImportError as e:
            print(
                f"Warning: Could not import command module '{module_name}': {e}", file=sys.stderr)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Get the module name for the command
    module_name = command_to_module.get(args.command, args.command)

    # Import the module for the selected command
    try:
        module = importlib.import_module(f'geocaching_utils.cli.{module_name}')

        # Execute the command
        if hasattr(module, 'handle'):
            return module.handle(args)
        else:
            print(
                f"Error: Command module '{module_name}' does not have a handle function", file=sys.stderr)
            return 1
    except ImportError as e:
        print(
            f"Error importing module for command '{args.command}': {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
