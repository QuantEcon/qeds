qeds
====

This package provides a simplified interface to datasets that we use
frequently.

Loading data
------------

To see a list of available datasets run

.. code:: python

    import qeds
    qeds.data.available()

To load one of the listed datasets run

.. code:: python

    df = qeds.data.load("dataset_name")

where ``dataset_name`` is replaced by one of the names returned by
``qeds.data.available()``.

When you first load a dataset, qeds will fetch the data from
somewhere online. It will then save a local copy of the data to your
hard drive. Subsequent requests to load a dataset (even in different
python sessions) will first attempt to load the data from your hard
drive and only fetch from online if necessary.

Configuration
-------------

The qeds library is configurable. Below is a listing of available
configuration options.

To see a list of valid configuration options run

.. code:: python

    import qeds
    qeds.data.config.describe_options()

To set a configuration use
``valourm.data.options[section.option] = value``.

For example, to set the configuration option for the BLS api_key I would
call:

.. code:: python

    import qeds
    qeds.data.options["bls.api_key"] = "MY_API_KEY"

Developer docs
--------------

Contributing datasets
~~~~~~~~~~~~~~~~~~~~~

To contribute a dataset you need to implement a function
``_retrieve_{name}`` inside the file ``data/retrieve.py``. This function
is responsible for obtaining the data either “by hand” (data hard coded
into the function) or from online. The function must return a pandas
DataFrame with the data.
