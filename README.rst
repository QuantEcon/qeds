Valorum
=======

This package provides a simplified interface to datasets that we use
frequently.

As of now (1-1-18) this package is not registered on pypy. To install
and use we recommend using the following steps from the command line:

1. Clone or download this repository
2. Change directory into the cloned repo
3. Call ``pip install -e .``, where you can change the python the
   package is installed into by providing the full path to the pip
   executable

Loading data
------------

To see a list of available datasets run

.. code:: python

    import valorum
    valorum.data.available()

To load one of the listed datasets run

.. code:: python

    df = valorum.data.load("dataset_name")

where ``dataset_name`` is replaced by one of the names returned by
``valorum.data.available()``.

When you first load a dataset, valorum will fetch the data from
somewhere online. It will then save a local copy of the data to your
hard drive. Subsequent requests to load a dataset (even in different
python sessions) will first attempt to load the data from your hard
drive and only fetch from online if necessary.

Configuration
-------------

The valorum library is configurable. Below is a listing of available
configuration options.

To see a list of valid configuration options run

.. code:: python

    import valorum
    valorum.data.config.describe_options()

To set a configuration use
``valourm.data.options[section.option] = value``.

For example, to set the configuration option for the BLS api_key I would
call:

.. code:: python

    import valorum
    valorum.data.options["bls.api_key"] = "MY_API_KEY"

Developer docs
--------------

Contributing datasets
~~~~~~~~~~~~~~~~~~~~~

To contribute a dataset you need to implement a function
``_retrieve_{name}`` inside the file ``data/retrieve.py``. This function
is responsible for obtaining the data either “by hand” (data hard coded
into the function) or from online. The function must return a pandas
DataFrame with the data.
