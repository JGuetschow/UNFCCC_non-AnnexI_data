"""
Read Indonesia's NC4 from pdf

This script reads data from Indonesia's NC4
Data are read from pdf using camelot.

TODO: elaborate on processing

"""

import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import (
    compression,
    downloaded_data_path,
    extracted_data_path,
    gas_baskets,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.Bosnia_and_Herzegovina.config_bih_btr1 import (
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    country_processing_step1,
    filter_remove,
    meta_data,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = downloaded_data_path / "UNFCCC" / "Bosnia_and_Herzegovina" / "BTR1"
    output_folder = extracted_data_path / "UNFCCC" / "Bosnia_and_Herzegovina"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "BIH_BTR1_2026_"
    inventory_file = "btr1_data.xlsx"

    # ###
    # read the data from xlsx
    # ###
    data_pd = pd.read_excel(
        input_folder / inventory_file, sheet_name="data", na_values="NaN"
    )

    # drop info about source tables etc
    data_pd = data_pd.drop(columns=["Table", "category name", "note"])
    # make sure all col headers are str
    data_pd.columns = data_pd.columns.map(str)

    # make sure all category codes are str
    data_pd["category"] = data_pd["category"].astype(str)

    data_if = pm2.pm2io.convert_wide_dataframe_if(
        data_pd,
        coords_cols=coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        filter_remove=filter_remove,
        meta_data=meta_data,
        time_format="%Y",
    )

    data_pm2 = pm2.pm2io.from_interchange_format(data_if)

    data_raw_pm2 = data_pm2.pr.loc[{"provenance": ["measured"]}]

    # ###
    # save data to IF and native format
    # ###
    data_raw_if = data_raw_pm2.pr.to_interchange_format()
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"] + "_raw"),
        data_raw_if,
    )

    encoding = {var: compression for var in data_raw_pm2.data_vars}
    data_raw_pm2.pr.to_netcdf(
        output_folder
        / (output_filename + coords_terminologies["category"] + "_raw.nc"),
        encoding=encoding,
    )

    ### add the processed data
    data_proc_pm2 = data_raw_pm2.copy()

    data_temp = data_proc_pm2.pr.loc[{"provenance": "measured"}]
    data_proc_pm2 = data_proc_pm2.pr.set("provenance", "derived", data_temp)
    data_proc_pm2 = data_proc_pm2.pr.loc[{"provenance": ["derived"]}]
    data_proc_pm2 = data_proc_pm2.pr.merge(data_pm2.pr.loc[{"provenance": ["derived"]}])

    # actual processing
    data_proc_pm2 = process_data_for_country(
        data_proc_pm2,
        entities_to_ignore=[],
        gas_baskets=gas_baskets,
        processing_info_country=country_processing_step1,
    )

    # adapt source and metadata
    current_source = data_proc_pm2.coords["source"].to_numpy()[0]
    data_temp = data_proc_pm2.pr.loc[{"source": current_source}]
    data_proc_pm2 = data_proc_pm2.pr.set("source", "BUR_NIR", data_temp)
    data_proc_pm2 = data_proc_pm2.pr.loc[{"source": ["BUR_NIR"]}]

    # ###
    # save data to IF and native format
    # ###
    data_proc_if = data_proc_pm2.pr.to_interchange_format()
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"]),
        data_proc_if,
    )

    encoding = {var: compression for var in data_proc_pm2.data_vars}
    data_proc_pm2.pr.to_netcdf(
        output_folder / (output_filename + coords_terminologies["category"] + ".nc"),
        encoding=encoding,
    )
