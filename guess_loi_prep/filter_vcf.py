import argparse
from subprocess import check_call

from guess_loi_prep.general import read_chromosomes


def filter_vcf():
    parser = argparse.ArgumentParser(description="""
            Filter a Gzipped ENSEMBL VCF file using a bedfile (require bedtools).
            """)

    parser.add_argument('vcf_file_gz', help="a Gzipped VCF file from ENSEMBL")
    parser.add_argument('bed_file', help="a bed file")

    args = parser.parse_args()

    check_call(["bedtools", "intersect", "-u", "-wa", "-header",
                "-a", args.vcf_file_gz,
                "-b", args.bed_file])


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


def filter_chromosome_vcfs(chromosomes, bed_file, filename):
    with open (filename, "wt") as fd:
        fixed_parameters = ["bedtools", "intersect", "-u", "-wa"]
        for count, chrom in enumerate(chromosomes):
            filename = chrom + '.vcf.gz'

            if count == 0:
                cmd = fixed_parameters + ['-header'] + ["-a", filename,"-b", bed_file]
            else:
                cmd = fixed_parameters + ["-a", filename,"-b", bed_file]

            check_call(cmd, stdout=fd)
