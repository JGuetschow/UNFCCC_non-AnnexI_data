"""
Read Guinea's BUR1 from pdf
"""

import camelot
import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import downloaded_data_path, extracted_data_path
from unfccc_ghg_data.helper.functions import (
    find_and_replace_values,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.Guinea.config_gin_bur1 import (
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    country_processing_step1,
    delete_row,
    delete_rows_by_category,
    filter_remove,
    gas_baskets,
    inv_conf,
    meta_data,
    page_def_templates,
    replace_categories,
    replace_info,
    set_value,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###

    input_folder = downloaded_data_path / "UNFCCC" / "Guinea" / "BUR1"
    output_folder = extracted_data_path / "UNFCCC" / "Guinea"
    if not output_folder.exists():
        output_folder.mkdir()

    pdf_file = "Rapport_IGES-Guinee-BUR1_VF.pdf"
    output_filename = "GIN_BUR1_2023_"
    category_column = f"category ({coords_terminologies['category']})"
    compression = dict(zlib=True, complevel=9)

    def repl(m):  # noqa: D103
        return m.group("code")

    # ###
    # 1. Read in main tables
    # ###

    df_main = None
    for page in inv_conf["pages_to_read"]["main"]:
        print("-" * 45)
        print(f"Reading table from page {page}.")

        tables_inventory_original = camelot.read_pdf(
            str(input_folder / pdf_file),
            pages=page,
            table_areas=page_def_templates[page]["area"],
            columns=page_def_templates[page]["cols"],
            flavor="stream",
            split_text=True,
        )

        print("Reading complete.")

        df_inventory = tables_inventory_original[0].df.copy()

        # set category names (they moved one row up)
        if page in set_value["main"].keys():
            for idx, col, value in set_value["main"][page]:
                df_inventory.loc[idx, col] = value
        # delete empty row
        if page in delete_row["main"].keys():
            for idx in delete_row["main"][page]:
                df_inventory = df_inventory.drop(index=idx)

        # add header and unit
        df_header = pd.DataFrame([inv_conf["header"], inv_conf["unit"]])
        df_inventory = pd.concat(
            [df_header, df_inventory], axis=0, join="outer"
        ).reset_index(drop=True)
        df_inventory = pm2.pm2io.nir_add_unit_information(
            df_inventory,
            unit_row=inv_conf["unit_row"],
            entity_row=inv_conf["entity_row"],
            regexp_entity=".*",
            regexp_unit=".*",
            default_unit="Gg",
        )

        print("Added unit information.")

        # set index
        df_inventory = df_inventory.set_index(inv_conf["index_cols"])

        # convert to long format
        df_inventory_long = pm2.pm2io.nir_convert_df_to_long(
            df_inventory, inv_conf["year"][page], inv_conf["header_long"]
        )

        # extract category from tuple
        df_inventory_long["orig_cat_name"] = df_inventory_long["orig_cat_name"].str[0]

        # prep for conversion to PM2 IF and native format
        df_inventory_long["category"] = df_inventory_long["orig_cat_name"]

        df_inventory_long["category"] = df_inventory_long["category"].replace(
            inv_conf["cat_codes_manual"]["main"]
        )

        df_inventory_long["category"] = df_inventory_long["category"].str.replace(
            ".", ""
        )

        # regex replacements
        df_inventory_long["category"] = df_inventory_long["category"].str.replace(
            inv_conf["cat_code_regexp"], repl, regex=True
        )

        df_inventory_long = df_inventory_long.reset_index(drop=True)

        df_inventory_long["data"] = df_inventory_long["data"].str.replace(",", ".")
        df_inventory_long["data"] = df_inventory_long["data"].str.replace("NE1", "NE")

        # make sure all col headers are str
        df_inventory_long.columns = df_inventory_long.columns.map(str)
        df_inventory_long = df_inventory_long.drop(columns=["orig_cat_name"])

        if df_main is None:
            df_main = df_inventory_long
        else:
            df_main = pd.concat(
                [df_main, df_inventory_long],
                axis=0,
                join="outer",
            ).reset_index(drop=True)

    print("Converting to interchange format.")
    df_all_IF = pm2.pm2io.convert_long_dataframe_if(
        df_main,
        coords_cols=coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping["main"],
        filter_remove=filter_remove,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )

    df_all_IF = find_and_replace_values(
        df=df_all_IF, replace_info=replace_info["main"], category_column=category_column
    )

    ### convert to primap2 format ###
    data_pm2_main = pm2.pm2io.from_interchange_format(df_all_IF)

    # ###
    # 2. Read energy sector tables
    # ###

    df_energy = None
    for page in inv_conf["pages_to_read"]["energy"]:
        print("-" * 45)
        print(f"Reading table from page {page}.")

        tables_inventory_original = camelot.read_pdf(
            str(input_folder / pdf_file), pages=page, flavor="lattice", split_text=True
        )

        print("Reading complete.")

        df_energy_year = pd.concat(
            [tables_inventory_original[0].df[2:], tables_inventory_original[1].df[3:]],
            axis=0,
            join="outer",
        ).reset_index(drop=True)

        # TODO This step should be done in pm2.pm2io.convert_long_dataframe_if()
        for row in delete_rows_by_category["energy"][page]:
            row_to_delete = df_energy_year.index[df_energy_year[0] == row][0]
            df_energy_year = df_energy_year.drop(index=row_to_delete)

        # add header and unit
        df_header = pd.DataFrame([inv_conf["header_energy"], inv_conf["unit_energy"]])

        df_energy_year = pd.concat(
            [df_header, df_energy_year], axis=0, join="outer"
        ).reset_index(drop=True)

        df_energy_year = pm2.pm2io.nir_add_unit_information(
            df_energy_year,
            unit_row=inv_conf["unit_row"],
            entity_row=inv_conf["entity_row"],
            regexp_entity=".*",
            regexp_unit=".*",
            default_unit="Gg",
        )

        print("Added unit information.")
        # set index
        df_energy_year = df_energy_year.set_index(inv_conf["index_cols"])

        # convert to long format
        df_energy_year_long = pm2.pm2io.nir_convert_df_to_long(
            df_energy_year, inv_conf["year"][page], inv_conf["header_long"]
        )

        # extract from tuple
        df_energy_year_long["orig_cat_name"] = df_energy_year_long["orig_cat_name"].str[
            0
        ]

        # prep for conversion to PM2 IF and native format
        # make a copy of the categories row
        df_energy_year_long["category"] = df_energy_year_long["orig_cat_name"]

        # replace cat names by codes in col "category"
        # first the manual replacements
        df_energy_year_long["category"] = df_energy_year_long["category"].str.replace(
            "\n", ""
        )
        df_energy_year_long["category"] = df_energy_year_long["category"].replace(
            inv_conf["cat_codes_manual"]["energy"]
        )

        df_energy_year_long["category"] = df_energy_year_long["category"].str.replace(
            ".", ""
        )

        # then the regex replacements
        df_energy_year_long["category"] = df_energy_year_long["category"].str.replace(
            inv_conf["cat_code_regexp"], repl, regex=True
        )

        df_energy_year_long = df_energy_year_long.reset_index(drop=True)

        df_energy_year_long["data"] = df_energy_year_long["data"].str.replace(",", ".")
        df_energy_year_long["data"] = df_energy_year_long["data"].str.replace(
            "NE1", "NE"
        )

        # make sure all col headers are str
        df_energy_year_long.columns = df_energy_year_long.columns.map(str)
        df_energy_year_long = df_energy_year_long.drop(columns=["orig_cat_name"])

        if df_energy is None:
            df_energy = df_energy_year_long
        else:
            df_energy = pd.concat(
                [df_energy, df_energy_year_long],
                axis=0,
                join="outer",
            ).reset_index(drop=True)

    print("Converting to interchange format.")
    df_energy_IF = pm2.pm2io.convert_long_dataframe_if(
        df_energy,
        coords_cols=coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping["energy"],
        filter_remove=filter_remove,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )

    ### convert to primap2 format ###
    data_pm2_energy = pm2.pm2io.from_interchange_format(df_energy_IF)

    # ###
    # 3. Read in afolu table
    # ###

    df_afolu = None
    for page in inv_conf["pages_to_read"]["afolu"]:
        print("-" * 45)
        print(f"Reading table from page {page}.")

        tables_inventory_original = camelot.read_pdf(
            str(input_folder / pdf_file), pages=page, flavor="lattice", split_text=True
        )
        print("Reading complete.")

        if page == "127":
            # table on page 127 has one extra row at the top
            # and one extra category 3.A.1.j
            df_afolu_year = tables_inventory_original[0].df[3:]
            # 3.A.1.a.i to 3.A.1.j exist twice.
            # Rename duplicate categories in tables.
            for index, category_name in replace_categories["afolu"]["127"]:
                df_afolu_year.loc[index, 0] = category_name
        else:
            # cut first two lines
            df_afolu_year = tables_inventory_original[0].df[2:]
            # On pages 124-126 the wrong categories are slightly different
            for index, category_name in replace_categories["afolu"]["124-126"]:
                df_afolu_year.loc[index, 0] = category_name

        # add header and unit
        df_header = pd.DataFrame([inv_conf["header_afolu"], inv_conf["unit_afolu"]])

        df_afolu_year = pd.concat(
            [df_header, df_afolu_year], axis=0, join="outer"
        ).reset_index(drop=True)

        df_afolu_year = pm2.pm2io.nir_add_unit_information(
            df_afolu_year,
            unit_row=inv_conf["unit_row"],
            entity_row=inv_conf["entity_row"],
            regexp_entity=".*",
            regexp_unit=".*",
            default_unit="Gg",
        )

        print("Added unit information.")

        # set index
        df_afolu_year = df_afolu_year.set_index(inv_conf["index_cols"])

        # convert to long format
        df_afolu_year_long = pm2.pm2io.nir_convert_df_to_long(
            df_afolu_year, inv_conf["year"][page], inv_conf["header_long"]
        )

        df_afolu_year_long["orig_cat_name"] = df_afolu_year_long["orig_cat_name"].str[0]

        # prep for conversion to PM2 IF and native format
        # make a copy of the categories row
        df_afolu_year_long["category"] = df_afolu_year_long["orig_cat_name"]

        # regex replacements
        df_afolu_year_long["category"] = df_afolu_year_long["category"].str.replace(
            inv_conf["cat_code_regexp"], repl, regex=True
        )

        df_afolu_year_long = df_afolu_year_long.reset_index(drop=True)

        df_afolu_year_long["data"] = df_afolu_year_long["data"].str.replace(",", ".")
        df_afolu_year_long["data"] = df_afolu_year_long["data"].str.replace("NE1", "NE")

        # make sure all col headers are str
        df_afolu_year_long.columns = df_afolu_year_long.columns.map(str)
        df_afolu_year_long = df_afolu_year_long.drop(columns=["orig_cat_name"])

        if df_afolu is None:
            df_afolu = df_afolu_year_long
        else:
            df_afolu = pd.concat(
                [df_afolu, df_afolu_year_long],
                axis=0,
                join="outer",
            ).reset_index(drop=True)

    print("Converting to interchange format.")
    df_afolu_IF = pm2.pm2io.convert_long_dataframe_if(
        df_afolu,
        coords_cols=coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping["afolu"],
        filter_remove=filter_remove,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )

    ### convert to primap2 format ###
    data_pm2_afolu = pm2.pm2io.from_interchange_format(df_afolu_IF)

    # ###
    # 4. Read in Waste tables - pages 128, 130
    # ###

    # There are three tables for three years on page 128
    # and another table for the last year on page 130

    # read the first three tables
    page = inv_conf["pages_to_read"]["waste"][0]
    tables_inventory_original_128 = camelot.read_pdf(
        str(input_folder / pdf_file), pages=page, flavor="lattice", split_text=True
    )

    # read last table
    page = inv_conf["pages_to_read"]["waste"][1]
    tables_inventory_original_130 = camelot.read_pdf(
        str(input_folder / pdf_file), pages=page, flavor="lattice", split_text=True
    )

    # combine in a dict
    df_waste_years = {
        "1990": tables_inventory_original_128[0].df,
        "2000": tables_inventory_original_128[1].df,
        "2010": tables_inventory_original_128[2].df,
        "2019": tables_inventory_original_130[0].df,
    }

    df_waste = None
    for year in df_waste_years.keys():
        print("-" * 45)
        print(f"Processing table for {year}.")

        df_waste_year = df_waste_years[year][2:]

        # add header and unit
        df_header = pd.DataFrame([inv_conf["header_waste"], inv_conf["unit_waste"]])

        df_waste_year = pd.concat(
            [df_header, df_waste_year], axis=0, join="outer"
        ).reset_index(drop=True)

        df_waste_year = pm2.pm2io.nir_add_unit_information(
            df_waste_year,
            unit_row=inv_conf["unit_row"],
            entity_row=inv_conf["entity_row"],
            regexp_entity=".*",
            regexp_unit=".*",
            default_unit="Gg",
        )

        print("Added unit information.")

        # set index
        df_waste_year = df_waste_year.set_index(inv_conf["index_cols"])

        # convert to long format
        df_waste_year_long = pm2.pm2io.nir_convert_df_to_long(
            df_waste_year, year, inv_conf["header_long"]
        )

        df_waste_year_long["orig_cat_name"] = df_waste_year_long["orig_cat_name"].str[0]

        # prep for conversion to PM2 IF and native format
        # make a copy of the categories row
        df_waste_year_long["category"] = df_waste_year_long["orig_cat_name"]

        # regex replacements
        df_waste_year_long["category"] = df_waste_year_long["category"].str.replace(
            inv_conf["cat_code_regexp"], repl, regex=True
        )

        df_waste_year_long = df_waste_year_long.reset_index(drop=True)

        df_waste_year_long["category"] = df_waste_year_long["category"].str.replace(
            ".", ""
        )
        df_waste_year_long["data"] = df_waste_year_long["data"].str.replace(",", ".")
        df_waste_year_long["data"] = df_waste_year_long["data"].str.replace("NE1", "NE")

        # make sure all col headers are str
        df_waste_year_long.columns = df_waste_year_long.columns.map(str)
        df_waste_year_long = df_waste_year_long.drop(columns=["orig_cat_name"])

        if df_waste is None:
            df_waste = df_waste_year_long
        else:
            df_waste = pd.concat(
                [df_waste, df_waste_year_long],
                axis=0,
                join="outer",
            ).reset_index(drop=True)

    print("Converting to interchange format.")
    df_waste_IF = pm2.pm2io.convert_long_dataframe_if(
        df_waste,
        coords_cols=coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping["waste"],
        filter_remove=filter_remove,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )

    ### convert to primap2 format ###
    data_pm2_waste = pm2.pm2io.from_interchange_format(df_waste_IF)

    # ###
    # 5. Read in trend tables - pages 131 - 137
    # ###

    df_trend = None
    pages = inv_conf["pages_to_read"]["trend"]
    entities = inv_conf["entity_for_page"]["trend"]

    # for this set of tables every page is a different entity
    for page, entity in zip(pages, entities):
        print("-" * 45)
        print(f"Reading table for page {page} and entity {entity}.")

        # First table must be read in with flavor="stream", as
        # flavor="lattice" raises an error. Maybe camelot issue
        # see https://github.com/atlanhq/camelot/issues/306,
        # or because characters in first row almost touch
        # the table grid.
        if page == "131":
            tables_inventory_original = camelot.read_pdf(
                str(input_folder / pdf_file),
                pages=page,
                table_areas=page_def_templates[page]["area"],
                columns=page_def_templates[page]["cols"],
                flavor="stream",
                split_text=True,
            )

            df_trend_entity = tables_inventory_original[0].df[1:]

        else:
            tables_inventory_original = camelot.read_pdf(
                str(input_folder / pdf_file),
                pages=page,
                flavor="lattice",
                split_text=True,
            )
            df_trend_entity = tables_inventory_original[0].df[3:]

        print("Reading complete.")

        if page in delete_rows_by_category["trend"].keys():
            for category in delete_rows_by_category["trend"][page]:
                row_to_delete = df_trend_entity.index[df_trend_entity[0] == category][0]
                df_trend_entity = df_trend_entity.drop(index=row_to_delete)

        df_trend_entity.columns = inv_conf["header_trend"]

        df_trend_entity = df_trend_entity.copy()

        # unit is always Gg
        df_trend_entity.loc[:, "unit"] = "Gg"

        # only one entity per table
        df_trend_entity.loc[:, "entity"] = entity

        df_trend_entity.loc[:, "category"] = df_trend_entity["orig_cat_name"]

        df_trend_entity["category"] = df_trend_entity["category"].replace(
            inv_conf["cat_codes_manual"]["trend"]
        )

        df_trend_entity.loc[:, "category"] = df_trend_entity["category"].str.replace(
            ".", ""
        )
        df_trend_entity.loc[:, "category"] = df_trend_entity["category"].str.replace(
            "\n", ""
        )

        df_trend_entity.loc[:, "category"] = df_trend_entity["category"].str.replace(
            inv_conf["cat_code_regexp"], repl, regex=True
        )

        df_trend_entity = df_trend_entity.reset_index(drop=True)

        print("Created category codes.")

        for year in inv_conf["header_trend"][1:]:
            df_trend_entity.loc[:, year] = df_trend_entity[year].str.replace(",", ".")
            df_trend_entity.loc[:, year] = df_trend_entity[year].str.replace(
                "NE1", "NE"
            )

        # make sure all col headers are str
        df_trend_entity.columns = df_trend_entity.columns.map(str)

        df_trend_entity = df_trend_entity.drop(columns=["orig_cat_name"])

        # TODO better to use pm2.pm2io.convert_wide_dataframe_if
        df_trend_entity_long = pd.wide_to_long(
            df_trend_entity, stubnames="data", i="category", j="time"
        )

        print("Converted to long format.")

        df_trend_entity_long = df_trend_entity_long.reset_index()

        if df_trend is None:
            df_trend = df_trend_entity_long
        else:
            df_trend = pd.concat(
                [df_trend, df_trend_entity_long],
                axis=0,
                join="outer",
            ).reset_index(drop=True)

    print("Converting to interchange format.")

    df_trend_IF = pm2.pm2io.convert_long_dataframe_if(
        df_trend,
        coords_cols=coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping["trend"],
        filter_remove=filter_remove,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )

    df_trend_IF = find_and_replace_values(
        df=df_trend_IF,
        replace_info=replace_info["trend"],
        category_column=category_column,
    )

    ### convert to primap2 format ###
    data_pm2_trend = pm2.pm2io.from_interchange_format(df_trend_IF)

    # ###
    # Combine tables
    # ###

    # merge main and energy
    # There are discrepancies larger than 0.86 for area category 1.A.2, entity NMVOC,
    # years 1990, 2000, 2010, 2019
    # It is assumed the main table has the correct values.
    print("Merging main and energy table.")
    data_pm2 = data_pm2_main.pr.merge(data_pm2_energy, tolerance=1)

    # merge afolu
    print("Merging afolu table.")
    data_pm2 = data_pm2.pr.merge(data_pm2_afolu, tolerance=0.11)

    # merge waste
    # increasing tolerance to merge values for 4.C, 1990, N2O - 0.003 in sector table,
    # 0.0034 in main table
    print("Merging waste table.")
    data_pm2 = data_pm2.pr.merge(data_pm2_waste, tolerance=0.15)

    # merge trend
    print("Merging trend table.")
    data_pm2 = data_pm2.pr.merge(data_pm2_trend, tolerance=0.11)

    # convert back to IF to have units in the fixed format
    # ( per year / per a / per annum)
    data_if = data_pm2.pr.to_interchange_format()

    # ###
    # Save raw data to IF and native format.
    # ###

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

    # ###
    # Processing
    # ###

    data_proc_pm2 = process_data_for_country(
        data_country=data_pm2,
        entities_to_ignore=[],
        gas_baskets=gas_baskets,
        filter_dims=None,  # leaving this explicit for now
        cat_terminology_out=None,
        category_conversion=None,
        sectors_out=None,
        processing_info_country=country_processing_step1,
    )

    # ###
    # save processed data to IF and native format
    # ###

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
