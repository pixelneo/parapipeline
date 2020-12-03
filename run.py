#!/usr/bin/env python3
'''
    Author: Ondrej Mekota o(at)mkta.eu
'''
from tag import tag_lang_files
from align import align_book_files
import pipeline.utils as utils

if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run pipeline.')
    parser.add_argument('-o','--output_dir', type=str, default='.', help='Directory to which to write the output files.')
    parser.add_argument('input', metavar='N', default=None, type=str, nargs='+', help='List of files to be processed. Format: NAME_LANG[_ID][.ext], for example Hobbit_eng.txt')

    args = parser.parse_args()

    config = utils.get_config()
    book_files, lang_files = utils.parse_input_files(args.input, config)


    # tag and align
    tag_lang_files(lang_files, config, args.output_dir)
    align_book_files(book_files, args.output_dir)
