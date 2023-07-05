# read Israel's BUR2 from pdf

# TODO: bunkers trend tables not read because of special format

from UNFCCC_GHG_data.helper import process_data_for_country, GWP_factors
from UNFCCC_GHG_data.helper import downloaded_data_path, extracted_data_path
import camelot
import primap2 as pm2
import pandas as pd
import locale

# configuration import
from config_ISR_BUR2 import trend_table_def, gwp_to_use
from config_ISR_BUR2 import inv_tab_conf, inv_table_def
from config_ISR_BUR2 import coords_cols, coords_terminologies, coords_defaults, \
    coords_value_mapping, filter_remove, filter_keep, meta_data
from config_ISR_BUR2 import cat_conversion, sectors_to_save, downscaling, \
    cats_to_agg, gas_baskets, terminology_proc
from config_ISR_BUR2 import is_int

### genral configuration
input_folder = downloaded_data_path / 'UNFCCC' / 'Israel' / 'BUR2'
output_folder = extracted_data_path / 'UNFCCC' / 'Israel'
if not output_folder.exists():
    output_folder.mkdir()

output_filename = 'ISR_BUR2_2021_'
inventory_file_pdf = '2nd_Biennial_Update_Report_2021_final.pdf'
#years_to_read = range(1990, 2018 + 1)
pages_to_read_trends = range(48, 54)
pages_to_read_inventory = range(54, 66)

# define locale to use for str to float conversion
locale_to_use = 'en_IL.UTF-8'
locale.setlocale(locale.LC_NUMERIC, locale_to_use)

compression = dict(zlib=True, complevel=9)

#### trend tables

# read
tables_trends = camelot.read_pdf(str(input_folder / inventory_file_pdf), pages=','.join(
    [str(page) for page in pages_to_read_trends]), flavor='lattice')

# convert to pm2
table_trends = None
for table in trend_table_def.keys():
    current_def = trend_table_def[table]
    new_table = None
    for subtable in current_def['tables']:
        if new_table is None:
            new_table = tables_trends[subtable].df
        else:
            new_table = pd.concat([new_table, tables_trends[subtable].df])

    for col in new_table.columns.values:
        new_table[col] = new_table[col].str.replace("\n", "")

    new_table.iloc[0, 0] = current_def['given_col']
    new_table.columns = new_table.iloc[0]
    new_table = new_table.drop(labels=[0])
    new_table = new_table.reset_index(drop=True)

    if 'take_only' in current_def.keys():
        new_table = new_table[
            new_table[current_def['given_col']].isin(current_def['take_only'])]

    time_cols = [col for col in new_table.columns.values if is_int(col)]
    for col in time_cols:
        # no NE,NA etc, just numbers, so we can just remove the ','
        new_table[col] = new_table[col].str.replace(',', '')
        new_table[col] = new_table[col].str.replace(' ', '')

    for col in current_def['cols_add']:
        new_table[col] = current_def['cols_add'][col]

    if table_trends is None:
        table_trends = new_table
    else:
        table_trends = pd.concat([table_trends, new_table])

# ###
# convert to PRIMAP2 interchange format
# ###
data_if_trends = pm2.pm2io.convert_wide_dataframe_if(
    table_trends,
    coords_cols=coords_cols,
    # add_coords_cols=add_coords_cols,
    coords_defaults=coords_defaults,
    coords_terminologies=coords_terminologies,
    coords_value_mapping=coords_value_mapping,
    # coords_value_filling=coords_value_filling,
    filter_remove=filter_remove,
    # filter_keep=filter_keep,
    meta_data=meta_data,
    convert_str=True,
    time_format='%Y'
)


data_pm2_trends = pm2.pm2io.from_interchange_format(data_if_trends)

#### inventory tables
# read inventory tables
tables_inv = camelot.read_pdf(
    str(input_folder / inventory_file_pdf),
    pages=','.join([str(page) for page in pages_to_read_inventory]),
    flavor='lattice')

