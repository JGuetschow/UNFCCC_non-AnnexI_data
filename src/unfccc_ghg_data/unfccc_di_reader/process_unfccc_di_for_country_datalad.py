"""
call process_DI_for_country_datalad

wrapper around process_DI_for_country_datalad such that it can be called
from doit in the current setup where doit runs on system python and
not in the venv.
"""

import argparse

from unfccc_ghg_data.unfccc_di_reader import process_DI_for_country_datalad

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--country", help="Country name or code")
    parser.add_argument(
        "--date",
        help="String with date to read and process. If not "
        "given latest data will be used",
        default=None,
    )
    args = parser.parse_args()
    country = args.country
    date_str = args.date

    if date_str == "None":
        date_str = None

    process_DI_for_country_datalad(country, date_str=date_str)
