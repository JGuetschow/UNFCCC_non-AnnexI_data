# TODO! Set env via doit and delete this when it works
import os

os.environ["UNFCCC_GHG_ROOT_PATH"] = (
    "/Users/danielbusch/Documents/UNFCCC_non-AnnexI_data"
)

import camelot
import primap2 as pm2
import pandas as pd
import numpy as np
import re
from datetime import date
import xarray as xr

from UNFCCC_GHG_data.helper import downloaded_data_path, extracted_data_path
from UNFCCC_GHG_data.helper.functions import find_and_replace_values
from config_GIN_BUR1 import coords_cols, coords_defaults, coords_terminologies
from config_GIN_BUR1 import (
    coords_value_mapping,
    filter_remove,
    meta_data,
    page_def_templates,
)
from config_GIN_BUR1 import inv_conf, country_processing_step1, gas_baskets, replace_info, replace_categories

# ###
# configuration
# ###

input_folder = downloaded_data_path / "UNFCCC" / "Guinea" / "BUR1"
output_folder = extracted_data_path / "UNFCCC" / "Guinea"
if not output_folder.exists() :
    output_folder.mkdir()

pdf_file = "Rapport_IGES-Guinee-BUR1_VF.pdf"
output_filename = "GIN_BUR1_2023_"
category_column = f"category ({coords_terminologies['category']})"
compression = dict(zlib=True, complevel=9)

# ###
# 1. Read in main tables
# ###

pages = ["110", "111", "112", "113"]
df_main = None
for page in pages :
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

    # move broken text in correct row (page 113 is fine)
    if page in ["110", "111", "112"] :
        df_inventory.at[4, 0] = "1.A.1 - Industries énergétiques"
        df_inventory = df_inventory.drop(index=3)
        df_inventory.at[8, 0] = "1.A.4 - Autres secteurs"
        df_inventory = df_inventory.drop(index=7)

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

    df_inventory_long["category"] = df_inventory_long["category"].str.replace(".", "")


    # regex replacements
    def repl(m) :
        return m.group("code")


    df_inventory_long["category"] = df_inventory_long["category"].str.replace(
        inv_conf["cat_code_regexp"], repl, regex=True
    )

    df_inventory_long = df_inventory_long.reset_index(drop=True)

    df_inventory_long["data"] = df_inventory_long["data"].str.replace(",", ".")
    df_inventory_long["data"] = df_inventory_long["data"].str.replace("NE1", "NE")

    # make sure all col headers are str
    df_inventory_long.columns = df_inventory_long.columns.map(str)
    df_inventory_long = df_inventory_long.drop(columns=["orig_cat_name"])

    if df_main is None :
        df_main = df_inventory_long
    else :
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

df_all_IF = find_and_replace_values(df=df_all_IF,
                                    replace_info=replace_info['main'],
                                    category_column=category_column
                                    )

### convert to primap2 format ###
data_pm2_main = pm2.pm2io.from_interchange_format(df_all_IF)

# ###
# 2. Read energy sector tables
# ###

pages = ["116", "117", "118", "119"]
df_energy = None
for page in pages :
    print("-" * 45)
    print(f"Reading table from page {page}.")

    tables_inventory_original = camelot.read_pdf(
        str(input_folder / pdf_file), pages=page, flavor="lattice", split_text=True
    )

    print("Reading complete.")

    # cut last two lines of second table to ignore additional information regarding biomass for energy production
    df_energy_year = pd.concat(
        [tables_inventory_original[0].df[2 :], tables_inventory_original[1].df[3 :-2]],
        axis=0,
        join="outer",
    ).reset_index(drop=True)

    row_to_delete = df_energy_year.index[
        df_energy_year[0]
        == "1.A.3.a.i - Aviation internationale (Soutes internationales)"
        ][0]
    df_energy_year = df_energy_year.drop(index=row_to_delete)

    row_to_delete = df_energy_year.index[
        df_energy_year[0]
        == "1.A.3.d.i - Navigation internationale (soutes internationales)"
        ][0]
    df_energy_year = df_energy_year.drop(index=row_to_delete)

    row_to_delete = df_energy_year.index[
        df_energy_year[0]
        == "1.A.5.c - Opérations multilatérales (Éléments pour information)"
        ][0]
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
    df_energy_year_long["orig_cat_name"] = df_energy_year_long["orig_cat_name"].str[0]

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
    def repl(m) :
        return m.group("code")


    df_energy_year_long["category"] = df_energy_year_long["category"].str.replace(
        inv_conf["cat_code_regexp"], repl, regex=True
    )

    df_energy_year_long = df_energy_year_long.reset_index(drop=True)

    df_energy_year_long["data"] = df_energy_year_long["data"].str.replace(",", ".")
    df_energy_year_long["data"] = df_energy_year_long["data"].str.replace("NE1", "NE")

    # make sure all col headers are str
    df_energy_year_long.columns = df_energy_year_long.columns.map(str)
    df_energy_year_long = df_energy_year_long.drop(columns=["orig_cat_name"])

    if df_energy is None :
        df_energy = df_energy_year_long
    else :
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

