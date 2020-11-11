#!/usr/bin/env python3
'''
    Author: Ondrej Mekota o(at)mkta.eu
'''

import os

import pipeline
from pipeline.transliterators import transliterate
import pipeline.utils as utils


def transliterate_files(lang_files, config, out_dir):

    for lang, books in lang_files.items():
        polyglot_code = utils.get_polyglot_lang_code(config, lang)
        for book_name, version, path in books:
            output = []
            with open(path) as f:
                lines = f.readlines()
            for i, line in enumerate(lines):
                output.append(' '.join(transliterate.transliterate(line, polyglot_code)))
            res = '\n'.join(output)
            utils.save_output(res, path, out_dir, '-trans.txt')


if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Transliterate files.')
    parser.add_argument('-d','--output_dir', type=str, default='.', help='Directory to which to write the output files.')
    parser.add_argument('input', metavar='N', default=None, type=str, nargs='+', help='List of files to be tagged. Format: NAME_LANG[_ID][.ext], for example Hobbit_eng.txt')
    args = parser.parse_args()


    # This is the main thing
    config = utils.get_config()
    book_files, lang_files = utils.parse_input_files(args.input)
    transliterate_files(lang_files, config, args.output_dir)
