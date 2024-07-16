"""
Read Bangladesh's BUR1 from pdf
"""

import camelot
import numpy as np
import pandas as pd
import primap2 as pm2
from config_bgd_bur1 import (
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    filter_remove,
    inv_conf,
    inv_conf_per_year,
    meta_data,
)

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    fix_rows,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###

    input_folder = downloaded_data_path / "UNFCCC" / "Bangladesh" / "BUR1"
    output_folder = extracted_data_path / "UNFCCC" / "Bangladesh"

    if not output_folder.exists():
        output_folder.mkdir()

    pdf_file = "Updated_BUR1_Report_15_11_2023.pdf"
    output_filename = "BGD_BUR1_2023_"
    category_column = f"category ({coords_terminologies['category']})"
    compression = dict(zlib=True, complevel=9)

    def repl(m):  # noqa: D103
        return m.group("code")

    # ###
    # 1. Read in main tables from the Annex
    # ###
    df_main = None
    df_year = None
    for year in reversed(list(inv_conf_per_year.keys())):
        print("-" * 60)
        print(f"Reading year {year}.")
        print("-" * 60)
        df_year = None
        for page in inv_conf_per_year[year]["page_defs"].keys():
            print(f"Reading table from page {page}.")

            # read from PDF
            tables_inventory_original = camelot.read_pdf(
                str(input_folder / pdf_file),
                pages=page,
                table_areas=inv_conf_per_year[year]["page_defs"][page]["area"],
                columns=inv_conf_per_year[year]["page_defs"][page]["cols"],
                flavor="stream",
                split_text=False,
            )
            print("Reading complete.")

            df_page = tables_inventory_original[0].df

            # cut rows at the top if needed
            skip_rows_start = inv_conf_per_year[year]["page_defs"][page][
                "skip_rows_start"
            ]
            if not skip_rows_start == 0:
                df_page = df_page[skip_rows_start:]

            # cut rows at the bottom if needed
            skip_rows_end = inv_conf_per_year[year]["page_defs"][page]["skip_rows_end"]
            if not skip_rows_end == 0:
                df_page = df_page[:-skip_rows_end]

            # stack the tables vertically
            if df_year is None:
                df_year = df_page
            else:
                df_year = pd.concat(
                    [
                        df_year,
                        df_page,
                    ],
                    axis=0,
                    join="outer",
                ).reset_index(drop=True)

        # fix content that spreads across multiple rows
        if "rows_to_fix" in inv_conf_per_year[year]:
            for n_rows in inv_conf_per_year[year]["rows_to_fix"].keys():
                print(f"Merge content for {n_rows=}")
                df_year = fix_rows(
                    df_year,
                    rows_to_fix=inv_conf_per_year[year]["rows_to_fix"][n_rows],
                    col_to_use=0,
                    n_rows=n_rows,
                )

        df_header = pd.DataFrame(
            [inv_conf_per_year[year]["header"], inv_conf_per_year[year]["unit"]]
        )
        skip_rows = inv_conf_per_year[year]["skip_rows"]

        df_year = pd.concat(
            [df_header, df_year[skip_rows:]], axis=0, join="outer"
        ).reset_index(drop=True)

        df_year = pm2.pm2io.nir_add_unit_information(
            df_year,
            unit_row=1,
            entity_row=0,
            regexp_entity=".*",
            regexp_unit=".*",
            default_unit="Gg",
        )

        print("Added unit information.")

        # set index
        df_year = df_year.set_index(inv_conf["index_cols"])

        # convert to long format
        df_year_long = pm2.pm2io.nir_convert_df_to_long(
            df_year, year, inv_conf["header_long"]
        )

        # extract from tuple
        df_year_long["orig_cat_name"] = df_year_long["orig_cat_name"].str[0]

        # prep for conversion to PM2 IF and native format
        # make a copy of the categories row
        df_year_long["category"] = df_year_long["orig_cat_name"]

        # first the manual replacements
        df_year_long["category"] = df_year_long["category"].replace(
            inv_conf_per_year[year]["cat_codes_manual"]
        )

        # Remove dots between letters in category codes
        df_year_long["category"] = df_year_long["category"].str.replace(".", "")
        # Some categories have a dash between the letters
        df_year_long["category"] = df_year_long["category"].str.replace("-", " ")

        # then the regex replacements
        df_year_long["category"] = df_year_long["category"].str.replace(
            inv_conf["cat_code_regexp"], repl, regex=True
        )

        df_year_long = df_year_long.reset_index(drop=True)

        # make sure all col headers are str
        df_year_long.columns = df_year_long.columns.map(str)

        df_year_long = df_year_long.drop(columns=["orig_cat_name"])

        # TODO Is there a better way to do this?
        # merge duplicate categories and sum their values
        if "merge_cats" in inv_conf_per_year[year]:
            cat = inv_conf_per_year[year]["merge_cats"]
            # filter by category to be merged
            df_temp = df_year_long.loc[df_year_long["category"] == cat]
            df_temp = df_temp.replace("", np.nan)
            df_temp["data"] = df_temp["data"].apply(float)
            # sum values for duplicate entries
            df_temp = df_temp.groupby(
                ["entity", "unit", "time", "category"], as_index=False
            )["data"].sum()
            # change back to empty strings
            df_temp = df_temp.replace(0, "")
            # drop category from df
            df_year_long = df_year_long.drop(
                df_year_long[df_year_long["category"] == cat].index
            )
            # append the summed up sub-set
            df_year_long = pd.concat(
                [df_temp, df_year_long],
                axis=0,
                join="outer",
            ).reset_index(drop=True)

        if df_main is None:
            df_main = df_year_long
        else:
            df_main = pd.concat(
                [df_main, df_year_long],
                axis=0,
                join="outer",
            ).reset_index(drop=True)

    ### convert to interchange format ###
    print("Converting to interchange format.")
    df_main_IF = pm2.pm2io.convert_long_dataframe_if(
        df_main,
        coords_cols=coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        filter_remove=filter_remove,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )
    pass
