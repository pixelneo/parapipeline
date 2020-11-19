#!/usr/bin/env python3
"""
    Author: Ondrej Mekota o(at)mkta.eu
"""

import os
import warnings

import treetaggerwrapper as ttw

from .base import BaseTagger

FILE_PATH = os.path.dirname(__file__)


class TreeTagger(BaseTagger):
    def __init__(self, config):
        super().__init__(config)

    def _check_model(self, lang):
        """ Check if model exists, is loaded, and load it if needed. """
        if lang not in self.models:
            tagdir = os.path.join(FILE_PATH, "treetagger")
            tagparfile = os.path.join(
                FILE_PATH, "treetagger", "lib", self._lang2modelname(lang)
            )

            self.models[lang] = ttw.TreeTagger(TAGDIR=tagdir, TAGPARFILE=tagparfile)

    def process(self, text: str, lang: str, in_format=None, out_format=None):
        """Tags plain text `text`
        Args:
            text: (str)
            lang: (str) ISO-639-3 code

        Yields:
            list of words - dicts for each sentece e.g.[{'word': 'skied', 'lemma': 'ski', ...}, ...]

        """
        self._check_model(lang)

        for s in text.splitlines():
            words = ttw.make_tags(self.models[lang].tag_text(s))
            res = []
            for w in words:
                res.append({"word": w.word, "lemma": w.lemma, "pos": w.pos})
            yield res

    def process_file(
        self,
        path: str,
        lang: str,
        encoding: str = "utf-8",
        in_format=None,
        out_format=None,
    ):
        """Loads plain text file, tags it, and returns list of sentences.

        Args:
            path: path to the file, the name of the file
            lang: (str)  ISO-639-3 code
            encoding: (str) encoding of the file

        Yields:
            list of words - dicts for each sentece e.g.[{'word': 'skied', 'lemma': 'ski', ...}, ...]

        """

        # TODO support also gzipped files
        with open(path, encoding=encoding) as f:
            text = f.read()

        return self.process(text, lang)