pages = ["124", "125", "126", "127"]
df_afolu = None
for page in pages :
    print("-" * 45)
    print(f"Reading table from page {page}.")

    tables_inventory_original = camelot.read_pdf(
        str(input_folder / pdf_file), pages=page, flavor="lattice", split_text=True
    )
    print("Reading complete.")

    if page == "127" :
        # table on page 127 has one extra row at the top
        # and one extra category 3.A.1.j
        df_afolu_year = tables_inventory_original[0].df[3 :]
        # 3.A.1.a.i to 3.A.1.j exist twice.
        # Rename duplicate categories in tables.
        for index, category_name in replace_categories['afolu']['127'] :
            df_afolu_year.at[index, 0] = category_name
    else :
        # cut first two lines
        df_afolu_year = tables_inventory_original[0].df[2 :]
        # On pages 124-126 the wrong categories are slightly different
        for index, category_name in replace_categories['afolu']['124-126'] :
            df_afolu_year.at[index, 0] = category_name

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

    df_afolu_year_long["orig_cat_name"] = df_afolu_year_long["orig_cat_name"].str[
        0
    ]  # extract from tuple

    # prep for conversion to PM2 IF and native format
    # make a copy of the categories row
    df_afolu_year_long["category"] = df_afolu_year_long["orig_cat_name"]


    # regex replacements
    def repl(m) :
        return m.group("code")


    df_afolu_year_long["category"] = df_afolu_year_long["category"].str.replace(
        inv_conf["cat_code_regexp"], repl, regex=True
    )

    df_afolu_year_long = df_afolu_year_long.reset_index(drop=True)

    df_afolu_year_long["data"] = df_afolu_year_long["data"].str.replace(",", ".")
    df_afolu_year_long["data"] = df_afolu_year_long["data"].str.replace("NE1", "NE")

    # make sure all col headers are str
    df_afolu_year_long.columns = df_afolu_year_long.columns.map(str)
    df_afolu_year_long = df_afolu_year_long.drop(columns=["orig_cat_name"])

    if df_afolu is None :
        df_afolu = df_afolu_year_long
    else :
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
page = "128"
tables_inventory_original_128 = camelot.read_pdf(
    str(input_folder / pdf_file), pages=page, flavor="lattice", split_text=True
)

# read last table
page = "130"
tables_inventory_original_130 = camelot.read_pdf(
    str(input_folder / pdf_file), pages=page, flavor="lattice", split_text=True
)

# save to dict
df_waste_years = {
    "1990" : tables_inventory_original_128[0].df,
    "2000" : tables_inventory_original_128[1].df,
    "2010" : tables_inventory_original_128[2].df,
    "2019" : tables_inventory_original_130[0].df,
}

