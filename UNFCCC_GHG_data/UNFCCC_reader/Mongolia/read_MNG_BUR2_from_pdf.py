import camelot
import primap2 as pm2
import pandas as pd

from UNFCCC_GHG_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    fix_rows,
    process_data_for_country,
)
from config_MNG_BUR2 import (
    inv_conf,
    inv_conf_per_year,
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    filter_remove,
    meta_data,
    country_processing_step1,
    gas_baskets,
)

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

# ###
# 1. Read in tables
# ###

df_all = None
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

    if year == "2020":
        break

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
    # TODO not sure this is needed
    df_year_long["category"] = df_year_long["category"].str.replace("\n", "")

    df_year_long["category"] = df_year_long["category"].replace(
        inv_conf["cat_codes_manual"]
    )
    # TODO not sure this is needed
    df_year_long["category"] = df_year_long["category"].str.replace(".", "")

    # then the regex replacements
    def repl(m):
        return m.group("code")

    df_year_long["category"] = df_year_long["category"].str.replace(
        inv_conf["cat_code_regexp"], repl, regex=True
    )

    df_year_long = df_year_long.reset_index(drop=True)

    df_year_long["data"] = df_year_long["data"].str.replace(",", "")

    # make sure all col headers are str
    df_year_long.columns = df_year_long.columns.map(str)

    df_year_long = df_year_long.drop(columns=["orig_cat_name"])

    if df_all is None:
        df_all = df_year_long
    else:
        df_all = pd.concat(
            [df_all, df_year_long],
            axis=0,
            join="outer",
        ).reset_index(drop=True)

### convert to interchange format ###
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

### convert to primap2 format ###
print("Converting to primap2 format.")
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
    filter_dims=None,
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