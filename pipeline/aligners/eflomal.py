#!/usr/bin/env python3
"""
    Author: Ondrej Mekota o(at)mkta.eu
"""

import os
import sys
import tempfile
import subprocess

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
            f2: xml file path, tokenized
            align:

        Returns:
            tuple of str, tuple of lists of int,  and tuple
            -   str, each line represents aligned segment,
                tokens are space separated, there is '|||' on each line,
                separating the two texts.
            -   tuple, lists of 'src' and 'tgt' aligned sentece indices
            -   tuple, contains lists for each text with original sentence endings
                e.g. ([[4,9],...],[...]) = first text's first sentence's tokens are 0,1,2,3, and its second sentence's tokens are 0..8.

        """
        sents = ([], [])
        indices = ([], [])
        original_sents_end = ([], [])

        # get tokenized sentences for both files
        for i, path in enumerate([f1, f2]):
            root = etree.parse(path).getroot()
            for t in root:
                for p in t:
                    for s in p:
                        tokens = []
                        for t in s:
                            tokens.append(t.text)
                        sents[i].append(tokens)

        root = etree.parse(align).getroot()
        for link in root:
            it = 0
            for i, ind_text in enumerate(link.get('xtargets').split(';')):
                indices[i].append([int(a) for a in ind_text.strip().split(' ') if a != ''])
                it += 1
            for i in range(it):
                if len(indices[i]) == 0:  # if there is an unaligned sentece
                    for j in range(it):  # remove all such links
                        indices[j].pop(-1)
                    break

        output = []
        for os1, os2 in zip(*indices):
            line = []
            if len(os1) == 0 or len(os2) == 0:
                raise ValueError('INTERNAL error: An unaligned sentece has appeared. This should never happen.')
                continue
            for i, ind_list in enumerate([os1, os2]):
                orig_ends = []
                curr_id = 0
                for l in ind_list:
                    line.extend(sents[i][l])
                    orig_ends.append(curr_id + len(sents[i][l]))
                original_sents_end[i].append(orig_ends)
                line.append('|||')  # separator for eflomal

            # TODO this will cause errors because original_sents_end is not the same length as indices
            # TODO indices has to correspond to original_sents_end and lines in the output !!!!!!!!!


            if line[-1] == '|||':
                line.pop(-1)
            output.append(' '.join(line))
        return '\n'.join(output), indices, original_sents_end

    def _convert_eflomal_output(self, links, sentence_indices, original_sents_end):
        """ Convert eflomal output to XML file

        Args:
            links: list of links per aligned sentences [['0-1', '3-2'], ...]
            sentence_indices: 
            original_sents_end: number of words per each sentence

        """
        # TODO iterate zip(sentence_indices), IGNORE such where at least of the lists is len()==0

        # TODO  test last commit



    def align_files(self, f1_tokenized, f2_tokenized, sent_alignment):
        """ Word align files

        Args:
            f1_tokenized: XML tokenized file
            f2_tokenized: XML tokenized file
            sent_alignment: XML alignment

        Returns:
            

        """
        try:
            fd0, in_path = tempfile.mkstemp()
            fd1, out_path = tempfile.mkstemp()
            text, sent_indices, original_sents_end = self._get_sents_from_xml(f1_tokenized, f2_tokenized, sent_alignment)
            with open(fd0, 'w') as f:
                f.write(text)

            args = ['-i', in_path, '-f', out_path, '--overwrite']
            p = subprocess.run(
                [os.path.join(FILE_PATH, 'eflomal/align.py'), *args],
                capture_output=True,
                encoding='utf-8',
            )
            with open(fd1) as f:
                links = [l.strip().split(' ') for l in f.readlines()]
            self._convert_eflomal_output(links, sentence_indices, original_sents_end)

        finally:
            os.remove(in_path)
            print(out_path)
            #os.remove(out_path)


if __name__=='__main__':
    a = WordAligner()
    #output, orig = a._get_sents_from_xml('../outputs/Guide_CES.txt_tagged.xml', '../outputs/Guide_DEU.txt_tagged.xml', '../outputs/guide_ces-deu_None-None_aligned.xml')
    print(a.align_files('../outputs-test/code_eng.txt_tagged.xml', '../outputs-test/code_slk.txt_tagged.xml', '../outputs-test/code_eng-slk_none-none_aligned.xml'))

