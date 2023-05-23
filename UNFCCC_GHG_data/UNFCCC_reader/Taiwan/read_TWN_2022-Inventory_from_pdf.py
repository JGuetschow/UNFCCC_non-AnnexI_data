# this script reads data from Taiwan's 2022 national inventory
# Data is read from the english summary pdf

import pandas as pd
import primap2 as pm2
import camelot
import copy

from UNFCCC_GHG_data.helper import downloaded_data_path, extracted_data_path
from primap2.pm2io._data_reading import matches_time_format

from config_TWN_NIR2022 import table_defs, page_defs
from config_TWN_NIR2022 import fix_rows, make_wide_table
from config_TWN_NIR2022 import gwp_to_use

# ###
# configuration
# ###
input_folder = downloaded_data_path / 'non-UNFCCC' / 'Taiwan'
# TODO: move file to subfolder
output_folder = extracted_data_path / 'non-UNFCCC' / 'Taiwan'
if not output_folder.exists():
    output_folder.mkdir()

output_filename = 'TWN_inventory_2022_'
inventory_file = '00_abstract_en.pdf'

cat_code_regexp = r'(?P<UNFCCC_GHG_data>^[a-zA-Z0-9\.]{1,7})\s.*'

time_format = "%Y"

coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
    # "area": "Geo_code",
}

add_coords_cols = {
    #    "orig_cat_name": ["orig_cat_name", "category"],
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_1996_Taiwan_Inv",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "TWN-GHG-Inventory",
    "provenance": "measured",
    "scenario": "2022NIR",
    "area": "TWN",
    # unit fill by table
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
}

coords_value_filling = {}

#
filter_remove = {}

filter_keep = {}

meta_data = {
    "references": "https://unfccc.saveoursky.org.tw/nir/tw_nir_2022.php",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "2022 Republic of China - National Greenhouse Gas Report",
    "comment": "Read fom pdf file and converted to PRIMAP2 format by Johannes Gütschow",
    "institution": "Republic of China - Environmental Protection Administration",
}

# config for part3: mapping to 2006 categpries

cat_mapping = {
    '3': 'M.AG',
    '3.A': '3.A.1',
    '3.B': '3.A.2',
    '3.C': '3.C.7',
    '3.D': 'M.3.AS',
    '3.F': '3.C.1.b',
    '3.H': '3.C.3',
    '4': 'M.LULUCF',
    '5': '4',
    '5.A': '4.A',
    '5.B': '4.B',
    '5.C': '4.C',
    '5.D': '4.D',
    '5.D.1': '4.D.1',
    '5.D.2': '4.D.2',
}

aggregate_cats = {
    '1.A': {'sources': ['1.A.1', '1.A.2', '1.A.3', '1.A.4'],
            'name': 'Fuel Combustion Activities'},
    '1.B': {'sources': ['1.B.1', '1.B.2'], 'name': 'Fugitive Emissions from Fuels'},
    '3.A': {'sources': ['3.A.1', '3.A.2'], 'name': 'Livestock'},
    '3.C.1': {'sources': ['3.C.1.b'], 'name': 'Emissions from Biomass Burning'},
    '3.C.5': {'sources': ['3.C.5.a', '3.C.5.b'],
              'name': 'Indirect N2O Emissions from Managed Soils'},
    '3.C': {'sources': ['3.C.1', '3.C.3', 'M.3.AS', '3.C.7'],
            'name': 'Aggregate sources and non-CO2 emissions sources on land'},
    '3': {'sources': ['M.AG', 'M.LULUCF'], 'name': 'AFOLU'},
    'M.AG.ELV': {'sources': ['3.C'],
                 'name': 'Agriculture excluding livestock emissions'},
}


# 2 for NF3, PFCs (from 2.E)
aggregate_cats_NF3_PFC = {
    '2': {'sources': ['2.E'], 'name': 'Industrial Process and Product Use Sector'},
}

