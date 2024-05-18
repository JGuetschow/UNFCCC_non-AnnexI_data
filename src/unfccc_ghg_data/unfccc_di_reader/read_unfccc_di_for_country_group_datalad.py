"""
Call read_DI_fro_country_group_datalad

wrapper around read_DI_for_country_group_datalad such that it can be called
from doit in the current setup where doit runs on system python and
not in the venv.
"""

import argparse

from unfccc_ghg_data.unfccc_di_reader import read_DI_for_country_group_datalad

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--annexI",
        help="read for AnnexI countries (default is for " "non-AnnexI)",
        action="store_true",
    )
    args = parser.parse_args()
    annexI = args.annexI

    read_DI_for_country_group_datalad(
        annexI=annexI,
    )
