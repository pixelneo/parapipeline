#!/usr/bin/env python3
"""
    Author: Ondrej Mekota o(at)mkta.eu
"""
import os

FILE_PATH = os.path.dirname(__file__)
os.environ["POLYGLOT_DATA_PATH"] = FILE_PATH

import polyglot
from polyglot.text import Text


def transliterate(text: str, polyglot_lang_code: str):
    """Transliterates `text` from alphabet `polyglot_lang_code` to english alphabet.
    If certain token cannot be transliterated, use the original token."""
    lang = polyglot_lang_code
    p_text = polyglot.text.Text(text, lang)
    transliterated = p_text.transliterate("en")
    result = [
        w_new if w_new != "" else w_orig
        for w_orig, w_new in zip(p_text.words, transliterated)
    ]
    return result


if __name__ == "__main__":
    pass
