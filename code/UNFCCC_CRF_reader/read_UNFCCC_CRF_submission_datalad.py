"""
wrapper around read_crf_for_country_datalad such that it can be called
from doit in the current setup where doit runs on system python and
not in the venv.
"""

from . import read_crf_for_country_datalad
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--country', help='Country name or code')
parser.add_argument('--submission_year', help='Submission round to read')
parser.add_argument('--submission_date', help='Date of submission to read', default=None)

args = parser.parse_args()

country = args.country
submission_year = args.submission_year
submission_date = args.submission_date

read_crf_for_country_datalad(
        country,
        submission_year=submission_year,
        submission_date=submission_date)