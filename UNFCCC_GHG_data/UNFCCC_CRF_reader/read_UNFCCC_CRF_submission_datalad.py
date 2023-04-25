"""
wrapper around read_crf_for_country_datalad such that it can be called
from doit in the current setup where doit runs on system python and
not in the venv.
"""

from .UNFCCC_CRF_reader_prod import read_crf_for_country_datalad
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--country', help='Country name or UNFCCC_GHG_data')
parser.add_argument('--submission_year', help='Submission round to read')
parser.add_argument('--submission_date', help='Date of submission to read', default=None)
parser.add_argument('--re_read', help='Read data also if already read before',
                    action='store_true')

args = parser.parse_args()

country = args.country
submission_year = args.submission_year
submission_date = args.submission_date
re_read = args.re_read


if submission_date == "None":
    submission_date = None

read_crf_for_country_datalad(
    country,
    submission_year=int(submission_year),
    submission_date=submission_date,
    re_read=re_read
)