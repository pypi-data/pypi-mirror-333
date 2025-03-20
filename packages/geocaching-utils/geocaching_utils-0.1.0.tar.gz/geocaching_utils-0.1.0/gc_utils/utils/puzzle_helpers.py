"""
General utilities for puzzle solving that aren't specific to ciphers or coordinates.
"""
import re
import itertools


def anagram_solver(letters, wordlist_path=None):
    """
    Find anagrams for a given set of letters.
    If a wordlist is provided, it will search for matches in that list.
    Otherwise, it will return all permutations.

    Args:
        letters (str): The letters to find anagrams for
        wordlist_path (str, optional): Path to a wordlist file. Defaults to None.

    Returns:
        list: Possible anagrams
    """
    letters = letters.lower().strip()

    # Remove spaces and sort the letters
    sorted_letters = ''.join(sorted(letters.replace(' ', '')))

    if wordlist_path:
        results = []
        try:
            with open(wordlist_path, 'r') as f:
                for line in f:
                    word = line.strip().lower()
                    sorted_word = ''.join(sorted(word))
                    if sorted_word == sorted_letters:
                        results.append(word)
        except Exception as e:
            return [f"Error reading wordlist: {str(e)}"]
        return results
    else:
        # If no wordlist, just generate permutations
        # Note: This can be VERY slow for long strings
        if len(letters) > 8:
            return ["Warning: String too long for permutation (> 8 chars). Provide a wordlist."]

        perms = [''.join(p) for p in itertools.permutations(letters)]
        # Remove duplicates
        return list(set(perms))


def ascii_to_text(ascii_list):
    """
    Convert ASCII values to text.

    Args:
        ascii_list (list or str): List of ASCII values or string of space-separated ASCII values

    Returns:
        str: Converted text
    """
    if isinstance(ascii_list, str):
        try:
            # Try to parse as space-separated ASCII values
            ascii_list = [int(x) for x in ascii_list.split()]
        except ValueError:
            return "Error: Could not parse input as ASCII values"

    try:
        return ''.join(chr(x) for x in ascii_list)
    except (ValueError, TypeError):
        return "Error: Invalid ASCII values"


def text_to_ascii(text):
    """
    Convert text to ASCII values.

    Args:
        text (str): The text to convert

    Returns:
        list: List of ASCII values
    """
    return [ord(c) for c in text]


def reverse_text(text):
    """
    Reverse the characters in a string.

    Args:
        text (str): The text to reverse

    Returns:
        str: The reversed text
    """
    return text[::-1]


def reverse_words(text):
    """
    Reverse the order of words in a string, but keep the characters in the same order.

    Args:
        text (str): The text with words to reverse

    Returns:
        str: The text with reversed word order
    """
    return ' '.join(text.split()[::-1])


def atbash_cipher(text):
    """
    Apply the Atbash cipher (A=Z, B=Y, etc.) to the input text.

    Args:
        text (str): The text to encode/decode

    Returns:
        str: The encoded/decoded text
    """
    result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                # A=65, Z=90 in ASCII
                result += chr(155 - ord(char))  # 155 = 65 + 90
            else:
                # a=97, z=122 in ASCII
                result += chr(219 - ord(char))  # 219 = 97 + 122
        else:
            result += char
    return result


def number_to_letter(numbers, offset=0):
    """
    Convert numbers to letters (A=1, B=2, etc.)

    Args:
        numbers (list or str): List of numbers or string of space-separated numbers
        offset (int, optional): Offset to apply (e.g., 0 means A=1, 1 means A=0). Defaults to 0.

    Returns:
        str: Converted text
    """
    result = ""
    if isinstance(numbers, str):
        numbers = [int(x) for x in numbers.split()]
    elif isinstance(numbers, list):
        numbers = [int(x) for x in numbers]
    for num in numbers:
        adjusted = num - offset
        if 1 <= adjusted <= 26:
            result += chr(adjusted + 64)  # 'A' = chr(65) => 1+64=65
    return result


def letter_to_number(text, offset=0):
    """
    Convert letters to numbers (A=1, B=2, etc.)

    Args:
        text (str): The text to convert
        offset (int, optional): Offset to apply (e.g., 0 means A=1, 1 means A=0). Defaults to 0.

    Returns:
        list: List of numbers
    """
    return [ord(c.upper()) - 64 - offset for c in text if c.isalpha()]


def extract_numbers(text):
    """
    Extract all numbers from a text string.

    Args:
        text (str): The text to extract numbers from

    Returns:
        list: List of extracted numbers
    """
    return [int(x) for x in re.findall(r'\d+', text)]
