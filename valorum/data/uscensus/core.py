import json
import os
import textwrap

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from ..config import options
from ..util import _make_list, QueryError


def _update_data_file():
    url = "https://api.census.gov/data.json"
    r = requests.get(url)
    file_path = os.path.join(options["uscensus.data_dir"], "data.json")
    with open(file_path, "w") as f:
        f.write(json.dumps(r.json()))


def _load_metadata():
    data_fn = os.path.join(options["uscensus.data_dir"], "data.json")
    if not os.path.isfile(data_fn):
        _update_data_file()

    with open(data_fn, "r") as f:
        _DATA_RAW = json.load(f)

    _DATA = pd.DataFrame(_DATA_RAW["dataset"])
    _DATA["c_dataset"] = _DATA["c_dataset"].apply(lambda x: "/".join(x))
    return _DATA_RAW, _DATA


_DATA_RAW, _DATA = _load_metadata()


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


class CensusData(object):
    def __init__(self, url=None, key=None):
        """
        Parameters
        ----------
        url : string, optional(default={url})
            The API url to be used when requesting data from the BLS

        key : string, optional
            The API registrationKey to be used when requesting data.
            There are three possibilities for determining which api key is
            used:

            1. User argument: if the argument supplied here is a valid
               BLS registration key, then that value will be used
            2. Environment variable: if step 1 fails, we will attempt to use
               the value of the environment variable {key_env_name}.
            3. Valorum conf: if that fails, we will attempt to look up the
               value in section `bls.api_key` if your valorum conf file

            If all three of those fail, we throw an error whose message
            contains instructions for how to obtain a registration key.

            If either step 2 or step 2 succeeds, we will store the api key
            in the valorumm conf fil under `bls.api_key`. This means you
            should only need to supply a key once per machine.
        """.format(
            url=options["uscensus.api_url"],
            key_env_name=options["uscensus.environment_variable"]
        )
        update_config = True
        if key is None:
            KEY_ENV_NAME = options["uscensus.environment_variable"]
            if KEY_ENV_NAME in os.environ:
                key = os.environ[KEY_ENV_NAME]
            elif options["uscensus.api_key"] is not None:
                key = options["uscensus.api_key"]
                update_config = False
            else:
                raise EnvironmentError("Census API key not detected")

        if update_config:
            options["uscensus.api_key"] = key

        if url is None:
            url = options["uscensus.api_url"]

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
        except:  # NOQA
            if "SIC" in kwargs or "SIC" in variables:
                try:
                    df = pd.read_json(r.content.replace(b"\\", b""))
                    df.columns = df.iloc[0, :].tolist()
                    df.drop(0, axis=0, inplace=True)
                except:  # NOQA
                    msg = "Couldn't parse query result into DataFrame."
                    raise QueryError(msg, r)
            else:
                msg = f"Query failed with status code {r.status_code}. "
                msg += f"Response from server was\n{r.content}"
                raise QueryError(msg, r)

        key = ("metropolitan statistical area/"
               "micropolitan statistical area")
        df.rename(
            columns={key: "MSA"},
            inplace=True
        )

        for k in df.columns:
            if k in ["state", "county", "us", "MSA", "zipcode"]:
                df[k] = df[k].astype(int)
                continue

            if k == "SIC":
                try:
                    df[k] = df[k].astype(int)
                except ValueError:
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
        return os.path.join(options["uscensus.data_dir"], f"{name}.json")

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

    def __init__(self, year, url=None, key=None):
        super(CountyBusinessPatterns, self).__init__(url, key)
        self.year = year
        self.dataset = f"{year}/cbp"

        meta = _DATA[
            (_DATA["c_dataset"] == "cbp") &
            (_DATA["temporal"] == f"{self.year}/{self.year}")
        ]

        if meta.shape[0] == 0:
            years = (
                _DATA[_DATA["c_dataset"] == "cbp"]
                ["temporal"]
                .str.split("/")
                .str.get(0)
                .astype(int)
            )
            min_year = years.min()
            max_year = years.max()
            m = f"Invalid year {year}. Must be in range {min_year}-{max_year}"
            raise ValueError(m)

        self.meta = meta
        self.vars_df = self._get_variables_file()


class ZipBusinessPatterns(CensusData):

    def __init__(self, year, url=None, key=None):
        super(ZipBusinessPatterns, self).__init__(url, key)
        self.year = year
        self.dataset = f"{year}/zbp"

        meta = _DATA[
            (_DATA["c_dataset"] == "zbp") &
            (_DATA["temporal"] == f"{self.year}/{self.year}")
            ]

        if meta.shape[0] == 0:
            years = (
                _DATA[_DATA["c_dataset"] == "zbp"]
                ["temporal"]
                .str.split("/")
                .str.get(0)
                .astype(int)
            )
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
