"""
This file provides the `data_read` function which reads data
from a particular folder on the computer
"""
import os
import pandas as pd
from .config import options, setup_logger

LOGGER = setup_logger(__name__)


def load(name, kwargs={}):
    # Create the file name that corresponds to where this file
    # should be stored
    EXTENSION = options["options.file_format"]
    fn = os.path.join(options["PATHS.data"], name) + "." + EXTENSION

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
    from .retrievers import __dict__ as retrievers

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
    EXTENSION = options["options.file_format"]
    fn = os.path.join(options["PATHS.data"], name + "." + EXTENSION)

    # Check whether the folder exists and if not create it
    if not os.path.exists(options["PATHS.data"]):
        os.makedirs(options["PATHS.data"])

    # Save data into folder
    if EXTENSION == "csv":
        df.to_csv(fn, **kwargs)
    elif EXTENSION == "pkl":
        df.to_pickle(fn, **kwargs)
    elif EXTENSION == "feather":
        df.to_feather(fn, **kwargs)

    return df


def available(name=None):
    """
    Return a list of available datasets

    Parameters
    ----------
    name : string (optional)
        A string used to filter datasets. Datasets that include ``name``
        in the name of the dataset are kept. If nothing is given for this
        argument, no filtering is done

    Returns
    -------
    datasets : list(string)
        A list of available
    """

    from .retrievers import __dict__ as retrievers

    skip = len("_retrieve_")
    out = (k[skip:] for k in retrievers.keys() if k.startswith("_retrieve_"))

    if name is None:
        return list(out)

    return list(k for k in out if name in k)
