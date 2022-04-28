#!/usr/bin/env python3

import re
import sys



LATIN_RE = re.compile(r"[A-Za-zěščřýžýáíéúůďťňóĚŠČŘÝŽÝÁÍÉÚŮĎŤŇÓöüäëèñĺçÖÜÄľĽËÈÑĹÇ]")


SOFT = ["Ь", "ь"]


TABLE = {
    # CAPITAL LETTERS
    "А": "A", "Б": "B", "В": "V", "Г": "H", "Ґ": "G", "Д": "D", "Е": "E",
    "Є": "JE", "Ж": "Ž", "З": "Z", "И": "Y", "І": "I", "Ї": "JI", "Й": "J",
    "К": "K", "Л": "L", "М": "M", "Н": "N", "О": "O", "П": "P", "Р": "R",
    "С": "S", "Т": "T", "У": "U", "Ф": "F", "Х": "CH", "Ц": "C", "Ч": "Č",
    "Ш": "Š", "Щ": "ŠČ", "Ю": "JU", "Я": "JA",

    # LOWECASE LETTERS
    "а": "a", "б": "b", "в": "v", "г": "h", "ґ": "g", "д": "d", "е": "e",
    "є": "je", "ж": "ž", "з": "z", "и": "y", "і": "i", "ї": "ji", "й": "j",
    "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r",
    "с": "s", "т": "t", "у": "u", "ф": "f", "х": "ch", "ц": "c", "ч": "č",
    "ш": "š", "щ": "šč", "ю": "ju", "я": "ja",
}


SOFTENING = {
    "D": "Ď", "T": "Ť", "N": "Ň",
    "d": "ď", "t": "ť", "n": "ň",
}


def cyril_to_latin(text):
    # HANDLE DOUBLE LETTERS THAT SHOULD BE KEPT
    # 1. Escape them if there are sepeterate by dash already
    text = text.replace("Ц-Г", "Ц---Г")
    text = text.replace("Й-А", "Й---А")
    text = text.replace("Й-І", "Й---І")
    text = text.replace("Й-Е", "Й---Е")
    text = text.replace("Й-У", "Й---У")
    text = text.replace("Ц-г", "Ц---г")
    text = text.replace("Й-а", "Й---а")
    text = text.replace("Й-і", "Й---і")
    text = text.replace("Й-е", "Й---е")
    text = text.replace("Й-у", "Й---у")
    text = text.replace("ц-г", "ц---г")
    text = text.replace("й-а", "й---а")
    text = text.replace("й-і", "й---і")
    text = text.replace("й-е", "й---е")
    text = text.replace("й-у", "й---у")

    # 2. Add dash not to merge them
    text = text.replace("ЦГ", "Ц-Г")
    text = text.replace("ЙА", "Й-А")
    text = text.replace("ЙІ", "Й-І")
    text = text.replace("ЙЕ", "Й-Е")
    text = text.replace("ЙУ", "Й-У")
    text = text.replace("Цг", "Ц-г")
    text = text.replace("Йа", "Й-а")
    text = text.replace("Йі", "Й-і")
    text = text.replace("Йе", "Й-е")
    text = text.replace("Йу", "Й-у")
    text = text.replace("цг", "ц-г")
    text = text.replace("цг", "ц-г")
    text = text.replace("йа", "й-а")
    text = text.replace("йі", "й-і")
    text = text.replace("йе", "й-е")
    text = text.replace("йу", "й-у")


    output = []

    if LATIN_RE.search(text):
        return f"<latin>{text}"

    for i, ch in enumerate(text):
        trans = TABLE.get(ch, ch)
        if len(trans) > 1 and i < len(text) - 1 and text[i + 1].islower():
            trans = trans[0] + trans[1:].lower()

        if ch.lower() == "je" and output and output[-1] in SOFTENING:
            if ch == "Є":
                trans = "Ě"
            if ch == "є":
                trans = "ě"

        if ch.lower() == "ja" and output and output[-1] in SOFTENING:
            output[-1] = SOFTENING.get(output[-1], output[-1])
            if ch == "Я":
                trans = "A"
            if ch == "я":
                trans = "a"

        if ch.lower() == "ju" and output and output[-1] in SOFTENING:
            output[-1] = SOFTENING.get(output[-1], output[-1])
            if ch == "Ю":
                trans = "U"
            if ch == "ю":
                trans = "u"

        if ch.lower() == "ji" and output and output[-1] in SOFTENING:
            output[-1] = SOFTENING.get(output[-1], output[-1])
            if ch == "Ї":
                trans = "I"
            if ch == "ї":
                trans = "i"

        if ch in SOFT and output:
            if output[-1] in SOFTENING:
                output[-1] = SOFTENING.get(output[-1], output[-1])
            else:
                output.append("ˇ")
            continue

        output.append(trans)
    return "".join(output)


def main():
    for line in sys.stdin:
        words = []
        for word in line.strip().split():
            words.append(cyril_to_latin(word))
        print(" ".join(words))


if __name__ == "__main__":
    main()
