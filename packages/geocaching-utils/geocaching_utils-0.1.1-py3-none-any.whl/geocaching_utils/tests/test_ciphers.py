"""
Tests for the ciphers module.
"""
import unittest
from geocaching_utils.utils import ciphers


class CipherTests(unittest.TestCase):
    """Test cases for the cipher utilities."""

    def test_caesar_decode(self):
        """Test Caesar cipher decoding."""
        # Test ROT13 (shift=13)
        self.assertEqual(ciphers.caesar_decode(
            "Uryyb, jbeyq!", shift=13), "Hello, world!")

        # Test with different shift
        self.assertEqual(ciphers.caesar_decode(
            "Jgnnq, yqtnf!", shift=2), "Hello, world!")

    def test_vigenere_decode(self):
        """Test Vigenère cipher decoding."""
        self.assertEqual(
            ciphers.vigenere_decode("Rijvs, uyvjn!", key="key"),
            "Hello, world!"
        )

    def test_morse_decode(self):
        """Test Morse code decoding."""
        morse = ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
        self.assertEqual(ciphers.morse_decode(morse), "HELLO WORLD")


if __name__ == "__main__":
    unittest.main()
