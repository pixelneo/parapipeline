#!/usr/bin/env python3
'''
    Author: Ondrej Mekota o(at)mkta.eu
'''

import os

import pipeline
from pipeline.transliterators import transliterate
import pipeline.utils as utils




def transliterate_files(config, files, lang, enc, out_dir, print_=False, return_=True):
    polyglot_code = utils.get_polyglot_lang_code(config, lang)
    assert not (return_ == True and print_ == True), 'Cannot both print and return from transliteration.'

    for path in files:
        output = []
        with open(path, encoding=enc) as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            output.append(' '.join(transliterate.transliterate(line, polyglot_code)))

        res = '\n'.join(output)

        if return_:
            return res
        elif print_:
            print(res)
        else:
            utils.save_output(res, path, out_dir, '-trans.txt')


if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Transliterate files.')
    parser.add_argument('-l','--language', type=str, required=True, help='ISO-693-3 code of language.')
    parser.add_argument('-e','--encoding', type=str, default='utf-8', help='Encoding of the files')

    # TODO change this
    # parser.add_argument('--out_format', type=str, default='conllu', help='TODO: change this: Format of the output: \'conllu\', \'vertical\', \'horizontal\', None')
    # parser.add_argument('--in_format', type=str, default='vertical', help='TODO: change this: Format of the input: \'conllu\', \'vertical\', \'horizontal\', \'split\', None. \'split\' performs sentence splitting')

    outputs = parser.add_mutually_exclusive_group(required=False)
    outputs.add_argument('-d','--output_dir', type=str, default='.', help='Directory to which to write output files')
    outputs.add_argument('--print', action='store_true', help='Instead of saving to file, print.')

    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument('-f','--input_file', type=str, default=None, required=False, help='Files specifying input file..')
    inputs.add_argument('-i','--input', metavar='N', default=None, required=False, type=str, nargs='+', help='List of files to be tagged.')

    args = parser.parse_args()

    # TODO handle args: print? --input_file/--input ? in/out format


    # This is the main thing
    config = pipeline.utils.get_config()
    output = transliterate_files(config, args.input, args.language, args.encoding, args.output_dir, args.print, return_ = False)



