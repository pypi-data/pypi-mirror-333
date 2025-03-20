"""
Tests for the puzzle_helpers module.
"""
import unittest
from gc_utils.utils import puzzle_helpers


class PuzzleHelpersTests(unittest.TestCase):
    """Test cases for the puzzle helper utilities."""

    def test_ascii_conversion(self):
        """Test ASCII to text and text to ASCII conversion."""
        # Test text to ASCII
        ascii_values = puzzle_helpers.text_to_ascii("Hello")
        self.assertEqual(ascii_values, [72, 101, 108, 108, 111])

        # Test ASCII to text
        text = puzzle_helpers.ascii_to_text([72, 101, 108, 108, 111])
        self.assertEqual(text, "Hello")

        # Test ASCII to text with string input
        text = puzzle_helpers.ascii_to_text("72 101 108 108 111")
        self.assertEqual(text, "Hello")

    def test_anagram_solver(self):
        """Test anagram solving."""
        # Simple test with short string
        anagrams = puzzle_helpers.anagram_solver("abc")
        self.assertIn("abc", anagrams)
        self.assertIn("cab", anagrams)
        self.assertIn("bca", anagrams)

        # Test warning for long string
        result = puzzle_helpers.anagram_solver("toolongstring")
        self.assertTrue(any("too long" in r.lower() for r in result))

    def test_reverse_functions(self):
        """Test text reversal functions."""
        # Test character reversal
        reversed_text = puzzle_helpers.reverse_text("Hello World")
        self.assertEqual(reversed_text, "dlroW olleH")

        # Test word order reversal
        reversed_words = puzzle_helpers.reverse_words("Hello World")
        self.assertEqual(reversed_words, "World Hello")

    def test_atbash_cipher(self):
        """Test Atbash cipher."""
        encoded = puzzle_helpers.atbash_cipher("Hello World")
        self.assertEqual(encoded, "Svool Dliow")

        # Test reversibility
        decoded = puzzle_helpers.atbash_cipher(encoded)
        self.assertEqual(decoded, "Hello World")

    def test_number_letter_conversion(self):
        """Test number to letter and letter to number conversion."""
        # Test letter to number
        numbers = puzzle_helpers.letter_to_number("ABC")
        self.assertEqual(numbers, [1, 2, 3])

        # Test with offset
        numbers = puzzle_helpers.letter_to_number("ABC", offset=1)
        self.assertEqual(numbers, [0, 1, 2])

        # Test number to letter
        letters = puzzle_helpers.number_to_letter([1, 2, 3])
        self.assertEqual(letters, "ABC")

        # Test with offset
        letters = puzzle_helpers.number_to_letter([0, 1, 2], offset=-1)
        self.assertEqual(letters, "ABC")

        # Test string input
        letters = puzzle_helpers.number_to_letter("1 2 3")
        self.assertEqual(letters, "ABC")

    def test_extract_numbers(self):
        """Test extracting numbers from text."""
        numbers = puzzle_helpers.extract_numbers(
            "The coordinates are N 47° 36.123 W 122° 19.456")
        self.assertEqual(numbers, [47, 36, 123, 122, 19, 456])


if __name__ == "__main__":
    unittest.main()
