from argparse import ArgumentParser
from os import makedirs
from os.path import join, exists
from subprocess import check_call

from guess_loi_prep.annotation import download_annotation
from guess_loi_prep.create_geneimprint_annotation import create_gene2source_dict
from guess_loi_prep.create_genetype_annotation import read_bed
from guess_loi_prep.create_par_regions import create_par_regions
from guess_loi_prep.download_genome import download_genome
from guess_loi_prep.download_variants import download_variants
from guess_loi_prep.filter_gtf import filter_gtf_by_genes
from guess_loi_prep.filter_vcf import filter_chromosome_vcfs, filter_global_vcf
from guess_loi_prep.general import read_chromosomes, species_name, check_file_exists, check_command_availability, \
    get_gatk_version
from guess_loi_prep.hisat_index import create_hisat_index
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

    # TODO: check this for correct annotations
    bed_annotated = "genes-and-sex-regions.bed"
    if not check_file_exists(bed_annotated):
        imprint_annotation_file = "igene_source_map.txt"
        if not exists(imprint_annotation_file):
            exit("Annotation file for imprinted genes not provided")

        # gene2info = create_geneimprint_annotation_dict(imprint_annotation_file)
        gene2info = create_gene2source_dict(imprint_annotation_file)
        # gene2type = create_genetype_annotation_dict(bed_file)
        par_chroms = create_par_regions(args.species + "-par.bed")
        annotate_bed(bed_file, bed_annotated, gene2info, par_chroms)

    genome_file = "genome.fa"
    genome_dict = "genome.dict"
    download_genome(args.species, args.ensembl_version, chromosomes)

    if not check_file_exists(genome_dict):
        check_call('gatk CreateSequenceDictionary -R=' + genome_file + ' -O=' + genome_dict, shell=True)

    if not check_file_exists(genome_file + '.fai'):
        check_call('samtools faidx ' + genome_file, shell=True)

    var_dir = "ensembl_variants"
    variants_file = args.species + '_brew.vcf'
    makedirs(var_dir, exist_ok=True)

    download_variants(args.species, args.ensembl_version, chromosomes, var_dir)

    if not check_file_exists(variants_file):
        if args.species != "homo_sapiens":
            filter_global_vcf("global.vcf.gz", bed_file, variants_file, var_dir)
        else:
            filter_chromosome_vcfs(chromosomes, bed_file, variants_file, var_dir)

    bi_vcf = 'snps-biallelic.vcf'
    multi_vcf = 'snps-multiallelic.vcf'
    i_bi_vcf = 'i_snps-biallelic.vcf'
    i_multi_vcf = 'i_snps-multiallelic.vcf'

    if not check_file_exists(bi_vcf) and not check_file_exists(multi_vcf):
        if not check_file_exists(i_bi_vcf) and not check_file_exists(i_multi_vcf):
            split_variants_to_files(variants_file, genome_file, i_bi_vcf, i_multi_vcf)
        update_vcf_seq_dict(i_bi_vcf, bi_vcf, genome_dict)
        gatk_index(bi_vcf)
        update_vcf_seq_dict(i_multi_vcf, multi_vcf, genome_dict)
        gatk_index(multi_vcf)

    wdir = "hisat2-index"
    makedirs(wdir, exist_ok=True)

    if not check_file_exists(join(wdir, 'genome.1.ht2')):
        create_hisat_index(genome_file, join(wdir, args.index_prefix), str(args.threads))


def update_vcf_seq_dict(in_vcf, output, genome_dict):
    check_command_availability(['gatk'])
    check_call(['gatk',
                'UpdateVCFSequenceDictionary',
                '--source-dictionary', genome_dict,
                '-V', in_vcf,
                '-O', output])


def gatk_index(vcf):
    check_command_availability(['gatk'])
    version = get_gatk_version()

    if version <= '4.0.11.0':
        check_call('gatk IndexFeatureFile -F ' + vcf, shell=True)
    else:
        check_call('gatk IndexFeatureFile -I ' + vcf, shell=True)


def annotate_bed(bed_file, output, gene2info, par=None):
    with open(output, 'wt') as out:
        with open(bed_file, "rt") as fd:
            for line in read_bed(fd):
                outline = line
                chrom, start, end, gene = line[:4]

                if gene in gene2info:
                    outline.append(gene2info[gene])

                if par is not None and chrom in par:
                    value = ','.join([i.data for i in par[chrom][int(end)]])
                    if value != '':
                        value = ';' + value
                        outline[5] += value

                out.write('\t'.join(outline) + "\n")


def parse_args():
    parser = ArgumentParser(description="Create the knowledge base")
    parser.add_argument('species', type=species_name, help='the species')
    parser.add_argument('chromosomes', help='a file with chromosomes to download')
    parser.add_argument('imprinted_genes', help='a file with the imprinted genes')
    parser.add_argument('-e', '--ensembl-version', type=int, help='the ENSEMBL annotation version')
    parser.add_argument('-i', '--index-prefix', help='hisat2-build index prefix', default="genome")
    parser.add_argument('-t', '--threads', help='hisat2-build number of threads', type=int, default=1)
    return parser.parse_args()


if __name__ == "__main__":
    main()
