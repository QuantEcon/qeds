import collections
import curses.ascii
import json
import os
import textwrap
import warnings

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
# from util import DATA_DIR, KEY_ENV_NAME, KEY_FILE_NAME, DEFAULT_API_URL
from .util import DATA_DIR, KEY_ENV_NAME, KEY_FILE_NAME, DEFAULT_API_URL


if not os.path.isdir(DATA_DIR):
    os.makedirs(DATA_DIR)


def _update_data_file():
    url = "https://api.census.gov/data.json"
    r = requests.get(url)
    file_path = os.path.join(DATA_DIR, "data.json")
    with open(file_path, "w") as f:
        f.write(json.dumps(r.json()))


def _load_metadata():
    if not os.path.isfile(os.path.join(DATA_DIR, "data.json")):
        _update_data_file()

    with open(os.path.join(DATA_DIR, "data.json"), "r") as f:
        _DATA_RAW = json.load(f)

    _DATA = pd.DataFrame(_DATA_RAW["dataset"])
    _DATA["c_dataset"] = _DATA["c_dataset"].apply(lambda x: "/".join(x))
    return _DATA_RAW, _DATA


_DATA_RAW, _DATA = _load_metadata()


def _make_list(x):
    if isinstance(x, int):
        return [x]

    if isinstance(x, str):
        return [x]

    if isinstance(x, collections.Sequence):
        return list(x)

    raise ValueError(f"Don't know how to make {x} a list")


def query_predicate_string(name, arg):
    arg = _make_list(arg)
    if len(arg) > 0:
        out = f"&{name}="
        out += f"&{name}=".join(str(i) for i in arg)
        return out
    else:
        return ""

    raise ValueError(f"Don't know how to handle query predicate arg {arg}")


def geo_predicate_string(name, arg):
    arg = _make_list(arg)
    return name + ":" + ",".join(str(i) for i in arg)


class QueryError(Exception):
    def __init__(self, msg, response):
        super(QueryError, self).__init__(msg)
        self.response = response


class CensusData(object):
    def __init__(self, url=DEFAULT_API_URL, key=None):
        if key is None:
            if KEY_ENV_NAME in os.environ:
                key = os.environ[KEY_ENV_NAME]
            elif os.path.isfile(KEY_FILE_NAME):
                with open(KEY_FILE_NAME, "r") as f:
                    key = f.read()
            else:
                raise EnvironmentError("Census API key not detected")

        API_KEY_LENGTH = 40
        if len(key) > API_KEY_LENGTH:
            key = key[:API_KEY_LENGTH]
            msg = f"API key too long, using first {API_KEY_LENGTH} characters"
            warnings.warn(msg)
        elif len(key) < API_KEY_LENGTH:
            msg = f"API key {key} too short. Should be {API_KEY_LENGTH} chars"
            raise ValueError(msg)

        if not all(curses.ascii.isxdigit(i) for i in key):
            msg = f"API key {key} contains invalid characters"
            raise ValueError(msg)

        self.key = key
        self.url = url

        self.sess = requests.Session()
        self.sess.mount(self.url, HTTPAdapter(max_retries=3))

        # NOTE: subclasses must define self.dataset, self.meta, and
        # self.vars_df

    def _geography_query(self, kwargs):
        """
        Given the information about the state and county, add `for` and `in`
        arguments to params
        """
        state = _make_list(kwargs.pop("state", []))
        county = _make_list(kwargs.pop("county", []))
        msa = _make_list(kwargs.pop("msa", []))

        out = ""
        if len(msa) > 0:
            out += "&for="
            out += geo_predicate_string(
                "metropolitan statistical area/micropolitan statistical area",
                msa
            )
            return out


        if len(county) == 0:
            if len(state) == 0:
                m = "Both state and county were empty. "
                m += "Some geography must be given"
                raise ValueError(m)

            # state is not empty
            out += "&for=" + geo_predicate_string("state", state)
            return out

        # county is not empty
        out += "&for=" + geo_predicate_string("county", county)

        if len(state) > 0:
            # also have in clause for states
            out += "&in=" + geo_predicate_string("state", state)

        return out

    def get(self, variables, start_time=None, end_time=None, timeout=None,
            **kwargs):
        """
        Get the specified variables from the data set

        Parameters
        ----------
        variables: list(str)
            A list of variables to obtain

        start_time, end_time: str, optional(default=None)
            A YYYY-MM-DD string specifying the starting and ending time. Only
            applicable for time series datasets

        **kwargs
            All other keyword arguments are used as predicates in the query
        """
        variables = _make_list(variables)

        self.validate_vars(variables)
        var_string = ",".join(variables)
        query = f"?get={var_string}&key={self.key}"

        # all kwargs must also be valid varirables, except for state, us,
        # and county, which are handled separately
        if "us" in kwargs:
            # if US is present, then we will skip the state/county args
            query += "&for=us:*"
            kwargs.pop("us")
        else:
            query += self._geography_query(kwargs)

        self.validate_vars(kwargs.keys())

        for (k, v) in kwargs.items():
            if k != "state" and k != "county":
                query += query_predicate_string(k, v)

        r = self.sess.get(self.url + self.dataset + query, timeout=timeout)
        if r.status_code != 200:
            msg = f"Query failed with status code {r.status_code}. "
            msg += f"Response from server was\n{r.content}"
            raise QueryError(msg, r)

        try:
            js = r.json()
            df = pd.DataFrame(js[1:], columns=js[0])
        except:
            if "SIC" in kwargs or "SIC" in variables:
                try:
                    df = pd.read_json(r.content.replace(b"\\", b""))
                    df.columns = df.iloc[0, :].tolist()
                    df.drop(0, axis=0, inplace=True)
                except:
                    msg = "Couldn't parse query result into DataFrame."
                    raise QueryError(msg, r)
            else:
                msg = f"Query failed with status code {r.status_code}. "
                msg += f"Response from server was\n{r.content}"
                raise QueryError(msg, r)

        df.rename(
            columns={"metropolitan statistical area/micropolitan statistical area": "MSA"},
            inplace=True
        )

        for k in df.columns:
            if k in ["state", "county", "us", "MSA", "zipcode"]:
                df[k] = df[k].astype(int)
                continue

            if k == "SIC":
                try:
                    df[k] = df[k].astype(int)
                except:
                    continue

            dtype_str = self.vars_df.loc["predicateType", k]
            if dtype_str == "string":
                # nothing to do
                continue

            if isinstance(dtype_str, float):
                # NaN -- nothing to do
                continue

            try:
                df[k] = df[k].astype(dtype_str)
            except TypeError:
                # couldn't do conversion -- probably a None somewhere
                # we will skip it for now and let the user worry about it
                continue

        return df

    def _variables_file_name(self):
        name = self.dataset.replace("/", "_")
        return os.path.join(DATA_DIR, f"{name}.json")

    def _get_variables_file(self):
        fn = self._variables_file_name()
        if os.path.isfile(fn):
            with open(fn, "r") as f:
                raw = json.load(f)
        else:
            r = self.sess.get(self.meta["c_variablesLink"].iloc[0])
            raw = r.json()
            with open(fn, "w") as f:
                f.write(json.dumps(r.json()))

        df = pd.DataFrame(raw["variables"])
        if "required" in df.columns:
            df.loc["required"] = df.loc["required"].fillna("False")
        return df

    # Validation
    def validate_vars(self, variables):
        for var in variables:
            if var.upper() not in self.vars_df.columns:
                varstring = textwrap.wrap(", ".join(self.vars_df.columns))
                m = f"\nInvalid variable {var} requested. "
                m += "Possilble choices are:\n"
                m += textwrap.indent("\n".join(varstring), "    ")
                raise ValueError(m)


