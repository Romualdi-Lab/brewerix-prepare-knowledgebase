from operator import itemgetter
from typing import List, Iterable


def sort_by_columns(lines: Iterable[List], columns: List) -> List:
    yield from sorted(lines, key=itemgetter(*columns))
