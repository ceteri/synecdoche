import pathlib
import sys

from icecream import ic
import requests

term = "weather"
words = set([])

api_url = "https://new.wordsmith.org/anagram/anagram.cgi?anagram={}&t=500&a=n".format(term)
response = requests.get(api_url)

pat_head = "Displaying all:"
pat_done = "<script>document.body"
ignore = True

for i, line in enumerate(response.text.split("\n")):
    if pat_done in line:
        ignore = True

    if not ignore:
        for word in line.strip().lstrip("</b><br>").rstrip("<br>").split(" "):
            words.add(word.lower())

    if ignore and pat_head in line:
        ignore = False

print(len(words), words)
