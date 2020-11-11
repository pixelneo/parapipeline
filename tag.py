#!/usr/bin/env python3
'''
    Author: Ondrej Mekota o(at)mkta.eu
'''


# TODO:
#  this file will take LANGUAGE and TEXTS, TRANSLITERATE if given language needs it, and TAG the texts, yielding output in TEI XML format


import os
import warnings

import pipeline
from pipeline.taggers.udpipe import UDPipeTagger
from pipeline.taggers.treetagger import TreeTagger
from pipeline.taggers.btagger import BTagger

from pipeline.transliterators import transliterate

import pipeline.utils as utils

def get_correct_tagger(config:dict, lang):
    if lang not in config:
        raise ValueError(f'ERROR: language code {lang} is not in the config')

    tagger = config[lang]['tagger']

    if tagger == 'udpipe':
        return UDPipeTagger(config)
    elif tagger == 'treetagger':
        return TreeTagger(config)
    elif tagger == 'btagger':
        return BTagger(config)
    else:
        raise ValueError(f'ERROR: tagger {tagger} does not exist')

def tag_files(tagger, books_info:tuple, config, lang, enc='utf-8', out_dir=None, print_=False):
    """ Tag `books_info` (bookname, version, path) files. All the files are in the same `lang`.
    """
    for book_name, version, path in books_info:
        sents_iter = tagger.process_file(path, lang, encoding=enc)
        sentences = sents_iter

        if config[lang]['transliterate']:
            polyglot_code = utils.get_polyglot_lang_code(config, lang)
            sentences = []
            for s in sents_iter:
                sent = []
                for w in s:
                    w['word_trans'] = ''.join(transliterate.transliterate(w['word'], polyglot_code))
                    w['lemma_trans'] = ''.join(transliterate.transliterate(w['lemma'], polyglot_code))
                    sent.append(w)
                sentences.append(sent)

        output_xml = utils.output_to_xml(sentences, os.path.basename(path), lang)  # TODO id_ if files given as list/by file
        if print_:
            print(output_xml)
        else:
            utils.save_output(output_xml, path, out_dir, '_tagged.xml')


def tag_lang_files(lang_files:dict, config, out_dir, print_=False):
    """ Tag `lang_files`
        {'eng': [('hobbit', 'a', '../hobbit_END_a.txt'), ('prince', 'a', ...)...], ...}
    """
    for lang, books in lang_files.items():
        tagger = get_correct_tagger(config, lang)
        tag_files(tagger, books, config, lang, out_dir=out_dir, print_=print_)




if __name__=='__main__':
    import argparse


    parser = argparse.ArgumentParser(description='Tag files.')

    #outputs = parser.add_mutually_exclusive_group(required=False)
    parser.add_argument('-d','--output_dir', type=str, default='.', help='Directory to which to write the output files.')
    #outputs.add_argument('--print', action='store_true', help='Instead of saving to file, print.')

    parser.add_argument('input', metavar='N', default=None, type=str, nargs='+', help='List of files to be tagged. Format: NAME_LANG[_ID][.ext], for example Hobbit_eng.txt')

    args = parser.parse_args()

    # This is the main thing
    config = pipeline.utils.get_config()
    book_files, lang_files = utils.parse_input_files(args.input)
    tag_lang_files(lang_files, config, args.output_dir)



