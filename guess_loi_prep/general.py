import re
from argparse import ArgumentTypeError
from operator import itemgetter
from os.path import exists
from shutil import which
from typing import List, Iterable


def sort_by_columns(lines: Iterable[List], columns: List) -> List:
    yield from sorted(lines, key=itemgetter(*columns))


def check_command_availability(commands):
    for cmd in commands:
        if which(cmd) is None:
            exit("program not installed: %s" % cmd)


def read_chromosomes(file):
    with open(file, "rt") as fd:
        chromosomes = []
        for line in fd:
            tokens = line.rstrip("\n").split('\t')
            if len(tokens) != 1:
                exit("Unexpected number of columns")
            chromosomes.append(tokens[0])
    return chromosomes


def species_name(string):
    if re.match(r'^[a-z]+_[a-z]+$', string) is None:
        msg = "%r is not a valid species name (ex homo_sapiens)" % string
        raise ArgumentTypeError(msg)
    return string


def check_file_exists(file):
    if exists(file):
        print("A file named '%s' is already present in the directory. Please remove manually to force re build" % file)
        return True
    return False


def get_gatk_version():
    "The Genome Analysis Toolkit (GATK) v4.1.4.0"
    version_lines = check_output(['gatk', 'HaplotypeCaller', '--version'], stderr=STDOUT, universal_newlines=True)

    raw_version = version_lines.split('\n')[0]
    m = re.match(r'Version:(\d\.\d\.\d+\.\d+)', raw_version)
    if m is None:
        m = re.match(r'.+\(GATK\) v(\d\.\d\.\d+\.\d+)', raw_version)
    version = m.group(1)

    return version
