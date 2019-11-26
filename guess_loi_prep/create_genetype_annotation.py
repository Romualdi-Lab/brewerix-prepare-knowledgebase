import argparse


def create_genetype_annotation():
    parser = argparse.ArgumentParser(description="""
            Format annotations
            """)

    parser.add_argument('file', help="annotation file")
    args = parser.parse_args()
    gene2type = create_genetype_annotation_dict(args.file)
    for gene in gene2type:
        print(gene + '\t' + ';'.join(gene2type[gene]))


def create_genetype_annotation_dict(bed):
    dict = {}
    with open(bed, 'rt') as fd:
        for _, _, _, key, _, type in read_bed(fd):
            if key not in dict:
                dict[key] = set([type])
            else:
                dict[key].add(type)
        return dict


def read_bed(fd):
    for line in fd:
        tokens = line.rstrip('\n').split('\t')
        print(tokens)
        if len(tokens) < 6:
            exit("annotation: Malformed input")
        yield tokens
