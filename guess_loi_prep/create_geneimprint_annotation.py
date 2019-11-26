import argparse


def create_geneimprint_annotation():
    parser = argparse.ArgumentParser(description="""
            Format annotations
            """)

    parser.add_argument('file', help="annotation file")
    args = parser.parse_args()
    gene2annotation = create_geneimprint_annotation_dict(args.file)
    for gene in gene2annotation:
        print(gene + '\t' + gene2annotation[gene])


def create_geneimprint_annotation_dict(file):
    dict = {}
    with open(file, 'rt') as fd:
        for key, *values in read_geneimprint_annotation(fd):
            mode, evidence, impr_allele, expr_allele = values
            annotation_list = [
                generate_if_not_na(mode, label="mode"),
                generate_if_not_na(evidence, label="evidence"),
                generate_if_not_na(impr_allele, label="imprinted_allele"),
                generate_if_not_na(expr_allele, label="expressed_allele"),
            ]

            annotation = []
            for a in annotation_list:
                if a is not None:
                    annotation.append(a)

            if key not in dict:
                dict[key] = ';'.join(annotation)
            else:
                exit('Duplicated key %s' % key)

        return dict


def generate_if_not_na(mode, label, glue=":"):
    if mode != "NA":
        return label + glue + mode


def read_geneimprint_annotation(fd):
    for line in fd:
        tokens = line.rstrip('\n').split('\t')
        if len(tokens) != 5:
            exit("Gene Imprint: Malformed input")
        yield tokens
