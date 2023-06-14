"""
wrapper around read_crf_for_country_datalad such that it can be called
from doit in the current setup where doit runs on system python and
not in the venv.
"""

from UNFCCC_GHG_data.UNFCCC_DI_reader import \
    process_DI_for_country_datalad
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--country', help='Country name or code')
parser.add_argument('--date', help='String with date to read and process. If not '
                                   'given latest data will be used', default=None)
args = parser.parse_args()
country = args.country
date_str = args.date

if date_str == "None":
    date_str = None

process_DI_for_country_datalad(country, date_str=date_str)