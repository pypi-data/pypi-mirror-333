"""
Cipher utilities for decoding various types of encryption methods commonly used in geocaching puzzles.
"""
from collections import Counter
import string


def caesar_decode(text, shift=13):
    """
    Decode a string that has been encoded with a Caesar cipher.

    Args:
        text (str): The text to decode
        shift (int, optional): The shift to apply. Defaults to 13 (ROT13).

    Returns:
        str: The decoded text
    """
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            # Convert to 0-25, shift, and convert back to ASCII
            result += chr((ord(char) - ascii_offset - shift) %
                          26 + ascii_offset)
        else:
            result += char
    return result


def vigenere_decode(text, key):
    result = ""
    key = key.lower()
    key_length = len(key)

    j = 0  # Index for tracking position in the key
    for char in text:
        if char.isalpha():
            # Determine if it's uppercase or lowercase
            is_upper = char.isupper()
            # Convert to base 0 (A/a = 0, Z/z = 25)
            char_code = ord(char.lower()) - ord('a')
            # Get the current key character and convert to base 0
            key_char = key[j % key_length]
            key_code = ord(key_char) - ord('a')

            # Perform the decoding: (char_code - key_code) % 26
            decoded_code = (char_code - key_code) % 26
            # Convert back to ASCII
            decoded_char = chr(decoded_code + ord('a'))

            # Restore the original case
            if is_upper:
                decoded_char = decoded_char.upper()

            result += decoded_char
            j += 1
        else:
            result += char

    return result


def frequency_analysis(text):
    """
    Perform frequency analysis on the input text.

    Args:
        text (str): The text to analyze

    Returns:
        dict: A dictionary mapping characters to their frequency counts
    """
    # Filter only alphabet characters and convert to lowercase
    filtered_text = ''.join(char.lower() for char in text if char.isalpha())
    return dict(Counter(filtered_text))


def substitution_bruteforce(text, known_patterns=None):
    """
    Attempt to decode a substitution cipher by statistical analysis.
    This is a simplified implementation and may not be effective for all ciphers.

    Args:
        text (str): The text to decode
        known_patterns (dict, optional): Known character mappings. Defaults to None.

    Returns:
        str: Best guess at decoded text
    """
    if not text:
        return ""

    # English letter frequency
    eng_freq = {
        'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7, 's': 6.3,
        'h': 6.1, 'r': 6.0, 'd': 4.3, 'l': 4.0, 'c': 2.8, 'u': 2.8, 'm': 2.4,
        'w': 2.4, 'f': 2.2, 'g': 2.0, 'y': 2.0, 'p': 1.9, 'b': 1.5, 'v': 1.0,
        'k': 0.8, 'j': 0.2, 'x': 0.2, 'q': 0.1, 'z': 0.1
    }

    # Get frequency of each character in the text
    freq = frequency_analysis(text)

    # Sort the characters by frequency
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    sorted_chars = [char for char, _ in sorted_freq]

    # Sort English letters by frequency
    sorted_eng = sorted(eng_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_eng_chars = [char for char, _ in sorted_eng]

    # Create the mapping
    mapping = {}
    for i, char in enumerate(sorted_chars):
        if i < len(sorted_eng_chars):
            mapping[char] = sorted_eng_chars[i]

    # Override with known patterns if provided
    if known_patterns:
        mapping.update(known_patterns)

    # Apply the mapping
    result = ""
    for char in text.lower():
        if char in mapping:
            # Preserve case
            if char.isupper():
                result += mapping[char].upper()
            else:
                result += mapping[char]
        else:
            result += char

    return result


def morse_decode(morse_code):
    """
    Decode Morse code to text.

    Args:
        morse_code (str): The Morse code to decode, with spaces between characters and slashes between words

    Returns:
        str: The decoded text
    """
    morse_dict = {
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
        '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
        '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
        '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
        '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
        '--..': 'Z', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
        '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
        '-----': '0', '.-.-.-': '.', '--..--': ',', '..--..': '?',
        '.----.': "'", '-.-.--': '!', '-..-.': '/', '-.--.': '(', '-.--.-': ')',
        '.-...': '&', '---...': ':', '-.-.-.': ';', '-...-': '=', '.-.-.': '+',
        '-....-': '-', '..--.-': '_', '.-..-.': '"', '...-..-': '$',
        '.--.-.': '@'
    }

    result = ""
    words = morse_code.strip().split(' / ')

    for word in words:
        for char in word.split():
            if char in morse_dict:
                result += morse_dict[char]
            else:
                result += '?'  # Unknown character
        result += ' '

    return result.strip()
