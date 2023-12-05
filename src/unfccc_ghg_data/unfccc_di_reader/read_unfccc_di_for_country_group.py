"""
This script is a wrapper around the read_UNFCCC_DI_for_country_group
function such that it can be called from datalad
"""

import argparse

from unfccc_ghg_data.UNFCCC_DI_reader import read_UNFCCC_DI_for_country_group

parser = argparse.ArgumentParser()
parser.add_argument('--annexI', help='read for AnnexI countries (default is for '
                                     'non-AnnexI)', action='store_true')
args = parser.parse_args()
annexI = args.annexI

read_UNFCCC_DI_for_country_group(
    annexI=annexI,
)
