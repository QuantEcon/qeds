import os

import pandas as pd
import requests
import warnings

from ..config import options, setup_logger

from .util import SOCRATA_STATUS_CODE_REASONS

LOGGER = setup_logger(__name__)


class SocrataData(object):

    _socrata_datasources = {
            "NYCOpenData": "https://data.cityofnewyork.us"
            }

    def __init__(self, dataset, datasource, key=None):
        """
        Socrata Open Data: https://dev.socrata.com/

        Parameters
        ----------
        dataset : string
            TODO

        datasource : string
            TODO

        key : string, optional
            The API registrationKey to be used when requesting data.
            There are three possibilities for determining which api key is
            used:

            1. User argument: if the argument supplied here is a valid
               Socrata app token, then that value will be used
            2. Environment variable: if step 1 fails, we will attempt to use
               the value of the environment variable {key_env_name}.
            3. Valorum conf: if that fails, we will attempt to look up the
               appropriate value in the Valorum configuration file

            If all three of those fail then we will revert to making public
            requests which may be throttled and thus be slower.

            If either step 1 or step 2 succeeds, we will store the api key
            in the valorumm conf file under `socrata.api_key`. This means you
            should only need to supply a key once per machine.
        """.format(key_env_name=options["socrata.environment_variable"])
        # Check whether it is a valid datasource
        if datasource not in self._socrata_datasources.keys():
            msg = "Dataset not found in list of Socrata datasets"
            msg += "\n\nIt either (1) does not exist, "
            msg += "(2) is not implemented, or (3) you have made a typo"
            raise ValueError(msg)

        # Check whether it is valid dataset
        if len(dataset) != 9:
            raise ValueError("Dataset must be of form XXXX-ZZZZ")

        # Find key
        update_config = True
        if key is None:
            KEY_ENV_NAME = options["socrata.environment_variable"]
            if KEY_ENV_NAME in os.environ:
                key = os.environ[KEY_ENV_NAME]
            elif options["socrata.api_key"] is not None:
                key = options["socrata.api_key"]
                update_config = False
            else:
                url = "https://dev.socrata.com/register"
                msg = "\nSocrata API key not detected"
                msg += " please obtain one from {}".format(url)
                msg += " and call `valorum.options['socrata.api_key']=key`"
                msg += "\nFor now we will use no key. Socrata might limit"
                msg += " our usage."
                warnings.warn(msg)

        # If we don't already have they key then save it
        if update_config:
            LOGGER.debug("Saving socrata API key")
            options["socrata.api_key"] = key

        # Get information ready for requests
        self.dataset = dataset
        self.datasource = datasource
        self.key = key
        self.base_url = self._socrata_datasources[datasource]
        self.headers = {"X-APP-TOKEN": key} if key is not None else {}

    def get(self, SoQL={}, limit=None):
        """
        Get self.dataset from self.datasource and convert to a
        pandas DataFrame

        Parameters
        ----------
        SoQL: Dict
            A dictionary which contains the filters and other restrictions
            that you'd like to place on the data as it is brought into
            the DataFrame https://dev.socrata.com/docs/queries/

        Returns
        -------
        df : pandas.DataFrame
            A pandas DataFrame contianing the requested series

        """
        # Build request that we will make
        req_url = self.base_url + "/resource/{}.json".format(self.dataset)

        # If we don't give it a limit, try and select all rows
        if limit is None:
            # Count how many rows there are using the `count(*)` option
            lim_params = SoQL.copy()
            lim_params.update({"$select": "count(*)"})

            # Make request and figure out limit
            LOGGER.debug("Requesting data from {} with params {}".format(
                req_url, lim_params
            ))
            req_count = requests.get(
                req_url, headers=self.headers, params=lim_params
            )
            limit = int(req_count.json()[0]["count"])

        # Add limit to params and request data
        SoQL["$limit"] = limit
        mystr = "Requesting data from {} with params {}"
        LOGGER.debug(mystr.format(req_url, SoQL))
        records = requests.get(req_url, headers=self.headers, params=SoQL)

        # Raise error if not success
        if records.status_code not in [200]:
            raise ValueError(SOCRATA_STATUS_CODE_REASONS[records.status_code])

        # Construct data
        df = pd.DataFrame.from_records(records.json())

        return df
