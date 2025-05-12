"""
Read Philippines' 2025 NICCDIES Inventory from csv file.

The csv file has been created by manually entering the data available at
https://niccdies.climate.gov.ph/ghg-inventory/national
Data extracted May 12th 2025
"""

import os
import sys

import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    gas_baskets,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.Philippines.config_PHL_2025_NICCDIES import (
    add_coords_cols,
    category_conversion,
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    meta_data,
    processing_info_country,
    terminology_proc,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = downloaded_data_path / "non-UNFCCC" / "Philippines" / "2025-NICCDIES"
    output_folder = extracted_data_path / "non-UNFCCC" / "Philippines"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "PHL_2025-NICCDIES_2025_"

    inventory_file = "2025-NICCDIES.csv"

    compression = dict(zlib=True, complevel=9)

    # ###
    # start data reading
    # ###

    # change working directory to script directory for proper folder names
    script_path = os.path.abspath(sys.argv[0])
    script_dir_name = os.path.dirname(script_path)
    os.chdir(script_dir_name)

    data_df = None

    data_df = pd.read_csv(input_folder / inventory_file)

    # create copies of category col for further processing
    data_df["orig_cat_name"] = data_df["Sector"]

    # ###
    # convert to PRIMAP2 interchange format
    # ###
    data_if = pm2.pm2io.convert_wide_dataframe_if(
        data_df,
        coords_cols=coords_cols,
        add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        # coords_value_filling=coords_value_filling,
        # filter_remove=filter_remove,
        # filter_keep=filter_keep,
        meta_data=meta_data,
        convert_str=True,
        copy_df=True,  # we need the unchanged DF for the conversion step
    )

    # conversion to PRIMAP2 native format
    data_pm2 = pm2.pm2io.from_interchange_format(data_if)
    # convert back to IF to have units in the fixed format
    data_pm2 = data_pm2.reset_coords(["orig_cat_name"], drop=True)
    data_if = data_pm2.pr.to_interchange_format()

    # ###
    # save data to IF and native format
    # ###
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"]), data_if
    )

    data_pm2 = pm2.pm2io.from_interchange_format(data_if)
    encoding = {var: compression for var in data_pm2.data_vars}
    data_pm2.pr.to_netcdf(
        output_folder / (output_filename + coords_terminologies["category"] + ".nc"),
        encoding=encoding,
    )

    # ###
    # conversion to ipcc 2006 categories
    # ###

    ### processing
    # aggregate gas baskets (some KYOTOGHG time seres were removed because of errors)
    # this also checks for inconsistencies
    data_proc_pm2 = process_data_for_country(
        data_pm2,
        entities_to_ignore=[],
        gas_baskets=gas_baskets,
        processing_info_country=processing_info_country,
        cat_terminology_out=terminology_proc,
        category_conversion=category_conversion,
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
        output_folder / (output_filename + terminology_proc),
        data_proc_if,
    )

    encoding = {var: compression for var in data_proc_pm2.data_vars}
    data_proc_pm2.pr.to_netcdf(
        output_folder / (output_filename + terminology_proc + ".nc"),
        encoding=encoding,
    )
