#!/usr/bin/env python3

import sys

UNIGRAM_TABLE = {
    "A": "А", "B": "Б", "V": "В", "H": "Г", "G": "Ґ", "D": "Д", "E": "Е",
    "Ž": "Ж", "Z": "З", "Y": "И", "I": "І", "J": "Й", "K": "К", "L": "Л",
    "M": "М", "N": "Н", "O": "О", "P": "П", "R": "Р", "S": "С", "T": "Т",
    "U": "У", "F": "Ф", "C": "Ц", "Č": "Ч", "Š": "Ш", "Ě": "Є", "Ď": "ДЬ",
    "Ť": "ТЬ", "Ň": "НЬ",

    "a": "а", "b": "б", "v": "в", "h": "г", "g": "ґ", "d": "д", "e": "е",
    "ž": "ж", "z": "з", "y": "и", "i": "і", "j": "й", "k": "к", "l": "л",
    "m": "м", "n": "н", "o": "о", "p": "п", "r": "р", "s": "с", "t": "т",
    "u": "у", "f": "ф", "c": "ц", "č": "ч", "š": "ш", "ě": "є", "ď": "дь",
    "ť": "ть", "ň": "нь", "ˇ": "ь"
}

BIGRAM_TABLE = {
    "ŠČ": "Щ", "JU": "Ю", "JA": "Я", "CH": "Х", "JE": "Є", "JI": "Ї",
    "ĎA": "ДЯ", "ŤA": "ТЯ", "ŇA": "НЯ", "ĎI": "ДЇ", "ŤI": "ТЇ", "ŇI": "НЇ",
    "ĎU": "ДЮ", "ŤU": "ТЮ", "ŇU": "НЮ",

    "Šč": "Щ", "Ju": "Ю", "Ja": "Я", "Ch": "Х", "Je": "Є", "Ji": "Ї",
    "Ďa": "Дя", "Ťa": "Тя", "Ňa": "Ня", "Ďi": "Дї", "Ťi": "Тї", "Ňi": "Нї",
    "Ďu": "Дю", "Ťu": "Тю", "Ňu": "Ню",

    "šč": "щ", "ju": "ю", "ja": "я", "ch": "х", "je": "є", "ji": "ї",
    "ďa": "дя", "ťa": "тя", "ňa": "ня", "ďi": "дї", "ťi": "тї", "ňi": "нї",
    "ďu": "дю", "ťu": "тю", "ňu": "ню",
}

NON_JOINING = ["цг", "йа", "йі", "йе", "йу", "шч"]


def latin_to_cyril(text):
    is_upper = (
        len([c for c in text if c.isupper()]) >
        len([c for c in text if c.islower()]))

    if text.startswith("<latin>"):
        return text[7:]

    output = []
    i = 0
    while i < len(text):
        if text[i:].startswith("<latin_char>"):
            output.append(text[i + 12])
            i += 13
            continue

        if i < len(text) - 1:
            bigram = text[i:i + 2]

            if bigram in BIGRAM_TABLE:
                trans = BIGRAM_TABLE[bigram]
                if is_upper and len(trans) > 1:
                    trans = trans.upper()
                i += 2
                if trans.islower() and output and output[-1].isupper() and len(output[-1]) > 1:
                    output[-1] = output[-1][0] + output[-1][1:].lower()
                output.append(trans)
                continue

        unigram = text[i]
        trans = UNIGRAM_TABLE.get(unigram, unigram)
        if is_upper and (len(trans) > 1 or trans == 'ь'):
            trans = trans.upper()
        if trans.islower() and output and output[-1].isupper() and len(output[-1]) > 1:
            output[-1] = output[-1][0] + output[-1][1:].lower()
        output.append(trans)
        i += 1

    out_str = "".join(output)

    for pair in NON_JOINING:
        # 1. Escape them if there are sepeterate by dash already
        out_str = out_str.replace(pair[0] + "-" + pair[1], pair[0] + pair[1])
        out_str = out_str.replace(
            pair[0].upper() + "-" + pair[1], pair[0].upper() + pair[1])
        out_str = out_str.replace(
            pair[0].upper() + "-" + pair[1].upper(),
            pair[0].upper() + pair[1].upper())

        # 2. Add dash not to merge them
        out_str = out_str.replace(
            pair[0] + "---" + pair[1], pair[0] + "-" + pair[1])
        out_str = out_str.replace(
            pair[0].upper() + "---" + pair[1], pair[0].upper() + "-" + pair[1])
        out_str = out_str.replace(
            pair[0].upper() + "---" + pair[1].upper(),
            pair[0].upper() + "-" + pair[1].upper())

    return out_str


def main():
    for line in sys.stdin:
        words = []
        for word in line.strip().split():
            words.append(latin_to_cyril(word))
        print(" ".join(words))


if __name__ == "__main__":
    main()
