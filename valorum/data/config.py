"""
This file reads in a configuration file if one already exists and
if one does not exist then it creates one

"""
import configparser
import os
import pathlib
import logging

# Get home directory and config file
_home = pathlib.Path.home()
BASE_PATH = _home.joinpath(".valorum")
CFG_FILE = BASE_PATH.joinpath("config.ini")
BASE_DATA_DIR = BASE_PATH.joinpath("data")

# Create configuration  TODO: Need better way to do this checking.. Not "safe"
vconf = configparser.ConfigParser()


def write_config():
    with open(CFG_FILE, "w") as config_file:
        vconf.write(config_file)


if os.path.exists(CFG_FILE) and os.path.exists(BASE_DATA_DIR):
    vconf.read(CFG_FILE)
else:
    os.mkdir(BASE_PATH)
    os.mkdir(BASE_DATA_DIR)
    vconf["PATHS"] = {
        "data": BASE_DATA_DIR,
        "config": CFG_FILE
    }
    vconf["options"] = {
        "file_format": "pkl"
    }

    write_config()


# --------------------- #
# logging configuration #
# --------------------- #

level = vconf.get("options", "log_level", fallback=50)
logging.basicConfig(
    format='%(levelname)s.%(name)s %(asctime)s: %(message)s',
    level=level
)


def setup_logger(module):
    log = logging.getLogger(module)
    log.setLevel(level)
    return log


# ------- #
# options #
# ------- #

EXTENSION = vconf.get("options", "file_format", fallback="pkl")
if EXTENSION not in ["csv", "feather", "pkl"]:
    m = "only accept extensions csv, feather, pkl\n"
    m += f"found {EXTENSION}. Defaulting to pkl"
    EXTENSION = "pkl"
    logging.warning(m)
