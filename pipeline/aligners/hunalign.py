#!/usr/bin/env python3
"""
    Author: Ondrej Mekota o(at)mkta.eu
"""

import os
import subprocess
import tempfile
import logging

FILE_PATH = os.path.dirname(__file__)


class Aligner:
    def _convert_output(self, output: str, len_src: int, len_tgt:int):
        """Converts output of hunalign to indices links

        Args:
            output: str output of hunalign

        Returns:
            a list of (tuple('type'), list('from'), list('to))
                e.g. ((1,2), [23], [22, 23])

        """
        rungs = [
            tuple([int(i) for i in x.strip().split('\t')[:2]])
            for x in output.strip().split('\n')
        ]

        # contains (link_type, from, to)
        #  where link_type is (int, int), and from, to are [int]
        #  e.g. ((1,2), [23], [22, 23])
        links = []

        # the first sentences of at least one of the languages are not aligned
        if rungs[0] != (0,0):
            index_ = 0 if rungs[0][0] != 0 else 1
            for index_ in [0,1]:
                type_ = (1,0) if index_ == 0 else (0,1)
                to_ = [rungs[0][0], rungs[0][1]][index_]
                for s in range(to_):
                    if index_ == 0:  # first n sentences of the first lang are not aligned
                        links.append((type_, [s], []))
                    elif index_ == 1: # first n sentences of the second lang are not aligned
                        links.append((type_, [], [s]))

        for rung, prev_rung in zip(rungs[1:], rungs):  # first one is always 0 0
            i_src = (min(prev_rung[0], len_src), min(rung[0], len_src))
            i_tgt = (min(prev_rung[1], len_tgt), min(rung[1], len_tgt))
            type_ = (i_src[1] - i_src[0], i_tgt[1] - i_tgt[0])
            from_ = list(range(*i_src))
            to_ = list(range(*i_tgt))
            links.append((type_, from_, to_))

        if rungs[-1] != (len_src, len_tgt):
            for index_ in [0,1]:
                type_ = (1,0) if index_ == 0 else (0,1)
                from_ = rungs[-1][index_]
                to_ = [len_src, len_tgt][index_]
                for s in range(from_, to_):
                    if index_ == 0:  # first n sentences of the first lang are not aligned
                        links.append((type_, [s], []))
                    elif index_ == 1: # first n sentences of the second lang are not aligned
                        links.append((type_, [], [s]))

        return links

    def align(self, src: str, tgt: str):
        """Aligns texts `src` and `tgt`

        Returns:
            a list of (tuple('type'), list('from'), list('to))
                e.g. ((1,2), [23], [22, 23])

        """
        try:
            fd0, src_path = tempfile.mkstemp()
            fd1, tgt_path = tempfile.mkstemp()
            with open(fd0, 'w') as f:
                f.write(src)
            with open(fd1, 'w') as f:
                f.write(tgt)

            output = self.align_files(src_path, tgt_path)

        finally:
            os.remove(src_path)
            os.remove(tgt_path)
        return output

    def align_files(self, path_src, path_tgt, opts=None):
        """Aligns files `path_src` and `path_tgt`

        Returns:
            a list of (tuple('type'), list('from'), list('to))
                e.g. ((1,2), [23], [22, 23])

        """
        args = ['-utf', '-realign', os.path.join(FILE_PATH,'hunalign/data/null.dic'), path_src, path_tgt]
        p = subprocess.run(
            [os.path.join(FILE_PATH, 'hunalign/src/hunalign/hunalign'), *args],
            capture_output=True,
            encoding='utf-8',
        )
        len_src = len_tgt = 0
        with open(path_src) as f:
            for i in f.readlines():
                len_src += 1
        with open(path_tgt) as f:
            for i in f.readlines():
                len_tgt += 1

        if p.stdout.strip() == '': #and p.stderr.strip() != '':
            logging.error(f'Hunalign error (sentence alignment of "{path_src}" and "{path_tgt}"), error: {p.stderr}')
            raise ValueError('Hunalign error')

        return self._convert_output(p.stdout, len_src, len_tgt)
