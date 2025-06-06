"""
Downloading and reading GHG data from the UNFCCC

Downloading and reading country greenhouse gas data submitted to the United Nations
Framework Convention on Climate Change (UNFCCC)in different submissions and
formats and providing it in a standadized nc and csv format compatible with primap2.
Data are read using different methods from APIs, xlsx and csv files as well as pdf
files.
"""

import importlib.metadata

from . import (
    helper,
    unfccc_crf_reader,
    unfccc_di_reader,
    unfccc_downloader,
    unfccc_reader,
)

__all__ = [
    "helper",
    "unfccc_crf_reader",
    "unfccc_di_reader",
    "unfccc_downloader",
    "unfccc_reader",
]

__version__ = importlib.metadata.version("unfccc_ghg_data")
