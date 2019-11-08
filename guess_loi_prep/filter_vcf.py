import argparse
from subprocess import check_call


def filter_vcf():
    parser = argparse.ArgumentParser(description="""
            Filter a Gzipped ENSEMBL CVF file using a bedfile (require bedtools).
            """)

    parser.add_argument('vcf_file_gz', help="a Gzipped VCF file from ENSEMBL")
    parser.add_argument('bed_file', help="a bed file")

    args = parser.parse_args()

    check_call(["bedtools", "intersect", "-u", "-wa", "-header",
                "-a", args.vcf_file_gz,
                "-b", args.bed_file])
