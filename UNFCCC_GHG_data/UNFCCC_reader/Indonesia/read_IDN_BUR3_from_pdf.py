# this script reads data from Indonesia's BUR3
# Data is read from pdf
# only the 2019 inventory is read as the BUR refers to BUR2 for earlier years

import pandas as pd
import primap2 as pm2
import camelot
import numpy as np
from primap2.pm2io._data_reading import matches_time_format
from UNFCCC_GHG_data.helper import downloaded_data_path, extracted_data_path

# ###
# configuration
# ###
input_folder = downloaded_data_path / 'UNFCCC' / 'Indonesia' / 'BUR3'
output_folder = extracted_data_path / 'UNFCCC' / 'Indonesia'
if not output_folder.exists():
    output_folder.mkdir()

output_filename = 'IDN_BUR3_2021_'

inventory_file = 'IndonesiaBUR_3_FINAL_REPORT_2.pdf'

gwp_to_use = 'SARGWP100'

pages_to_read = range(61,65) # 65 is not read properly but contains almost no data anyway, so add it by hand '61-65'

compression = dict(zlib=True, complevel=9)

year = 2019
entity_row = 0
unit_row = 1
index_cols = "Categories"
# special header as category UNFCCC_GHG_data and name in one column
header_long = ["orig_cat_name", "entity", "unit", "time", "data"]


# manual category codes
cat_codes_manual = {
    'Total National Emissions and Removals': '0',
    'Peat Decomposition': 'M.3.B.4.APD',
    'Peat Fire': 'M.3.B.4.APF',
    '4A1.2 Industrial Solid Waste Disposal': 'M.4.A.Ind',
    #'3A2b Direct N2O Emissions from Manure Management': '3.A.2',
}

cat_code_regexp = r'(?P<UNFCCC_GHG_data>^[a-zA-Z0-9]{1,4})\s.*'

coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

add_coords_cols = {
    "orig_cat_name": ["orig_cat_name", "category"],
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "IDN-GHG-Inventory",
    "provenance": "measured",
    "area": "IDN",
    "scenario": "BUR3",
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        'Total 3 Gases': f"CO2CH4N2O ({gwp_to_use})",
        'Net CO2 (1) (2)': 'CO2',
        'CH4': f"CH4 ({gwp_to_use})",
        'N2O': f"N2O ({gwp_to_use})",
        'HFCs': f"HFCS ({gwp_to_use})",
        'PFCs': f"PFCS ({gwp_to_use})",
        'SF6': f"SF6 ({gwp_to_use})",
        'NOx': 'NOX',
        'CO': 'CO', # no mapping, just added for completeness here
        'NMVOCs': 'NMVOC',
        'SO2': 'SO2', # no mapping, just added for completeness here
        'Other halogenated gases with CO2 equivalent conversion factors (3)': f"OTHERHFCS ({gwp_to_use})",
    },
}


filter_remove = {
    "fHFC": {"entity": 'Other halogenated gases without CO2 equivalent conversion factors (4)'}
}

filter_keep = {}

meta_data = {
    "references": "https://unfccc.int/documents/403577",
    "rights": "",
    "contact": "mail@johannes-guestchow.de",
    "title": "Indonesia. Biennial update report (BUR). BUR3",
    "comment": "Read fom pdf by Johannes Gütschow",
    "institution": "UNFCCC",
}

# convert to mass units where possible
entities_to_convert_to_mass = [
    'CH4', 'N2O', 'SF6'
]

# CO2 equivalents don't make sense for these substances, so unit has to be Gg instead of Gg CO2 equivalents as indicated in the table
entities_to_fix_unit = [
    'NOx', 'CO', 'NMVOCs', 'SO2'
]

