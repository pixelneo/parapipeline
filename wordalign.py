#!/usr/bin/env python3
'''
    Author: Ondrej Mekota o(at)mkta.eu
'''

import itertools
import logging

#from joblib import Parallel, delayed

from tag import tag_lang_files
from align import align_book_files
from pipeline.aligners import eflomal
from pipeline import utils


def word_align_book_files(book_files, out_dir, rewrite:bool = False):
    """ input like {'hobbit': [('eng', 'a', '../hobbit_ENG_a.txt'), ('pol', 'a', ...)...], ...} """
    a = eflomal.WordAligner()
    logging.info('Started word aligning...')
    for book, texts in book_files.items():
        pairs = itertools.combinations(texts, 2)
        for (l1, v1, file1), (l2, v2, file2) in pairs:
            out_name = f'{book}_{l1}-{l2}_{v1}-{v2}'
            if utils.file_exists(out_name, out_dir, '_word-aligned.xml') and not rewrite:
                # if already aligned file exist and we are not going to `rewerite` them
                logging.warning(f'skipping pair "{file1}" and "{file2}"')
                continue
            if not utils.file_exists(out_name, out_dir, '_aligned.xml'):
                logging.warning(f'files "{file1}" and "{file2}" were not sentence aligned, aligning...')
                align_book_files({book: [(l1, v1, file1), (l2, v2, file2)]}, out_dir, rewrite)

            if not utils.file_exists(file1, out_dir, '_tagged.xml'):
                logging.warning(f'file "{file1}" is not tagged, tagging...')
                tag_lang_files({l1: [(book, v1, file1)]}, out_dir, rewrite)
            if not utils.file_exists(file2, out_dir, '_tagged.xml'):
                logging.warning(f'file "{file2}" is not tagged, tagging...')
                tag_lang_files({l2: [(book, v2, file2)]}, out_dir, rewrite)


            logging.info(f'word-aligning "{file1}" and "{file2}"')
            links = a.align_files(file1, file2)
            output_xml = utils.word_alignment_to_xml(links, file1, file2)
            utils.save_output(output_xml, out_name, out_dir, '_word-aligned.xml')
            logging.info(f'DONE word aligning "{file1}" and "{file2}"')
    logging.info('DONE word aligning')


if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Word align files.')
    parser.add_argument('-o','--output_dir', type=str, default='.', help='Directory to which to write the output files.')
    parser.add_argument('input', metavar='N', default=None, type=str, nargs='+', help='List of files to be aligned. Format: NAME_LANG[_ID][.ext], for example Hobbit_eng.txt')

    args = parser.parse_args()

    # This is the main thing
    config = utils.get_config()
    book_files, lang_files = utils.parse_input_files(args.input, config)
    word_align_book_files(book_files, args.output_dir)
