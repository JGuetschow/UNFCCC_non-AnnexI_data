"""
Read Burundi's BUR1 from pdf
"""

import camelot
import numpy as np
import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.Cabo_Verde.config_cpv_bur1 import (
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    coords_value_mapping_main,
    country_processing_step1,
    filter_remove,
    inv_conf,
    inv_conf_main,
    inv_conf_per_sector,
    meta_data,
    trend_years,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###

    # for regex later
    def repl(m):  # noqa: D103
        return m.group("code")

    input_folder = downloaded_data_path / "UNFCCC" / "Cabo_Verde" / "BUR1"
    output_folder = extracted_data_path / "UNFCCC" / "Cabo_Verde"

    if not output_folder.exists():
        output_folder.mkdir()

    pdf_file = "BUR_EN_Digital.pdf"
    output_filename = "CPV_BUR1_2023_"
    category_column = f"category ({coords_terminologies['category']})"
    compression = dict(zlib=True, complevel=9)

    # ###
    # 1. Read sector-specific main tables for 2019
    # ###

    df_main = None
    for page in reversed(inv_conf_main["pages"].keys()):
        print(f"Read table on page {page}")
        tables_inventory_original = camelot.read_pdf(
            str(input_folder / pdf_file),
            pages=page,
            flavor="lattice",
            split_text=True,
        )

        df_page = tables_inventory_original[0].df

        skip_rows_start = inv_conf_main["pages"][page]["skip_rows_start"]
        if not skip_rows_start == 0:
            df_page = df_page[skip_rows_start:]

        df_page.columns = inv_conf_main["pages"][page]["column_names"]

        # first the manual replacements
        df_page["category"] = df_page["category"].replace(
            inv_conf_main["pages"][page]["cat_codes_manual"]
        )

        # Remove dots between letters in category codes
        df_page["category"] = df_page["category"].str.replace(".", "")
        # Some categories have a dash between the letters
        df_page["category"] = df_page["category"].str.replace("-", " ")

        # then the regex replacements
        df_page["category"] = df_page["category"].str.replace(
            inv_conf["cat_code_regexp"], repl, regex=True
        )

        df_page = pd.melt(
            df_page,
            id_vars="category",
            value_vars=inv_conf_main["pages"][page]["entities"],
        )

        df_page = df_page.rename({"value": "data", "variable": "entity"}, axis=1)

        df_page["data"] = df_page["data"].str.replace(",", ".")

        # df_page["unit"] = df_page["entity"]

        # set unit based on entity
        df_page["unit"] = df_page["entity"].replace(
            inv_conf_main["pages"][page]["unit_for_entity"]
        )

        # stack the tables vertically
        if df_main is None:
            df_main = df_page
        else:
            df_main = pd.concat(
                [
                    df_main,
                    df_page,
                ],
                axis=0,
                join="outer",
            ).reset_index(drop=True)

    df_main["time"] = inv_conf["year"]

    # remove wrong codes in data column
    df_main["data"] = df_main["data"].str.replace("HFC", "")

    # Sum up the values for duplicate categories
    cat = inv_conf["merge_cats"]
    df_temp = df_main.loc[df_main["category"] == cat]
    df_temp["data"] = df_temp["data"].replace("", np.nan).apply(float)
    df_temp = df_temp.groupby(
        ["category", "entity", "unit", "time"], as_index=False
    ).sum()
    # change back to empty strings
    df_temp = df_temp.replace(0, "")
    # drop category from df
    df_main = df_main.drop(df_main[df_main["category"] == cat].index)
    # append the summed up sub-set
    df_main = pd.concat(
        [df_main, df_temp],
        axis=0,
        join="outer",
    ).reset_index(drop=True)

    df_main_if = pm2.pm2io.convert_long_dataframe_if(
        df_main,
        coords_cols=coords_cols,
        # add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping_main,
        # coords_value_filling=coords_value_filling,
        filter_remove=filter_remove,
        # filter_keep=filter_keep,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )

    ### convert to primap2 format ###
    print("Converting to primap2 format.")
    data_main_pm2 = pm2.pm2io.from_interchange_format(df_main_if)

    # ###
    # 2. Read trend tables 1995, 2000, 2005, 2010, 2015 and 2019
    # ###
    df_trend = None
    for sector in reversed(inv_conf_per_sector.keys()):
        tables_inventory_original = camelot.read_pdf(
            str(input_folder / pdf_file),
            pages=inv_conf_per_sector[sector]["page"],
            flavor="lattice",
            split_text=True,
        )

        df_page = tables_inventory_original[0].df

        # cut rows at the top if needed
        skip_rows_start = inv_conf_per_sector[sector]["skip_rows_start"]
        if not skip_rows_start == 0:
            df_page = df_page[skip_rows_start:]

        # drop columns if needed
        if "drop_cols" in inv_conf_per_sector[sector].keys():
            # print(df_current.columns.to_numpy())
            df_page = df_page.drop(columns=inv_conf_per_sector[sector]["drop_cols"])

        df_page.columns = inv_conf_per_sector[sector]["header"]

        # fill empty strings with NaN and the forward fill category names
        df_page["category"] = df_page["category"].replace("", np.nan).ffill()

        # remove /n from category names
        df_page["category"] = df_page["category"].str.replace("\n", "")
        # manual replacement of categories
        df_page["category"] = df_page["category"].replace(
            inv_conf_per_sector[sector]["cat_codes_manual"]
        )

        # remove all thousand separator commas
        for year in trend_years:
            df_page[year] = df_page[year].str.replace(",", ".")

        # add unit
        df_page["unit"] = inv_conf_per_sector[sector]["unit"]

        # add entity if needed
        if "entity" in inv_conf_per_sector[sector].keys():
            df_page["entity"] = inv_conf_per_sector[sector]["entity"]

        # stack the tables vertically
        if df_trend is None:
            df_trend = df_page
        else:
            df_trend = pd.concat(
                [
                    df_trend,
                    df_page,
                ],
                axis=0,
                join="outer",
            ).reset_index(drop=True)

    df_trend_if = pm2.pm2io.convert_wide_dataframe_if(
        df_trend,
        coords_cols=coords_cols,
        # add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        # coords_value_filling=coords_value_filling,
        filter_remove=filter_remove,
        # filter_keep=filter_keep,
        meta_data=meta_data,
    )

    ### convert to primap2 format ###
    print("Converting to primap2 format.")
    data_trend_pm2 = pm2.pm2io.from_interchange_format(df_trend_if)

    # ###
    # Merge the main table for 2019 and the trend tables
    # ###

    print("Merging main table and trend tables")
    print("Merging waste table.")
    data_pm2 = data_main_pm2.pr.merge(data_trend_pm2)  # , tolerance=0.10)

    # # ###
    # # Save raw data to IF and native format.
    # # ###

    data_if = data_pm2.pr.to_interchange_format()

    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"] + "_raw"),
        data_if,
    )

    encoding = {var: compression for var in data_pm2.data_vars}
    data_pm2.pr.to_netcdf(
        output_folder
        / (output_filename + coords_terminologies["category"] + "_raw.nc"),
        encoding=encoding,
    )

    # # ###
    # # Processing
    # # ###

    # create the gas baskets before aggregating the categories
    # data_proc_pm2_gas_baskets = process_data_for_country(
    #     data_country=data_pm2,
    #     entities_to_ignore=[],
    #     gas_baskets=gas_baskets,
    #     filter_dims=None,
    #     cat_terminology_out=None,
    #     category_conversion=None,
    #     sectors_out=None,
    #     processing_info_country=None,
    # )

    data_proc_pm2 = process_data_for_country(
        data_country=data_pm2,
        entities_to_ignore=[],
        gas_baskets=None,
        filter_dims=None,
        cat_terminology_out=None,
        category_conversion=None,
        sectors_out=None,
        processing_info_country=country_processing_step1,
    )

    # # ###
    # # save processed data to IF and native format
    # # ###

    terminology_proc = coords_terminologies["category"]

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

    print("Saved processed data.")
