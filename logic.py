import math
import random
from itertools import zip_longest


# copied from https://docs.python.org/library/itertools.html#itertools-recipes
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def bingo_from_iterable(values, num_cols=None):
    # strip surrounding whitespace (e.g. the newline of file lines, the \r of
    # textarea lines) and drop empty values
    filtered_values = [value.strip() for value in values
                       if value is not None and value.strip()]
    random.shuffle(filtered_values)
    if num_cols is None:
        num_cols = int(math.sqrt(len(filtered_values)))
    # missing cells are None (JSON null), so they can't clash with a real value
    return grouper(filtered_values, num_cols)