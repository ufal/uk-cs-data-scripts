#!/usr/bin/env python3

import sys
import fasttext

TOTAL = 357405323

def main():
    model = fasttext.load_model('/lnet/work/people/libovicky/ua/lid.176.ftz')

    kept = 0
    for i, line in enumerate(sys.stdin):
        line = line.strip()
        print(f"Processed {i + 1}, {100 * (i + 1)/ TOTAL:.1f}%, kept ({100 * kept / (i + 1):.1f}%)",
              end="\r", file=sys.stderr)

        if len(line) < 5:
            continue

        if len(line) > 1000:
            continue

        simple_tokens = len(line.split())
        if simple_tokens > 120:
            continue

        if len(line) / simple_tokens > 10:
            continue

        if len(line) / simple_tokens < 3:
            continue

        if model.predict(line.strip(), k=1)[0][0][9:] == "uk":
            print(line)
            kept += 1

    print("", file=sys.stderr)


if __name__ == "__main__":
    main()
