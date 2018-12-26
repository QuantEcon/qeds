import collections
import datetime
import os
import random
import pandas as pd


def _ensure_dir(dirname):
    if not os.path.isdir(dirname):
        os.makedirs(dirname)


def _make_list(x):
    if isinstance(x, int):
        return [x]

    if isinstance(x, str):
        return [x]

    if isinstance(x, collections.Sequence):
        return list(x)

    raise ValueError("Don't know how to make {} a list".format(x))


class QueryError(Exception):
    def __init__(self, msg, response):
        super(QueryError, self).__init__(msg)
        self.response = response


def iter_chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:(i + n)]


def random_dates(startdate, enddate, N, format="%Y-%m-%d"):
    # dates
    start = pd.to_datetime(startdate).to_pydatetime()
    end = pd.to_datetime(enddate).to_pydatetime()
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds

    def rand_time():
        return datetime.timedelta(seconds=random.randrange(int_delta))

    return [start + rand_time() for i in range(N)]