# process
table_inv = None
for table in inv_table_def.keys():
    new_table = None
    print(f"working on year {table}")
    for subtable in inv_table_def[table]['tables']:
        print(f"adding table {subtable}")
        if new_table is None:
            new_table = tables_inv[subtable].df
        else:
            new_table = pd.concat([new_table, tables_inv[subtable].df], axis=0,
                                  join='outer')
            new_table = new_table.reset_index(drop=True)

        # replace line breaks, double, and triple spaces in category names
        new_table.iloc[:, 0] = new_table.iloc[:, 0].str.replace("\n", " ")
        new_table.iloc[:, 0] = new_table.iloc[:, 0].str.replace("   ", " ")
        new_table.iloc[:, 0] = new_table.iloc[:, 0].str.replace("  ", " ")

    if table == "2010":
        # table has a broken header. use last one
        new_table.iloc[inv_tab_conf["entity_row"]] = inv_tab_conf["header_2010"]
    else:
        # replace line breaks in units and entities
        new_table.iloc[inv_tab_conf["entity_row"]] = new_table.iloc[
            inv_tab_conf["entity_row"]].str.replace('\n', '')

    # get_year
    year = new_table.iloc[inv_tab_conf["cat_pos"][0], inv_tab_conf["cat_pos"][1]]

    # set category col label
    new_table.iloc[inv_tab_conf["cat_pos"][0], inv_tab_conf["cat_pos"][1]] = 'category'

    new_table = pm2.pm2io.nir_add_unit_information(
        new_table,
        unit_row=inv_tab_conf["unit_row"], entity_row=inv_tab_conf["entity_row"],
        regexp_entity=inv_tab_conf["regex_entity"], regexp_unit=inv_tab_conf[
            "regex_unit"],
        default_unit="", manual_repl_unit=inv_tab_conf["unit_repl"])

    # fix individual values
    if table == '1996':
        loc = new_table[new_table["category"] == "NITRIC ACID PRODUCTION"].index
        value = new_table.loc[loc, "CH4"].values
        new_table.loc[loc, "N2O"] = value[0, 0]
        new_table.loc[loc, "CH4"] = ''
    if table == '2015':
        loc_total = new_table[
            new_table["category"] == "Total national emissions and removals"].index
        loc_IPPU = new_table[new_table["category"] == "2. Industrial processes"].index
        value = new_table.loc[loc_IPPU, "PFCs"].values
        new_table.loc[loc_total, "PFCs"] = value[0, 0]

    # remove lines with empty category
    new_table = new_table.drop(new_table[new_table["category"] == ""].index)

    # rename E. Other (please specify) according to row above
    e_locs = list(new_table[new_table["category"] == "E. Other (please specify)"].index)
    for loc in e_locs:
        iloc = new_table.index.get_loc(loc)
        if new_table.iloc[iloc - 1]["category"][
            0] == "D. CO2 emissions and removals from soil":
            new_table.loc[loc]["category"] = "E. Other (LULUCF)"
        elif new_table.iloc[iloc - 1]["category"][0] in ["D.Waste-water handling",
                                                         'D. Waste-water handling']:
            new_table.loc[loc]["category"] = "E. Other (Waste)"

    # rename G. Other (please specify) according to row above
    g_locs = list(new_table[new_table["category"] == "G. Other (please specify)"].index)
    for loc in g_locs:
        iloc = new_table.index.get_loc(loc)
        if new_table.iloc[iloc - 1]["category"][
            0] == "F. Field burning of agricultural residues":
            new_table.loc[loc]["category"] = "G. Other (Agri)"
        elif new_table.iloc[iloc - 1]["category"][
            0] == "F. Consumption of halocarbons and sulphur hexafluoride":
            new_table.loc[loc]["category"] = "G. Other (IPPU)"

    # set index and convert to long format
    new_table = new_table.set_index(inv_tab_conf["index_cols"])
    new_table_long = pm2.pm2io.nir_convert_df_to_long(new_table, year,
                                                      inv_tab_conf["header_long"])
    # remove line breaks in values
    new_table_long["data"] = new_table_long["data"].str.replace("\n", "")

    if table_inv is None:
        table_inv = new_table_long
    else:
        table_inv = pd.concat([table_inv, new_table_long], axis=0, join='outer')
        table_inv = table_inv.reset_index(drop=True)

# no NE,NA etc, just numbers, so we can just remove the ','
table_inv["data"] = table_inv["data"].str.replace(',', '')
table_inv["data"] = table_inv["data"].str.replace(' ', '')

# ###
# convert to PRIMAP2 interchange format
# ###
data_if_inv = pm2.pm2io.convert_long_dataframe_if(
    table_inv,
    coords_cols=coords_cols,
    # add_coords_cols=add_coords_cols,
    coords_defaults=coords_defaults,
    coords_terminologies=coords_terminologies,
    coords_value_mapping=coords_value_mapping,
    # coords_value_filling=coords_value_filling,
    filter_remove=filter_remove,
    # filter_keep=filter_keep,
    meta_data=meta_data,
    convert_str=True,
    time_format='%Y',
)

data_pm2_inv = pm2.pm2io.from_interchange_format(data_if_inv)

#### combine
# tolerance needs to be high as rounding in trend tables leads to inconsistent data
data_pm2 = data_pm2_inv.pr.merge(data_pm2_trends,tolerance=0.11)
# convert back to IF to have units in the fixed format
data_if = data_pm2.pr.to_interchange_format()

# ###
# save data to IF and native format
# ###
if not output_folder.exists():
    output_folder.mkdir()
pm2.pm2io.write_interchange_format(
    output_folder / (output_filename + coords_terminologies["category"] + "_raw"), data_if)

encoding = {var: compression for var in data_pm2.data_vars}
data_pm2.pr.to_netcdf(
    output_folder / (output_filename + coords_terminologies["category"] + "_raw.nc"),
    encoding=encoding)


#### processing
data_proc_pm2 = data_pm2

# combine CO2 emissions and removals
temp_CO2 = data_proc_pm2["CO2"].copy()
#data_proc_pm2["CO2"] = data_proc_pm2[["CO2 emissions", "CO2 removals"]].to_array()
# .pr.sum(dim="variable", skipna=True, min_count=1)
data_proc_pm2["CO2"] = data_proc_pm2[["CO2 emissions", "CO2 removals"]].pr.sum\
    (dim="entity", skipna=True, min_count=1)
data_proc_pm2["CO2"].attrs = temp_CO2.attrs
data_proc_pm2["CO2"] = data_proc_pm2["CO2"].fillna(temp_CO2)

# actual processing
country_processing_step1 = {
    'aggregate_cats': cats_to_agg,
}
data_proc_pm2 = process_data_for_country(
    data_proc_pm2,
    entities_to_ignore=['CO2 emissions', 'CO2 removals'],
    gas_baskets={},
    processing_info_country=country_processing_step1,
)

country_processing_step2 = {
    'downscale': downscaling,
}
data_proc_pm2 = process_data_for_country(
    data_proc_pm2,
    entities_to_ignore=[],
    gas_baskets=gas_baskets,
    processing_info_country=country_processing_step2,
    cat_terminology_out = terminology_proc,
    category_conversion = cat_conversion,
    sectors_out = sectors_to_save,
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