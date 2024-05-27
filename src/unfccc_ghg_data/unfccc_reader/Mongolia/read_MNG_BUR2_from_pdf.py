"""
Read Mongolia's BUR2 from pdf
"""
# TODO: Delete when this is finished
import os

os.environ[
    "UNFCCC_GHG_ROOT_PATH"
] = "/Users/danielbusch/Documents/UNFCCC_non-AnnexI_data/"

import camelot  # noqa: E402
import pandas as pd  # noqa: E402
from config_mng_bur2 import (  # noqa: E402
    coords_terminologies,
)

from unfccc_ghg_data.helper import (  # noqa: E402
    downloaded_data_path,
    extracted_data_path,
    fix_rows,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###

    input_folder = downloaded_data_path / "UNFCCC" / "Mongolia" / "BUR2"
    output_folder = extracted_data_path / "UNFCCC" / "Mongolia"

    if not output_folder.exists():
        output_folder.mkdir()

    pdf_file = "20231112_NIR_MGL.pdf"
    output_filename = "MNG_BUR2_2023_"
    category_column = f"category ({coords_terminologies['category']})"
    compression = dict(zlib=True, complevel=9)

    def repl(m):  # noqa: D103
        return m.group("code")

    # ###
    # 1. Read in main tables
    # ###

    # df_main = None
    # for year in inv_conf_per_year.keys():
    #     print("-" * 60)
    #     print(f"Reading year {year}.")
    #     print("-" * 60)
    #     df_year = None
    #     for page in inv_conf_per_year[year]["page_defs"].keys():
    #         print(f"Reading table from page {page}.")
    #         tables_inventory_original = camelot.read_pdf(
    #             str(input_folder / pdf_file),
    #             pages=page,
    #             table_areas=inv_conf_per_year[year]["page_defs"][page]["area"],
    #             columns=inv_conf_per_year[year]["page_defs"][page]["cols"],
    #             flavor="stream",
    #             split_text=True,
    #         )
    #         print("Reading complete.")
    #
    #         df_page = tables_inventory_original[0].df
    #
    #         if df_year is None:
    #             df_year = df_page
    #         else:
    #             df_year = pd.concat(
    #                 [df_year, df_page],
    #                 axis=0,
    #                 join="outer",
    #             ).reset_index(drop=True)
    #
    #     print(f"Concatenating all tables for {year}.")
    #
    #     # fix content that spreads across multiple rows
    #     if "rows_to_fix" in inv_conf_per_year[year]:
    #         for n_rows in inv_conf_per_year[year]["rows_to_fix"].keys():
    #             print(f"Merge content for {n_rows=}")
    #             df_year = fix_rows(
    #                 df_year,
    #                 rows_to_fix=inv_conf_per_year[year]["rows_to_fix"][n_rows],
    #                 col_to_use=0,
    #                 n_rows=n_rows,
    #             )
    #
    #     df_header = pd.DataFrame([inv_conf["header"], inv_conf["unit"]])
    #
    #     skip_rows = 11
    #     df_year = pd.concat(
    #         [df_header, df_year[skip_rows:]], axis=0, join="outer"
    #     ).reset_index(drop=True)
    #
    #     df_year = pm2.pm2io.nir_add_unit_information(
    #         df_year,
    #         unit_row=inv_conf["unit_row"],
    #         entity_row=inv_conf["entity_row"],
    #         regexp_entity=".*",
    #         regexp_unit=".*",
    #         default_unit="Gg",
    #     )
    #
    #     print("Added unit information.")
    #
    #     # set index
    #     df_year = df_year.set_index(inv_conf["index_cols"])
    #
    #     # convert to long format
    #     df_year_long = pm2.pm2io.nir_convert_df_to_long(
    #         df_year, year, inv_conf["header_long"]
    #     )
    #
    #     # extract from tuple
    #     df_year_long["orig_cat_name"] = df_year_long["orig_cat_name"].str[0]
    #
    #     # prep for conversion to PM2 IF and native format
    #     # make a copy of the categories row
    #     df_year_long["category"] = df_year_long["orig_cat_name"]
    #
    #     # replace cat names by codes in col "category"
    #     # first the manual replacements
    #
    #     df_year_long["category"] = df_year_long["category"].replace(
    #         inv_conf["cat_codes_manual"]
    #     )
    #
    #     df_year_long["category"] = df_year_long["category"].str.replace(".", "")
    #
    #     # then the regex replacements
    #     df_year_long["category"] = df_year_long["category"].str.replace(
    #         inv_conf["cat_code_regexp"], repl, regex=True
    #     )
    #
    #     df_year_long = df_year_long.reset_index(drop=True)
    #
    #     df_year_long["data"] = df_year_long["data"].str.replace(",", "")
    #
    #     # make sure all col headers are str
    #     df_year_long.columns = df_year_long.columns.map(str)
    #
    #     df_year_long = df_year_long.drop(columns=["orig_cat_name"])
    #
    #     if df_main is None:
    #         df_main = df_year_long
    #     else:
    #         df_main = pd.concat(
    #             [df_main, df_year_long],
    #             axis=0,
    #             join="outer",
    #         ).reset_index(drop=True)
    #
    # ### convert to interchange format ###
    # print("Converting to interchange format.")
    # df_main_IF = pm2.pm2io.convert_long_dataframe_if(
    #     df_main,
    #     coords_cols=coords_cols,
    #     coords_defaults=coords_defaults,
    #     coords_terminologies=coords_terminologies,
    #     coords_value_mapping=coords_value_mapping,
    #     filter_remove=filter_remove,
    #     meta_data=meta_data,
    #     convert_str=True,
    #     time_format="%Y",
    # )
    #
    # ### convert to primap2 format ###
    # print("Converting to primap2 format.")
    # data_main_pm2 = pm2.pm2io.from_interchange_format(df_main_IF)
    #
    # # ###
    # # 2. Read in trend tables
    # # ###
    #
    # df_trend = None
    # for entity in inv_conf_per_entity.keys():
    #     print("-" * 60)
    #     print(f"Reading entity {entity}.")
    #
    #     df_entity = None
    #
    #     for page in inv_conf_per_entity[entity]["page_defs"].keys():
    #         print(f"Reading page {page}.")
    #
    #         tables_inventory_original = camelot.read_pdf(
    #             str(input_folder / pdf_file),
    #             pages=page,
    #             table_areas=inv_conf_per_entity[entity]["page_defs"][page]["area"],
    #             columns=inv_conf_per_entity[entity]["page_defs"][page]["cols"],
    #             flavor="stream",
    #             split_text=True,
    #         )
    #         df_page = tables_inventory_original[0].df
    #
    #         if df_entity is None:
    #             df_entity = df_page
    #         else:
    #             df_entity = pd.concat(
    #                 [df_entity, df_page],
    #                 axis=0,
    #                 join="outer",
    #             ).reset_index(drop=True)
    #         print(f"adding table from page {page}.")
    #
    #     if "rows_to_fix" in inv_conf_per_entity[entity]:
    #         for n_rows in inv_conf_per_entity[entity]["rows_to_fix"].keys():
    #             print(f"Merge content for {n_rows=}")
    #             df_entity = fix_rows(
    #                 df_entity,
    #                 rows_to_fix=inv_conf_per_entity[entity]["rows_to_fix"][n_rows],
    #                 col_to_use=0,
    #                 n_rows=n_rows,
    #             )
    #
    #     df_entity.columns = df_entity.iloc[0, :]
    #     df_entity = df_entity[1:]
    #
    #     # unit is always Gg
    #     df_entity.loc[:, "unit"] = inv_conf_per_entity[entity]["unit"]
    #
    #     # only one entity per table
    #     df_entity.loc[:, "entity"] = entity
    #
    #     # TODO: Fix pandas "set value on slice of copy" warning
    #     df_entity.loc[:, "category"] = df_entity.loc[
    #         :, inv_conf_per_entity[entity]["category_column"]
    #     ]
    #
    #     if "rows_to_drop" in inv_conf_per_entity[entity]:
    #         for row in inv_conf_per_entity[entity]["rows_to_drop"]:
    #             row_to_delete = df_entity.index[df_entity["category"] == row][0]
    #             df_entity = df_entity.drop(index=row_to_delete)
    #
    #     df_entity.loc[:, "category"] = df_entity.loc[:, "category"].replace(
    #         inv_conf_per_entity[entity]["cat_codes_manual"]
    #     )
    #
    #     df_entity.loc[:, "category"] = df_entity["category"].str.replace(
    #         inv_conf["cat_code_regexp"], repl, regex=True
    #     )
    #
    #     df_entity = df_entity.drop(
    #         columns=inv_conf_per_entity[entity]["columns_to_drop"]
    #     )
    #
    #     for year in inv_conf_per_entity[entity]["years"]:
    #         df_entity.loc[:, year] = df_entity[year].str.replace(",", "")
    #
    #     if df_trend is None:
    #         df_trend = df_entity
    #     else:
    #         df_trend = pd.concat(
    #             [df_trend, df_entity],
    #             axis=0,
    #             join="outer",
    #         ).reset_index(drop=True)
    #
    # ### convert to interchange format ###
    # df_trend_IF = pm2.pm2io.convert_wide_dataframe_if(
    #     data_wide=df_trend,
    #     coords_cols=coords_cols,
    #     coords_defaults=coords_defaults,
    #     coords_terminologies=coords_terminologies,
    #     coords_value_mapping=coords_value_mapping,
    #     # filter_remove=filter_remove,
    #     meta_data=meta_data,
    #     convert_str=True,
    #     time_format="%Y",
    # )
    #
    # ### convert to primap2 format ###
    # print("Converting to primap2 format.")
    # data_trend_pm2 = pm2.pm2io.from_interchange_format(df_trend_IF)

    # ###
    # 3. Read in aggregated tables from 1990 - 2020
    # ###

    # Work in progress
    # noinspection PyInterpreter
    inv_conf_per_sector = {
        "total": {
            "page_defs": {
                "32": {
                    "area": ["64,649,547,106"],
                    "cols": ["106,182,237,294,345,403,480"],
                },
            },
            "entity": "KYOTOGHG (SARGWP100)",
            # "category_column": "Categories",
            # "columns_to_drop": ["Categories"],
            # "years": ["1990", "1995", "2000", "2005", "2010", "2015", "2020"],
            "unit": "Gg CO2e",
            "last_year": "2020",
            "rows_to_fix": {
                -3: [
                    "Year",
                ],
            },
            "year_column": " Year ",
            # TODO some categories are not recognized!
            "cat_codes_manual": {
                "Energy": "1",
                "IPPU": "2",
                "Agriculture": "3",
                "Waste": "4",
                "LULUCF": "M.LULUCF",
                "Total (excl. LULUCF)": "M.0.EL",
                "Total (incl. LULUCF)": "M.0",
            },
        },
        "energy": {
            "page_defs": {
                "43": {
                    "area": ["59,478,544,79"],
                    "cols": ["97,160,220,262,338,388,452,502"],
                },
                "44": {
                    "area": ["60,773,546,582"],
                    "cols": ["103,165,226,274,329,384,444,494"],
                },
            },
            "entity": "KYOTOGHG (SARGWP100)",
            # "category_column" : "Categories",
            # "columns_to_drop" : ["Categories"],
            # "years" : ["1990", "1995", "2000", "2005", "2010", "2015", "2020"],
            "unit": "Gg CO2e",
            "last_year": "2020",
            "rows_to_fix": {
                11: [
                    "Years",
                ],
            },
            "rows_to_drop": [0, 2],
            "year_column": "Years     ",
            "cat_codes_manual": {
                r" 1.A.1.a.i Electricity  generation  ": "1.A.1.a.i",
                r" 1.A.1.a.ii  Combined  heat and ipower peneration (CHP)": "1.A.1.a.ii",  # noqa: E501
                r" 1.A.1.c.ii  Other  energy ndustries ": "1.A.1.c.ii",
                r"Manufacturing industries and  construction   ": "1.A.2",
                r" 1.A.3.a 1 Civil  aviation t  ": "1.A.3.a",
                r" .A.3.b Road  ransportation  ": "1.A.3.b",
                r" 1.A.3.c Railways    ": "1.A.3.c",
                r" 1.A.3.e.ii  Off-road   ": "1.A.3.e.ii",
            },
        },
    }

    df_agg = None
    for sector in inv_conf_per_sector.keys():
        print("-" * 60)
        print(f"Reading sector {sector}.")

        df_sector = None

        for page in [*inv_conf_per_sector[sector]["page_defs"]]:
            tables_inventory_original = camelot.read_pdf(
                str(input_folder / pdf_file),
                pages=page,
                table_areas=inv_conf_per_sector[sector]["page_defs"][page]["area"],
                columns=inv_conf_per_sector[sector]["page_defs"][page]["cols"],
                flavor="stream",
                split_text=True,
            )

            df_sector_page = tables_inventory_original[0].df

            if df_sector is None:
                df_sector = df_sector_page
            else:
                df_sector = pd.concat(
                    [df_sector, df_sector_page],
                    axis=0,
                    join="outer",
                ).reset_index(drop=True)

            print(f"adding table from page {page}.")

        last_row = df_sector.loc[df_sector[0] == "2020"].index[0]

        df_sector = df_sector[0 : last_row + 1]

        if "rows_to_fix" in inv_conf_per_sector[sector]:
            for n_rows in inv_conf_per_sector[sector]["rows_to_fix"].keys():
                print(f"Merge content for {n_rows=}")
                df_sector = fix_rows(
                    df_sector,
                    rows_to_fix=inv_conf_per_sector[sector]["rows_to_fix"][n_rows],
                    col_to_use=0,
                    n_rows=n_rows,
                )

        df_sector = df_sector.reset_index(drop=True)

        if "rows_to_drop" in inv_conf_per_sector[sector]:
            for row in inv_conf_per_sector[sector]["rows_to_drop"]:
                df_sector = df_sector.drop(index=row)

        df_sector = df_sector.set_index(0)

        # transpose so categegories are in first columns
        df_sector = df_sector.T

        df_sector = df_sector.rename(
            columns={inv_conf_per_sector[sector]["year_column"]: "category"}
        )

        # unit is always Gg
        df_sector.loc[:, "unit"] = inv_conf_per_sector[sector]["unit"]

        # only one entity per table
        df_sector.loc[:, "entity"] = inv_conf_per_sector[sector]["entity"]

        df_sector["category"] = df_sector["category"].str.replace("\n", "")

        df_sector.loc[:, "category"] = df_sector.loc[:, "category"].replace(
            inv_conf_per_sector[sector]["cat_codes_manual"]
        )

        if df_sector is None:
            df_agg = df_sector
        else:
            df_agg = pd.concat(
                [df_agg, df_sector],
                axis=0,
                join="outer",
            ).reset_index(drop=True)

        for year in [str(y) for y in range(1990, 2021)]:
            df_agg.loc[:, year] = df_agg[year].str.replace(",", "")

        print(df_agg)

    # # ###
    # # Merge main and trend tables.
    # # ###
    #
    # print("Merging main and trend table.")
    # data_pm2 = data_main_pm2.pr.merge(data_trend_pm2, tolerance=1)
    #
    # # ###
    # # Save raw data to IF and native format.
    # # ###
    #
    # data_if = data_pm2.pr.to_interchange_format()
    #
    # pm2.pm2io.write_interchange_format(
    #     output_folder / (output_filename + coords_terminologies["category"] + "_raw"),
    #     data_if,
    # )
    #
    # encoding = {var: compression for var in data_pm2.data_vars}
    # data_pm2.pr.to_netcdf(
    #     output_folder
    #     / (output_filename + coords_terminologies["category"] + "_raw.nc"),
    #     encoding=encoding,
    # )
    #
    # # ###
    # # Processing
    # # ###
    #
    # data_proc_pm2 = process_data_for_country(
    #     data_country=data_pm2,
    #     entities_to_ignore=[],
    #     gas_baskets=gas_baskets,
    #     filter_dims=None,
    #     cat_terminology_out=None,
    #     category_conversion=None,
    #     sectors_out=None,
    #     processing_info_country=country_processing_step1,
    # )
    #
    # # ###
    # # save processed data to IF and native format
    # # ###
    #
    # terminology_proc = coords_terminologies["category"]
    #
    # data_proc_if = data_proc_pm2.pr.to_interchange_format()
    #
    # if not output_folder.exists():
    #     output_folder.mkdir()
    # pm2.pm2io.write_interchange_format(
    #     output_folder / (output_filename + terminology_proc), data_proc_if
    # )
    #
    # encoding = {var: compression for var in data_proc_pm2.data_vars}
    # data_proc_pm2.pr.to_netcdf(
    #     output_folder / (output_filename + terminology_proc + ".nc"),
    #     encoding=encoding
    # )
    #
    # print("Saved processed data.")
