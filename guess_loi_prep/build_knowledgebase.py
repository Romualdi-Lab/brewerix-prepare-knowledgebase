from argparse import ArgumentParser
from os import makedirs

from guess_loi_prep.annotation import download_annotation
from guess_loi_prep.download_variants import download_variants
from guess_loi_prep.filter_vcf import filter_chromosome_vcfs
from guess_loi_prep.general import read_chromosomes, species_name, check_file_exists
from guess_loi_prep.variant_selection import split_variants_to_files


def main():
    args = parse_args()
    chromosomes = read_chromosomes(args.chromosomes)
    gtf_gz = args.species + '.chr.gtf.gz'
    if not check_file_exists(gtf_gz):
        download_annotation(args.species, args.ensembl_version)

    bed_file = "igenes_and_xgenes.bed"
    # filter_gtf_by_genes(args.imprinted_genes, gtf_gz, bed_file)

    # download_genome(args.species, args.ensembl_version, chromosomes)

    genome_file = "genome.fa"
    var_dir = "ensembl_variants"
    variants_file = args.species + '_brew.vcf'

    makedirs(var_dir, exist_ok=True)
    download_variants(args.species, args.ensembl_version, chromosomes, var_dir)
    if not check_file_exists(variants_file):
        filter_chromosome_vcfs(chromosomes, bed_file, variants_file, var_dir)

    split_variants_to_files(variants_file, genome_file, 'snps-biallelic.vcf', 'snps-multiallelic.vcf')

    # gatk IndexFeatureFile -F
    # CreateSequenceDictionary R=genome-nrm.fa O=genome-nrm.dict
    # samtools faidx genome-nrm.fa


def parse_args():
    parser = ArgumentParser(description="Create the knowledge base")
    parser.add_argument('species', type=species_name, help='the species')
    parser.add_argument('chromosomes', help='a file with chromosomes to download')
    parser.add_argument('imprinted_genes', help='a file with the imprinted genes')
    parser.add_argument('-e', '--ensembl-version', type=int, help='the ENSEMBL annotation version')
    return parser.parse_args()


if __name__ == "__main__":
    main()
