from argparse import ArgumentParser

from guess_loi_prep.general import read_chromosomes


def main():
    args = parse_args()
    chromosomes = read_chromosomes(args.chromosomes)


    with open("genome.fa", "wt") as fd:
        for chrom in chromosomes:
            try:
                download_chromosome(chrom, args.species, fd, args.ensembl_version)
            except DownloadError as e:
                exit(str(e))


def parse_args():
    parser = ArgumentParser(description="Create the knowledge base")
    parser.add_argument('species', type=species_name, help='the species')
    parser.add_argument('chromosomes', help='a file with chromosomes to download')
    parser.add_argument('imprinted_genes', help='a file with the imprinted genes')
    parser.add_argument('-e', '--ensembl-version', type=int, help='the ENSEMBL annotation version')
    return parser.parse_args()


if __name__ == "__main__":
    main()
