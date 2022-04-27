"""
CRF reader module
"""

from pathlib import Path

from .UNFCCC_CRF_reader import read_crf_for_country

root_path = Path(__file__).parents[3]
log_path = root_path / "log"
downloaded_data_path = root_path / "downloaded_data" / "UNFCCC"
extracted_data_path = root_path / ""

custom_country_mapping = {
    "EUA": "European Union",
    "EUC": "European Union",
    "FRK": "France",
    "DKE": "Denmark",
    "DNM": "Denmark",
    "GBK": "United Kingdom",
}