df_waste = None
for year in df_waste_years.keys() :
    print("-" * 45)
    print(f"Processing table for {year}.")

    df_waste_year = df_waste_years[year][2 :]

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
    def repl(m) :
        return m.group("code")


    df_waste_year_long["category"] = df_waste_year_long["category"].str.replace(
        inv_conf["cat_code_regexp"], repl, regex=True
    )

    df_waste_year_long = df_waste_year_long.reset_index(drop=True)

    df_waste_year_long["category"] = df_waste_year_long["category"].str.replace(".", "")
    df_waste_year_long["data"] = df_waste_year_long["data"].str.replace(",", ".")
    df_waste_year_long["data"] = df_waste_year_long["data"].str.replace("NE1", "NE")

    # make sure all col headers are str
    df_waste_year_long.columns = df_waste_year_long.columns.map(str)
    df_waste_year_long = df_waste_year_long.drop(columns=["orig_cat_name"])

    if df_waste is None :
        df_waste = df_waste_year_long
    else :
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
pages = ["131", "132", "133", "134", "135", "136", "137"]
entities = ["CO2", "CH4", "N2O", "NOx", "CO", "NMVOCs", "SO2"]

# for this set of tables every page is a different entity
for page, entity in zip(pages, entities) :
    # The table for CO seems completely mixed up and should not be considered.
    # The total CO values for 1990 equal the values in the main table.
    # The total CO values for 1995 equal the values for 2000 in the main table.
    # The total CO values for 2000 equal the values for 2010 in the main table.
    # The total CO values for 2005 are identical to the 2019 values in the same table.
    # The total CO values for 2010 are identical to the 1990 values in the same table.
    # The total CO values for 2019 are identical to the 1995 values in the same table.
    # And so on.
    if entity == "CO" :
        continue

    print("-" * 45)
    print(f"Reading table for page {page} and entity {entity}.")

    # First table must be read in with flavor="stream", as
    # flavor="lattice" raises an error. Maybe camelot issue
    # see https://github.com/atlanhq/camelot/issues/306,
    # or because characters in first row almost touch
    # the table grid.
    if page == "131" :
        tables_inventory_original = camelot.read_pdf(
            str(input_folder / pdf_file),
            pages=page,
            table_areas=page_def_templates[page]["area"],
            columns=page_def_templates[page]["cols"],
            flavor="stream",
            split_text=True,
        )

        df_trend_entity = tables_inventory_original[0].df[1 :]

        # The categories 3.D / 3.D.1 / 3.D.2 contain values different to the main table
        # They should also not contain negative values according to IPCC methodology:
        # https://www.ipcc-nggip.iges.or.jp/public/2006gl/
        # Therefore, the rows are deleted from the table.
        row_to_delete = df_trend_entity.index[df_trend_entity[0] == "3.D - Autres"][0]
        df_trend_entity = df_trend_entity.drop(index=row_to_delete)

        row_to_delete = df_trend_entity.index[
            df_trend_entity[0] == "3.D.1 - Produits ligneux récoltés"
            ][0]
        df_trend_entity = df_trend_entity.drop(index=row_to_delete)

        row_to_delete = df_trend_entity.index[
            df_trend_entity[0] == "3.D.2 - Autres (veuillez spécifier)"
            ][0]
        df_trend_entity = df_trend_entity.drop(index=row_to_delete)

    else :
        tables_inventory_original = camelot.read_pdf(
            str(input_folder / pdf_file), pages=page, flavor="lattice", split_text=True
        )
        df_trend_entity = tables_inventory_original[0].df[3 :]

    print("Reading complete.")

    # Add columns
    # 'data' prefix is needed for pd.wide_to_long() later
    columns_years = [
        "data1990",
        "data1995",
        "data2000",
        "data2005",
        "data2010",
        "data2015",
        "data2018",
        "data2019",
    ]
    df_trend_entity.columns = ["orig_cat_name"] + columns_years

    df_trend_entity = df_trend_entity.copy()

    # unit is always Gg
    df_trend_entity.loc[:, "unit"] = "Gg"

    # only one entity per table
    df_trend_entity.loc[:, "entity"] = entity

    df_trend_entity.loc[:, "category"] = df_trend_entity["orig_cat_name"]

    # Delete empty line for pages 132-137.
    if page != "131" :
        row_to_delete = df_trend_entity.index[df_trend_entity["category"] == ""][0]
        df_trend_entity = df_trend_entity.drop(index=row_to_delete)

    df_trend_entity["category"] = df_trend_entity["category"].replace(
        inv_conf["cat_codes_manual"]["trend"]
    )

    df_trend_entity.loc[:, "category"] = df_trend_entity["category"].str.replace(
        ".", ""
    )
    df_trend_entity.loc[:, "category"] = df_trend_entity["category"].str.replace(
        "\n", ""
    )


    def repl(m) :
        return m.group("code")


    df_trend_entity.loc[:, "category"] = df_trend_entity["category"].str.replace(
        inv_conf["cat_code_regexp"], repl, regex=True
    )

    df_trend_entity = df_trend_entity.reset_index(drop=True)

    print("Created category codes.")

    for year in columns_years :
        df_trend_entity.loc[:, year] = df_trend_entity[year].str.replace(",", ".")
        df_trend_entity.loc[:, year] = df_trend_entity[year].str.replace("NE1", "NE")

    # make sure all col headers are str
    df_trend_entity.columns = df_trend_entity.columns.map(str)

    df_trend_entity = df_trend_entity.drop(columns=["orig_cat_name"])

    # TODO wide in IF gibt es convert_wide_dataframe_if
    df_trend_entity_long = pd.wide_to_long(
        df_trend_entity, stubnames="data", i="category", j="time"
    )

    print("Converted to long format.")

    df_trend_entity_long = df_trend_entity_long.reset_index()

    if df_trend is None :
        df_trend = df_trend_entity_long
    else :
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

