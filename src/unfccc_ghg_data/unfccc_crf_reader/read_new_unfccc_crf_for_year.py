"""
Wrapper for the read_crf_for_country

Wrapper around the read_crf_for_country
function such that it can be called from datalad
"""

import argparse

from unfccc_ghg_data.unfccc_crf_reader.unfccc_crf_reader_prod import (
    read_new_crf_for_year,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--countries', help='List of country codes', default=None)
    parser.add_argument("--submission_year", help="Submission round to read", type=int)
    parser.add_argument(
        "--submission_date", help="Date of submission to read", default=None
    )
    parser.add_argument(
        "--re_read", help="Read data also if already read before", action="store_true"
    )

    args = parser.parse_args()

    # countries = args.countries
    # if countries == "None":
    #    countries = None
    submission_year = args.submission_year
    re_read = args.re_read
    print(f"!!!!!!!!!!!!!!!!!!!!script: re_read={re_read}")
    read_new_crf_for_year(
        submission_year=int(submission_year),
        #    countries=countries,
        re_read=re_read,
    )
