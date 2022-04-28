#!/usr/bin/env python3

"""Simple length-base filtering."""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("corpora", nargs="+", type=str)
    parser.add_argument("--src", default="cs", type=str)
    parser.add_argument("--tgt", default="uk", type=str)
    parser.add_argument("--max-len", help="Max len in tokens.", default=100)
    parser.add_argument("--max-ratio", default=1.5, type=float)
    args = parser.parse_args()

    assert args.max_ratio > 1.0

    for corpus in args.corpora:
        print(corpus, file=sys.stderr)
        src_file = open(f"{corpus}.{args.src}")
        tgt_file = open(f"{corpus}.{args.tgt}")

        src_out = open(f"{corpus}.correct-length.{args.src}", "w")
        tgt_out = open(f"{corpus}.correct-length.{args.tgt}", "w")

        for src_line, tgt_line in zip(src_file, tgt_file):
            src_line = src_line.rstrip("\n")
            tgt_line = tgt_line.rstrip("\n")

            if not src_line or not tgt_line:
                continue

            if (len(src_line.split()) > args.max_len or
                    len(tgt_line.split()) > args.max_len):
                continue

            if (len(src_line) / len(tgt_line) > args.max_ratio or
                    len(tgt_line) / len(src_line) > args.max_ratio):
                continue

            print(src_line.rstrip("\n"), file=src_out)
            print(tgt_line.rstrip("\n"), file=tgt_out)

        src_file.close()
        tgt_file.close()
        src_out.close()
        tgt_out.close()


if __name__ == "__main__":
    main()
