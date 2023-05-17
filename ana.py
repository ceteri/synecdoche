#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Wrapper for the Internet Anagram Server.
"""

from collections import defaultdict
import pathlib
import sys
import typing

from icecream import ic
import requests


def explode (
    text: str,
    ) -> list:
    """
Explode a word into a list of characters
    """
    return list(text.replace(" ", "").lower())


def request_words (
    term: str,
    ) -> typing.List[ str ]:
    """
Make an API call to the anagram server.
    """
    api_url = f"https://new.wordsmith.org/anagram/anagram.cgi?anagram={ term }&t=500&a=n"
    response = requests.get(api_url)

    pat_head = "Displaying all:"
    pat_done = "<script>document.body"
    ignore = True

    words = set([])

    for i, line in enumerate(response.text.split("\n")):
        if pat_done in line:
            ignore = True

        if not ignore:
            for word in line.strip().lstrip("</b><br>").rstrip("<br>").lower().split(" "):
                words.add(word)

        if ignore and pat_head in line:
            ignore = False

    return words


if __name__ == "__main__":
    text: str = "bitwest the best weekend of my year"
    ic(text)

    targets: typing.List[ str ] = [
        "monkey",
        "tribe",
        "fete",
        "by",
        "swathed",
        "sweet",
    ]
    ic(targets)

    letters: typing.Dict[ str, int ] = defaultdict(int)

    for char in explode(text):
        letters[char] += 1

    ic(letters)

    for word in targets:
        for char in explode(word):
            letters[char] -= 1

    residual = [
        char * count
        for char, count in sorted(letters.items())
    ]

    term: str = "".join(residual)
    ic(term)

    words = request_words(term)
    ic(len(words), words)