df_trend_IF = find_and_replace_values(df=df_trend_IF,
                                      replace_info=replace_info["trend"],
                                      category_column=category_column)

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
# increasing tolerance to merge values for 4.C, 1990, N2O - 0.003 in sector table, 0.0034 in main table
print("Merging waste table.")
data_pm2 = data_pm2.pr.merge(data_pm2_waste, tolerance=0.15)

# merge trend
print("Merging trend table.")
data_pm2 = data_pm2.pr.merge(data_pm2_trend, tolerance=0.11)

# convert back to IF to have units in the fixed format ( per year / per a / per annum)
data_if = data_pm2.pr.to_interchange_format()

# ###
# Save raw data to IF and native format.
# ###

pm2.pm2io.write_interchange_format(
    output_folder / (output_filename + coords_terminologies["category"] + "_raw"),
    data_if,
)

encoding = {var : compression for var in data_pm2.data_vars}
data_pm2.pr.to_netcdf(
    output_folder / (output_filename + coords_terminologies["category"] + "_raw.nc"),
    encoding=encoding,
)

# ###
# Processing
# ###

entities_to_ignore = []
processing_info_country = country_processing_step1

# Gather information
data_country = data_pm2

countries = list(data_country.coords[data_country.attrs["area"]].values)
if len(countries) > 1 :
    raise ValueError(
        f"Found {len(countries)} countries. Only single country data "
        f"can be processed by this function. countries: {countries}"
    )
else :
    country_code = countries[0]

# get category terminology
cat_col = data_country.attrs["cat"]
temp = re.findall(r"\((.*)\)", cat_col)
cat_terminology_in = temp[0]

# get scenario
scenarios = list(data_country.coords[data_country.attrs["scen"]].values)
if len(scenarios) > 1 :
    raise ValueError(
        f"Found {len(scenarios)} scenarios. Only single scenario data "
        f"can be processed by this function. Scenarios: {scenarios}"
    )
scenario = scenarios[0]

# get source
sources = list(data_country.coords["source"].values)
if len(sources) > 1 :
    raise ValueError(
        f"Found {len(sources)} sources. Only single source data "
        f"can be processed by this function. Sources: {sources}"
    )
source = sources[0]

# check if category name column present
if "orig_cat_name" in data_country.coords :
    cat_name_present = True
else :
    cat_name_present = False

# 1: general processing
# remove unused cats
data_country = data_country.dropna(f"category ({cat_terminology_in})", how="all")
# remove unused years
data_country = data_country.dropna("time", how="all")
# remove variables only containing nan
nan_vars_country = [
    var
    for var in data_country.data_vars
    if bool(data_country[var].isnull().all().data) is True
]
print(f"removing all-nan variables: {nan_vars_country}")
data_country = data_country.drop_vars(nan_vars_country)

tolerance = 0.01
agg_tolerance = tolerance

aggregate_cats_current = country_processing_step1["aggregate_cats"]

