"""
CRF reader module
"""

#from pathlib import Path
from . import crf_specifications
from .UNFCCC_CRF_reader_prod import read_crf_for_country, read_crf_for_country_datalad

__all__ = ["crf_specifications", "read_crf_for_country", "read_crf_for_country_datalad"]

