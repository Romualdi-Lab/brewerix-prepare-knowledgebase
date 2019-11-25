import argparse
from os.path import join
from subprocess import check_call

from guess_loi_prep.general import read_chromosomes


def filter_vcf():
    parser = argparse.ArgumentParser(description="""
            Filter a Gzipped ENSEMBL VCF file using a bedfile (require bedtools).
            """)

    parser.add_argument('vcf_file_gz', help="a Gzipped VCF file from ENSEMBL")
    parser.add_argument('bed_file', help="a bed file")
    parser.add_argument('output_file', help="an output vcf file")

    args = parser.parse_args()

    filter_global_vcf(args.vcf_file_gz, args.bed_file, args.output)


def filter_vcfs():
    parser = argparse.ArgumentParser(description="""
            Filter a Gzipped ENSEMBL VCFs file using a bedfile (require bedtools).
            Files should be listed in the chromosomes file without .vcf.gz.
            """)

    parser.add_argument('chromosomes', help="a file with chromosome names")
    parser.add_argument('bed_file', help="a bed file")
    parser.add_argument('output_file', help="an output vcf file")

    args = parser.parse_args()
    chromosomes = read_chromosomes(args.chromosomes)
    filter_chromosome_vcfs(chromosomes, args.bed_file, args.output_file)


def filter_chromosome_vcfs(chromosomes, bed_file, filename, directory=None):
    directory = directory if directory else '.'

    with open(filename, "wt") as fd:
        fixed_parameters = ["bedtools", "intersect", "-u", "-wa"]
        for count, chrom in enumerate(chromosomes):
            local_vcf = join(directory, chrom + '.vcf.gz')

            if count == 0:
                cmd = fixed_parameters + ['-header'] + ["-a", local_vcf, "-b", bed_file]
            else:
                cmd = fixed_parameters + ["-a", local_vcf, "-b", bed_file]

            check_call(cmd, stdout=fd)


def filter_global_vcf(vcf_file_gz, bed_file, filename, directory=None):
    directory = directory if directory else '.'
    local_vcf = join(directory, vcf_file_gz)

    with open(filename, "wt") as fd:
        check_call(["bedtools", "intersect", "-u", "-wa", "-header",
                    "-a", local_vcf,
                    "-b", bed_file], stdout=fd)
