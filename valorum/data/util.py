import collections


def _make_list(x):
    if isinstance(x, int):
        return [x]

    if isinstance(x, str):
        return [x]

    if isinstance(x, collections.Sequence):
        return list(x)

    raise ValueError(f"Don't know how to make {x} a list")


class QueryError(Exception):
    def __init__(self, msg, response):
        super(QueryError, self).__init__(msg)
        self.response = response


def iter_chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:(i + n)]
