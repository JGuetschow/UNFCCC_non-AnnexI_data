"""
helper functions and definitions

helper functions and definitions used by the different readers and downloader in
the unfccc_ghg_data package
"""

from .definitions import (
    AI_countries,
    GWP_factors,
    all_countries,
    code_path,
    compression,
    custom_country_mapping,
    custom_folders,
    dataset_path,
    dataset_path_UNFCCC,
    downloaded_data_path,
    downloaded_data_path_UNFCCC,
    extracted_data_path,
    extracted_data_path_UNFCCC,
    gas_baskets,
    legacy_data_path,
    log_path,
    nAI_countries,
    root_path,
)
from .functions import (
    convert_categories,
    create_folder_mapping,
    fix_rows,
    get_code_file,
    get_country_code,
    get_country_name,
    make_wide_table,
    process_data_for_country,
)

__all__ = [
    "root_path",
    "code_path",
    "log_path",
    "extracted_data_path",
    "extracted_data_path_UNFCCC",
    "legacy_data_path",
    "downloaded_data_path",
    "downloaded_data_path_UNFCCC",
    "dataset_path",
    "dataset_path_UNFCCC",
    "custom_country_mapping",
    "custom_folders",
    "GWP_factors",
    "gas_baskets",
    "get_country_code",
    "get_country_name",
    "convert_categories",
    "create_folder_mapping",
    "process_data_for_country",
    "fix_rows",
    "get_code_file",
    "compression",
    "make_wide_table",
    "nAI_countries",
    "AI_countries",
    "all_countries",
]
