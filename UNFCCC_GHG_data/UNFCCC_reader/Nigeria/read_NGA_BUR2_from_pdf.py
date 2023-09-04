# this script reads data from Nigeria's BUR2
# Data is read from the pdf file

import pandas as pd
import primap2 as pm2
import numpy as np
import camelot
import locale
from copy import deepcopy
from UNFCCC_GHG_data.helper import downloaded_data_path, extracted_data_path
from UNFCCC_GHG_data.helper import process_data_for_country, gas_baskets
from config_NGA_BUR2 import tables_trends
from config_NGA_BUR2 import pages_inventory, year_inventory, entity_row, unit_row, \
   index_cols, header_long, units_inv
from config_NGA_BUR2 import cat_code_regexp, cat_codes_manual
from config_NGA_BUR2 import coords_cols, coords_defaults, coords_terminologies, \
    coords_value_mapping, meta_data, filter_remove #, add_coords_cols
from config_NGA_BUR2 import processing_info_step1, processing_info_step2

# ###
# configuration
# ###
# define locale to use for str to float conversion
locale_to_use = 'en_NG.UTF-8'
locale.setlocale(locale.LC_NUMERIC, locale_to_use)

input_folder = downloaded_data_path / 'UNFCCC' / 'Nigeria' / 'BUR2'
output_folder = extracted_data_path / 'UNFCCC' / 'Nigeria'
if not output_folder.exists():
   output_folder.mkdir()

output_filename = 'NGA_BUR2_2021_'
compression = dict(zlib=True, complevel=9)
inventory_file = 'NIGERIA_BUR_2_-_Second_Biennial_Update_Report_%28BUR2%29.pdf'

## read 2019 inventory
df_inventory = None
for page in pages_inventory.keys():
    tables = camelot.read_pdf(str(input_folder / inventory_file), pages=str(page),
                              flavor='lattice')
    df_this_table = tables[pages_inventory[page]].df
    # replace line breaks, double, and triple spaces in category names
    df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("\n", " ")
    df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("   ", " ")
    df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("  ", " ")
    # replace line breaks in units and entities
    df_this_table.iloc[entity_row] = df_this_table.iloc[entity_row].str.replace('\n',
                                                                                '')
    df_this_table.iloc[unit_row] = df_this_table.iloc[unit_row].str.replace('\n', '')

    # fillna in unit row
    df_this_table.iloc[unit_row][df_this_table.iloc[unit_row]==""] = np.nan
    df_this_table.iloc[unit_row] = df_this_table.iloc[unit_row].fillna(
        method='ffill')
    df_this_table = pm2.pm2io.nir_add_unit_information(df_this_table, unit_row=unit_row,
                                                       entity_row=entity_row,
                                                       regexp_entity=".*",
                                                       manual_repl_unit=units_inv,
                                                       default_unit="")

    # set index and convert to long format
    df_this_table = df_this_table.set_index(index_cols)
    df_this_table_long = pm2.pm2io.nir_convert_df_to_long(df_this_table, year_inventory,
                                                          header_long)

    # combine with tables for other sectors (merge not append)
    if df_inventory is None:
        df_inventory = df_this_table_long
    else:
        df_inventory = pd.concat([df_inventory, df_this_table_long], axis=0, join='outer')

# replace cat names by codes in col "category"
# first the manual replacements
df_inventory["category"] = df_inventory["category"].replace(cat_codes_manual)
# then the regex replacements
repl = lambda m: m.group('code')
df_inventory["category"] = df_inventory["category"].str.replace(cat_code_regexp, repl, regex=True)
df_inventory = df_inventory.reset_index(drop=True)

# ###
# convert to PRIMAP2 interchange format
# ###
data_inv_if = pm2.pm2io.convert_long_dataframe_if(
    df_inventory,
    coords_cols=coords_cols,
    #add_coords_cols=add_coords_cols,
    coords_defaults=coords_defaults,
    coords_terminologies=coords_terminologies,
    coords_value_mapping=coords_value_mapping,
    filter_remove=filter_remove,
    meta_data=meta_data,
    convert_str=True,
    time_format='%Y',
    )

data_inv_pm2 = pm2.pm2io.from_interchange_format(data_inv_if)

