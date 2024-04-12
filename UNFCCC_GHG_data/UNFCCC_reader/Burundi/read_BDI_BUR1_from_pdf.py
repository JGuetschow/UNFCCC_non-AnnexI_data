import os

os.environ["UNFCCC_GHG_ROOT_PATH"] = (
    "/Users/danielbusch/Documents/UNFCCC_non-AnnexI_data"
)

import camelot
import primap2 as pm2
import pandas as pd

from UNFCCC_GHG_data.helper import downloaded_data_path, extracted_data_path
from UNFCCC_GHG_data.helper.functions import process_data_for_country

from config_BDI_BUR1 import (
    inv_conf,
    meta_data,
    filter_remove,
    coords_value_mapping,
    coords_terminologies,
    coords_defaults,
    coords_cols,
    years_to_read,
    gas_baskets,
    country_processing_step1,
)

# ###
# configuration
# ###

input_folder = downloaded_data_path / "UNFCCC" / "Burundi" / "BUR1"
output_folder = extracted_data_path / "UNFCCC" / "Burundi"

if not output_folder.exists():
    output_folder.mkdir()

pdf_file = "Burundi_BUR_1_Report__Francais.pdf"
output_filename = "BDI_BUR1_2023_"
category_column = f"category ({coords_terminologies['category']})"
compression = dict(zlib=True, complevel=9)

# ###
# 1. Read in tables
# ###

# table for the year 2005

df_all = None
for year in years_to_read:
    print("-" * 60)
    print(f"Reading year {year}.")
    print("-" * 60)
    df_year = None
    for page in inv_conf[year]["pages_to_read"]:
        print("-" * 20)
        print(f"Reading table from page {page}.")

        tables_inventory_original = camelot.read_pdf(
            str(input_folder / pdf_file),
            pages=page,
            # table_areas=page_def_templates[page]["area"],
            # columns=page_def_templates[page]["cols"],
            flavor="lattice",
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

    # remove line breaks
    for column in df_year.columns:
        df_year[column] = df_year[column].str.replace("\n", "")

    # fix broken values in cells
    if "fix_values" in inv_conf[year].keys():
        for index, column, value in inv_conf[year]["fix_values"]:
            df_year.at[index, column] = value

    # delete extra columns
    if "delete_columns" in inv_conf[year].keys():
        for column in inv_conf[year]["delete_columns"]:
            print(f"Delete columns {column} for year {year}")
            df_year = df_year.drop(columns=column)
        df_year.columns = range(df_year.columns.size)

    df_header = pd.DataFrame([inv_conf["header"], inv_conf["unit"]])

    df_year = pd.concat([df_header, df_year[2:]], axis=0, join="outer").reset_index(
        drop=True
    )

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
    df_year_long["category"] = df_year_long["category"].str.replace("\n", "")

    df_year_long["category"] = df_year_long["category"].replace(
        inv_conf["cat_codes_manual"]
    )

    df_year_long["category"] = df_year_long["category"].str.replace(".", "")

    # then the regex replacements
    def repl(m):
        return m.group("code")

    df_year_long["category"] = df_year_long["category"].str.replace(
        inv_conf["cat_code_regexp"], repl, regex=True
    )

    df_year_long = df_year_long.reset_index(drop=True)

    df_year_long["data"] = df_year_long["data"].str.replace(",", ".")
    df_year_long["data"] = df_year_long["data"].str.replace("NE1", "NE")

    # make sure all col headers are str
    df_year_long.columns = df_year_long.columns.map(str)
    df_year_long = df_year_long.drop(columns=["orig_cat_name"])

    assert "1A3di" not in df_year_long["category"].unique()

    if df_all is None:
        df_all = df_year_long
    else:
        df_all = pd.concat(
            [df_all, df_year_long],
            axis=0,
            join="outer",
        ).reset_index(drop=True)


print("Converting to interchange format.")
df_all_IF = pm2.pm2io.convert_long_dataframe_if(
    df_all,
    coords_cols=coords_cols,
    coords_defaults=coords_defaults,
    coords_terminologies=coords_terminologies,
    coords_value_mapping=coords_value_mapping,
    filter_remove=filter_remove,
    meta_data=meta_data,
    convert_str=True,
    time_format="%Y",
)

print("Converting to primap2 format.")
### convert to primap2 format ###
data_pm2 = pm2.pm2io.from_interchange_format(df_all_IF)


# ###
# Save raw data to IF and native format.
# ###

data_if = data_pm2.pr.to_interchange_format()

pm2.pm2io.write_interchange_format(
    output_folder / (output_filename + coords_terminologies["category"] + "_raw"),
    data_if,
)

encoding = {var: compression for var in data_pm2.data_vars}
data_pm2.pr.to_netcdf(
    output_folder / (output_filename + coords_terminologies["category"] + "_raw.nc"),
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
