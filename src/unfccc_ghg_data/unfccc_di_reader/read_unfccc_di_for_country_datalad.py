"""
Call read_DI_for_country_datalad

wrapper around read_DI_for_country_datalad such that it can be called
from doit in the current setup where doit runs on system python and
not in the venv.
"""

import argparse

from unfccc_ghg_data.unfccc_di_reader import read_DI_for_country_datalad

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--country", help="Country name or code")

    args = parser.parse_args()
    country = args.country

    read_DI_for_country_datalad(country)
