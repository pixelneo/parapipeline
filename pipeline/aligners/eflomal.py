#!/usr/bin/env python3
"""
    Author: Ondrej Mekota o(at)mkta.eu
"""

import os
import sys

from lxml import etree

FILE_PATH = os.path.dirname(__file__)
sys.path.append(os.path.join(FILE_PATH, '..'))


import taggers.udpipe
class WordAligner:
    def __init__(self):
        pass


    def _get_sents_from_xml(self, f1, f2, align):
        """  Extract sentence aligned 'segments'

        Args:
            f1: xml file path, tokenized
            f2: cml file path, tokenized
            align:

        Returns:
            tuple of str and tuple
            -   str, each line represents aligned segment,
                tokens are space separated, there is '|||' on each line,
                separating the two texts.
            -   tuple, contains lists for each text with original sentence endings
                e.g. ([[4,9],...],[...]) = first text's first sentence's tokens are 0,1,2,3.

        """
        sents = ([], [])
        indices = ([], [])
        original_sents_end = ([], [])

        # get tokenized sentences for both files
        for i, path in enumerate([f1, f2]):
            root = etree.parse(path, encoding='utf-8')
            for p in root.get_children():
                for s in p.get_children():
                    tokens = []
                    for t in s.get_children():
                        tokens.append(t.text)
                    sents[i].append(tokens)

        root = etree.parse(align, encoding='utf-8')
        for link in root.get_children():
            for i, ind_text in enumerate(link.get('xtargets').split(';')):
                indices[i].append(ind_text.split(' '))

        output = []
        for os1, os2 in indices:
            line = []
            for i, ind_list in enumerate([os1, os2]):
                orig_ends = []
                curr_id = 0
                for l in ind_list:
                    line.extend(sents[l])
                    orig_ends.append(curr_id + len(sents[l]))
                original_sents_end[i].append(orig_ends)
                line.append('|||')  # separator for eflomal
            output.append(' '.join(line))
        return '\n'.join(output), original_sents_end


    def align_files(self, f1_tokenized, f2_tokenized, sent_alignment):
        # return links
        raise NotImplementedError()

        try:
            fds, out = tempfile.mkstemp()
            self._convert_input(f1_tokenized, f2_tokenized, sent_alignment, out)

        finally:
            os.remove(src_file)
            os.remove(tgt_file)


if __name__=='__main__':
    a = WordAligner()
    print(a._get_sents_from_xml(TODO))  # TODO

