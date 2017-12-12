"""
This file provides the `data_read` function which reads data
from a particular folder on the computer
"""
import os
import pandas as pd
from .config import vconf, our_datasets, setup_logger, EXTENSION
from .retrieve import data_retrieve

BASE_PATH = vconf["PATHS"]["data"]
LOGGER = setup_logger(__name__)


def data_read(name, kwargs={}):
    # Create the file name that corresponds to where this file
    # should be stored
    fn = os.path.join(BASE_PATH, name) + "." + EXTENSION

    # Check whether the file exists
    if os.path.exists(fn):
        LOGGER.debug(f"Loading data from {fn}")
        # If it exists, read it in directly
        if EXTENSION == "csv":
            df = pd.read_csv(fn, **kwargs)
        elif EXTENSION == "pkl":
            df = pd.read_pickle(fn, **kwargs)
        elif EXTENSION == "feather":
            df = pd.read_feather(fn, **kwargs)

    elif name in our_datasets:
        # Create the data
        LOGGER.debug(f"Attempting to retrieve the data")
        df = data_retrieve(name, **kwargs)

    else:
        msg = "The dataset name that you gave is not on your computer \n"
        msg += "and can not be retrieved by our library. Are you sure \n"
        msg += "you typed it correctly?"
        raise ValueError(msg)

    return df
