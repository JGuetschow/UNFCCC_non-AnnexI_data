"""
Read data from Taiwan's 2023 national inventory

Data are read from the english summary pdf
"""

import copy

import camelot
import pandas as pd
import primap2 as pm2
from config_twn_nir2022 import fix_rows
from config_twn_nir2023 import (
    add_coords_cols,
    basket_copy,
    cat_code_regexp,
    cat_conversion,
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    meta_data,
    page_defs,
    table_defs,
    terminology_proc,
)
from primap2.pm2io._data_reading import matches_time_format

from unfccc_ghg_data.helper import (
    compression,
    downloaded_data_path,
    extracted_data_path,
    gas_baskets,
    make_wide_table,
    process_data_for_country,
)

# ###
# configuration
# ###
input_folder = downloaded_data_path / "non-UNFCCC" / "Taiwan" / "2023_NIR"
output_folder = extracted_data_path / "non-UNFCCC" / "Taiwan"
if not output_folder.exists():
    output_folder.mkdir()

output_filename = "TWN_inventory_2023_"
inventory_file = "2023_NIR_executive_summary_english.pdf"


def repl(m):  # noqa: D103
    return m.group("UNFCCC_GHG_data")


# ###
# read the tables from pdf
# ###

all_tables = []
for page in page_defs:
    print(f"Reading from page {page}")
    new_tables = camelot.read_pdf(
        str(input_folder / inventory_file),
        pages=page,
        **page_defs[page],
    )
    for table in new_tables:
        all_tables.append(table.df)


# ###
# convert tables to primap2 format
# ###
data_pm2 = None
for table_name in table_defs.keys():
    print(f"Working on table: {table_name}")

    table_def = copy.deepcopy(table_defs[table_name])
    # combine all raw tables
    df_this_table = all_tables[table_def["tables"][0]].copy(deep=True)
    if len(table_def["tables"]) > 1:
        for table in table_def["tables"][1:]:
            df_this_table = pd.concat(
                [df_this_table, all_tables[table]], axis=0, join="outer"
            )

    # fix for table ES3.6
    if table_name == "ES3.6":
        col_idx = df_this_table[0] == "Total CO Emission"
        df_this_table.loc[col_idx, 1:] = ""
        df_this_table.loc[col_idx, 0] = "Total CO2 Emission"

    df_this_table = df_this_table.reset_index(drop=True)

    # fix categories if necessary
    if "fix_cats" in table_def.keys():
        for col in table_def["fix_cats"]:
            df_this_table[col] = df_this_table[col].replace(table_def["fix_cats"][col])

    # fix rows
    for col in table_def["rows_to_fix"].keys():
        for n_rows in table_def["rows_to_fix"][col].keys():
            print(f"Fixing {col}, {n_rows}")
            # replace line breaks, long hyphens, double, and triple spaces in category names
            df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("\n", " ")
            df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("   ", " ")
            df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("  ", " ")
            df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("-", "-")
            df_this_table = fix_rows(
                df_this_table, table_def["rows_to_fix"][col][n_rows], col, n_rows
            )

    # split by entity
    if "gas_splitting" in table_def.keys():
        col_entity = [""] * len(df_this_table)
        last_entity = ""
        for i in range(0, len(df_this_table)):
            current_header = df_this_table[table_def["col_wide_kwd"]].iloc[i]
            if current_header in table_def["gas_splitting"].keys():
                last_entity = table_def["gas_splitting"][current_header]
            col_entity[i] = last_entity

        df_this_table["entity"] = col_entity
        table_def["index_cols"].append("entity")

    # make a wide table
    df_this_table = make_wide_table(
        df_this_table,
        table_def["wide_keyword"],
        table_def["col_wide_kwd"],
        table_def["index_cols"],
    )

    if "drop_rows" in table_def.keys():
        df_this_table = df_this_table.drop(table_def["drop_rows"], axis=0)

    # reset row index
    df_this_table = df_this_table.reset_index(drop=False)

    # add entity
    if "entity" in table_def.keys():
        df_this_table["entity"] = table_def["entity"]

    # add unit
    df_this_table["unit"] = table_def["unit"]

    df_this_table = df_this_table.rename(
        {table_def["index_cols"][0]: "orig_cat_name"}, axis=1
    )

    # print(table_def["index_cols"][0])
    # print(df_this_table.columns.values)

    # make a copy of the categories row
    df_this_table["category"] = df_this_table["orig_cat_name"]

    # replace cat names by codes in col "category"
    # first the manual replacements
    df_this_table["category"] = df_this_table["category"].replace(
        table_def["cat_codes_manual"]
    )

    # then the regex replacements
    df_this_table["category"] = df_this_table["category"].str.replace(
        cat_code_regexp, repl, regex=True
    )

    ### convert to PRIMAP2 IF
    # remove ','
    time_format = "%Y"
    time_columns = [
        col
        for col in df_this_table.columns.to_numpy()
        if matches_time_format(col, time_format)
    ]

    for col in time_columns:
        df_this_table.loc[:, col] = df_this_table.loc[:, col].str.replace(
            ",", "", regex=False
        )

    # drop orig_cat_name as it's not unique per category
    df_this_table = df_this_table.drop(columns="orig_cat_name")

    # coords_defaults_this_table = coords_defaults.copy()
    # coords_defaults_this_table["unit"] = table_def["unit"]
    df_this_table_if = pm2.pm2io.convert_wide_dataframe_if(
        df_this_table,
        coords_cols=coords_cols,
        add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        # coords_value_filling=coords_value_filling,
        # filter_remove=filter_remove,
        # filter_keep=filter_keep,
        meta_data=meta_data,
    )

    this_table_pm2 = pm2.pm2io.from_interchange_format(df_this_table_if)

    if data_pm2 is None:
        data_pm2 = this_table_pm2
    else:
        data_pm2 = data_pm2.pr.merge(this_table_pm2)

# convert back to IF to have units in the fixed format
data_if = data_pm2.pr.to_interchange_format()

# ###
# save data
# ###
# data in original categories
pm2.pm2io.write_interchange_format(
    output_folder / (output_filename + coords_terminologies["category"]), data_if
)
encoding = {var: compression for var in data_pm2.data_vars}
data_pm2.pr.to_netcdf(
    (output_folder / (output_filename + coords_terminologies["category"])).with_suffix(
        ".nc"
    ),
    encoding=encoding,
)


# ###
# convert to IPCC2006 categories
# ###
data_proc_pm2 = data_pm2.copy(deep=True)


country_processing = {
    "basket_copy": basket_copy,
}

data_proc_pm2 = process_data_for_country(
    data_proc_pm2,
    entities_to_ignore=[],
    gas_baskets=gas_baskets,
    processing_info_country=country_processing,
    cat_terminology_out=terminology_proc,
    category_conversion=cat_conversion,
)

# convert to IF
data_proc_if = data_proc_pm2.pr.to_interchange_format()

# ###
# save data
# ###
# data in 2006 categories
pm2.pm2io.write_interchange_format(
    output_folder / (output_filename + "IPCC2006_PRIMAP"), data_proc_if
)
encoding = {var: compression for var in data_proc_pm2.data_vars}
data_proc_pm2.pr.to_netcdf(
    (output_folder / (output_filename + "IPCC2006_PRIMAP")).with_suffix(".nc"),
    encoding=encoding,
)
