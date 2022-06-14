#!/usr/bin/env python3

"""Remove nonprintable characters.

Based on this
https://stackoverflow.com/questions/92438/stripping-non-printable-characters-from-a-string-in-python
"""

import argparse
import itertools
import re
import sys


assert sys.version_info >= (3, 6), "Use Python 3.6 or newer"


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("--keep-tab", action="store_true")
    args = parser.parse_args()

    if args.keep_tab:
        control_chars = ''.join(
            map(chr, itertools.chain(
                range(0x00, 0x09), range(0x0a, 0x20), range(0x7f, 0xa0))))
    else:
        control_chars = ''.join(
            map(chr, itertools.chain(range(0x00, 0x20), range(0x7f, 0xa0))))

    control_char_re = re.compile('[%s]' % re.escape(control_chars))

    for line in sys.stdin:
        print(control_char_re.sub('', line.strip()))


if __name__ == "__main__":
    main()
