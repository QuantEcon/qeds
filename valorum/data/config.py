"""
This file reads in a configuration file if one already exists and
if one does not exist then it creates one
"""
import configparser
import os
import pathlib
import logging
import warnings

# Get home directory and config file
_home = str(pathlib.Path.home())
_BASE_PATH = os.path.join(_home, ".valorum")
CFG_FILE = os.path.join(_BASE_PATH, "config.ini")
BASE_DATA_DIR = os.path.join(_BASE_PATH, "data")

if not os.path.isdir(_BASE_PATH):
    os.mkdir(_BASE_PATH)


class Option:
    __slots__ = ["name", "default", "doc", "validator"]

    def __init__(self, name, default, doc, validator):
        self.name = name
        self.default = default
        self.doc = doc
        self.validator = validator

    def __str__(self):
        info = dict(name=self.name, default=self.default, doc=self.doc)
        if self.default is not None:
            msg = "  - {name} (default={default}) : {doc}"
        else:
            msg = "  - {name} : {doc}"

        return msg.format(**info)

    def __repr__(self):
        return self.__str__()


def _no_validation(x):
    pass


def _member_validation(allowed):
    def func(val):
        if val not in allowed:
            msg = "Value {} not allowed. Acceptable values are {}"
            raise configparser.Error(msg)

    return func


# dict holding all config options. Maps from vconf section name to a list of
# options
_valid_options = {
    "PATHS": [
        Option(
            "base",
            str(_BASE_PATH),
            "Default directory for all things valorum",
            _no_validation
        ),
        Option(
            "data",
            str(BASE_DATA_DIR),
            "Default directory for saving loaded data",
            _no_validation
        ),
    ],
    "options": [
        Option(
            "file_format",
            "pkl",
            "File format for saving loaded data",
            _member_validation(["pkl", "csv", "feather"])
        ),
        Option(
            "log_level",
            "CRITICAL",
            "Default level for filtering logging messages",
            _member_validation([
                "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"
            ])
        )
    ],
    "uscensus": [
        Option(
            "api_key",
            None,
            """API key for accessing data from US Census Bureau\
            API. Obtain one at https://api.census.gov/data/key_signup.html""",
            _no_validation
        ),
        Option(
            "data_dir",
            os.path.join(_BASE_PATH, "uscensus", "data"),
            "Directory to store the supplementary files for uscensus api",
            _no_validation
        ),
        Option(
            "environment_variable",
            "USCENSUS_API_KEY",
            "Environment variable to search for api_key for US Census Bureau",
            _no_validation
        ),
        Option(
            "api_url",
            "https://api.census.gov/data/",
            "URL through which to access the US Census Bureau API",
            _no_validation
        )
    ],
    "bls": [
        Option(
            "api_key",
            None,
            """API key for accessing data from US Bureau of Labor Statistics\
            API. Obtain one at https://data.bls.gov/registrationEngine/""",
            _no_validation
        ),
        Option(
            "environment_variable",
            "BLS_API_KEY",
            "Environment variable to search for api_key for BLS",
            _no_validation
        ),
        Option(
            "api_url",
            "https://api.bls.gov/publicAPI/v2/timeseries/data/",
            "URL through which to access the BLS API",
            _no_validation
        )
    ],
    "socrata": [
        Option(
            "api_key",
            None,
            """API key for accessing data from the Socrata API. Obtain one at\
            https://dev.socrata.com/register/""",
            _no_validation
        ),
        Option(
            "environment_variable",
            "SOCRATA_API_KEY",
            "Environment variable to search for api_key for Socrata",
            _no_validation
        ),
    ]
}


def _get_option(section, name, warn=False):
    if section not in _valid_options:
        msg = "Unknown config section {}. Valid sections are {}"
        valid = list(_valid_options.keys())
        m = msg.format(section, valid)
        if warn:
            warnings.warn(m)
            return
        raise ValueError(m)

    options = _valid_options[section]

    if name not in [o.name for o in options]:
        msg = "Unknown option {}. Known options are {}"
        valid = [o.name for o in options]
        m = msg.format(section, valid)
        if warn:
            warnings.warn(m)
            return
        raise ValueError(m)

    _opt = None
    for o in options:
        if o.name == name:
            _opt = o
            break

    if _opt is None:
        m = "Not sure how I got here... file a bug report."
        if warn:
            warnings.warn(m)
            return
        raise ValueError(m)

    return _opt


def _validate_config_setting(section, name, value):
    option = _get_option(section, name)
    option.validator(value)


# -------------- #
# Convenient API #
# -------------- #

class _DictOptions(object):
    def __init__(self):
        self.vconf = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        if os.path.exists(CFG_FILE):
            self.vconf.read(CFG_FILE)

        # add defaults to config
        for (sec, opts) in _valid_options.items():
            if not self.vconf.has_section(sec):
                self.vconf.add_section(sec)

            for o in opts:
                if self.vconf.has_option(sec, o.name):
                    continue
                # vconf doesn't have option, write one if we have a default
                if o.default is not None:
                    self.vconf.set(sec, o.name, o.default)

        # save updated config
        self.write_config()

    def validate_config(self, warn=True):
        """
        Validate all settings in the config

        Parameters
        ----------
        warn : bool, optional(default=True)
            Indicator for whether the function should warn or raise errors
            when an invalid config value is found. Default is warn
        """
        for (section, options) in self.vconf.items():
            if section == "DEFAULT":
                continue
            if section not in _valid_options:
                warnings.warn("Unknown section {}".format(section))

            for (name, value) in options.items():
                _opt = _get_option(section, name, warn)
                if _opt is not None:
                    _opt.validator(value)

    def write_config(self):
        with open(CFG_FILE, "w") as config_file:
            self.vconf.write(config_file)

    def set_config(self, section, name, value, write=True):
        """
        Set a configuration value and (optionally) save to config file

        Parameters
        ----------
        section : str
            The section name for the config option

        name : str
            The name of the config value to set in under the section

        value : any
            The value to be associated with the name

        write : bool, optional(default=True)
            Bool indicating if the config file should be written to disk after
            updating the value
        """
        _validate_config_setting(section, name, value)
        self.vconf.set(section, name, value)

        if write:
            self.write_config()

    def _get_sec_opt(self, key):
        parts = key.split(".")
        if len(parts) != 2:
            raise ValueError("key must have form SECTION.option")

        return parts

    def __setitem__(self, key, val):
        section, name = self._get_sec_opt(key)
        if val is not None:
            self.set_config(section, name, val)

    def __getitem__(self, key, default=None):
        section, name = self._get_sec_opt(key)
        if self.vconf.has_option(section, name):
            return self.vconf.get(section, name)

        if default is not None:
            return default

        return _get_option(section, name).default


options = _DictOptions()


def describe_options():
    msg = "Valorum configuration options are:\n\n"
    for (sec, options) in _valid_options.items():
        msg += sec + "\n"
        for o in options:
            msg += str(o) + "\n"

        msg += "\n"

    print(msg)


# --------------------- #
# logging configuration #
# --------------------- #

def setup_logger(module):
    log = logging.getLogger(module)
    log.setLevel(options["options.log_level"])
    return log
