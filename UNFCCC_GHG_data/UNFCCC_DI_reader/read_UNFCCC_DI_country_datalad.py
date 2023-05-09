"""
wrapper around read_crf_for_country_datalad such that it can be called
from doit in the current setup where doit runs on system python and
not in the venv.
"""

from UNFCCC_DI_reader_core import read_DI_for_country_datalad
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--country', help='Country name or code')

args = parser.parse_args()

country = args.country

read_DI_for_country_datalad(
    country,
)