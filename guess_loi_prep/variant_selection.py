import argparse

from pysam import VariantFile, FastaFile
from pysam.libcbcf import VariantRecord


def create_vcf_for_brew_loi():
    parser = argparse.ArgumentParser(description="""
            Select variants from a Gzipped ENSEMBL VCF file.
            Exclude sites with Reference allele not present in the reference.
            Marks multi allelic sites and SNV that share the same position (the second is marked).
            
            """)

    parser.add_argument('vcf_file_gz', help="a Gzipped VCF file from ENSEMBL")
    parser.add_argument('genome_file', help="the fasta reference genome")

    args = parser.parse_args()

    # with NamedTemporaryFile() as tmp:
    #     with gzip.open(args.vcf_file_gz, 'rb') as gtf:
    #         for line in gtf:
    #             tmp.write(line)
    #
    #     tmp.seek(0)
    #
    #     split_variants(tmp.name, args.genome_file)
    # split_variants(args.vcf_file_gz, args.genome_file)
    split_variants_to_files(args.vcf_file_gz, args.genome_file, 'biallelic.vcf', 'multiallic.vcf')


def split_variants_to_files(vcf_file, genome_file, bi_file, multi_file):
    vcf = VariantFile(vcf_file)
    genome = FastaFile(genome_file)
    vcf.header.add_line('##INFO=<ID=multi,Number=0,Type=Flag,'
                        'Description="Variant with multiple allele">')
    vcf.header.add_line('##INFO=<ID=duplicated,Number=0,Type=Flag,'
                        'Description="Duplicated in position">')
    vcf.header.formats.add('GT', 1, 'String', "Genotype")
    vcf.header.add_sample("Genotype")

    with open(bi_file, 'wt') as outbi:
        with open(multi_file, 'wt') as outmu:

            outbi.write(str(vcf.header))
            outmu.write(str(vcf.header))

            for multi_alleles, duplicated, record in iter_wanted_variants(vcf, genome):
                record = record_to_string(record) + ['GT', '0/1']
                record = '\t'.join(record)
                if duplicated:
                    continue
                if multi_alleles:
                    outmu.write(record + '\n')
                else:
                    outbi.write(record + '\n')


def split_variants(vcf_file, genome_file):
    vcf = VariantFile(vcf_file)
    genome = FastaFile(genome_file)
    vcf.header.add_line('##INFO=<ID=multi,Number=0,Type=Flag,'
                        'Description="Variant with multiple allele">')
    vcf.header.add_line('##INFO=<ID=duplicated,Number=0,Type=Flag,'
                        'Description="Duplicated in position">')
    vcf.header.formats.add('GT', 1, 'String', "Genotype")
    vcf.header.add_sample("Genotype")

    print(vcf.header, end='')

    for multi_alleles, duplicated, record in iter_wanted_variants(vcf, genome):
        record = record_to_string(record) + ['GT', '0/1']
        if multi_alleles:
            add = "multi" if record[6] else ";multi"
            record[6] += add

        if duplicated:
            add = "duplicated" if record[6] else ";duplicated"
            record[6] += add

        record = '\t'.join(record)

        print(record)


def record_to_string(record):
    info_field = format_item_list(record.info.items())
    filter_filed = format_item_list(record.filter.items())
    qual_field = '.' if not record.qual else record.qual

    if record.alts is None:
        alts = ','.join(non_ref_alleles(record.ref))
    else:
        alts = ','.join([a for a in record.alts])

    return [record.chrom, str(record.pos), record.id, record.ref, alts,
            qual_field, filter_filed, info_field]


def non_ref_alleles(ref):
    nucleotides = ["A", "C", "G", "T"]
    nucleotides.remove(ref)
    return tuple(nucleotides)


def format_item_list(items):
    if not len(items):
        return '.'
    item_string = []
    for i in items:
        key, value = i
        if value is True:
            item_string.append(key)
        else:
            item_string.append(key + '=' + str(value))
    return ';'.join(item_string)


def iter_wanted_variants(vcf, genome):
    chrom = None
    pos = None

    for record in vcf:  # type: VariantRecord
        multi_alleles = False
        duplicated = False
        ref_seq = genome.fetch(record.chrom, record.pos-1, record.pos)

        if not ref_seq == record.ref:
            continue

        if not record.info.get("TSA") == "SNV":
            continue

        if chrom is not None and record.chrom < chrom:
            exit("disorder found in chromosomes")

        if not record.chrom == chrom:
            pos = None

        if pos is not None and record.pos < pos:
            exit("disorder found position")

        if pos is not None and pos == record.pos:
            duplicated = True

        chrom = record.chrom
        pos = record.pos

        if len(record.alleles) != 2:
            multi_alleles = True

        yield [multi_alleles, duplicated, record]
