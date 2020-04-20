from argparse import ArgumentParser
from os.path import join

from guess_loi_prep.download import download, DownloadError
from guess_loi_prep.general import read_chromosomes, species_name, check_file_exists


def main():
    args = parse_args()
    chromosomes = read_chromosomes(args.chromosomes)
    download_variants(args.species, args.ensembl_version, chromosomes)


def download_variants(species, ensembl_version, chromosomes, directory=None):
    directory = directory if directory else '.'
    if species != "homo_sapiens":
        if not check_file_exists(join(directory, 'global.vcf.gz')):
            try:
                download_global_variants(species, ensembl_version, directory)
            except DownloadError as e:
                exit(str(e))
    else:
        for chrom in chromosomes:
            if not check_file_exists(join(directory, chrom + '.vcf.gz')):
                try:
                    download_chromosome_variants(chrom, species, ensembl_version, directory)
                except DownloadError as e:
                    exit(str(e))


def download_global_variants(species, ensembl_version=None, directory=None):
    release = "release-%s/variation" % ensembl_version if ensembl_version else "current_variation"
    directory = directory if directory else '.'
    url = "ftp://ftp.ensembl.org/pub/%s/vcf/%s/%s.vcf.gz" % (release, species, species)
    download(url, join(directory, 'global.vcf.gz'))


def download_chromosome_variants(chrom, species, ensembl_version=None, directory=None):
    release = "release-%s/variation" % ensembl_version if ensembl_version else "current_variation"
    directory = directory if directory else '.'
    url = "ftp://ftp.ensembl.org/pub/%s/vcf/%s/%s-chr%s.vcf.gz" % (release, species, species, chrom)
    download(url, join(directory, chrom + '.vcf.gz'))


def parse_args():
    parser = ArgumentParser(description="Download ENSEMBL genome")
    parser.add_argument('species', type=species_name, help='the species')
    parser.add_argument('chromosomes', help='a file with chromosomes to download')
    parser.add_argument('-e', '--ensembl-version', type=int, help='the ENSEMBL annotation version')
    return parser.parse_args()


if __name__ == "__main__":
    main()
