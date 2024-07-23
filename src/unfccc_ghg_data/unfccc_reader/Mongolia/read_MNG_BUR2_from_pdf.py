"""
Read Mongolia's BUR2 from pdf
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
from unfccc_ghg_data.unfccc_reader.Mongolia.config_mng_bur2 import (
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    country_processing_step1,
    filter_remove,
    gas_baskets,
    inv_conf,
    inv_conf_harvested_wood_products,
    inv_conf_per_entity,
    inv_conf_per_sector,
    inv_conf_per_year,
    meta_data,
)

# pd.options.mode.chained_assignment = None  # default='warn'

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

    df_main = None
    for year in inv_conf_per_year.keys():
        print("-" * 60)
        print(f"Reading year {year}.")
        print("-" * 60)
        df_year = None
        for page in inv_conf_per_year[year]["page_defs"].keys():
            print(f"Reading table from page {page}.")
            tables_inventory_original = camelot.read_pdf(
                str(input_folder / pdf_file),
                pages=page,
                table_areas=inv_conf_per_year[year]["page_defs"][page]["area"],
                columns=inv_conf_per_year[year]["page_defs"][page]["cols"],
                flavor="stream",
                split_text=True,
            )
            print("Reading complete.")

            df_page = tables_inventory_original[0].df

            if df_year is None:
                df_year = df_page
            else:
                df_year = pd.concat(
                    [df_year, df_page],
                    axis=0,
                    join="outer",
                ).reset_index(drop=True)

        print(f"Concatenating all tables for {year}.")

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

        df_header = pd.DataFrame([inv_conf["header"], inv_conf["unit"]])

        skip_rows = 11
        df_year = pd.concat(
            [df_header, df_year[skip_rows:]], axis=0, join="outer"
        ).reset_index(drop=True)

        df_year = pm2.pm2io.nir_add_unit_information(
            df_year,
            unit_row=inv_conf["unit_row"],
            entity_row=inv_conf["entity_row"],
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

        # replace cat names by codes in col "category"
        # first the manual replacements

        df_year_long["category"] = df_year_long["category"].replace(
            inv_conf["cat_codes_manual"]
        )

        df_year_long["category"] = df_year_long["category"].str.replace(".", "")

        # then the regex replacements
        df_year_long["category"] = df_year_long["category"].str.replace(
            inv_conf["cat_code_regexp"], repl, regex=True
        )

        df_year_long = df_year_long.reset_index(drop=True)

        df_year_long["data"] = df_year_long["data"].str.replace(",", "")

        # make sure all col headers are str
        df_year_long.columns = df_year_long.columns.map(str)

        df_year_long = df_year_long.drop(columns=["orig_cat_name"])

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

    ### convert to primap2 format ###
    print("Converting to primap2 format.")
    data_main_pm2 = pm2.pm2io.from_interchange_format(df_main_IF)

    # ###
    # 2. Read in trend tables
    # ###

    df_trend = None
    for entity in inv_conf_per_entity.keys():
        print("-" * 60)
        print(f"Reading entity {entity}.")

        df_entity = None

        for page in inv_conf_per_entity[entity]["page_defs"].keys():
            print(f"Reading page {page}.")

            tables_inventory_original = camelot.read_pdf(
                str(input_folder / pdf_file),
                pages=page,
                table_areas=inv_conf_per_entity[entity]["page_defs"][page]["area"],
                columns=inv_conf_per_entity[entity]["page_defs"][page]["cols"],
                flavor="stream",
                split_text=True,
            )
            df_page = tables_inventory_original[0].df

            if df_entity is None:
                df_entity = df_page
            else:
                df_entity = pd.concat(
                    [df_entity, df_page],
                    axis=0,
                    join="outer",
                ).reset_index(drop=True)
            print(f"adding table from page {page}.")

        if "rows_to_fix" in inv_conf_per_entity[entity]:
            for n_rows in inv_conf_per_entity[entity]["rows_to_fix"].keys():
                print(f"Merge content for {n_rows=}")
                df_entity = fix_rows(
                    df_entity,
                    rows_to_fix=inv_conf_per_entity[entity]["rows_to_fix"][n_rows],
                    col_to_use=0,
                    n_rows=n_rows,
                )

        df_entity.columns = df_entity.iloc[0, :]
        # make a copy to avoid SettingWithCopyWarning
        df_entity = df_entity[1:].copy()

        # unit is always Gg
        df_entity.loc[:, "unit"] = inv_conf_per_entity[entity]["unit"]

        # only one entity per table
        df_entity.loc[:, "entity"] = entity

        # TODO: Fix pandas "set value on slice of copy" warning
        df_entity.loc[:, "category"] = df_entity.loc[
            :, inv_conf_per_entity[entity]["category_column"]
        ]

        if "rows_to_drop" in inv_conf_per_entity[entity]:
            for row in inv_conf_per_entity[entity]["rows_to_drop"]:
                row_to_delete = df_entity.index[df_entity["category"] == row][0]
                df_entity = df_entity.drop(index=row_to_delete)

        df_entity.loc[:, "category"] = df_entity.loc[:, "category"].replace(
            inv_conf_per_entity[entity]["cat_codes_manual"]
        )

        df_entity.loc[:, "category"] = df_entity["category"].str.replace(
            inv_conf["cat_code_regexp"], repl, regex=True
        )

        df_entity = df_entity.drop(
            columns=inv_conf_per_entity[entity]["columns_to_drop"]
        )

        for year in inv_conf_per_entity[entity]["years"]:
            df_entity.loc[:, year] = df_entity[year].str.replace(",", "")

        if df_trend is None:
            df_trend = df_entity
        else:
            df_trend = pd.concat(
                [df_trend, df_entity],
                axis=0,
                join="outer",
            ).reset_index(drop=True)

    ### convert to interchange format ###
    df_trend_IF = pm2.pm2io.convert_wide_dataframe_if(
        data_wide=df_trend,
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
    data_trend_pm2 = pm2.pm2io.from_interchange_format(df_trend_IF)

    # ###
    # 3 Read harvested wood products table
    # ###

    # The table for harvested wood products is in a different format
    # and needs to be read in separately.

    print("-" * 60)
    print("Reading sector harvested wood products table.")
    print("-" * 60)

    df_hwp = None
    for part in [*inv_conf_harvested_wood_products["parts"]]:
        tables_inventory_original = camelot.read_pdf(
            str(input_folder / pdf_file),
            pages=inv_conf_harvested_wood_products["page"],
            table_areas=inv_conf_harvested_wood_products["parts"][part]["page_defs"][
                "area"
            ],
            columns=inv_conf_harvested_wood_products["parts"][part]["page_defs"][
                "cols"
            ],
            flavor="stream",
            split_text=True,
        )

        df_hwp_part = tables_inventory_original[0].df

        if "rows_to_fix" in inv_conf_harvested_wood_products["parts"][part]:
            for n_rows in inv_conf_harvested_wood_products["parts"][part][
                "rows_to_fix"
            ].keys():
                df_hwp_part = fix_rows(
                    df_hwp_part,
                    rows_to_fix=inv_conf_harvested_wood_products["parts"][part][
                        "rows_to_fix"
                    ][n_rows],
                    col_to_use=0,
                    n_rows=n_rows,
                )

        df_hwp_part = df_hwp_part.drop(1, axis=0).reset_index(drop=True)

        if df_hwp is None:
            df_hwp = df_hwp_part
        else:
            # stack horizontally
            df_hwp = pd.concat(
                [df_hwp, df_hwp_part.drop(0, axis=1)],
                axis=1,
                join="outer",
            ).reset_index(drop=True)

    # assign the years to the columns
    df_hwp = pd.DataFrame(df_hwp.to_numpy()[1:], columns=df_hwp.iloc[0])

    df_hwp = df_hwp.rename(
        columns={inv_conf_harvested_wood_products["category_column"]: "category"}
    )

    df_hwp.loc[:, "category"] = df_hwp.loc[:, "category"].replace(
        inv_conf_harvested_wood_products["cat_codes_manual"]
    )

    # unit is always the same
    df_hwp.loc[:, "unit"] = inv_conf_harvested_wood_products["unit"]

    # and only one entity per table
    df_hwp.loc[:, "entity"] = inv_conf_harvested_wood_products["entity"]

    # ###
    # 4. Read in aggregated tables from 1990 - 2020
    # ###

    df_agg = None

    for sector in list(inv_conf_per_sector.keys()):
        print("-" * 60)
        print(
            f"Reading sector {sector} on page(s) \
            {[*inv_conf_per_sector[sector]['page_defs']]}."
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

        # TODO This is the same functionality as remove_duplicates ?
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

    # add harvested wood products table and all the other sectors together
    df_agg = pd.concat(
        [df_agg, df_hwp],
        axis=0,
        join="outer",
    ).reset_index(drop=True)

    # There are more tables in the document that could be read, but are less relevant
    # on pages 67, 78, 91, 105/6, 110/111

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

    # # ###
    # # Merge tables.
    # # ###

    print("Merging main and trend table.")
    data_pm2 = data_main_pm2.pr.merge(data_trend_pm2, tolerance=1)

    print("Merging sector tables.")
    data_pm2 = data_pm2.pr.merge(data_agg_pm2, tolerance=1)

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
    data_proc_pm2_gas_baskets = process_data_for_country(
        data_country=data_pm2,
        entities_to_ignore=[],
        gas_baskets=gas_baskets,
        filter_dims=None,
        cat_terminology_out=None,
        category_conversion=None,
        sectors_out=None,
        processing_info_country=None,
    )

    data_proc_pm2 = process_data_for_country(
        data_country=data_proc_pm2_gas_baskets,
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
