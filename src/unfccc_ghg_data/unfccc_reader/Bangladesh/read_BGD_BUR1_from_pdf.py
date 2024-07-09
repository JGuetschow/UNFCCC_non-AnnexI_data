"""
Read Bangladesh's BUR1 from pdf
"""

import camelot
import pandas as pd
from config_bgd_bur1 import coords_terminologies, inv_conf_per_year

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

    # ###
    # 1. Read in main tables from the Annex
    # ###

    df_year = None
    for year in inv_conf_per_year.keys():
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
        pass
        # df_header = pd.DataFrame([inv_conf["header"], inv_conf["unit"]])
        #
        # skip_rows = 11
        # df_year = pd.concat(
        #     [df_header, df_year[skip_rows:]], axis=0, join="outer"
        # ).reset_index(drop=True)
        #
        # df_year = pm2.pm2io.nir_add_unit_information(
        #     df_year,
        #     unit_row=inv_conf["unit_row"],
        #     entity_row=inv_conf["entity_row"],
        #     regexp_entity=".*",
        #     regexp_unit=".*",
        #     default_unit="Gg",
        # )
        #
        # print("Added unit information.")
        #
        # # set index
        # df_year = df_year.set_index(inv_conf["index_cols"])
        #
        # # convert to long format
        # df_year_long = pm2.pm2io.nir_convert_df_to_long(
        #     df_year, year, inv_conf["header_long"]
        # )
        #
        # # extract from tuple
        # df_year_long["orig_cat_name"] = df_year_long["orig_cat_name"].str[0]
        #
        # # prep for conversion to PM2 IF and native format
        # # make a copy of the categories row
        # df_year_long["category"] = df_year_long["orig_cat_name"]
        #
        # # replace cat names by codes in col "category"
        # # first the manual replacements
        #
        # df_year_long["category"] = df_year_long["category"].replace(
        #     inv_conf["cat_codes_manual"]
        # )
        #
        # df_year_long["category"] = df_year_long["category"].str.replace(".", "")
        #
        # # then the regex replacements
        # df_year_long["category"] = df_year_long["category"].str.replace(
        #     inv_conf["cat_code_regexp"], repl, regex=True
        # )
        #
        # df_year_long = df_year_long.reset_index(drop=True)
        #
        # df_year_long["data"] = df_year_long["data"].str.replace(",", "")
        #
        # # make sure all col headers are str
        # df_year_long.columns = df_year_long.columns.map(str)
        #
        # df_year_long = df_year_long.drop(columns=["orig_cat_name"])
        #
        # if df_main is None:
        #     df_main = df_year_long
        # else:
        #     df_main = pd.concat(
        #         [df_main, df_year_long],
        #         axis=0,
        #         join="outer",
        #     ).reset_index(drop=True)
