"""
CLI command for decoding various ciphers.
"""
import argparse
from gc_utils.utils import ciphers


def register_subcommand(subparsers):
    """Register the cipher subcommand with the parser."""
    decode_parser = subparsers.add_parser(
        'cipher',
        help='Decode various types of ciphers'
    )

    decode_parser.add_argument(
        '--mode',
        required=True,
        choices=['caesar', 'vigenere', 'atbash', 'morse'],
        help='Cipher mode to use for decoding'
    )

    # Mode-specific arguments
    decode_parser.add_argument(
        '--shift',
        type=int,
        default=13,
        help='Shift value for Caesar cipher (default: 13 for ROT13)'
    )

    decode_parser.add_argument(
        '--key',
        help='Key for Vigenère cipher'
    )

    decode_parser.add_argument(
        'text',
        help='Text to decode'
    )

    return decode_parser


def handle(args):
    """Handle the cipher command."""
    method = args.mode.lower()
    text = args.text

    if method == 'caesar':
        result = ciphers.caesar_decode(text, shift=args.shift)
    elif method == 'vigenere':
        if not args.key:
            print("Error: Key is required for Vigenère cipher")
            return 1
        result = ciphers.vigenere_decode(text, key=args.key)
    elif method == 'atbash':
        # Import the atbash cipher function from puzzle_helpers
        from gc_utils.utils.puzzle_helpers import atbash_cipher
        result = atbash_cipher(text)
    elif method == 'morse':
        result = ciphers.morse_decode(text)
    else:
        print(f"Error: Unsupported cipher mode: {method}")
        return 1

    print(result)
    return 0