## trend tables
data_trend_pm2 = None
for table in tables_trends.keys():
    print(table)
    current_table = deepcopy(tables_trends[table])
    tables = camelot.read_pdf(str(input_folder / inventory_file),
                              pages=current_table["page"],
                              table_areas=current_table["area"],
                              columns=current_table["cols"],
                              flavor='stream',
                              split_text=True)
    df_this_table = tables[0].df

    # merge rows for entity and unit
    rows_to_merge = df_this_table.iloc[current_table["label_rows"]]
    indices_to_merge = rows_to_merge.index
    # join the three rows
    new_row = rows_to_merge.agg(' '.join)
    df_this_table.loc[indices_to_merge[0]] = new_row
    df_this_table = df_this_table.drop(indices_to_merge)
    new_row = new_row.str.replace("  ", " ")
    new_row = new_row.str.replace("   ", " ")
    new_row = new_row.str.strip()

    df_this_table.columns = new_row

    # remove columns not needed
    if 'remove_cols' in current_table.keys():
        df_this_table = df_this_table.drop(columns=current_table["remove_cols"])

    df_this_table = df_this_table.set_index("Year")

    # transpose to wide format
    df_this_table = df_this_table.transpose()

    # remove "," (thousand sep) from data
    for col in df_this_table.columns:
        df_this_table.loc[:, col] = df_this_table.loc[:, col].str.strip()
        repl = lambda m: m.group('part1') + m.group('part2')
        df_this_table.loc[:, col] = df_this_table.loc[:, col].str.replace(
            '(?P<part1>[0-9]+),(?P<part2>[0-9\.]+)$', repl, regex=True)
        df_this_table[col][df_this_table[col].isnull()] = 'NaN'


    # metadta in forst col instread of index
    df_this_table = df_this_table.reset_index()
    df_this_table = df_this_table.rename(columns={"index": "Year"})

    # make sure we have str not a number format for the dates
    df_this_table.columns = df_this_table.columns.map(str)

    current_table["coords_defaults"].update(coords_defaults)
    # convert to interchange format
    data_current_if = pm2.pm2io.convert_wide_dataframe_if(
        df_this_table,
        coords_cols=current_table["coords_cols"],
        coords_defaults=current_table["coords_defaults"],
        coords_terminologies=coords_terminologies,
        coords_value_mapping=current_table["coords_value_mapping"],
        meta_data=meta_data,
        convert_str=True,
        time_format='%Y',
    )
# todo: convert to native format before merge
    data_current_pm2 = pm2.pm2io.from_interchange_format(data_current_if)
    if data_trend_pm2 is None:
        data_trend_pm2 = data_current_pm2
    else:
        data_trend_pm2 = data_trend_pm2.pr.merge(data_current_pm2)

data_pm2 = data_inv_pm2.pr.merge(data_trend_pm2, tolerance=0.05) # some rounding in
# trends needs higher tolerance

data_if = data_pm2.pr.to_interchange_format()

# ###
# save raw data to IF and native format
# ###
if not output_folder.exists():
    output_folder.mkdir()
pm2.pm2io.write_interchange_format(
    output_folder / (output_filename + coords_terminologies["category"] + "_raw"),
    data_if)

encoding = {var: compression for var in data_pm2.data_vars}
data_pm2.pr.to_netcdf(
    output_folder / (output_filename + coords_terminologies["category"] + "_raw.nc"),
    encoding=encoding)


#### processing
data_proc_pm2 = data_pm2
terminology_proc = coords_terminologies["category"]

# actual processing
data_proc_pm2 = process_data_for_country(
    data_proc_pm2,
    entities_to_ignore=[],
    gas_baskets={},
    processing_info_country=processing_info_step1,
)

data_proc_pm2 = process_data_for_country(
    data_proc_pm2,
    entities_to_ignore=[],
    gas_baskets=gas_baskets,
    processing_info_country=processing_info_step2,
    cat_terminology_out = terminology_proc,
    #category_conversion = None,
    #sectors_out = None,
)

# adapt source and metadata
# TODO: processing info is present twice
current_source = data_proc_pm2.coords["source"].values[0]
data_temp = data_proc_pm2.pr.loc[{"source": current_source}]
data_proc_pm2 = data_proc_pm2.pr.set("source", 'BUR_NIR', data_temp)

# ###
# save data to IF and native format
# ###
data_proc_if = data_proc_pm2.pr.to_interchange_format()
if not output_folder.exists():
    output_folder.mkdir()
pm2.pm2io.write_interchange_format(
    output_folder / (output_filename + terminology_proc), data_proc_if)

encoding = {var: compression for var in data_proc_pm2.data_vars}
data_proc_pm2.pr.to_netcdf(
    output_folder / (output_filename + terminology_proc + ".nc"),
    encoding=encoding)