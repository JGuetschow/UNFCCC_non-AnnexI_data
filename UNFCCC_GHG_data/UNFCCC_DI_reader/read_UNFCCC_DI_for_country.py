"""
This script is a wrapper around the read__for_country
function such that it can be called from datalad
"""

import argparse
from UNFCCC_GHG_data.UNFCCC_DI_reader.UNFCCC_DI_reader_core import \
    read_UNFCCC_DI_for_country


parser = argparse.ArgumentParser()
parser.add_argument('--country', help='Country code')
parser.add_argument('--date', help='String with current date')
args = parser.parse_args()

country_code = args.country
date_str = args.date

read_UNFCCC_DI_for_country(
    country_code=country_code,
    category_groups=None, # read all categories
    read_subsectors=False, # not applicable as we read all categories
    date_str=date_str,
    pm2if_specifications=None, # automatically use the right specs for AI and NAI
    default_gwp=None, # automatically uses right default GWP for AI and NAI
    debug=False,
)