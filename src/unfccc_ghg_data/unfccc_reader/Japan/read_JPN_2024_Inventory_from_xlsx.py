"""
Read Japan's 2024 inventory from xlsx

Files available here: https://www.nies.go.jp/gio/en/aboutghg/index.html

"""

import os
import sys

import pandas as pd
import primap2 as pm2
from config_JPN_INV2024 import (
    basket_copy,
    cat_conversion,
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    filter_remove,
    gas_baskets,
    meta_data,
    sheets_to_read,
    terminology_proc,
    time_format,
)

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    process_data_for_country,
)

pd.set_option("future.no_silent_downcasting", True)

# ###
# configuration
# ###

# folders and files
input_folder = downloaded_data_path / "non-UNFCCC" / "Japan" / "2024-Inventory"
output_folder = extracted_data_path / "non-UNFCCC" / "Japan"
if not output_folder.exists():
    output_folder.mkdir()

output_filename = "JPN_2023-Inventory_2024_"

inventory_file = "L5-7gas_2024_gioweb_ver1.0.xlsx"

# time_format = "%Y"
name_for_cat_col = "category"
compression = dict(zlib=True, complevel=9)

# ###
# start data reading
# ###

# change working directory to script directory for proper folder names
script_path = os.path.abspath(sys.argv[0])
script_dir_name = os.path.dirname(script_path)
os.chdir(script_dir_name)

data_pm2 = None

for sheet in sheets_to_read:
    # read sheet for the year. Each sheet contains several tables,
    # we only read the upper row as the other tables are summary tables
    current_sheet_config = sheets_to_read[sheet]
    df_current = pd.read_excel(
        input_folder / inventory_file,
        sheet_name=sheet,
        engine="openpyxl",
        **current_sheet_config["xls_params"],
    )

    # process category and entity
    if current_sheet_config["entity"].startswith("COL_"):
        # processing with entity
        entity_col = current_sheet_config["entity"][4:]
        df_current[entity_col] = df_current[entity_col].ffill()
        df_current[current_sheet_config["cat_cols"]] = df_current[
            current_sheet_config["cat_cols"]
        ].fillna(value="Total")
        df_current[entity_col] = df_current[entity_col].str.replace("\n", "")
        df_current[entity_col] = df_current[entity_col].str.strip()
    else:
        # entity given for whole table
        # print('not implemented')
        df_current[current_sheet_config["cat_cols"]] = df_current[
            current_sheet_config["cat_cols"]
        ].bfill(axis=1)
        df_current = df_current.drop(columns=current_sheet_config["cat_cols"][1:])
    df_current = df_current.rename(
        columns={current_sheet_config["cat_cols"][0]: name_for_cat_col}
    )
    df_current[name_for_cat_col] = df_current[name_for_cat_col].str.replace("\n", "")
    df_current[name_for_cat_col] = df_current[name_for_cat_col].str.strip()

    # convert to primap2 format
    coords_value_mapping_current = coords_value_mapping.copy()
    coords_value_mapping_current["category"] = current_sheet_config["cat_mapping"]
    coords_cols_current = coords_cols.copy()
    coords_defaults_current = coords_defaults.copy()
    coords_defaults_current["unit"] = current_sheet_config["unit"]
    if current_sheet_config["entity"].startswith("COL_"):
        coords_cols_current["entity"] = entity_col
    else:
        coords_defaults_current["entity"] = current_sheet_config["entity"]

    # make sure all column names are str
    df_current.columns = df_current.columns.astype(str)

    data_current_if = pm2.pm2io.convert_wide_dataframe_if(
        df_current,
        coords_cols=coords_cols_current,
        add_coords_cols=None,
        coords_defaults=coords_defaults_current,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping_current,
        # coords_value_filling=None,
        filter_remove=filter_remove,
        # filter_keep=filter_keep,
        meta_data=meta_data,
        time_format=time_format,
    )
    data_current_pm2 = pm2.pm2io.from_interchange_format(data_current_if)

    if data_pm2 is None:
        data_pm2 = data_current_pm2
    else:
        data_pm2 = data_pm2.pr.merge(data_current_pm2)

# convert back to IF to have units in the fixed format
data_if = data_pm2.pr.to_interchange_format()

# ###
# save data to IF and native format
# ###
pm2.pm2io.write_interchange_format(
    output_folder / (output_filename + coords_terminologies["category"]), data_if
)

encoding = {var: compression for var in data_pm2.data_vars}
data_pm2.pr.to_netcdf(
    output_folder / (output_filename + coords_terminologies["category"] + ".nc"),
    encoding=encoding,
)

# ###
# conversion to ipcc 2006 categories
# ###

data_pm2_2006 = data_pm2.copy()

# actual processing

country_processing = {
    "basket_copy": basket_copy,
}

data_pm2_2006 = process_data_for_country(
    data_pm2_2006,
    entities_to_ignore=[],
    gas_baskets=gas_baskets,
    processing_info_country=country_processing,
    cat_terminology_out=terminology_proc,
    category_conversion=cat_conversion,
    # sectors_out=sectors_to_save,
)

# adapt source and metadata
# TODO: processing info is present twice
current_source = data_pm2_2006.coords["source"].to_numpy()[0]
data_temp = data_pm2_2006.pr.loc[{"source": current_source}]
data_pm2_2006 = data_pm2_2006.pr.set("source", "AI_INV", data_temp)
data_pm2_2006 = data_pm2_2006.pr.loc[{"source": ["AI_INV"]}]


# convert back to IF to have units in the fixed format
data_if_2006 = data_pm2_2006.pr.to_interchange_format()

pm2.pm2io.write_interchange_format(
    output_folder / (output_filename + terminology_proc),
    data_if_2006,
)

encoding = {var: compression for var in data_pm2_2006.data_vars}
data_pm2_2006.pr.to_netcdf(
    output_folder / (output_filename + terminology_proc + ".nc"),
    encoding=encoding,
)
