#!/usr/bin/env python3
"""
    Author: Ondrej Mekota o(at)mkta.eu
"""

import os
import subprocess
import tempfile

FILE_PATH = os.path.dirname(__file__)


class Aligner:
    def _convert_output(self, output: str):
        """Converts output of hunalign to indices links

        Args:
            output: str output of hunalign

        Returns:
            a list of (tuple('type'), list('from'), list('to))
                e.g. ((1,2), [23], [22, 23])

        """
        rungs = [
            tuple([int(i) for i in x.strip().split("\t")[:2]])
            for x in output.strip().split("\n")
        ]

        # contains (link_type, from, to)
        #  where link_type is (int, int), and from, to are [int]
        #  e.g. ((1,2), [23], [22, 23])
        links = []

        for rung, prev_rung in zip(rungs[1:], rungs):  # first one is always 0 0
            i_src = (prev_rung[0], rung[0])
            i_tgt = (prev_rung[1], rung[1])
            type_ = (i_src[1] - i_src[0], i_tgt[1] - i_tgt[0])
            from_ = list(range(*i_src))
            to_ = list(range(*i_tgt))
            links.append((type_, from_, to_))

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
            with open(fd0, "w") as f:
                f.write(src)
            with open(fd1, "w") as f:
                f.write(tgt)

            output = self.align_files(src_path, tgt_path, opts=["-utf"])

        finally:
            os.remove(src_path)
            os.remove(tgt_path)
        return output

    def align_files(self, path_src, path_tgt, opts=[]):
        """Aligns files `path_src` and `path_tgt`

        Returns:
            a list of (tuple('type'), list('from'), list('to))
                e.g. ((1,2), [23], [22, 23])

        """
        args = [os.path.join(FILE_PATH, "hunalign/data/null.dic"), path_src, path_tgt]
        args.extend(opts)
        p = subprocess.run(
            [os.path.join(FILE_PATH, "hunalign/src/hunalign/hunalign"), *args],
            capture_output=True,
            encoding="utf-8",
        )
        return self._convert_output(p.stdout)