class CountyBusinessPatterns(CensusData):

    def __init__(self, year, url=DEFAULT_API_URL, key=None):
        super(CountyBusinessPatterns, self).__init__(url, key)
        self.year = year
        self.dataset = f"{year}/cbp"

        meta = _DATA[
            (_DATA["c_dataset"] == "cbp") &
            (_DATA["temporal"] == f"{self.year}/{self.year}")
        ]

        if meta.shape[0] == 0:
            years = _DATA[
                _DATA["c_dataset"] == "cbp"
            ]["temporal"].str.split("/").str.get(0).astype(int)
            min_year = years.min()
            max_year = years.max()
            m = f"Invalid year {year}. Must be in range {min_year}-{max_year}"
            raise ValueError(m)

        self.meta = meta
        self.vars_df = self._get_variables_file()


class ZipBusinessPatterns(CensusData):

    def __init__(self, year, url=DEFAULT_API_URL, key=None):
        super(ZipBusinessPatterns, self).__init__(url, key)
        self.year = year
        self.dataset = f"{year}/zbp"

        meta = _DATA[
            (_DATA["c_dataset"] == "zbp") &
            (_DATA["temporal"] == f"{self.year}/{self.year}")
        ]

        if meta.shape[0] == 0:
            years = _DATA[
                _DATA["c_dataset"] == "zbp"
            ]["temporal"].str.split("/").str.get(0).astype(int)
            min_year = years.min()
            max_year = years.max()
            m = f"Invalid year {year}. Must be in range {min_year}-{max_year}"
            raise ValueError(m)

        self.meta = meta
        self.vars_df = self._get_variables_file()

    def _geography_query(self, kwargs):
        """
        Extract zipcode and state from kwargs and build appropriate geography
        query
        """
        out = ""
        zipcode = _make_list(kwargs.pop("zipcode", []))
        state = _make_list(kwargs.pop("state", []))

        if len(zipcode) == 0:
            if len(state) == 0:
                m = "Both state and zipcode were empty. "
                m += "Some geography must be given"
                raise ValueError(m)

            # state is not empty
            out += "&for=" + geo_predicate_string("zipcode", "*")
            out += "&in=" + geo_predicate_string("state", state)
            return out

        # zipcode is not empty
        out += "&for=" + geo_predicate_string("zipcode", zipcode)

        if len(state) > 0:
            # also have in clause for states
            out += "&in=" + geo_predicate_string("state", state)

        return out

if __name__ == '__main__':
    cbp = CountyBusinessPatterns(2010)
