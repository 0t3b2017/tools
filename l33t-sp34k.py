#!/usr/bin/env python3

from sys import argv

"""
Docstring for l33t-sp3@k

Converts regular text into "leet speak" (l33t sp3@k) by replacing certain letters with numbers or symbols and reverse it.
"""

def to_leet_speak(text):
    """Converts regular text to leet speak."""
    leet_dict = {
        'a': '4',
        'e': '3',
        'i': '1',
        'o': '0',
        's': '5',
        't': '7',
        'A': '@',
        'E': '3',
        'I': '1',
        'O': '0',
        'S': '5',
        'T': '7',
        ' ': '+'
    }
    return ''.join(leet_dict.get(char, char) for char in text)


def from_leet_speak(leet_text):
    """Converts leet speak back to regular text."""
    reverse_leet_dict = {
        '4': 'a',
        '3': 'e',
        '1': 'i',
        '0': 'o',
        '5': 's',
        '7': 't'
    }
    return ''.join(reverse_leet_dict.get(char, char) for char in leet_text)


def reverse_leet_speak(leet_text):
    """Reverses leet speak phrase."""
    return leet_text[::-1]
    

if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: python3 l33t-sp3@k.py <text>")
        exit(1)
    print("Reversed Text:", reverse_leet_speak(to_leet_speak(argv[1]))[:15])

