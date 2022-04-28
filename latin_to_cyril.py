#!/usr/bin/env python3

import string
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


def latin_to_cyril(text):
    is_upper = (
        len( [c for c in text if c.isupper()]) >
        len([c for c in text if c.islower()]))

    no_punct = text.strip(string.punctuation).lower()

    if text.startswith("<latin>"):
        return text[7:]

    output = []
    i = 0
    while i < len(text):
        if i < len(text) - 1:
            bigram = text[i:i + 2]

            ignore_bigram = False

            if bigram in BIGRAM_TABLE and not ignore_bigram:
                trans = BIGRAM_TABLE[bigram]
                if is_upper and len(trans) > 1:
                    trans = trans.upper()
                output.append(trans)
                i += 2
                continue

        unigram = text[i]
        trans = UNIGRAM_TABLE.get(unigram, unigram)
        if is_upper and (len(trans) > 1 or trans == 'ь'):
            trans = trans.upper()
        output.append(trans)
        i += 1

    out_str = "".join(output)
    out_str = out_str.replace("Ц-Г", "ЦГ")
    out_str = out_str.replace("Й-А", "ЙА")
    out_str = out_str.replace("Й-І", "ЙІ")
    out_str = out_str.replace("Й-Е", "ЙЕ")
    out_str = out_str.replace("Й-У", "ЙУ")
    out_str = out_str.replace("Ц-г", "Цг")
    out_str = out_str.replace("Й-а", "Йа")
    out_str = out_str.replace("Й-і", "Йі")
    out_str = out_str.replace("Й-е", "Йе")
    out_str = out_str.replace("Й-у", "Йу")
    out_str = out_str.replace("ц-г", "цг")
    out_str = out_str.replace("й-а", "йа")
    out_str = out_str.replace("й-і", "йі")
    out_str = out_str.replace("й-е", "йе")
    out_str = out_str.replace("й-у", "йу")

    out_str = out_str.replace("Ц---Г", "Ц-Г")
    out_str = out_str.replace("Й---А", "Й-А")
    out_str = out_str.replace("Й---І", "Й-І")
    out_str = out_str.replace("Й---Е", "Й-Е")
    out_str = out_str.replace("Й---У", "Й-У")
    out_str = out_str.replace("Ц---г", "Ц-г")
    out_str = out_str.replace("Й---а", "Й-а")
    out_str = out_str.replace("Й---і", "Й-і")
    out_str = out_str.replace("Й---е", "Й-е")
    out_str = out_str.replace("Й---у", "Й-у")
    out_str = out_str.replace("ц---г", "ц-г")
    out_str = out_str.replace("й---а", "й-а")
    out_str = out_str.replace("й---і", "й-і")
    out_str = out_str.replace("й---е", "й-е")
    out_str = out_str.replace("й---у", "й-у")
    return out_str


def main():
    for line in sys.stdin:
        words = []
        for word in line.strip().split():
            words.append(latin_to_cyril(word))
        print(" ".join(words))


if __name__ == "__main__":
    main()
