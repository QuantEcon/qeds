"""
This file provides the `data_read` function which reads data
from a particular folder on the computer
"""
import json
import os
import pandas as pd
from .config import options, setup_logger
from .util import _ensure_dir

LOGGER = setup_logger(__name__)

_ensure_dir(options["PATHS.data"])

_METADATA_FN = os.path.join(options["PATHS.data"], "metadata.json")
if not os.path.isfile(_METADATA_FN):
    with open(_METADATA_FN, "w") as f:
        json.dump(dict(), f)


def _update_metadata(name, metadata):
    with open(_METADATA_FN, "r") as f:
        current = json.load(f)

    current[name] = metadata
    with open(_METADATA_FN, "w") as f:
        json.dump(current, f)

    return current


def _get_metadata(name):
    with open(_METADATA_FN, "r") as f:
        current = json.load(f)

    return current.get(name, dict())

def _remove_old_index(df):
    if "Unnamed: 0" in df.columns:
        df.drop("Unnamed: 0", axis=1, inplace=True)

    return df


def load(name, kwargs={}):
    # Create the file name that corresponds to where this file
    # should be stored
    EXTENSION = options["options.file_format"]
    fn = os.path.join(options["PATHS.data"], name) + "." + EXTENSION

    def _update_using_meta(df):
        meta = _get_metadata(name)
        for col in meta.get("parse_dates", []):
            df[col] = pd.to_datetime(df[col])
        if len(meta.get("index", dict())) > 0:
            if EXTENSION in ["csv", "feather"]:
                df.set_index(meta["index"], inplace=True)

        return df

    # Check whether the file exists
    if os.path.exists(fn):
        LOGGER.debug("Loading data from {}".format(fn))
        # If it exists, read it in directly
        if EXTENSION == "csv":
            out = _update_using_meta(pd.read_csv(fn, **kwargs))
        elif EXTENSION == "pkl":
            out = _update_using_meta(pd.read_pickle(fn, **kwargs))
        elif EXTENSION == "feather":
            out = _update_using_meta(pd.read_feather(fn, **kwargs))

        else:
            raise ValueError("Unknown extension type {}".format(EXTENSION))

        return _remove_old_index(out)
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
        is saved at "$qeds/data/name.{file_ending}"

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
    df, metadata = func()
    _update_metadata(name, metadata)

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
        df.reset_index().to_feather(fn, **kwargs)

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
