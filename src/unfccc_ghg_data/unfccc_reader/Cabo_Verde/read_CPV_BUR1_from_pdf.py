"""
Read Burundi's BUR1 from pdf
"""

import camelot
import numpy as np
import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import downloaded_data_path, extracted_data_path
from unfccc_ghg_data.unfccc_reader.Cabo_Verde.config_cpv_bur1 import (
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    inv_conf_main,
    inv_conf_per_sector,
    meta_data,
    trend_years,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###

    input_folder = downloaded_data_path / "UNFCCC" / "Cabo_Verde" / "BUR1"
    output_folder = extracted_data_path / "UNFCCC" / "Cabo_Verde"

    if not output_folder.exists():
        output_folder.mkdir()

    pdf_file = "BUR_EN_Digital.pdf"
    output_filename = "CPV_BUR1_2023_"
    category_column = f"category ({coords_terminologies['category']})"
    compression = dict(zlib=True, complevel=9)

    # ###
    # 2. Read sector-specific main tables for 2019
    # ###

    df_main = None
    for page in inv_conf_main["pages"].keys():
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

    # ###
    # 1. Read trend tables 1995, 2000, 2005, 2010, 2015 and 2019
    # ###
    df_trend = None
    for sector in inv_conf_per_sector.keys():
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
            df_page[year] = df_page[year].str.replace(",", "")

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

    data_if = pm2.pm2io.convert_wide_dataframe_if(
        df_trend,
        coords_cols=coords_cols,
        # add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        # coords_value_filling=coords_value_filling,
        # filter_remove=filter_remove,
        # filter_keep=filter_keep,
        meta_data=meta_data,
    )

    ### convert to primap2 format ###
    print("Converting to primap2 format.")
    data_pm2 = pm2.pm2io.from_interchange_format(data_if)
