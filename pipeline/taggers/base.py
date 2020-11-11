#!/usr/bin/env python3
'''
    Author: Ondrej Mekota o(at)mkta.eu
'''

import os

FILE_PATH = os.path.dirname(__file__)

class BaseTagger:
    def __init__(self, config):
        self.config = config
        self.models = {}


    def _lang2modelname(self, lang_code:str):
        """ Get model name by language code or raise exception if there is no model. """
        if lang_code not in self.config or self.config[lang_code]['model'] == '':
            raise ValueError(f'ERROR: given language ({lang_code}) has not model')
        return self.config[lang_code]['model']


    def process(self, text: str, lang:str, in_format=None, out_format=None):
        """  Tags plain text `text`
        Args:
            text: (str)
            in_format: (str) 'conllu', 'horizontal', 'vertical', 'split'
            out_format: (str) 'conllu', 'horizontal', 'vertical'
            lang: (str) ISO-639-3 code

        Yields:
            list of words - dicts for each sentece e.g.[{'word': 'skied', 'lemma': 'ski', ...}, ...]

        """
        raise NotImplementedError('Not implemented base class')


    def process_file(self, path: str, lang:str, encoding:str='utf-8', in_format:str=None, out_format:str=None):
        """ Loads plain text file, tags it, and returns list of sentences.

        Args:
            path: path to the file, the name of the file
            lang: (str)  ISO-639-3 code
            in_format: (str) 'conllu', 'horizontal', 'vertical', 'split'
            out_format: (str) 'conllu', 'horizontal', 'vertical'
            encoding: (str) encoding of the file

        """
        raise NotImplementedError('Not implemented base class')


class Sentence:
    def __init__(self, words):
        self.words = words


    def __iter__(self):
        for w in words:
            pass
        # TODO how to do this with several taggers, each tagger could give this class an iterator over words, then we would just iterate over that




# # TODO not sure if this is the best way
# #   what if a sentence returned a dict, which is easily transformable to XML attributes 
# class Word:
    # def __init__(self):
        # pass

    # @property
    # def word(self):
        # raise NotImplementedError()

    # @property
    # def lemma(self):
        # raise NotImplementedError()

    # @property
    # def (self):
        # raise NotImplementedError()


