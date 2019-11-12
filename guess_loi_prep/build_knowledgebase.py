from argparse import ArgumentParser
from os import makedirs
from subprocess import check_call

from guess_loi_prep.annotation import download_annotation
from guess_loi_prep.download_genome import download_genome
from guess_loi_prep.download_variants import download_variants
from guess_loi_prep.filter_gtf import filter_gtf_by_genes
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
    if not check_file_exists(bed_file):
        filter_gtf_by_genes(args.imprinted_genes, gtf_gz, bed_file)

    genome_file = "genome.fa"
    genome_dict = "genome.dict"
    download_genome(args.species, args.ensembl_version, chromosomes)
    check_call('gatk CreateSequenceDictionary -R=' + genome_file + ' -O=' + genome_dict, shell=True)
    check_call('samtools faidx ' + genome_file, shell=True)

    var_dir = "ensembl_variants"
    variants_file = args.species + '_brew.vcf'
    makedirs(var_dir, exist_ok=True)
    download_variants(args.species, args.ensembl_version, chromosomes, var_dir)

    if not check_file_exists(variants_file):
        filter_chromosome_vcfs(chromosomes, bed_file, variants_file, var_dir)

    bi_vcf = 'snps-biallelic.vcf'
    multi_vcf = 'snps-multiallelic.vcf'

    if not check_file_exists(bi_vcf) and check_file_exists(multi_vcf):
        split_variants_to_files(variants_file, genome_file, bi_vcf, multi_vcf)
        check_call('gatk IndexFeatureFile -F ' + bi_vcf, shell=True)
        check_call('gatk IndexFeatureFile -F ' + multi_vcf, shell=True)


def parse_args():
    parser = ArgumentParser(description="Create the knowledge base")
    parser.add_argument('species', type=species_name, help='the species')
    parser.add_argument('chromosomes', help='a file with chromosomes to download')
    parser.add_argument('imprinted_genes', help='a file with the imprinted genes')
    parser.add_argument('-e', '--ensembl-version', type=int, help='the ENSEMBL annotation version')
    return parser.parse_args()


if __name__ == "__main__":
    main()
