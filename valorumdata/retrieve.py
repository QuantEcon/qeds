"""
This file is used to retrieve various datasets.

The main function is `data_retrieve` which calls `_data_retrieve_name`
to go retrieve the data from online.
"""
import pandas as pd
from .config import vconfig


base_path = vconfig["PATH"]["data"]


def data_retrieve(name, kwargs):
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
    # Create the function that will get called to retrieve the data
    retrieve_func = eval("_data_retrieve_{}".format(name))

    # Call retrieval function
    df = retrieve_func()

    # Save file
    fn = base_path.joinpath(name + ".csv")
    df.to_csv(filename, **kwargs)

    return df


def _data_retrieve_test():
    df = pd.DataFrame({"A": [0, 1, 2],
                       "B": [3, 4, 5],
                       "C": [6, 7, 8]})

    return df

