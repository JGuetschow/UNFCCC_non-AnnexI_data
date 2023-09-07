"""
This script is a wrapper around the read_year_to_test_specs
function such that it can be called from datalad
"""

from UNFCCC_GHG_data.UNFCCC_CRF_reader.UNFCCC_CRF_reader_devel import read_year_to_test_specs
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--submission_year', help='Submission round to read', type=int)
parser.add_argument('--data_year', help='Data year to read', type=int, default=2010)
parser.add_argument('--country', help='Country to read', type=str, default=None)
parser.add_argument('--totest', help='read tables to test', action='store_true')
args = parser.parse_args()


submission_year = args.submission_year
data_year = args.data_year
country = args.country
#print(f"totest: {args.totest}")
if args.totest:
    totest = True
else:
    totest = False

read_year_to_test_specs(
    submission_year=submission_year,
    data_year=data_year,
    totest=totest,
    country_code=country,
)


