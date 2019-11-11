from argparse import ArgumentParser

from guess_loi_prep.commands.annotation import species_name
from guess_loi_prep.download import download, DownloadError
from guess_loi_prep.general import read_chromosomes


def main():
    args = parse_args()
    chromosomes = read_chromosomes(args.chromosomes)
    for chrom in chromosomes:
        try:
            download_chromosome_variants(chrom, args.species, args.ensembl_version)
        except DownloadError as e:
            exit(str(e))


def download_chromosome_variants(chrom, species, ensembl_version=None):
    release = "release-%s/gtf" % ensembl_version if ensembl_version else "current_variation"
    url = "ftp://ftp.ensembl.org/pub/%s/vcf/%s/%s-chr%s.vcf.gz" % (release, species, species, chrom)
    download(url, chrom + '.vcf.gz')


def parse_args():
    parser = ArgumentParser(description="Download ENSEMBL genome")
    parser.add_argument('species', type=species_name, help='the species')
    parser.add_argument('chromosomes', help='a file with chromosomes to download')
    parser.add_argument('-e', '--ensembl-version', type=int, help='the ENSEMBL annotation version')
    return parser.parse_args()


if __name__ == "__main__":
    main()
