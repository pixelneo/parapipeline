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
            f2: xml file path, tokenized
            align:

        Returns:
            tuple of str and tuple
            -   str, each line represents aligned segment,
                tokens are space separated, there is '|||' on each line,
                separating the two texts.
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
            for i, ind_text in enumerate(link.get('xtargets').split(';')):
                indices[i].append([int(a) for a in ind_text.strip().split(' ') if a != ''])

        output = []
        for os1, os2 in zip(*indices):
            line = []
            for i, ind_list in enumerate([os1, os2]):
                orig_ends = []
                curr_id = 0
                for l in ind_list:
                    line.extend(sents[i][l])
                    orig_ends.append(curr_id + len(sents[i][l]))
                original_sents_end[i].append(orig_ends)
                line.append('|||')  # separator for eflomal
            if line[-1] == '|||':
                line.pop(-1)
            output.append(' '.join(line))
        return '\n'.join(output), original_sents_end


    def align_files(self, f1_tokenized, f2_tokenized, sent_alignment):
        # return links
        raise NotImplementedError()

        try:
            fd0, in_path = tempfile.mkstemp()
            fd1, out_path = tempfile.mkstemp()
            text, original_sents_end = self._get_sents_from_xml(f1_tokenized, f2_tokenized, sent_alignment, out)
            with open(fd0, 'w') as f:
                f.write(text)

            args = ['-i', in_path]
            p = subprocess.run(
                [os.path.join(FILE_PATH, 'eflomal/align.py'), *args],
                capture_output=True,
                encoding='utf-8',
            )
            output = p.stdout
            return output

        finally:
            os.remove(in_path)
            os.remove(out_path)


if __name__=='__main__':
    a = WordAligner()
    #output, orig = a._get_sents_from_xml('../outputs/Guide_CES.txt_tagged.xml', '../outputs/Guide_DEU.txt_tagged.xml', '../outputs/guide_ces-deu_None-None_aligned.xml')
    print(a.align_files('../outputs/Guide_CES.txt_tagged.xml', '../outputs/Guide_DEU.txt_tagged.xml', '../outputs/guide_ces-deu_None-None_aligned.xml'))

