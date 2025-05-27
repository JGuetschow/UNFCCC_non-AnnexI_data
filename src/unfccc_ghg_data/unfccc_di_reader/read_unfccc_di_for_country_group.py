"""
Call read_UNFCCC_DI_for_country_group

This script is a wrapper around the read_UNFCCC_DI_for_country_group
function such that it can be called from datalad
"""

import argparse

from unfccc_ghg_data.unfccc_di_reader import read_UNFCCC_DI_for_country_group

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--annexI",
        help="read for AnnexI countries (default is for non-AnnexI)",
        action="store_true",
    )
    args = parser.parse_args()
    annexI = args.annexI

    read_UNFCCC_DI_for_country_group(
        annexI=annexI,
    )
