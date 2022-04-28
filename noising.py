#!/usr/bin/env python3

"""Add synthetic noise on source side.

Synthetic noise to be sampled on the source side of the translation to improve
robustness towards what we expect on the input.

Types of noise we expect:
    * Punctuation stripping
    * Ommiting accents
    * Lower/upper case
"""

import random
import unicodedata
import re
import string
import sys

PUNCT = re.compile("[" + re.escape(string.punctuation) + "„“»«]")


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def main():
    for line in sys.stdin:
        line = line.strip()
        if random.random() < .05:
            line = line.lower()
        if random.random() < .05:
            backup = line
            line = " ".join(PUNCT.sub(" ", line).split())
            if line == "":
                line = backup

        remove_accent_p = 0.
        if random.random() < .2:
            remove_accent_p = .1
        elif random.random() < .4:
            remove_accent_p = .5
        elif random.random() < .8:
            remove_accent_p = 1.

        noisy_words = []
        for word in line.split():
            if random.random() < remove_accent_p:
                word = strip_accents(word)
            if (word and word[-1] in string.punctuation
                    and random.random() < 0.2):
                word = word[:-1]
            if word:  # the previous line can delete the word
                noisy_words.append(word)

        if (noisy_words and noisy_words[-1][-1] in string.punctuation
                and random.random() < 0.2):
            noisy_words[-1] = noisy_words[-1][:-1]

        if random.random() < .1:
            noisy_words[0] = noisy_words[0].lower()

        if random.random() < .05:
            start_index = random.randint(0, len(noisy_words))
            end_index = random.randint(start_index, len(noisy_words))
            for i in range(start_index, end_index):
                noisy_words[i] = noisy_words[i].upper()

        print(" ".join(noisy_words))


if __name__ == "__main__":
    main()
