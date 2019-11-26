from itertools import groupby
from operator import itemgetter

from intervaltree import IntervalTree


def create_par_regions(bed_file):
    with open(bed_file, "rt") as fd:
        chroms = {}

        for chromosome, entries in groupby(read_bed(fd), itemgetter(0)):
            tree = IntervalTree()

            for entry in entries:
                start, stop, gene = entry[1:4]
                tree[start:stop] = gene

            chroms[chromosome] = tree

        return chroms


def read_bed(fd):
    for line in fd:
        tokens = line.rstrip('\n').split('\t')
        if len(tokens) < 4:
            exit("Par region bed: Malformed input")
        yield tokens
