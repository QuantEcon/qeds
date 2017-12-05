"""
This file provides the `data_read` function which reads data
from a particular folder on the computer
"""
import os
import pandas as pd
from .config import vconfig

base_path = vconfig["PATH"]["data"]


def data_read(name, kwargs):
    # Create the file name that corresponds to where this file
    # should be stored
    fn = base_path.joinpath(name)

    # Check whether the file exists
    if os.path.exists(fn):
        # If it exists, read it in directly
        df = pd.read_csv(fn, **kwargs)

    elif name in our_datasets:
        # Create the data
        df = data_retrieve(name)

    else:
        msg = "The dataset name that you gave is not on your computer \n"
        msg += "and can not be retrieved by our library. Are you sure \n"
        msg += "you typed it correctly?"
        raise ValueError(msg)

    return df

