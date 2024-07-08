"""
Read Thailand's BUR4 from pdf

This script reads data from Thailand's BUR4
Data is read from two csv files which have been created manually from ocr processed
pdf files

.. code-block:: bash

    pdftk Thailand_BUR4_final_28122022.pdf cat 65-67east output inventory_2019.pdf
    ocrmypdf --force-ocr inventory_2019.pdf inventory_2019_ocr.pdf
    pdftk Thailand_BUR4_final_28122022.pdf cat 69 output trends.pdf
    ocrmypdf --force-ocr trends.pdf trends_ocr.pdf

Values for HFCs and SF6 have been taken from Table2-9 where they are present in
CO2eq and thus HFC data can be used and SF6 data is not 0 as in the mein inventory
tables

"""


import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.Thailand.config_tha_bur4 import (
    cat_codes_manual_main_sector_ts,
    cat_conversion,
    coords_cols,
    coords_cols_indirect,
    coords_cols_main_sector_ts,
    coords_defaults,
    coords_defaults_indirect,
    coords_defaults_main_sector_ts,
    coords_terminologies,
    coords_value_mapping,
    country_processing_step1,
    country_processing_step2,
    filter_remove,
    gas_baskets,
    inv_conf,
    meta_data,
    sectors_to_save,
    terminology_proc,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = downloaded_data_path / "UNFCCC" / "Thailand" / "BUR4"
    output_folder = extracted_data_path / "UNFCCC" / "Thailand"
    if not output_folder.exists():
        output_folder.mkdir()

    inventory_file = "THA_inventory_2019.csv"
    trends_file = "THA_trends_2000-2019.csv"
    indirect_file = "THA_indirect_2000-2019.csv"
    output_filename = "THA_BUR4_2022_"

    compression = dict(zlib=True, complevel=9)

    # ###
    # read the inventory data and convert to PM2 IF
    # ###
    df_inventory = pd.read_csv(input_folder / inventory_file, header=None)
    df_inventory = pm2.pm2io.nir_add_unit_information(
        df_inventory,
        unit_row=inv_conf["unit_row"],
        entity_row=inv_conf["entity_row"],
        regexp_entity=".*",
        regexp_unit=".*",
        default_unit="Gg",
    )
    # set index and convert to long format
    df_inventory = df_inventory.set_index(inv_conf["index_cols"])
    df_inventory_long = pm2.pm2io.nir_convert_df_to_long(
        df_inventory, inv_conf["year"], inv_conf["header_long"]
    )
    df_inventory_long["orig_cat_name"] = df_inventory_long["orig_cat_name"].str[0]

    # prep for conversion to PM2 IF and native format
    # make a copy of the categories row
    df_inventory_long["category"] = df_inventory_long["orig_cat_name"]

    # replace cat names by codes in col "category"
    # first the manual replacements
    df_inventory_long["category"] = df_inventory_long["category"].replace(
        inv_conf["cat_codes_manual"]
    )

    # then the regex replacements
    def repl(m):  # noqa: D103
        return m.group("code")

    df_inventory_long["category"] = df_inventory_long["category"].str.replace(
        inv_conf["cat_code_regexp"], repl, regex=True
    )
    df_inventory_long = df_inventory_long.reset_index(drop=True)

    # make sure all col headers are str
    df_inventory_long.columns = df_inventory_long.columns.map(str)

    df_inventory_long = df_inventory_long.drop(columns=["orig_cat_name"])

    data_inventory_IF = pm2.pm2io.convert_long_dataframe_if(
        df_inventory_long,
        coords_cols=coords_cols,
        # add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        # coords_value_filling=coords_value_filling,
        filter_remove=filter_remove,
        # filter_keep=filter_keep,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )

    # ###
    # read the main sector time series and convert to PM2 IF
    # ###
    df_main_sector_ts = pd.read_csv(input_folder / trends_file)

    df_main_sector_ts = df_main_sector_ts.transpose()
    df_main_sector_ts = df_main_sector_ts.reset_index(drop=False)
    cols = df_main_sector_ts.iloc[0].copy(deep=True)
    cols.iloc[0] = "category"
    cols.iloc[1:] = cols.iloc[1:].astype(int).astype(str)
    df_main_sector_ts.columns = cols
    df_main_sector_ts = df_main_sector_ts.drop(0)

    # replace cat names by codes in col "category"
    df_main_sector_ts["category"] = df_main_sector_ts["category"].replace(
        cat_codes_manual_main_sector_ts
    )

    data_main_sector_ts_IF = pm2.pm2io.convert_wide_dataframe_if(
        df_main_sector_ts,
        coords_cols=coords_cols_main_sector_ts,
        # add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults_main_sector_ts,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        # coords_value_filling=coords_value_filling,
        filter_remove=filter_remove,
        # filter_keep=filter_keep,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )

    # ###
    # read the indirect gases time series and convert to PM2 IF
    # ###
    df_indirect = pd.read_csv(input_folder / indirect_file)

    df_indirect = df_indirect.transpose()
    df_indirect = df_indirect.reset_index(drop=False)
    cols = df_indirect.iloc[0].copy(deep=True)
    cols.iloc[0] = "entity"
    cols.iloc[1:] = cols.iloc[1:].astype(int).astype(str)
    df_indirect.columns = cols
    df_indirect = df_indirect.drop(0)

    data_indirect_IF = pm2.pm2io.convert_wide_dataframe_if(
        df_indirect,
        coords_cols=coords_cols_indirect,
        # add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults_indirect,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        # coords_value_filling=coords_value_filling,
        # filter_remove=filter_remove,
        # filter_keep=filter_keep,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )

    # ###
    # merge the three datasets
    # ###
    data_inventory_pm2 = pm2.pm2io.from_interchange_format(data_inventory_IF)
    data_main_sector_ts_pm2 = pm2.pm2io.from_interchange_format(data_main_sector_ts_IF)
    data_indirect_pm2 = pm2.pm2io.from_interchange_format(data_indirect_IF)

    data_all_pm2 = data_inventory_pm2.pr.merge(data_main_sector_ts_pm2)
    data_all_pm2 = data_all_pm2.pr.merge(data_indirect_pm2)

    data_all_if = data_all_pm2.pr.to_interchange_format()

    # ###
    # save raw data to IF and native format
    # ###
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"] + "_raw"),
        data_all_if,
    )

    encoding = {var: compression for var in data_all_pm2.data_vars}
    data_all_pm2.pr.to_netcdf(
        output_folder
        / (output_filename + coords_terminologies["category"] + "_raw.nc"),
        encoding=encoding,
    )

    # ###
    # ## process the data
    # ###
    data_proc_pm2 = data_all_pm2

    # combine CO2 emissions and removals
    data_proc_pm2["CO2"] = data_proc_pm2[["CO2 emissions", "CO2 removals"]].pr.sum(
        dim="entity", skipna=True, min_count=1
    )
    data_proc_pm2["CO2"].attrs["entity"] = "CO2"

    # actual processing
    data_proc_pm2 = process_data_for_country(
        data_proc_pm2,
        entities_to_ignore=["CO2 emissions", "CO2 removals"],
        gas_baskets={},
        processing_info_country=country_processing_step1,
    )

    data_proc_pm2 = process_data_for_country(
        data_proc_pm2,
        entities_to_ignore=[],
        gas_baskets=gas_baskets,
        processing_info_country=country_processing_step2,
        cat_terminology_out=terminology_proc,
        category_conversion=cat_conversion,
        sectors_out=sectors_to_save,
    )

    # adapt source and metadata
    # TODO: processing info is present twice
    current_source = data_proc_pm2.coords["source"].to_numpy()[0]
    data_temp = data_proc_pm2.pr.loc[{"source": current_source}]
    data_proc_pm2 = data_proc_pm2.pr.set("source", "BUR_NIR", data_temp)

    # ###
    # save data to IF and native format
    # ###
    data_proc_if = data_proc_pm2.pr.to_interchange_format()
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + terminology_proc), data_proc_if
    )

    encoding = {var: compression for var in data_proc_pm2.data_vars}
    data_proc_pm2.pr.to_netcdf(
        output_folder / (output_filename + terminology_proc + ".nc"), encoding=encoding
    )
