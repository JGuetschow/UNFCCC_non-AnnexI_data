# this script takes country as input (from doit) and
# runs displays available submissions and datasets

import argparse
from UNFCCC_GHG_data.helper.functions import get_country_submissions
from UNFCCC_GHG_data.helper.functions import get_country_datasets

# Find the right function and possible input and output files and
# read the data using datalad run.
parser = argparse.ArgumentParser()
parser.add_argument('--country', help='Country name or UNFCCC_GHG_data')
args = parser.parse_args()
country = args.country

# print available submissions
print("="*15 + " Available submissions " + "="*15)
get_country_submissions(country, True)
print("")

#print available datasets
print("="*15 + " Available datasets " + "="*15)
get_country_datasets(country, True)