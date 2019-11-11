from argparse import ArgumentParser

from guess_loi_prep.commands.annotation import species_name
from guess_loi_prep.download import DownloadError, download_and_unpack
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


def download_chromosome(chrom, species, fd, ensembl_version=None):
    release = "release-%s/gtf" % ensembl_version if ensembl_version else "current_fasta"
    url = "ftp://ftp.ensembl.org/pub/%s/%s/dna/*.dna.chromosome.%s.fa.gz" % (release, species, chrom)
    download_and_unpack(url, fd)


def parse_args():
    parser = ArgumentParser(description="Download ENSEMBL genome")
    parser.add_argument('species', type=species_name, help='the species')
    parser.add_argument('chromosomes', help='a file with chromosomes to download')
    parser.add_argument('-e', '--ensembl-version', type=int, help='the ENSEMBL annotation version')
    return parser.parse_args()


if __name__ == "__main__":
    main()
