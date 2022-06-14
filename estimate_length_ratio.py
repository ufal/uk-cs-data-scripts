#!/usr/bin/env python3

"""Estimate character length ratios of parallel data."""

import argparse


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("src", type=argparse.FileType('r'))
    parser.add_argument("tgt", type=argparse.FileType('r'))
    args = parser.parse_args()

    src_to_tgt = []
    tgt_to_src = []

    for src_line, tgt_line in zip(args.src, args.tgt):
        src_line, tgt_line = src_line.strip(), tgt_line.strip()
        if src_line and tgt_line:
            src_to_tgt.append(len(src_line) / len(tgt_line))
            tgt_to_src.append(len(tgt_line) / len(src_line))

    src_to_tgt.sort()
    tgt_to_src.sort()

    print("SRC / TGT")
    for i in range(1, 11):
        print(f"{i}\t{src_to_tgt[i * len(src_to_tgt) // 10 - 1]}")
    print()
    print("TGT / SRC")
    for i in range(1, 11):
        print(f"{i}\t{tgt_to_src[i * len(tgt_to_src) // 10 - 1]}")


if __name__ == "__main__":
    main()
