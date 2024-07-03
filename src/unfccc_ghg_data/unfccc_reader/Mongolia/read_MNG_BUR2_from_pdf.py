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
import primap2 as pm2  # noqa: E402
from config_mng_bur2 import (  # noqa: E402
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    meta_data,
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
    # 2.5 Read harvested wood products table
    # ###

    # The table for harvested wood products is in a different format
    # and needs to be read in separately.

    inv_conf_harvested_wood_products = {
        'page' : '151',
        "category_column" : 'Categories',
        "cat_codes_manual" : {
            'GHG emission' : '3.D.1',
        },
        'unit' : 'Gg',
        'entity' : 'CO2',
        'parts' : {
            "part_1" : {
                "page_defs" :
                    {
                        "area" : ["52,690,555,647"],
                        "cols" : ["101,149,196,231,268,310,351,398,433,476,514"],
                    },
                "rows_to_fix" : {
                    3 : [
                        "GHG",
                    ],
                },
            },
            "part_2" : {
                "page_defs" :
                    {
                        "area" : ["52,637,555,596"],
                        "cols" : ["99,150,197,239,281,326,372,425,469,516"],
                    },
                "rows_to_fix" : {
                    3 : [
                        "GHG",
                    ],
                },
            },
            "part_3" : {
                "page_defs" :
                    {
                        "area" : ["52,591,550,547"],
                        "cols" : ["106,156,197,239,281,326,372,420,465,509"],
                    },
                "rows_to_fix" : {
                    3 : [
                        "GHG",
                    ],
                },
            }},
    }

    print("-" * 60)
    print(
        f"Reading sector harvested wood products table."
    )

    df_hwp = None
    for part in [*inv_conf_harvested_wood_products['parts']] :
        tables_inventory_original = camelot.read_pdf(
            str(input_folder / pdf_file),
            pages=inv_conf_harvested_wood_products['page'],
            table_areas=inv_conf_harvested_wood_products['parts'][part]["page_defs"]["area"],
            columns=inv_conf_harvested_wood_products['parts'][part]["page_defs"]["cols"],
            flavor="stream",
            split_text=True,
        )

        df_hwp_part = tables_inventory_original[0].df

        if "rows_to_fix" in inv_conf_harvested_wood_products['parts'][part]:
            for n_rows in inv_conf_harvested_wood_products['parts'][part]["rows_to_fix"].keys():
                df_hwp_part = fix_rows(
                    df_hwp_part,
                    rows_to_fix=inv_conf_harvested_wood_products['parts'][part]["rows_to_fix"][n_rows],
                    col_to_use=0,
                    n_rows=n_rows,
                )

        df_hwp_part = df_hwp_part.drop(1, axis=0).reset_index(drop=True)

        if df_hwp is None :
            df_hwp = df_hwp_part
        else :
            df_hwp = pd.concat(
                [df_hwp, df_hwp_part.drop(0, axis=1)],
                axis=1,
                join="outer",
            ).reset_index(drop=True)

    df_hwp = pd.DataFrame(df_hwp.values[1 :], columns=df_hwp.iloc[0])

    df_hwp = df_hwp.rename(
        columns={inv_conf_harvested_wood_products["category_column"] : "category"}
    )

    df_hwp.loc[:, "category"] = df_hwp.loc[:, "category"].replace(
        inv_conf_harvested_wood_products["cat_codes_manual"]
    )


    # unit is always the same
    df_hwp.loc[:, "unit"] = inv_conf_harvested_wood_products["unit"]

    # and only one entity per table
    df_hwp.loc[:, "entity"] = inv_conf_harvested_wood_products["entity"]

    # ###
    # 3. Read in aggregated tables from 1990 - 2020
    # ###

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
                " Energy ": "1",
                " IPPU ": "2",
                " Agriculture ": "3",
                " Waste ": "4",
                " LULUCF ": "M.LULUCF",
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
        "energy cont": {
            "page_defs": {
                "44": {
                    "area": ["59,552,553,84"],
                    "cols": ["103,173,219,274,330,382,443,494"],
                },
            },
            "entity": "KYOTOGHG (SARGWP100)",
            # "category_column" : "Categories",
            # "columns_to_drop" : ["Categories"],
            # "years" : ["1990", "1995", "2000", "2005", "2010", "2015", "2020"],
            "unit": "Gg CO2e",
            "last_year": "2020",
            "rows_to_fix": {
                8: [
                    "Years",
                ],
            },
            "rows_to_drop": [0, 2],
            "year_column": "Years    ",
            "cat_codes_manual": {
                "Other sectors 1.A.4.a Commercial/ Institutional  ": "1.A.4.a",
                " 1.A.4.b Residen-tial  ": "1.A.4.b",
                " 1.A.4.c.i Agriculture -Stationary  ": "1.A.4.c.i",
                " 1.A.4.c.ii Agriculture -Off-road vehicles and other machinery": "1.A.4.c.ii",  # noqa: E501
                "Non-specified 1.A.5.a Stationary  ": "1.A.5.a",
                "Fugitive emis 1.B.1.a Coal mining & handling (surface mining) ": "1.B.1.a",  # noqa: E501
                "sions from fu 1.B.2.a.ii Oil -Flaring  ": "1.B.2.a.ii",
                "els 1.B.2.a.iii.2 Oil production and upgrading ": "1.B.2.a.iii",
            },
        },
        "ippu": {
            "page_defs": {
                "74": {
                    "area": ["68,701,544,313"],
                    "cols": ["97,188,261,358,462"],
                },
            },
            "entity": "KYOTOGHG (SARGWP100)",
            # "category_column" : "Categories",
            # "columns_to_drop" : ["Categories"],
            # "years" : ["1990", "1995", "2000", "2005", "2010", "2015", "2020"],
            "unit": "Gg CO2e",
            "last_year": "2020",
            "rows_to_fix": {
                3: [
                    "Year",
                ],
            },
            "year_column": "Year ",
            "cat_codes_manual": {
                "2.A-Mineral industry ": "2.A",
                "2.C-Metal industry ": "2.C",
                "2.D-Non-energy products from fuels and solvent use": "2.D",
                "2.F-Product uses as substitutes for ozone depleting substances": "2.F",
                "2. IPPU Total ": "2",
            },
            "remove_duplicates": ["2"],
        },
        "livestock": {
            "page_defs": {
                "103": {
                    "area": ["62,480,544,82"],
                    "cols": ["97,182,259,326,403,474"],
                },
            },
            # "entity": "KYOTOGHG (SARGWP100)",
            # "category_column" : "Categories",
            # "columns_to_drop" : ["Categories"],
            # "years" : ["1990", "1995", "2000", "2005", "2010", "2015", "2020"],
            "unit": "Gg CO2e",
            "last_year": "2020",
            "rows_to_fix": {
                3: [
                    "Year",
                ],
            },
            "rows_to_drop": [0, 1],
            "year_column": "Year ",
            # TODO: This is far from than the actual categories but works for now
            "cat_codes_manual": {
                "Fermentation Gg": "3.A.1",
                "Management CH4": "3.A.2",
                " (Total CH4) ": "3.A",
                "Fermentation Gg C": "3.A.1",
                "Management O2e": "3.A.2",
                " (Gg CO2e) ": "3.A",
            },
            "multi_entity": {
                "unit": ["Gg", "Gg", "Gg", "Gg CO2e", "Gg CO2e", "Gg CO2e"],
                "entity": [
                    "CH4",
                    "CH4",
                    "CH4",
                    "KYOTOGHG (SARGWP100)",
                    "KYOTOGHG (SARGWP100)",
                    "KYOTOGHG (SARGWP100)",
                ],
            },
        },
        "biomass_burning": {
            "page_defs": {
                "114": {
                    "area": ["70,214,544,78"],
                    "cols": ["116,185,239,304,365,426,491"],
                },
                "115": {
                    "area": ["72,777,545,505"],
                    "cols": ["123,190,250,313,374,438,495"],
                },
            },
            "last_year": "2020",
            "col_to_use": 5,
            "rows_to_fix": {
                7: [
                    "3.C.1 - Emiss",
                ],
            },
            "year_column": "  Year  ",
            # TODO: These categories are technically duplicate, just with a different unit
            "categories_to_drop": [
                "3.C.1 -Emiss  CH4 (Gg CO2e)",
                "ions from bioma (CO2e) N2O (Gg CO2e)",
                "ss burning  Total (Gg CO2e)",
            ],
            # TODO: This is far from than the actual categories but works for now
            "cat_codes_manual": {
                " 3.C.1  CH4 (Gg) ": "3.C.1",
                " -Emissions fr  N2O (Gg) ": "3.C.1",
                " om biomass bur  NOx (Gg) ": "3.C.1",
                " ning  CO(Gg) ": "3.C.1",
            },
            "multi_entity": {
                "unit": ["Gg", "Gg", "Gg", "Gg"],
                "entity": [
                    "CH4",
                    "N2O",
                    "NOx",
                    "CO",
                ],
            },
        },
        "managed_soils_direct": {
            "page_defs": {
                "119": {
                    "area": ["70,600,541,173"],
                    "cols": ["114,191,245,328,400,476"],
                },
            },
            "last_year": "2020",
            "col_to_use": 3,
            "rows_to_fix": {
                10: [
                    "Urine and dung",
                ],
            },
            "year_column": "  Year   ",
            # # TODO: technically duplicate, just with a different unit
            "categories_to_drop": [
                " 3.C.4 -Direct N2O Emissions from managed soils (CO2e) Gg CO2e",
            ],
            # TODO: This is far from than the actual categories but works for now
            "cat_codes_manual": {
                # TODO the next 4 categories are made up placeholders
                " Inorganic N fertilizer application  N2O (Gg)": "3.C.4.i",
                " Organic N applied as fertilizer (manure) N2O (Gg)": "3.C.4.ii",
                "Urine and dung N deposited on pasture, range and paddock by grazing animals N2O (Gg)": "3.C.4.iii",
                "  N in crop residues  N2O (Gg)": "3.C.4.iiii",
                " 3.C.4 -Direct N2O Emissions from managed soils N2O (Gg)": "3.C.4",
            },
            "multi_entity": {
                "unit": ["Gg", "Gg", "Gg", "Gg", "Gg"],
                "entity": [
                    "N2O",
                    "N2O",
                    "N2O",
                    "N2O",
                    "N2O",
                ],
            },
        },
        "managed_soils_indirect": {
            "page_defs": {
                "125": {
                    "area": ["74,214,539,83"],
                    "cols": ["125,222,309,423"],
                },
                "126": {
                    "area": ["72,775,539,369"],
                    "cols": ["148,248,351,459"],
                },
            },
            "last_year": "2020",
            "col_to_use": 3,
            "rows_to_fix": {
                7: [
                    "3.C.5 - Indirect N2O",
                ],
            },
            "year_column": "  Year  ",
            # # TODO: technically duplicate, just with a different unit
            "categories_to_drop": [
                "3.C.5 -Indirect N2O emissions from managed  soils Gg CO2e"
            ],
            # TODO: This is far from than the actual categories but works for now
            "cat_codes_manual": {
                # TODO the next 2 categories are made up placeholders
                " Volatilization  pathway Gg N2O": "3.C.5.i",
                " Leaching/runoff  pathway Gg N2O": "3.C.5.ii",
                "3.C.5 -Indirect N2O emissions from managed  soils Gg N2O": "3.C.5",
            },
            "entity": "N2O",
            "unit": "Gg",
        },
        "bio_waste" : {
            "page_defs" : {
                "157" : {
                    "area" : ["68,748,541,228"],
                    "cols" : ["108,176,222,283,332,387,429"],
                },
            },
            "last_year" : "2020",
            "rows_to_fix" : {
                2 : [
                    "Year",
                ],
            },
            "year_column" : 'Year ',
            # # TODO: technically duplicate, just with a different unit
            "categories_to_drop" : [
                'Total emissions from SWDS Gg CO2e'
            ],
            # TODO: This is far from than the actual categories but works for now
            "cat_codes_manual" : {
                # TODO the categories are made up placeholders
                'Food ' : "4.A.1.food",
                 'Garden ' : "4.A.1.garden",
                 'Paper Gg CH4' : "4.A.1.paper",
                 'Wood ' : "4.A.1.wood",
                 'Textile ' : "4.A.1.textile",
                 'Total ' : "4.A.1.",
            },
            "entity" : "CH4 ",
            "unit" : "Gg",
        },
        "wastewater" : {
            "page_defs" : {
                "161" : {
                    "area" : ["60,480,541,85"],
                    "cols" : ["98,165,226,281,340,408,465"],
                },
                "162" : {
                    "area" : ["62,775,541,613"],
                    "cols" : ["110,176,229,288,349,414,486"],
                },
            },
            "last_year" : "2020",
            "col_to_use" : 7,
            "rows_to_fix" : {
                10 : [
                    "Wastewater",
                ],
            },
            "year_column" : '   Year  ',
            # # TODO: technically duplicate, just with a different unit
            "categories_to_drop" : [
                ' Domestic wastewater  CH4 emissions ',
                ' Domestic wastewater  N2O emissions (Gg C',
                ' Industrial wastewater  CH4 emissions O2 e)',
                'Wastewater treatment and discharge  Total emissions ',
                ],
            # TODO: This is far from than the actual categories but works for now
            "cat_codes_manual" : {
                # TODO the categories are made up placeholders
                ' Domestic wastewater  CH4 emissions (Gg CH4)' : '4.D.1',
                ' Domestic wastewater  N2O emissions (Gg N2O)' : '4.D.1',
                ' Industrial wastewater  CH4 emissions (Gg CH4)' : '4.D.2',
            },
            "multi_entity" : {
                "unit" : ["Gg", "Gg", "Gg"],
                "entity" : [
                    "CH4",
                    "N2O",
                    "CH4",
                ],
            },
        }
    }

    df_agg = None
    # TODO remove `reversed` (only for development)
    for sector in list(reversed(list(inv_conf_per_sector.keys()))):
        print("-" * 60)
        print(
            f"Reading sector {sector} on page(s) {[*inv_conf_per_sector[sector]['page_defs']]}."
        )

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
                # set the row
                if "col_to_use" in inv_conf_per_sector[sector].keys():
                    col_to_use = inv_conf_per_sector[sector]["col_to_use"]
                else:
                    col_to_use = 0
                df_sector = fix_rows(
                    df_sector,
                    rows_to_fix=inv_conf_per_sector[sector]["rows_to_fix"][n_rows],
                    col_to_use=col_to_use,
                    n_rows=n_rows,
                )

        df_sector = df_sector.reset_index(drop=True)

        if "rows_to_drop" in inv_conf_per_sector[sector]:
            for row in inv_conf_per_sector[sector]["rows_to_drop"]:
                df_sector = df_sector.drop(index=row)

        # TODO: Is it necessary to set the index here?
        df_sector = df_sector.set_index(0)

        # transpose so categegories are in first columns
        df_sector = df_sector.T

        df_sector = df_sector.rename(
            columns={inv_conf_per_sector[sector]["year_column"]: "category"}
        )

        df_sector["category"] = df_sector["category"].str.replace("\n", "")

        # TODO Is it not the same as remove categories further down?
        if "categories_to_drop" in inv_conf_per_sector[sector]:
            for row in inv_conf_per_sector[sector]["categories_to_drop"]:
                row_to_delete = df_sector.index[df_sector["category"] == row][0]
                df_sector = df_sector.drop(index=row_to_delete)

        df_sector.loc[:, "category"] = df_sector.loc[:, "category"].replace(
            inv_conf_per_sector[sector]["cat_codes_manual"]
        )

        if "multi_entity" in inv_conf_per_sector[sector]:
            df_sector["entity"] = inv_conf_per_sector[sector]["multi_entity"]["entity"]
            df_sector["unit"] = inv_conf_per_sector[sector]["multi_entity"]["unit"]
            # df_sector = df_sector.set_index(["entity", "unit", "category"])

        else:
            # unit is always the same
            df_sector.loc[:, "unit"] = inv_conf_per_sector[sector]["unit"]

            # and only one entity per table
            df_sector.loc[:, "entity"] = inv_conf_per_sector[sector]["entity"]

        # Some categories are in two tables (summary and sector)
        # Duplicates need to be removed
        if "remove_duplicates" in inv_conf_per_sector[sector]:
            for row in inv_conf_per_sector[sector]["remove_duplicates"]:
                row_to_delete = df_sector.index[df_sector["category"] == row][0]
                df_sector = df_sector.drop(index=row_to_delete)

        if df_agg is None:
            df_agg = df_sector
        else:
            df_agg = pd.concat(
                [df_agg, df_sector],
                axis=0,
                join="outer",
            ).reset_index(drop=True)

        for year in [str(y) for y in range(1990, 2021)]:
            df_agg.loc[:, year] = df_agg[year].str.replace(",", "")

        # print(df_agg)
    pass

    ### convert to interchange format ###
    df_agg_IF = pm2.pm2io.convert_wide_dataframe_if(
        data_wide=df_agg,
        coords_cols=coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        # filter_remove=filter_remove,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )

    ### convert to primap2 format ###
    print("Converting to primap2 format.")
    data_agg_pm2 = pm2.pm2io.from_interchange_format(df_agg_IF)

    pass
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
