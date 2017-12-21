import os
import pandas as pd
from ..config import BASE_PATH

DEFAULT_API_URL = "https://api.census.gov/data/"
KEY_ENV_NAME = "USCENSUS_API_KEY"
DATA_DIR = os.path.join(BASE_PATH, "uscensus", "data")

cbp_industry_var = {
    1986: "SIC",
    1987: "SIC",
    1988: "SIC",
    1989: "SIC",
    1990: "SIC",
    1991: "SIC",
    1992: "SIC",
    1993: "SIC",
    1994: "SIC",
    1995: "SIC",
    1996: "SIC",
    1997: "SIC",
    1998: "NAICS1997",
    1999: "NAICS1997",
    2000: "NAICS1997",
    2001: "NAICS1997",
    2002: "NAICS1997",
    2003: "NAICS2002",
    2004: "NAICS2002",
    2005: "NAICS2002",
    2006: "NAICS2002",
    2007: "NAICS2002",
    2008: "NAICS2007",
    2009: "NAICS2007",
    2010: "NAICS2007",
    2011: "NAICS2007",
    2012: "NAICS2012",
    2013: "NAICS2012",
    2014: "NAICS2012",
    2015: "NAICS2012"
}


def update_fips_2010():
    url = "https://www2.census.gov/geo/docs/reference"
    url += "/codes/files/national_county.txt"
    df = pd.read_csv(url, header=None)
    df.columns = [
        "State_Name",
        "State",
        "County",
        "County_Name",
        "Class_FIPS"
    ]
    df.set_index(["State", "County"], inplace=True)
    df.index.name = "FIPS"
    df.sort_index(inplace=True)
    df.to_csv(os.path.join(DATA_DIR, "fips2010.csv"))
    return df


def get_fips_2010():
    path = os.path.join(DATA_DIR, "fips2010.csv")
    if os.path.isfile(path):
        return pd.read_csv(path, index_col=[0, 1])

    else:
        return update_fips_2010()


def get_naics2002_to_sics():
    path = os.path.join(DATA_DIR, "naics2002_to_sic.csv")
    if os.path.isfile(path):
        return pd.read_csv(path, index_col=0)
    else:
        return update_naics2002_to_sics()


# stuff to make working with this data bearable
def update_naics2002_to_sics():
    url = "https://www.census.gov/eos/www/naics/"
    url += "concordances/1987_SIC_to_2002_NAICS.xls"
    df = pd.read_excel(url, skip_footer=1)
    df.to_csv(os.path.join(DATA_DIR, "naics2002_to_sic.csv"))
    return df


def naics2002_to_sics(start):
    df = get_naics2002_to_sics()
    subsets = df[df["2002 NAICS"].astype(str).str.startswith(start)]
    return subsets["SIC"].dropna().astype(int).unique()


def update_naics_crosswalk():
    url = "https://www.census.gov/eos/www/naics/concordances"
    url += "/{}_to_{}_NAICS.xlsx"
    df = pd.read_excel(
        url.format(2017, 2012),
        skiprows=2,
        usecols=[0, 2],
        names=["NAICS2017", "NAICS2012"],
    ).merge(pd.read_excel(
        url.format(2012, 2007)[:-1],
        skiprows=2,
        usecols=[0, 2],
        names=["NAICS2012", "NAICS2007"],
    )).merge(pd.read_excel(
        url.format(2007, 2002)[:-1],
        skiprows=2,
        usecols=[0, 2],
        names=["NAICS2007", "NAICS2002"],
    ))
    df.to_csv(os.path.join(DATA_DIR, "naics_crosswalk.csv"))
    return df


def get_naics_crosswalk():
    path = os.path.join(DATA_DIR, "naics_crosswalk.csv")
    if os.path.isfile(path):
        return pd.read_csv(path, index_col=0)
    else:
        return update_naics_crosswalk()


# SIC codes
def update_sic86():
    url = "http://www2.census.gov/programs-surveys/cbp/technical-documentation"
    url += "/records-layouts/sic-code-descriptions/sic86.txt"
    df = pd.read_csv(url, sep="    ")
    df.columns = ["SIC", "NAME"]
    df.to_csv(os.path.join(DATA_DIR, "sic86.csv"))
    return df


def get_sic86():
    path = os.path.join(DATA_DIR, "sic86.csv")
    if os.path.isfile(path):
        return pd.read_csv(path, index_col=0)
    else:
        return update_sic86()


def update_sic87():
    url = "http://www2.census.gov/programs-surveys/cbp/technical-documentation"
    url += "/records-layouts/sic-code-descriptions/sic87.txt"
    df = pd.read_csv(url, sep="    ")
    df.columns = ["SIC", "NAME"]
    df.to_csv(os.path.join(DATA_DIR, "sic87.csv"))
    return df


def get_sic87():
    path = os.path.join(DATA_DIR, "sic87.csv")
    if os.path.isfile(path):
        return pd.read_csv(path, index_col=0)
    else:
        return update_sic87()