print(
    f"Aggregating categories for country {country_code}, source {source}, "
    f"scenario {scenario}"
)
for cat_to_agg in aggregate_cats_current :
    print(f"Category: {cat_to_agg}")
    source_cats = aggregate_cats_current[cat_to_agg]["sources"]
    data_agg = data_country.pr.loc[{"category" : source_cats}].pr.sum(
        dim="category", skipna=True, min_count=1
    )
    nan_vars = [
        var for var in data_agg.data_vars if data_agg[var].isnull().all().data is True
    ]
    data_agg = data_agg.drop(nan_vars)
    if len(data_agg.data_vars) > 0 :
        data_agg = data_agg.expand_dims([f"category (" f"{cat_terminology_in})"])
        data_agg = data_agg.assign_coords(
            coords={
                f"category ({cat_terminology_in})" : (
                    f"category ({cat_terminology_in})",
                    [cat_to_agg],
                )
            }
        )
        if cat_name_present :
            cat_name = aggregate_cats_current[cat_to_agg]["name"]
            data_agg = data_agg.assign_coords(
                coords={
                    "orig_cat_name" : (
                        f"category ({cat_terminology_in})",
                        [cat_name],
                    )
                }
            )
        data_country = data_country.pr.merge(data_agg, tolerance=agg_tolerance)
    else :
        print(f"no data to aggregate category {cat_to_agg}")

from UNFCCC_GHG_data.helper import GWP_factors

# copy HFCs and PFCs with default factors
GWPs_to_add = country_processing_step1["basket_copy"]["GWPs_to_add"]
entities = country_processing_step1["basket_copy"]["entities"]
source_GWP = country_processing_step1["basket_copy"]["source_GWP"]
for entity in entities :
    data_source = data_country[f"{entity} ({source_GWP})"]
    for GWP in GWPs_to_add :
        data_GWP = data_source * GWP_factors[f"{source_GWP}_to_{GWP}"][entity]
        data_GWP.attrs["entity"] = entity
        data_GWP.attrs["gwp_context"] = GWP
        data_country[f"{entity} ({GWP})"] = data_GWP

# create gas baskets
entities_present = set(data_country.data_vars)
for basket in gas_baskets.keys() :
    basket_contents_present = [
        gas for gas in gas_baskets[basket] if gas in entities_present
    ]
    if len(basket_contents_present) > 0 :
        if basket in list(data_country.data_vars) :
            data_country[basket] = data_country.pr.fill_na_gas_basket_from_contents(
                basket=basket,
                basket_contents=basket_contents_present,
                skipna=True,
                min_count=1,
            )
        else :
            try :
                # print(data_country.data_vars)
                data_country[basket] = xr.full_like(
                    data_country["CO2"], np.nan
                ).pr.quantify(units="Gg CO2 / year")
                data_country[basket].attrs = {
                    "entity" : basket.split(" ")[0],
                    "gwp_context" : basket.split(" ")[1][1 :-1],
                }
                data_country[basket] = data_country.pr.gas_basket_contents_sum(
                    basket=basket,
                    basket_contents=basket_contents_present,
                    min_count=1,
                )
                entities_present.add(basket)
            except Exception as ex :
                print(
                    f"No gas basket created for {country_code}, {source}, "
                    f"{scenario}: {ex}"
                )

# amend title and comment
data_country.attrs["comment"] = (
        data_country.attrs["comment"] + f" Processed on " f"{date.today()}"
)
data_country.attrs["title"] = (
        data_country.attrs["title"] + f" Processed on " f"{date.today()}"
)

# ###
# save processed data to IF and native format
# ###
data_proc_pm2 = data_country

terminology_proc = coords_terminologies["category"]

data_proc_if = data_proc_pm2.pr.to_interchange_format()

if not output_folder.exists() :
    output_folder.mkdir()
pm2.pm2io.write_interchange_format(
    output_folder / (output_filename + terminology_proc), data_proc_if
)

encoding = {var : compression for var in data_proc_pm2.data_vars}
data_proc_pm2.pr.to_netcdf(
    output_folder / (output_filename + terminology_proc + ".nc"), encoding=encoding
)

print("Saved processed data.")
