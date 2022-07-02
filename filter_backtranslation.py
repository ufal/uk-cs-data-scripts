#!/usr/bin/env python3

"""Simple rule-based filtering of back-translated data.

Remove sentences with: too many spaces, too much punctuation, suspuciously long
and short sentences, and sentences with repeated tokens.
"""

import argparse
import string
import sys


def space_ratio(line):
    return len([x for x in line if x.isspace()]) / len(line)


def punct_ratio(line):
    return len([x for x in line if x in string.punctuation]) / len(line)


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("src_in", type=argparse.FileType("r"))
    parser.add_argument("tgt_in", type=argparse.FileType("r"))
    parser.add_argument("src_out", type=argparse.FileType("w"))
    parser.add_argument("tgt_out", type=argparse.FileType("w"))
    args = parser.parse_args()

    for ln_num, (src_line, tgt_line) in enumerate(
            zip(args.src_in, args.tgt_in)):
        print(ln_num, file=sys.stderr, end="\r")
        src_line, tgt_line = src_line.strip(), tgt_line.strip()

        if not src_line:
            continue
        if not tgt_line:
            continue

        if space_ratio(tgt_line) > 0.3:
            continue

        if punct_ratio(tgt_line) > 0.2:
            continue

        if len(src_line) / len(tgt_line) > 1.8:
            continue
        if len(tgt_line) / len(src_line) > 1.8:
            continue

        simple_tok = tgt_line.split()
        is_repeated = False
        for i in range(2, len(simple_tok)):
            if simple_tok[i] == simple_tok[i - 1] == simple_tok[i - 2]:
                is_repeated = True
                break

        if is_repeated:
            continue

        print(src_line, file=args.src_out)
        print(tgt_line, file=args.tgt_out)
    print("", file=sys.stderr)

    args.src_in.close()
    args.tgt_in.close()
    args.src_out.close()
    args.tgt_out.close()


if __name__ == "__main__":
    main()

