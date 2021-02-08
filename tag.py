#!/usr/bin/env python3
'''
    Author: Ondrej Mekota o(at)mkta.eu
'''

import os
import logging
import warnings

from joblib import Parallel, delayed

import pipeline
from pipeline.taggers.udpipe import UDPipeTagger
from pipeline.taggers.treetagger import TreeTagger
from pipeline.taggers.btagger import BTagger
from pipeline.taggers.classlamodel import ClasslaTagger
from pipeline.transliterators import transliterate
import pipeline.utils as utils


def _get_correct_tagger(config:dict, lang):
    if lang not in config:
        raise ValueError(f'ERROR: language code {lang} is not in the config')

    tagger = config[lang]['tagger']

    if tagger == 'udpipe':
        return UDPipeTagger(config)
    elif tagger == 'treetagger':
        return TreeTagger(config)
    elif tagger == 'btagger':
        return BTagger(config)
    elif tagger == 'classla':
        return ClasslaTagger(config)
    else:
        raise ValueError(f'ERROR: tagger {tagger} does not exist')


def _parallel_tag_files(book_name, version, path, config, lang, enc='utf-8', out_dir=None, print_=False, rewrite:bool =False):
    if utils.file_exists(path, out_dir, '_tagged.xml') and not rewrite:
        # if already aligned file exist and we are not going to `rewerite` them
        logging.warning(f'skipping file "{path}"')
        return
    logging.info(f'tagging "{path}"...')
    try:
        tagger = _get_correct_tagger(config, lang)
    except ValueError as e:
        logging.error(f'tagger for {lang} does not exist')

    sents_iter = tagger.process_file(path, lang, encoding=enc)
    sentences = sents_iter

    if config[lang]['transliterate']:
        logging.info(f'transliterating "{path}"...')
        polyglot_code = utils.get_polyglot_lang_code(config, lang)
        sentences = []
        for s in sents_iter:
            sent = []
            for w in s:
                w['word_trans'] = ''.join(transliterate.transliterate(w['word'], polyglot_code))
                w['lemma_trans'] = ''.join(transliterate.transliterate(w['lemma'], polyglot_code))
                sent.append(w)
            sentences.append(sent)
        logging.info(f'DONE transliterating "{path}"')
    output_xml = utils.output_to_xml(sentences, os.path.basename(path), lang)  # TODO id_ if files given as list/by file

    if print_:
        logging.info(output_xml)
    else:
        utils.save_output(output_xml, path, out_dir, '_tagged.xml')
    logging.info(f'DONE tagging "{path}"')


def tag_lang_files(lang_files:dict, config, out_dir, print_=False, rewrite:bool = False):
    """ Tag `lang_files`
        {'eng': [('hobbit', 'a', '../hobbit_END_a.txt'), ('prince', 'a', ...)...], ...}
    """
    logging.info('Started tagging...')
    flat_files = utils.flatten_lang_files(lang_files)
    Parallel(n_jobs=-1)(delayed(_parallel_tag_files)(book_name, version, path, config, lang, out_dir=out_dir, print_=print_, rewrite=rewrite) for book_name, version, path, lang in flat_files)
    # for lang, books in lang_files.items():
        # tagger = _get_correct_tagger(config, lang)
        # _tag_files(tagger, books, config, lang, out_dir=out_dir, print_=print_, rewrite=rewrite)
    logging.info('DONE tagging')


if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Tag files.')
    parser.add_argument('-d','--output_dir', type=str, default='.', help='Directory to which to write the output files.')
    parser.add_argument('input', metavar='N', default=None, type=str, nargs='+', help='List of files to be tagged. Format: NAME_LANG[_ID][.ext], for example Hobbit_eng.txt')

    args = parser.parse_args()

    # This is the main thing
    config = pipeline.utils.get_config()
    book_files, lang_files = utils.parse_input_files(args.input, config)
    tag_lang_files(lang_files, config, args.output_dir)
