"""
This file provides the `data_read` function which reads data
from a particular folder on the computer
"""
import os
import pandas as pd
from .config import vconf, setup_logger, EXTENSION

BASE_PATH = vconf["PATHS"]["data"]
LOGGER = setup_logger(__name__)


def load(name, kwargs={}):
    # Create the file name that corresponds to where this file
    # should be stored
    fn = os.path.join(BASE_PATH, name) + "." + EXTENSION

    # Check whether the file exists
    if os.path.exists(fn):
        LOGGER.debug(f"Loading data from {fn}")
        # If it exists, read it in directly
        if EXTENSION == "csv":
            return pd.read_csv(fn, **kwargs)
        elif EXTENSION == "pkl":
            return pd.read_pickle(fn, **kwargs)
        elif EXTENSION == "feather":
            return pd.read_feather(fn, **kwargs)
    else:
        return retrieve(name)
    

def retrieve(name, kwargs={}):
    """
    Retrieves a dataset according to the instructions maintained in
    another function `_data_retrieve_{name}` and saves it to your
    computer

    Parameters
    ----------
    name : string
        The name of the dataset that you want to retrieve from online. It
        is saved at "$VALORUM/data/name.{file_ending}"

    Returns
    -------
    None

    """
    from .retrieve import __dict__ as retrievers

    func_name = "_retrieve_{}".format(name)
    func = retrievers.get(func_name, None)
    if func is None:
        msg = "The dataset name that you gave ({}) is not on your computer \n"
        msg += "and can not be retrieved by our library. Are you sure \n"
        msg += "you typed it correctly?"
        raise ValueError(msg.format(name))

    # Call retrieval function
    df = func()

    # Save file
    fn = os.path.join(BASE_PATH, name+"."+EXTENSION)
    if EXTENSION == "csv":
        df.to_csv(fn, **kwargs)
    elif EXTENSION == "pkl":
        df.to_pickle(fn, **kwargs)
    elif EXTENSION == "feather":
        df.to_feather(fn, **kwargs)

    return df
