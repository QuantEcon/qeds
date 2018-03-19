import datetime
import os

import pandas as pd
import requests
from requests.adapters import HTTPAdapter

from ..config import options, setup_logger
from ..util import _make_list, QueryError, iter_chunks

from .util import LIMITS, BLS_STATUS_CODE_REASONS

LOGGER = setup_logger(__name__)


class BLSData(object):
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
            url=options["bls.api_url"],
            key_env_name=options["bls.environment_variable"]
        )

        update_config = True
        if key is None:
            KEY_ENV_NAME = options["bls.environment_variable"]
            if KEY_ENV_NAME in os.environ:
                key = os.environ[KEY_ENV_NAME]
            elif options["bls.api_key"] is not None:
                key = options["bls.api_key"]
                update_config = False
            else:
                url = "https://data.bls.gov/registrationEngine/"
                msg = f"BLS API key not detected. Please make one at {url}"
                msg += " and call `valorum.options['bls.api_key']=key`"
                raise EnvironmentError(msg)

        if update_config:
            options["bls.api_key"] = key

        if url is None:
            url = options["bls.api_url"]

        self.key = key
        self.url = url
        self.headers = {"Content-Type": "application/json"}

        self.sess = requests.Session()
        self.sess.mount(self.url, HTTPAdapter(max_retries=3))

    def get(self, series, startyear=None, endyear=None, nice_names=True,
            wide=False):
        """
        Get requested ``series`` from ``startyear`` to ``endyear`` as a
        pandas DataFrame

        Parameters
        ----------
        series : string or list(string)
            A valid BLS series name, or list of series names

        startyear: int, optional(default=endyear - 19)
            The starting year for which to obtain data. The default is 19
            years before the endyear, so 20 years of data are obtained

        endyear: int, optional(default=current_year)
            The ending year for data lookup. The default is the current year

        nice_names: bool, optional(default=True)
            Fill the `variable` column of the output with the series title
            instead of the series id. For example, if you request series
            ``LASST040000000000006``, and pass ``nice_names=True``, then the
            corresponding entry in the ``variable`` column will be
            ``Labor Force: Arizona (S)`` instead of the series id.

        wide: bool, optional(default=False)
            Toggles the return of a wide DataFrame with the index being the
            date and one variable per column

        Returns
        -------
        df : pandas.DataFrame
            A pandas DataFrame contianing the requested series

        """

        series = _make_list(series)
        nyear = LIMITS["years_per_query"]
        nseries = LIMITS["series_per_query"]

        if endyear is None:
            endyear = datetime.datetime.now().year
        if startyear is None:
            startyear = endyear - (nyear - 1)

        # Chunk on years if user asked for more than 20 years
        if endyear - startyear > (nyear - 1):
            to_cat = []
            years = range(startyear, endyear + 1)
            for year_chunks in iter_chunks(years, nyear):
                df = self.get(
                    series, year_chunks[0], year_chunks[-1], nice_names, wide
                )
                to_cat.append(df)

            return pd.concat(to_cat, ignore_index=True)

        # Chunk on series if user asked for more than 50 series
        if len(series) > nseries:
            to_cat = []
            for series_chunk in iter_chunks(series, nseries):
                df = self.get(
                    series_chunk, startyear, endyear, nice_names, wide
                )
                to_cat.append(df)

            return pd.concat(to_cat, ignore_index=True)

        body = {
            "startyear": startyear,
            "endyear": endyear,
            "seriesid": series,
            "registrationKey": self.key,
            "catalog": True if nice_names else False,
        }
        res = self.sess.post(self.url, json=body)

        if res.status_code == 200:
            data = res.json()
        elif res.status_code == 202:
            # 202 means the bls servers are still processing...
            # we'll try to read it anyway, even though there will probably
            # be errors later
            data = res.json()
        elif res.status_code in BLS_STATUS_CODE_REASONS:
            msg = f"Request failed with code {res.status_code} and message "
            msg += BLS_STATUS_CODE_REASONS(res.status_code)
            raise QueryError(msg, res)
        else:
            msg = f"Request failed unexpectedly with code {res.status_code}"
            raise QueryError(msg, res)

        # at this point we should have data

        dfs = []
        for series in data["Results"]["series"]:
            df = pd.DataFrame(
                series["data"],
                columns=["value", "year", "period"]
            )
            if df.shape[0] == 0:
                LOGGER.debug("Query was empty for " + series['seriesID'])
                continue

            # see if quarterly, monthly, or annual
            freq = series["data"][0]["period"][0]
            if freq == "M":
                df["Date"] = pd.to_datetime(
                    df["year"] + df["period"], format="%YM%m"
                )
            elif freq == "A":
                df["Date"] = pd.to_datetime(df["year"], format="%Y")
            elif freq == "Q":
                df["Date"] = pd.to_datetime(df["year"] + df["period"].str[2])
            else:
                msg = f"Unknown frequency {freq}. Please open an issue"
                raise ValueError(msg)

            df.drop(["year", "period"], axis=1, inplace=True)

            if nice_names:
                if "series_title" in series.get("catalog", []):
                    df["variable"] = series["catalog"]["series_title"]
            else:
                df["variable"] = series["seriesID"]

            try:
                df["value"] = df["value"].astype(float)
            except ValueError:
                pass

            dfs.append(df)

        df = pd.concat(dfs, ignore_index=True)

        if wide:
            return df.set_index(["Date", "variable"]).unstack()["value"]
        else:
            return df
