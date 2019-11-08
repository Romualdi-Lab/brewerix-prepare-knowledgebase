from operator import itemgetter
from shutil import which
from typing import List, Iterable


def sort_by_columns(lines: Iterable[List], columns: List) -> List:
    yield from sorted(lines, key=itemgetter(*columns))


def check_command_availability(commands):
    for cmd in commands:
        if which(cmd) is None:
            exit("program not installed: %s" % cmd)
