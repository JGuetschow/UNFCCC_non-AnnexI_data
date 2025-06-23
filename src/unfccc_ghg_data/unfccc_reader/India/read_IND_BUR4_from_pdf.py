"""
Read India's BUR4 from pdf

This script reads data from India's BUR4
Trend data are read from pdf using camelot.
The 2020 inventory is read from csv which was created manually from data
read using camelot as some values were mixed with text and needed manual correction.


"""


import camelot
import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    fix_rows,
    process_data_for_country,
)

# configuration import
from unfccc_ghg_data.unfccc_reader.India.config_ind_bur4 import (
    cat_conversion_inventory,
    cat_conversion_trends,
    coords_cols,
    coords_cols_trends,
    coords_defaults,
    coords_defaults_trends,
    coords_terminologies,
    coords_value_mapping,
    coords_value_mapping_trends,
    filter_remove,
    filter_remove_trends,
    gas_baskets,
    index_cols,
    meta_data,
    page_def_trends,
    terminology_proc,
    unit_info,
)

if __name__ == "__main__":
    ### general configuration
    input_folder = downloaded_data_path / "UNFCCC" / "India" / "BUR4"
    output_folder = extracted_data_path / "UNFCCC" / "India"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "IND_BUR4_2024_"
    inventory_file_pdf = "India_BUR-4.pdf"
    inventory_file_csv = "India_BUR4_2020_inventory.csv"

    compression = dict(zlib=True, complevel=9)

    #### trend tables

    data_trends_pm2 = None
    # read
    for page in page_def_trends:
        table_def = page_def_trends[page]
        tables_trends = camelot.read_pdf(
            str(input_folder / inventory_file_pdf),
            pages=page,
            table_areas=table_def["table_areas"],
            flavor=table_def["flavor"],
        )
        df_trends = tables_trends[0].df

        # fix rows
        if "rows_to_fix" in table_def:
            for n_rows in table_def["rows_to_fix"].keys():
                print(f"Fixing split rows: {n_rows}")
                df_trends = fix_rows(
                    df_trends, table_def["rows_to_fix"][n_rows], 0, n_rows
                )
            df_trends = df_trends.reset_index(drop=True)

        df_trends.columns = df_trends.loc[table_def["entity_row"]]

        # remove unit row
        df_trends = df_trends.drop(
            index=[table_def["entity_row"], table_def["unit_row"]]
        )

        # ###
        # convert to PRIMAP2 interchange format
        # ###
        data_trends_if_page = pm2.pm2io.convert_wide_dataframe_if(
            df_trends,
            coords_cols=coords_cols_trends,
            coords_defaults=coords_defaults_trends,
            coords_terminologies=coords_terminologies,
            coords_value_mapping=coords_value_mapping_trends,
            filter_remove=filter_remove_trends,
            meta_data=meta_data,
            convert_str=True,
            time_format="%Y",
        )

        data_trends_pm2_page = pm2.pm2io.from_interchange_format(data_trends_if_page)
        if data_trends_pm2 is None:
            data_trends_pm2 = data_trends_pm2_page
        else:
            data_trends_pm2 = data_trends_pm2.pr.merge(data_trends_pm2_page)

    # convert back to IF to have units in the fixed format
    data_trends_if = data_trends_pm2.pr.to_interchange_format()

    # ###
    # save raw data to IF and native format
    # ###
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder
        / (output_filename + coords_terminologies["category"] + "_trends_raw"),
        data_trends_if,
    )

    encoding = {var: compression for var in data_trends_pm2.data_vars}
    data_trends_pm2.pr.to_netcdf(
        output_folder
        / (output_filename + coords_terminologies["category"] + "_trends_raw.nc"),
        encoding=encoding,
    )

    # ##############
    # 2020 inventory
    # ##############

    df_inventory = pd.read_csv(input_folder / inventory_file_csv)
    # bring unit and entity infor in standard NIR format
    df_inventory = pm2.pm2io.nir_add_unit_information(df_inventory, **unit_info)
    # set index and convert to long format
    entities = df_inventory.columns.get_level_values(0).to_numpy()
    units = df_inventory.columns.get_level_values(1).to_numpy()
    units[0] = ""
    df_inventory.columns = [entities, units]
    df_inventory = df_inventory.set_index(index_cols)
    header_long = ["category", "entity", "unit", "time", "data"]
    df_inventory_long = pm2.pm2io.nir_convert_df_to_long(
        df_inventory, 2020, header_long
    )

    df_inventory_long = df_inventory_long.reset_index(drop=True)

    # make sure all col headers are str
    df_inventory_long.columns = df_inventory_long.columns.map(str)

    # make sure all cats are str and not int
    df_inventory_long["category"] = df_inventory_long["category"].astype("str")
    df_inventory_long["category"] = df_inventory_long["category"].str.strip()

    data_inventory_if = pm2.pm2io.convert_long_dataframe_if(
        df_inventory_long,
        coords_cols=coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        filter_remove=filter_remove,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )

    # conversion to PRIMAP2 native format
    data_inventory_pm2 = pm2.pm2io.from_interchange_format(data_inventory_if)

    # convert back to IF to have units in the fixed format
    data_inventory_if = data_inventory_pm2.pr.to_interchange_format()

    # ###
    # save raw data to IF and native format
    # ###
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder
        / (output_filename + coords_terminologies["category"] + "_inventory_raw"),
        data_inventory_if,
    )

    encoding = {var: compression for var in data_inventory_pm2.data_vars}
    data_inventory_pm2.pr.to_netcdf(
        output_folder
        / (output_filename + coords_terminologies["category"] + "_inventory_raw.nc"),
        encoding=encoding,
    )

    # #########################################
    # convert 2020 inventory to 2006 categories
    # #########################################

    #### processing
    data_inventory_proc_pm2 = data_inventory_pm2

    # combine CO2 emissions and removals
    temp_CO2 = data_inventory_proc_pm2["CO2 emission"].copy()
    # data_proc_pm2["CO2"] = data_proc_pm2[["CO2 emissions", "CO2 removals"]].to_array()
    # .pr.sum(dim="variable", skipna=True, min_count=1)
    data_inventory_proc_pm2["CO2 removal"] = data_inventory_proc_pm2["CO2 removal"] * -1
    data_inventory_proc_pm2["CO2"] = data_inventory_proc_pm2[
        ["CO2 emission", "CO2 removal"]
    ].pr.sum(dim="entity", skipna=True, min_count=1)
    data_inventory_proc_pm2["CO2"].attrs = temp_CO2.attrs
    data_inventory_proc_pm2["CO2"].attrs["entity"] = "CO2"
    data_inventory_proc_pm2["CO2"] = data_inventory_proc_pm2["CO2"].fillna(temp_CO2)

    # actual processing

    # processing_info_country = {
    #     'remove_ts': remove_ts2019,
    # }

    data_inventory_proc_pm2 = process_data_for_country(
        data_inventory_proc_pm2,
        entities_to_ignore=["CO2 emission", "CO2 removal"],
        gas_baskets=gas_baskets,
        processing_info_country=None,
        cat_terminology_out=terminology_proc,
        category_conversion=cat_conversion_inventory,
        # sectors_out = sectors_to_save,
    )

    # adapt source and metadata
    current_source = data_inventory_proc_pm2.coords["source"].to_numpy()[0]
    data_temp = data_inventory_proc_pm2.pr.loc[{"source": current_source}]
    data_inventory_proc_pm2 = data_inventory_proc_pm2.pr.set(
        "source", "BUR_NIR", data_temp
    )
    data_inventory_proc_pm2 = data_inventory_proc_pm2.pr.loc[{"source": ["BUR_NIR"]}]

    # ######################################
    # convert trends data to 2006 categories
    # ######################################

    #### processing
    data_trends_proc_pm2 = data_trends_pm2

    # actual processing

    terminology_proc = "IPCC2006_PRIMAP"

    data_trends_proc_pm2 = process_data_for_country(
        data_trends_proc_pm2,
        entities_to_ignore=[],
        gas_baskets={},
        cat_terminology_out=terminology_proc,
        category_conversion=cat_conversion_trends,
    )

    # adapt source and metadata
    # TODO: processing info is present twice
    current_source = data_trends_proc_pm2.coords["source"].to_numpy()[0]
    data_temp = data_trends_proc_pm2.pr.loc[{"source": current_source}]
    data_trends_proc_pm2 = data_trends_proc_pm2.pr.set("source", "BUR_NIR", data_temp)
    data_trends_proc_pm2 = data_trends_proc_pm2.pr.loc[{"source": ["BUR_NIR"]}]

    # combine two datasets and save data
    data_pm2 = data_inventory_proc_pm2.pr.merge(data_trends_proc_pm2)

    # convert back to IF to have units in the fixed format
    data_if = data_pm2.pr.to_interchange_format()

    # ###
    # save processed data to IF and native format
    # ###
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + terminology_proc),
        data_if,
    )

    encoding = {var: compression for var in data_pm2.data_vars}
    data_pm2.pr.to_netcdf(
        output_folder / (output_filename + terminology_proc),
        encoding=encoding,
    )
