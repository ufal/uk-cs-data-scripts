#!/usr/bin/env python3

"""Language ID using FastText.

The FastText models can be downloaded from:
    https://fasttext.cc/docs/en/language-identification.html
"""

import argparse
import sys

import fasttext


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument(
        "model", nargs="?", type=str,
        default="/lnet/work/people/libovicky/ua/lid.176.ftz")
    args = parser.parse_args()

    model = fasttext.load_model(args.model)

    for line in sys.stdin:
        print(model.predict(line.strip(), k=1)[0][0][9:])


if __name__ == "__main__":
    main()
