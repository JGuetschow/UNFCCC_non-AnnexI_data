"""
script to display information on country

This script takes country as input (from doit) and displays available
submissions and datasets both read and not read
"""

import argparse

from unfccc_ghg_data.helper.functions import get_country_datasets, get_country_submissions

# Find the right function and possible input and output files and
# read the data using datalad run.
parser = argparse.ArgumentParser()
parser.add_argument('--country', help='Country name or code')
args = parser.parse_args()
country = args.country

# print available submissions
print("="*15 + " Available submissions " + "="*15)
get_country_submissions(country, True)
print("")

#print available datasets
print("="*15 + " Available datasets " + "="*15)
get_country_datasets(country, True)
