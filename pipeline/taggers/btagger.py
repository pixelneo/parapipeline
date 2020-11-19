#!/usr/bin/env python3
"""
    Author: Ondrej Mekota o(at)mkta.eu
"""

import os
import warnings
import subprocess
import tempfile
import re

from corpy.morphodita import Tokenizer

from .base import BaseTagger

FILE_PATH = os.path.dirname(__file__)


class BTagger(BaseTagger):
    def __init__(self, config):
        super().__init__(config)
        self.tokenizer = Tokenizer("generic")

    def process(self, text: str, lang: str, in_format=None, out_format=None):
        """Tags plain text `text`
        ! For BTagger, this is not optimized, yet.

        Args:
            text: (str)
            lang: (str) ISO-639-3 code

        Yields:
            list of words - dicts for each sentece e.g.[{'word': 'skied', 'lemma': 'ski', ...}, ...]

        """
        try:
            fd, in_file = tempfile.mkstemp()
            with open(fd, "w") as f:
                f.write(text)
            iter_ = self.process_file(in_file, lang, "utf-8")
        finally:
            pass

        return iter_

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
        # java -cp BTagger.jar bTagger/BTagger -p JOB_NAME input_file.txt param/mk/pos.fea param/mk/pos.scr
        # java -cp BTagger.jar bTagger/BTagger -p JOB_NAME taggedFILE.txt param/mk/lem.fea param/mk/lem.scr
        # java -cp BTagger.jar LCS_WDiff2L Tagged-lemmatized-file.txt x.out 1 3

        lang_code = self.config[lang]["lang_code"]
        btagger_path = os.path.join(FILE_PATH, "btagger", "BTagger.jar")
        lang_path = os.path.join(FILE_PATH, "btagger", "param", lang_code)

        with open(path, encoding=encoding) as f:
            sents = f.readlines()

        tokenized = "\n\n".join(
            ("\n".join((w for w in self.tokenizer.tokenize(s))) for s in sents)
        )

        try:
            fd, in_file = tempfile.mkstemp()
            with open(fd, "w") as f:
                f.write(tokenized)

            job_name = str(abs(hash(path)))
            job_name_tagged = f"{job_name}Tagged.txt"
            args = [
                "-cp",
                btagger_path,
                "bTagger/BTagger",
                "-p",
                job_name,
                in_file,
                os.path.join(lang_path, "pos.fea"),
                os.path.join(lang_path, "pos.scr"),
            ]
            p = subprocess.run(["java", *args], capture_output=True)
        finally:
            os.remove(in_file)

        args[5] = job_name_tagged
        args[6] = os.path.join(lang_path, "lem.fea")
        args[7] = os.path.join(lang_path, "lem.scr")

        p = subprocess.run(["java", *args], capture_output=True)

        try:
            fd, out_file = tempfile.mkstemp()
            args = [
                "-cp",
                btagger_path,
                "LCS_WDiff2L",
                job_name_tagged,
                out_file,
                "1",
                "3",
            ]
            p = subprocess.run(["java", *args], capture_output=True)

            # TODO check if this is necessary
            subprocess.run(["dos2unix", out_file], capture_output=True)

            with open(out_file) as f:
                sents = f.read().strip().split("\n\n")

        finally:
            os.remove(out_file)
            os.remove(job_name_tagged)

        # TODO what is there are more subsequent empty lines
        for s in sents:
            # word \t tag \t lemma \n
            yield [
                {"word": w[0], "tag": w[1], "lemma": w[2]}
                for w in (x.split("\t") for x in s.split("\n") if x.strip() != "")
            ]
