"""
wrapper around read_crf_for_country_datalad such that it can be called
from doit in the current setup where doit runs on system python and
not in the venv.
"""

from UNFCCC_GHG_data.UNFCCC_DI_reader import \
    read_DI_for_country_group_datalad
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--annexI', help='read for AnnexI countries (default is for '
                                     'non-AnnexI)', action='store_true')
args = parser.parse_args()
annexI = args.annexI

read_DI_for_country_group_datalad(
    annexI=annexI,
)
