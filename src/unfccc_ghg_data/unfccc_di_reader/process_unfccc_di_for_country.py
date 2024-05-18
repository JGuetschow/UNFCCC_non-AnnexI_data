"""
call process_and_save_UNFCCC_DI_for_country

This script is a wrapper around the process_and_save_UNFCCC_DI_for_country
function such that it can be called from datalad
"""

import argparse

from unfccc_ghg_data.unfccc_di_reader import process_and_save_UNFCCC_DI_for_country

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--country", help="Country code")
    parser.add_argument(
        "--date",
        help="String with date to read and process. If not "
        "given latest data will be used",
        default=None,
    )
    args = parser.parse_args()

    country_code = args.country
    date_str = args.date

    if date_str == "None":
        date_str = None

    process_and_save_UNFCCC_DI_for_country(
        country_code=country_code,
        date_str=date_str,
    )
