"""
This script is a wrapper around the read_crf_for_country
function such that it can be called from datalad
"""

from UNFCCC_GHG_data.UNFCCC_CRF_reader.UNFCCC_CRF_reader_prod import read_crf_for_country
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--country', help='Country name or UNFCCC_GHG_data')
parser.add_argument('--submission_year', help='Submission round to read', type=int)
parser.add_argument('--submission_date', help='Date of submission to read', default=None)
parser.add_argument('--re_read', help='Read data also if already read before',
                    action='store_true')

args = parser.parse_args()

country = args.country
submission_year = args.submission_year
submission_date = args.submission_date
re_read = args.re_read
if submission_date == 'None':
    submission_date = None

read_crf_for_country(
    country,
    submission_year=submission_year,
    submission_date=submission_date,
    re_read=re_read
)

