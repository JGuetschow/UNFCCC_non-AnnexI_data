"""
This script is a wrapper around the read_year_to_test_specs
function such that it can be called from datalad
"""

from UNFCCC_CRF_reader_devel import read_year_to_test_specs
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--submission_year', help='Submission round to read', type=int)
parser.add_argument('--data_year', help='Data year to read', type=int, default=2010)
args = parser.parse_args()


submission_year = args.submission_year
data_year = args.data_year

read_year_to_test_specs(
    submission_year=submission_year,
    data_year=data_year,
)