compression = dict(zlib=True, complevel=9)

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
                [df_this_table, all_tables[table]],
                axis=0,
                join='outer')

    # fix for table ES3.6
    if table_name == 'ES3.6':
        col_idx = df_this_table[0] == "Total CO Emission"
        df_this_table.loc[col_idx, 1:] = ''
        df_this_table.loc[col_idx, 0] = 'Total CO2 Emission'

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
            df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("–", "-")
            df_this_table = fix_rows(df_this_table,
                                     table_def["rows_to_fix"][col][n_rows], col, n_rows)

    # split by entity
    if "gas_splitting" in table_def.keys():
        col_entity = [''] * len(df_this_table)
        last_entity = ''
        for i in range(0, len(df_this_table)):
            current_header = df_this_table[table_def["col_wide_kwd"]].iloc[i]
            if current_header in table_def["gas_splitting"].keys():
                last_entity = table_def["gas_splitting"][current_header]
            col_entity[i] = last_entity

        df_this_table["entity"] = col_entity
        table_def["index_cols"].append("entity")

    # make a wide table
    df_this_table = make_wide_table(df_this_table, table_def["wide_keyword"],
                                    table_def["col_wide_kwd"], table_def["index_cols"])

    if "drop_rows" in table_def.keys():
        df_this_table = df_this_table.drop(table_def["drop_rows"], axis=0)

    # reset row index
    df_this_table = df_this_table.reset_index(drop=False)

    # add entity
    if "entity" in table_def.keys():
        df_this_table["entity"] = table_def["entity"]

    # add unit
    df_this_table["unit"] = table_def["unit"]

    df_this_table = df_this_table.rename({table_def["index_cols"][0]: "orig_cat_name"},
                                         axis=1)

    # print(table_def["index_cols"][0])
    # print(df_this_table.columns.values)

    # make a copy of the categories row
    df_this_table["category"] = df_this_table["orig_cat_name"]

    # replace cat names by codes in col "category"
    # first the manual replacements
    df_this_table["category"] = df_this_table["category"].replace(
        table_def["cat_codes_manual"])
    # then the regex replacements
    repl = lambda m: m.group('UNFCCC_GHG_data')
    df_this_table["category"] = df_this_table["category"].str.replace(cat_code_regexp,
                                                                      repl, regex=True)

    ### convert to PRIMAP2 IF
    # remove ','
    time_format = '%Y'
    time_columns = [
        col
        for col in df_this_table.columns.values
        if matches_time_format(col, time_format)
    ]

    for col in time_columns:
        df_this_table.loc[:, col] = df_this_table.loc[:, col].str.replace(',', '',
                                                                          regex=False)

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
        meta_data=meta_data
    )

    this_table_pm2 = pm2.pm2io.from_interchange_format(df_this_table_if)

    if data_pm2 is None:
        data_pm2 = this_table_pm2
    else:
        data_pm2 = data_pm2.pr.merge(this_table_pm2)

# convert back to IF to have units in the fixed format
data_if = data_pm2.pr.to_interchange_format()


# ###
# convert to IPCC2006 categories
# ###
data_if_2006 = data_if.copy(deep=True)
data_if_2006
# filter_data(data_if_2006, filter_remove=filter_remove_IPCC2006)
data_if_2006 = data_if_2006.replace(
    {'category (IPCC2006_1996_Taiwan_Inv)': cat_mapping})

# rename the category col
data_if_2006.rename(
    columns={'category (IPCC2006_1996_Taiwan_Inv)': 'category (IPCC2006_PRIMAP)'},
    inplace=True)
data_if_2006.attrs['attrs']['cat'] = 'category (IPCC2006_PRIMAP)'
data_if_2006.attrs['dimensions']['*'] = [
    'category (IPCC2006_PRIMAP)' if item == 'category (IPCC2006_1996_Taiwan_Inv)'
    else item for item in data_if_2006.attrs['dimensions']['*']]

