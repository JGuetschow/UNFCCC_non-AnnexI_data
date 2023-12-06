"""
This script is a wrapper around the process_UNFCCC_DI_for_country_group
function such that it can be called from datalad
"""

import argparse

from unfccc_ghg_data.unfccc_di_reader import process_UNFCCC_DI_for_country_group

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--annexI', help='read for AnnexI countries (default is for '
                                         'non-AnnexI)', action='store_true')
    parser.add_argument('--date', help='date of input data to use (default is None '
                                           'to read latest data)', default=None)
    args = parser.parse_args()
    annexI = args.annexI
    date_str = args.date
    if date_str == "None":
        date_str = None

    process_UNFCCC_DI_for_country_group(
        annexI=annexI,
        date_str=date_str,
    )