# add the data for the last page by hand as it's only one row
data_last_page = [
    ['5B Other (please specify)', 'Total 3 Gases', 'GgCO2eq', '2019', 'NE'],
    ['5B Other (please specify)', 'Net CO2 (1) (2)', 'GgCO2eq', '2019', np.nan],
    ['5B Other (please specify)', 'CH4', 'GgCO2eq', '2019', np.nan],
    ['5B Other (please specify)', 'N2O', 'GgCO2eq', '2019', np.nan],
    ['5B Other (please specify)', 'HFCs', 'GgCO2eq', '2019', np.nan],
    ['5B Other (please specify)', 'PFCs', 'GgCO2eq', '2019', np.nan],
    ['5B Other (please specify)', 'SF6', 'GgCO2eq', '2019', np.nan],
    ['5B Other (please specify)', 'Other halogenated gases with CO2 equivalent conversion factors (3)', 'GgCO2eq', '2019', np.nan],
    ['5B Other (please specify)', 'Other halogenated gases without CO2 equivalent conversion factors (4)', 'GgCO2eq', '2019', np.nan],
    ['5B Other (please specify)', 'NOx', 'GgCO2eq', '2019', np.nan],
    ['5B Other (please specify)', 'CO', 'GgCO2eq', '2019', np.nan],
    ['5B Other (please specify)', 'NMVOCs', 'GgCO2eq', '2019', np.nan],
    ['5B Other (please specify)', 'SO2', 'GgCO2eq', '2019', np.nan],
]

df_last_page = pd.DataFrame(data_last_page, columns=header_long)

aggregate_cats = {
    '1.A.4': {'sources': ['1.A.4.a', '1.A.4.b'], 'name': 'Other Sectors (calculated)'},
    '2.A.4': {'sources': ['2.A.4.a', '2.A.4.b', '2.A.4.d'], 'name': 'Other Process uses of Carbonates (calculated)'},
    '2.B.8': {'sources': ['2.B.8.a', '2.B.8.b', '2.B.8.c', '2.B.8.f'], 'name': 'Petrochemical and Carbon Black production (calculated)'},
    '4.A': {'sources': ['4.A.2', 'M.4.A.Ind'], 'name': 'Solid Waste Disposal (calculated)'},
}

aggregate_cats_N2O = {
    '3.A.2': {'sources': ['3.A.2.b'], 'name': '3A2 Manure Management'},
    '3.A': {'sources': ['3.A.2'], 'name': '3A Livestock'},
}

aggregate_cats_CO2CH4N2O = {
    '3.A.2': {'sources': ['3.A.2', '3.A.2.b'], 'name': '3A2 Manure Management'},
}

df_all = None

for page in pages_to_read:
    tables = camelot.read_pdf(str(input_folder / inventory_file), pages=str(page),
                              flavor='lattice')
    df_this_table = tables[0].df
    # replace line breaks, double, and triple spaces in category names
    df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("\n", " ")
    df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("   ", " ")
    df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("  ", " ")
    # replace line breaks in units and entities
    df_this_table.iloc[entity_row] = df_this_table.iloc[entity_row].str.replace('\n',
                                                                                '')
    df_this_table.iloc[unit_row] = df_this_table.iloc[unit_row].str.replace('\n', '')

    df_this_table = pm2.pm2io.nir_add_unit_information(df_this_table, unit_row=unit_row,
                                                       entity_row=entity_row,
                                                       regexp_entity=".*",
                                                       default_unit="GgCO2eq")  # , **unit_info)

    # set index and convert to long format
    df_this_table = df_this_table.set_index(index_cols)
    df_this_table_long = pm2.pm2io.nir_convert_df_to_long(df_this_table, year,
                                                          header_long)
    df_this_table_long["orig_cat_name"] = df_this_table_long["orig_cat_name"].str[0]

    # combine with tables for other sectors (merge not append)
    if df_all is None:
        df_all = df_this_table_long
    else:
        df_all = pd.concat([df_all, df_this_table_long], axis=0, join='outer')

# add the last page manually
df_all = pd.concat([df_all, df_last_page], axis=0, join='outer')

# fix the units of aerosols and precursors
for entity in entities_to_fix_unit:
    df_all["unit"][df_all["entity"] == entity] = "Gg"

# make a copy of the categories row
df_all["category"] = df_all["orig_cat_name"]

# replace cat names by codes in col "category"
# first the manual replacements
df_all["category"] = df_all["category"].replace(cat_codes_manual)
# then the regex replacements
repl = lambda m: m.group('UNFCCC_GHG_data')
df_all["category"] = df_all["category"].str.replace(cat_code_regexp, repl, regex=True)
df_all = df_all.reset_index(drop=True)

###### convert to primap2 IF

# replace "," with "" in data
df_all.loc[:, "data"] = df_all.loc[:, "data"].str.replace(',','', regex=False)

# make sure all col headers are str
df_all.columns = df_all.columns.map(str)



