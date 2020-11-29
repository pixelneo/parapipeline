#!/usr/bin/env python3
"""
    Author: Ondrej Mekota o(at)mkta.eu
"""

import os
import warnings

from corpy.udpipe import Model

from .base import BaseTagger

FORMATS = ['conllu', 'vertical', 'horizontal', 'matxin', 'epe', None]
FILE_PATH = os.path.dirname(__file__)


class UDPipeTagger(BaseTagger):
    """ UDPipeTagger  """

    def __init__(self, config):
        super().__init__(config)

    def _check_model(self, lang):
        """ Check if model exists, is loaded, and load it if needed. """
        if lang not in self.models:
            model_path = os.path.join(
                FILE_PATH, 'udpipe', 'models', self._lang2modelname(lang)
            )
            self.models[lang] = Model(model_path)

    def process(self, text: str, lang: str, in_format=None, out_format=None):
        """Tags plain text `text`
        Args:
            text: (str)
            in_format: (str) 'conllu', 'horizontal', 'vertical', 'split', None
            out_format: (str) 'conllu', 'horizontal', 'vertical', None
            lang: (str) ISO-639-3 code

        Returns:
            list(output of corpy.udpipe.process)

        Yields:
            list of words - dicts for each sentece e.g.[{'word': 'skied', 'lemma': 'ski', ...}, ...]

        """
        self._check_model(lang)
        if in_format not in FORMATS:
            if in_format != 'split':
                warnings.warn(f'in_format: {in_format} does not exist, using default.')
            in_format = None
        if out_format not in FORMATS:
            warnings.warn(f'out_format: {out_format} does not exist, using default.')
            out_format = None

        if out_format is None:
            for line in text.splitlines():
                res = []
                for s in self.models[lang].process(line, parse=False, in_format=in_format, out_format=out_format):
                    for w in s.words[1:]:  # index 0 always contains <root>
                        res.append(
                            {
                                'word': w.form,
                                'lemma': w.lemma,
                                'upos': w.upostag,
                                'xpos': w.xpostag,
                                'feats': w.feats,
                            }
                        )
                yield res
        else:
            return list(
                self.models[lang].process(
                    text, parse=False, in_format=in_format, out_format=out_format
                )
            )

    def process_file(
        self,
        path: str,
        lang: str,
        encoding: str = 'utf-8',
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
            list(output of corpy.udpipe.process)

        Yields:
            list of words - dicts for each sentece e.g.[{'word': 'skied', 'lemma': 'ski', ...}, ...]

        """

        # TODO support also gzipped files
        with open(path, encoding=encoding) as f:
            text = f.read()

        return self.process(text, lang, in_format, out_format)


def save_output(text: str, path: str, extension):
    ''' Save `text` to `path`.`extension`. '''
    with open(f'{path}.{extension}', 'w') as f:
        f.write(text)
