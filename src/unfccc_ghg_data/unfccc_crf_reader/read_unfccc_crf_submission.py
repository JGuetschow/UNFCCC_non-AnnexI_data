"""
Wrapper around read_crf_for_country

Wrapper around the read_crf_for_country
function such that it can be called from datalad
"""

import argparse

from unfccc_ghg_data.unfccc_crf_reader.unfccc_crf_reader_prod import (
    read_crf_for_country,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--country", help="Country name or code")
    parser.add_argument("--submission_year", help="Submission round to read", type=int)
    parser.add_argument(
        "--date_or_version", help="Date or version of submission to read", default=None
    )
    parser.add_argument(
        "--re_read", help="Read data also if already read before", action="store_true"
    )
    parser.add_argument("--type", help="CRF or CRT tables", default="CRF")

    args = parser.parse_args()

    country = args.country
    submission_year = args.submission_year
    date_or_version = args.date_or_version
    re_read = args.re_read
    submission_type = args.type
    if date_or_version == "None":
        date_or_version = None

    read_crf_for_country(
        country,
        submission_year=submission_year,
        date_or_version=date_or_version,
        re_read=re_read,
        submission_type=submission_type,
    )
