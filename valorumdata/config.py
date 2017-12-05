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

# Create configuration
vconf = configparser.ConfigParser()
if os.path.exists(_cfg_file):
    vconf.read('.valorumdata.cfg')
else:
    vconf["PATHS"] = {
        "data": base_path.joinpath("data"),
        "config": _cfg_file
        }

    with open(_cfg_file, "w") as config_file:
        vconf.write(config_file)

