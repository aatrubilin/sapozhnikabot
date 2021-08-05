from constants import VOWEL_TO_RHYME, VOWELS
from pymorphy2 import MorphAnalyzer

morph = MorphAnalyzer()


def _is_styllable(word):
    res = []
    read_vowel = False
    for char in word:
        is_vowel = char in VOWELS
        if read_vowel and not is_vowel:
            break
        if is_vowel:
            read_vowel = True
        res.append(char)
    return "".join(res)


def get_rhyme(text):
    for word in reversed(text.split(" ")):
        p = morph.parse(word)[0]
        if p.tag.POS in ("NOUN", "ADJF"):
            styllable = _is_styllable(word)
            if styllable and styllable != word:
                len_styllable = len(styllable)
                return VOWEL_TO_RHYME[styllable[-1]] + word[len_styllable:]
