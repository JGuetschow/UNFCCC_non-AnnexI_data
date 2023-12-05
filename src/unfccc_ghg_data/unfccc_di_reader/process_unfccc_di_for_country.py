"""
This script is a wrapper around the read__for_country
function such that it can be called from datalad
"""

import argparse

from unfccc_ghg_data.UNFCCC_DI_reader import process_and_save_UNFCCC_DI_for_country

parser = argparse.ArgumentParser()
parser.add_argument('--country', help='Country code')
parser.add_argument('--date', help='String with date to read and process. If not '
                                   'given latest data will be used', default=None)
args = parser.parse_args()

country_code = args.country
date_str = args.date

if date_str == "None":
    date_str = None

process_and_save_UNFCCC_DI_for_country(
    country_code=country_code,
    date_str=date_str,
)
