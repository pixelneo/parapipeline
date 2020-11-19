#!/usr/bin/env python3
"""
    Author: Ondrej Mekota o(at)mkta.eu
"""

import os
import warnings

import classla

from .base import BaseTagger

FORMATS = ["conllu", "vertical", "horizontal", "matxin", "epe", None]
FILE_PATH = os.path.dirname(__file__)


class ClasslaTagger(BaseTagger):
    """ ClasslaTagger """

    def __init__(self, config):
        super().__init__(config)

    def _check_model(self, lang):
        """ Check if model exists, is loaded, and load it if needed. """
        if lang not in self.models:
            lang_code = self._lang2modelname(lang)
            self.models[lang] = classla.Pipeline(
                lang=lang_code, models_dir=os.path.join(FILE_PATH, "classla", "models")
            )

    def process(self, text: str, lang: str, in_format=None, out_format=None):
        """Tags plain text `text`
        Args:
            text: (str)
            in_format: (str) 'conllu', 'horizontal', 'vertical', 'split', None
            out_format: (str) 'conllu', 'horizontal', 'vertical', None
            lang: (str) ISO-639-3 code

        Returns:
            list

        Yields:
            list of words - dicts for each sentece e.g.[{'word': 'skied', 'lemma': 'ski', ...}, ...]

        """
        self._check_model(lang)
        nlp = self.models[lang]
        for s_raw in text.strip().split("\n"):
            s = nlp(s_raw)
            res = []
            for s2 in s.sentences:  # sentence segmentation is performed
                for t in s2.tokens:
                    for w in t.words:
                        src = (
                            ("word", w.text),
                            ("lemma", w.lemma),
                            ("upos", w.upos),
                            ("xpos", w.xpos),
                            ("feats", w.feats),
                        )
                        a = [(k, v) for k, v in src if v is not None]
                        res.append(dict(a))
            yield res

    def process_file(
        self,
        path: str,
        lang: str,
        encoding: str = "utf-8",
        in_format: str = None,
        out_format: str = None,
    ):
        """Loads plain text file, tags it, and returns list of sentences.

        Args:
            path: path to the file, the name of the file
            lang: (str)  ISO-639-3 code
            in_format: (str) 'conllu', 'horizontal', 'vertical', 'split', None
            out_format: (str) 'conllu', 'horizontal', 'vertical', None
            encoding: (str) encoding of the file

        Returns:
            list

        Yields:
            list of words - dicts for each sentece e.g.[{'word': 'skied', 'lemma': 'ski', ...}, ...]

        """

        # TODO support also gzipped files
        with open(path, encoding=encoding) as f:
            text = f.read()

        return self.process(text, lang, in_format, out_format)


def save_output(text: str, path: str, extension):
    """ Save `text` to `path`.`extension`. """
    with open(f"{path}.{extension}", "w") as f:
        f.write(text)
