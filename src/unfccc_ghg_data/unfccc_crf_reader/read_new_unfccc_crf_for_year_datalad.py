"""
wrapper around read_crf_for_country_datalad such that it can be called
from doit in the current setup where doit runs on system python and
not in the venv.
"""

import argparse

from unfccc_ghg_data.unfccc_crf_reader.unfccc_crf_reader_prod import read_new_crf_for_year_datalad
from unfccc_ghg_data.unfccc_crf_reader.util import NoCRFFilesError

parser = argparse.ArgumentParser()
#parser.add_argument('--countries', help='List of country codes', default=None)
parser.add_argument('--submission_year', help='Submission round to read')
parser.add_argument('--re_read', help='Read data also if already read before',
                    action='store_true')

args = parser.parse_args()

#countries = args.countries
#if countries == "None":
#    countries = None
submission_year = args.submission_year
re_read = args.re_read
print(f"!!!!!!!!!!!!!!!!!!!!script_dl: re_read={re_read}")
try:
    read_new_crf_for_year_datalad(
        submission_year=int(submission_year),
#        countries=countries,
        re_read=re_read
    )
except NoCRFFilesError as err:
    print(f"NoCRFFilesError: {err}")
