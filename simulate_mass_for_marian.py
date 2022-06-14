#!/usr/bin/env python3

"""Prepare trainig data for MASS-like pretrainig with Marian."""

import argparse
import random
import sys

import sentencepiece


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("spm_model", type=str, help="SentencePiece model.")
    parser.add_argument(
        "input", type=argparse.FileType("r"), nargs="?", default=sys.stdin)
    parser.add_argument("--mask-ratio", type=float, default=0.5)
    parser.add_argument("--mask-token", type=str, default="<mask>")
    args = parser.parse_args()

    tokenizer = sentencepiece.SentencePieceProcessor(model_file=args.spm_model)

    for line in args.input:
        tokens = tokenizer.encode(
            line.strip(), out_type=str, enable_sampling=False,
            alpha=1.0, nbest_size=-1)

        if len(tokens) < 2:
            continue

        mask_start = random.randint(0, len(tokens) - 1)
        mask_end = min(
            len(tokens), mask_start + int(len(tokens) * args.mask_ratio))

        src_tokens = []
        # tgt_tokens = []

        for i, tok in enumerate(tokens):
            if mask_start <= i < mask_end:
                thres = random.uniform(0, 1)
                if thres < .8:
                    src_tokens.append(args.mask_token)
                elif thres < .9:
                    src_tokens.append(tok)
                else:
                    src_tokens.append(
                        tokenizer.id_to_piece(random.randint(
                            1, tokenizer.vocab_size() - 1)))
                # tgt_tokens.append(tok)
            else:
                src_tokens.append(tok)
                # tgt_tokens.append(args.mask_token)

        src = tokenizer.decode(src_tokens)
        # tgt = tokenizer.decode(tgt_tokens)

        print(f"{src}\t{line.strip()}")


if __name__ == "__main__":
    main()
