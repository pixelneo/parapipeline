#!/usr/bin/env python3
'''
    Author: Ondrej Mekota o(at)mkta.eu
'''

import itertools

from pipeline.aligners import hunalign
from pipeline import utils


def align_files(path_src, path_tgt):
    a = hunalign.Aligner()
    links = a.align_files(path_src, path_tgt)
    return utils.alignment_to_xml(links, path_src, path_tgt)

def align(src, tgt):
    a = hunalign.Aligner()
    return a.align(src, tgt)

def align_book_files(book_files, out_dir):
    """ input like {'hobbit': [('eng', 'a', '../hobbit_ENG_a.txt'), ('pol', 'a', ...)...], ...} """
    a = hunalign.Aligner()
    for book, texts in book_files.items():
        pairs = itertools.combinations(texts, 2)
        for (l1, v1, file1), (l2, v2, file2) in pairs:
            links = a.align_files(file1, file2)
            output_xml = utils.alignment_to_xml(links, file1, file2)
            utils.save_output(output_xml, f'{book}_{l1}-{l2}_{v1}-{v2}', out_dir, '_aligned.xml')




if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Align files.')

    #outputs = parser.add_mutually_exclusive_group(required=False)
    parser.add_argument('-o','--output_dir', type=str, default='.', help='Directory to which to write the output files.')
    # outputs.add_argument('--print', action='store_true', help='Instead of saving to file, print.')

    parser.add_argument('input', metavar='N', default=None, type=str, nargs='+', help='List of files to be tagged. Format: NAME_LANG[_ID][.ext], for example Hobbit_eng.txt')


    args = parser.parse_args()

    # TODO handle args: print? --input_file/--input ? in/out format


    # This is the main thing
    # with open(args.src) as f:
        # src = f.read()
    # with open(args.tgt) as f:
        # tgt = f.read()
    # print(align(src, tgt))

    config = utils.get_config()
    book_files, lang_files = utils.parse_input_files(args.input)
    align_book_files(book_files, args.output_dir)


