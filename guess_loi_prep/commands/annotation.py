from argparse import ArgumentParser

from guess_loi_prep.annotation import download_annotation
from guess_loi_prep.download import DownloadError
from guess_loi_prep.general import species_name


def main():
    args=parse_args()
    try:
        download_annotation(args.species, args.ensembl_version)
    except DownloadError as e:
        exit(str(e))


def parse_args():
    parser = ArgumentParser(description="Download ENSEMBL gtf")
    parser.add_argument('species', type=species_name, help='the species')
    parser.add_argument('-e', '--ensembl-version', type=int, help='the ENSEMBL annotation version')
    return parser.parse_args()


if __name__ == "__main__":
    main()
