"""
CLI command for puzzle solving tools.
"""
import argparse
from gc_utils.utils import puzzle_helpers


def register_subcommand(subparsers):
    """Register the tools subcommand with the parser."""
    puzzle_parser = subparsers.add_parser(
        'tools',
        help='Various puzzle solving utilities'
    )

    # Use --mode argument instead of subcommands
    puzzle_parser.add_argument(
        '--mode',
        required=True,
        choices=['ascii-to-text', 'text-to-ascii',
                 'anagram', 'a1z26', 'reverse'],
        help='Puzzle operation to perform'
    )

    # Input argument - used by all modes but with different meaning
    puzzle_parser.add_argument(
        'input',
        help='Input text or values for the selected mode'
    )

    # Mode-specific arguments
    puzzle_parser.add_argument(
        '--wordlist',
        help='Path to a wordlist file for anagram mode (optional)'
    )

    puzzle_parser.add_argument(
        '--direction',
        choices=['to-numbers', 'to-letters'],
        help='Conversion direction for a1z26 mode'
    )

    puzzle_parser.add_argument(
        '--offset',
        type=int,
        default=0,
        help='Offset to apply for a1z26 mode (e.g., -1 would make A=0, B=1, etc.)'
    )

    puzzle_parser.add_argument(
        '--words-only',
        action='store_true',
        help='Reverse the word order only, not the characters (for reverse mode)'
    )

    return puzzle_parser


def handle(args):
    """Handle the tools command."""
    mode = args.mode

    try:
        if mode == 'ascii-to-text':
            result = puzzle_helpers.ascii_to_text(args.input)
            print(result)

        elif mode == 'text-to-ascii':
            result = puzzle_helpers.text_to_ascii(args.input)
            print(' '.join(str(val) for val in result))

        elif mode == 'anagram':
            result = puzzle_helpers.anagram_solver(
                args.input,
                wordlist_path=args.wordlist
            )
            if len(result) > 100:
                print(
                    f"Found {len(result)} possible anagrams. Showing first 100:")
                for word in result[:100]:
                    print(word)
                print(f"... and {len(result) - 100} more")
            else:
                print(f"Found {len(result)} possible anagrams:")
                for word in result:
                    print(word)

        elif mode == 'a1z26':
            if not args.direction:
                print("Error: --direction is required for a1z26 mode")
                return 1

            if args.direction == 'to-numbers':
                result = puzzle_helpers.letter_to_number(
                    args.input, offset=args.offset)
                print(' '.join(str(num) for num in result))
            else:  # to-letters
                result = puzzle_helpers.number_to_letter(
                    args.input, offset=args.offset)
                print(result)

        elif mode == 'reverse':
            if args.words_only:
                result = puzzle_helpers.reverse_words(args.input)
            else:
                result = puzzle_helpers.reverse_text(args.input)
            print(result)

        return 0
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
