"""
This file reads in a configuration file if one already exists and
if one does not exist then it creates one

"""
import configparser
import os
import pathlib


# Get home directory and config file
_home = pathlib.Path.home()
base_path = _home.joinpath(".valorum")
_cfg_file = base_path.joinpath("config.ini")
_data_path = base_path.joinpath("data")

# List of all of our datasets
our_datasets = ["test"]

# Create configuration  TODO: Need better way to do this checking.. Not "safe"
vconf = configparser.ConfigParser()
if os.path.exists(_cfg_file) and os.path.exists(_data_path):
    vconf.read(_cfg_file)
else:
    os.mkdir(base_path)
    os.mkdir(_data_path)
    vconf["PATHS"] = {
        "data": _data_path,
        "config": _cfg_file
        }

    with open(_cfg_file, "w") as config_file:
        vconf.write(config_file)