# ###
# convert to PRIMAP2 interchange format
# ###
data_if = pm2.pm2io.convert_long_dataframe_if(
    df_all,
    coords_cols=coords_cols,
    add_coords_cols=add_coords_cols,
    coords_defaults=coords_defaults,
    coords_terminologies=coords_terminologies,
    coords_value_mapping=coords_value_mapping,
    #coords_value_filling=coords_value_filling,
    filter_remove=filter_remove,
    #filter_keep=filter_keep,
    meta_data=meta_data,
    convert_str=True
    )

cat_label = "category (IPCC2006)"

# fix error cats
data_if[cat_label] = data_if[cat_label].str.replace("error_", "")

# aggregate categories
attrs = data_if.attrs
for cat_to_agg in aggregate_cats:
    mask = data_if[cat_label].isin(aggregate_cats[cat_to_agg]["sources"])
    df_test = data_if[mask]

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

        df_combine.insert(0, cat_label, cat_to_agg)
        df_combine.insert(1, "orig_cat_name", aggregate_cats[cat_to_agg]["name"])

        df_combine = df_combine.reset_index()

        data_if = pd.concat([data_if, df_combine])
    else:
        print(f"no data to aggregate category {cat_to_agg}")


# delete cat 3 for N2O as it's wrong
index_3A_N2O = data_if[(data_if[cat_label] == '3') &
                       (data_if['entity'] == 'N2O')].index
data_if = data_if.drop(index_3A_N2O)

# aggregate cat 3 for N2O
for cat_to_agg in aggregate_cats_N2O:
    mask = data_if[cat_label].isin(aggregate_cats_N2O[cat_to_agg]["sources"])
    df_test = data_if[mask]
    df_test = df_test[df_test["entity"] == "N2O"]

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

        df_combine.insert(0, cat_label, cat_to_agg)
        df_combine.insert(1, "orig_cat_name", aggregate_cats_N2O[cat_to_agg]["name"])

        df_combine = df_combine.reset_index()

        data_if = pd.concat([data_if, df_combine])
    else:
        print(f"no data to aggregate category {cat_to_agg}")

# delete cat 3.A.2 for CO2CH4N2O as it's wrong
index_3A2_CO2CH4N2O = data_if[(data_if[cat_label] == '3.A.2') &
                       (data_if['entity'] == 'CH4CO2N2O (SARGWP100)')].index
data_if = data_if.drop(index_3A2_CO2CH4N2O)

# aggregate cat 3 for N2O
for cat_to_agg in aggregate_cats_CO2CH4N2O:
    mask = data_if[cat_label].isin(aggregate_cats_CO2CH4N2O[cat_to_agg]["sources"])
    df_test = data_if[mask]
    df_test = df_test[df_test["entity"] == "CO2CH4N2O (SARGWP100)"]

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

        df_combine.insert(0, cat_label, cat_to_agg)
        df_combine.insert(1, "orig_cat_name", aggregate_cats_CO2CH4N2O[cat_to_agg]["name"])

        df_combine = df_combine.reset_index()

        data_if = pd.concat([data_if, df_combine])
    else:
        print(f"no data to aggregate category {cat_to_agg}")


data_if.attrs = attrs

data_pm2 = pm2.pm2io.from_interchange_format(data_if)

# # convert to mass units from CO2eq
# entities_to_convert = [f"{entity} ({gwp_to_use})" for entity in
#                        entities_to_convert_to_mass]
#
# for entity in entities_to_convert:
#     converted = data_pm2[entity].pr.convert_to_mass()
#     basic_entity = entity.split(" ")[0]
#     converted = converted.to_dataset(name=basic_entity)
#     data_pm2 = data_pm2.pr.merge(converted)
#     data_pm2[basic_entity].attrs["entity"] = basic_entity
#
# # drop the GWP data
# data_pm2 = data_pm2.drop_vars(entities_to_convert)

# convert back to IF to have units in the fixed format
data_if = data_pm2.pr.to_interchange_format()

# ###
# save data to IF and native format
# ###
if not output_folder.exists():
    output_folder.mkdir()
pm2.pm2io.write_interchange_format(
    output_folder / (output_filename + coords_terminologies["category"]), data_if)

encoding = {var: compression for var in data_pm2.data_vars}
data_pm2.pr.to_netcdf(
    output_folder / (output_filename + coords_terminologies["category"] + ".nc"),
    encoding=encoding)