# aggregate categories
for cat_to_agg in aggregate_cats:
    mask = data_if_2006["category (IPCC2006_PRIMAP)"].isin(
        aggregate_cats[cat_to_agg]["sources"])
    df_test = data_if_2006[mask]

    if len(df_test) > 0:
        print(f"Aggregating category {cat_to_agg}")
        df_combine = df_test.copy(deep=True)

        time_format = '%Y'
        time_columns = [
            col
            for col in df_combine.columns.values
            if matches_time_format(col, time_format)
        ]

        for col in time_columns:
            df_combine[col] = pd.to_numeric(df_combine[col], errors="coerce")

        df_combine = df_combine.groupby(
            by=['source', 'scenario (PRIMAP)', 'provenance', 'area (ISO3)', 'entity',
                'unit']).sum(min_count=1)

        df_combine.insert(0, "category (IPCC2006_PRIMAP)", cat_to_agg)
        # df_combine.insert(1, "cat_name_translation", aggregate_cats[cat_to_agg]["name"])
        # df_combine.insert(2, "orig_cat_name", "computed")

        df_combine = df_combine.reset_index()

        data_if_2006 = data_if_2006.append(df_combine)
        data_if_2006 = data_if_2006.reset_index(drop=True)
    else:
        print(f"no data to aggregate category {cat_to_agg}")

# aggregate categories
for cat_to_agg in aggregate_cats_NF3_PFC:
    mask = data_if_2006["category (IPCC2006_PRIMAP)"].isin(
        aggregate_cats_NF3_PFC[cat_to_agg]["sources"])
    mask_gas = data_if_2006["entity"].isin(
        [f"NF3 ({gwp_to_use})", f"PFCS ({gwp_to_use})"])
    df_test = data_if_2006[mask & mask_gas]

    if len(df_test) > 0:
        print(f"Aggregating category {cat_to_agg}")
        df_combine = df_test.copy(deep=True)

        time_format = '%Y'
        time_columns = [
            col
            for col in df_combine.columns.values
            if matches_time_format(col, time_format)
        ]

        for col in time_columns:
            df_combine[col] = pd.to_numeric(df_combine[col], errors="coerce")

        df_combine = df_combine.groupby(
            by=['source', 'scenario (PRIMAP)', 'provenance', 'area (ISO3)', 'entity',
                'unit']).sum(min_count=1)

        df_combine.insert(0, "category (IPCC2006_PRIMAP)", cat_to_agg)
        # df_combine.insert(1, "cat_name_translation", aggregate_cats[cat_to_agg]["name"])
        # df_combine.insert(2, "orig_cat_name", "computed")

        df_combine = df_combine.reset_index()

        data_if_2006 = data_if_2006.append(df_combine)
        data_if_2006 = data_if_2006.reset_index(drop=True)
    else:
        print(f"no data to aggregate category {cat_to_agg}")

# conversion to PRIMAP2 native format
data_pm2_2006 = pm2.pm2io.from_interchange_format(data_if_2006)

# convert to mass units from CO2eq
entities_to_convert = ['N2O', 'SF6', 'CH4', 'NF3']
entities_to_convert = [f"{entity} ({gwp_to_use})" for entity in entities_to_convert]

for entity in entities_to_convert:
    converted = data_pm2_2006[entity].pr.convert_to_mass()
    basic_entity = entity.split(" ")[0]
    converted = converted.to_dataset(name=basic_entity)
    data_pm2_2006 = data_pm2_2006.pr.merge(converted)
    data_pm2_2006[basic_entity].attrs["entity"] = basic_entity

# drop the GWP data
data_pm2_2006 = data_pm2_2006.drop_vars(entities_to_convert)

# convert to IF
data_if_2006 = data_pm2_2006.pr.to_interchange_format()

# ###
# save data
# ###
# data in original categories
pm2.pm2io.write_interchange_format(output_folder /
                                   (output_filename + coords_terminologies["category"]),
                                   data_if)
encoding = {var: compression for var in data_pm2.data_vars}
data_pm2.pr.to_netcdf((output_folder /
                      (output_filename + coords_terminologies[
                          "category"])).with_suffix(".nc"),
                      encoding=encoding)

# data in 2006 categories
pm2.pm2io.write_interchange_format(output_folder /
                                   (output_filename + "IPCC2006_PRIMAP"), data_if_2006)
encoding = {var: compression for var in data_pm2_2006.data_vars}
data_pm2_2006.pr.to_netcdf((output_folder /
                            (output_filename + "IPCC2006_PRIMAP")).with_suffix(".nc"),
                           encoding=encoding)
