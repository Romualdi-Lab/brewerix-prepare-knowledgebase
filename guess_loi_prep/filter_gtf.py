import argparse
import gzip
from itertools import groupby
from operator import itemgetter
from typing import List

from guess_loi_prep.general import sort_by_columns


def filter_gtf():
    parser = argparse.ArgumentParser(description="""
            Filter a Gzipped ENSEMBL GTF file by a list of imprinted gene names.
            Sexual chromosomes are retained as well.
            Consider using bedtools as well.
            """)

    parser.add_argument('genes', help="Imprinted genes file name")
    parser.add_argument('gtf', help="Gzipped GTF")

    args = parser.parse_args()
    filtered_gtf = filter_gft_by_imprinted_genes(args.genes, args.gtf)

    for key, values in groupby(sort_by_columns(filtered_gtf, [0, 3, 1]), itemgetter(0, 3)):
        entries = list(values)

        if len(entries) == 1:
            print('\t'.join([str(x) for x in entries[0]]))
        else:
            union = entries.pop(0)
            chrom, start, stop, gene = union[:4]
            annotation = union[4:]
            genomic_range = set(range(start, stop))

            for entry in entries:
                gr = set(range(entry[1], entry[2]))
                if not genomic_range.intersection(gr):
                    print('\t'.join([chrom, str(min(genomic_range)), str(max(genomic_range)), gene] + annotation))
                    genomic_range = gr
                else:
                    genomic_range = genomic_range.union(gr)

            # print('\t'.join([str(x) for x in entry]))
            print('\t'.join([chrom, str(min(genomic_range)), str(max(genomic_range)), gene] + annotation))


def filter_gft_by_imprinted_genes(igenes_file: str, gtf_file: str, keep_chrs=None) -> List:
    if keep_chrs is None:
        keep_chrs = ["X", "Y"]
    igenes = list(read_imprinted_genes(igenes_file))
    for entry in read_gtf(gtf_file):
        chrom, start, stop, gene = entry[:4]
        anno = entry[4:]
        if gene in igenes or chrom in keep_chrs:
            yield [chrom, int(start), int(stop), gene] + anno


def read_imprinted_genes(file):
    with open(file, 'r') as igenes:
        for gene in igenes:
            yield gene.rstrip("\n")


def read_gtf(file, features=None):
    """

    :param file: str with a filename. Imput must be Gzipped
    :type features: List
    """
    if features is None:
        features = ["gene"]

    for chrom, _, feature, start, end, _, strand, _, annotation in iterlines(file):
        if feature in features:
            required_fields = parse_annotation(annotation, fields=["gene_name", "gene_biotype"])
            yield [chrom, start, end] + [required_fields[0]] + [strand] + required_fields[1:]


def iterlines(filename):
    with gzip.open(filename, 'rb') as gtf:
        for line in gtf:
            line = line.decode()
            if line[0] == "#":
                continue
            tokens = line.strip("\n").split('\t')
            if len(tokens) == 9:
                yield tokens
            else:
                exit('The input file does not have 9 columns')


def parse_annotation(anno, fields=None):
    """

    :param anno: string with annotation. "; " as separator and ";" end character.
    :type fields: List
    """
    if fields is None:
        fields = ["gene_name", "gene_biotype"]

    anno = anno.replace('"', '').rstrip(';').split('; ')
    anno_dict = dict((a.split(' ')) for a in anno)
    return [get_annotation_value(key, anno_dict) for key in fields]


def get_annotation_value(key, dict_map):
    if key in dict_map:
        return dict_map[key]
    else:
        return 'NA'
