import argparse
from subprocess import check_call

from guess_loi_prep.general import check_command_availability


def create_hisat2_index():
    parser = argparse.ArgumentParser(description="""
            Create hisat2 Index
            """)

    parser.add_argument('genome', help="Genome fa file")
    parser.add_argument('prefix', help="index prefix")
    parser.add_argument('-t', '--threads', help="number of cores", default=1)
    args = parser.parse_args()

    check_command_availability(["hisat2", "hisat2-build"])
    create_hisat_index(args.genome, args.prefix, args.threads)


def create_hisat_index(genome, prefix, threads):
    check_call(['hisat2-build',
                '-p', threads,
                genome, prefix])
