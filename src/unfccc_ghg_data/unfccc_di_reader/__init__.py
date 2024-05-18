"""
submodule to read data from UNFCCC DI API using the unfccc_di_api package
"""

# import unfccc_di_api
from .unfccc_di_reader_core import (
    convert_DI_data_to_pm2_if,
    convert_DI_IF_data_to_pm2,
    read_UNFCCC_DI_for_country,
    read_UNFCCC_DI_for_country_group,
)
from .unfccc_di_reader_datalad import (
    process_DI_for_country_datalad,
    process_DI_for_country_group_datalad,
    read_DI_for_country_datalad,
    read_DI_for_country_group_datalad,
)
from .unfccc_di_reader_helper import determine_filename
from .unfccc_di_reader_proc import (
    process_and_save_UNFCCC_DI_for_country,
    process_UNFCCC_DI_for_country,
    process_UNFCCC_DI_for_country_group,
)

__all__ = [
    "read_UNFCCC_DI_for_country",
    "convert_DI_data_to_pm2_if",
    "convert_DI_IF_data_to_pm2",
    "read_UNFCCC_DI_for_country_group",
    "process_UNFCCC_DI_for_country",
    "process_and_save_UNFCCC_DI_for_country",
    "process_UNFCCC_DI_for_country_group",
    "process_DI_for_country_group_datalad",
    "read_DI_for_country_datalad",
    "process_DI_for_country_datalad",
    "read_DI_for_country_group_datalad",
    "determine_filename",
]
