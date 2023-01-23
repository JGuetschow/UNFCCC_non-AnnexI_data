# this script reads data from Thailand's BUR3
# Data is read from the pdf file

import pandas as pd
import primap2 as pm2
from pathlib import Path
import camelot
import copy

from primap2.pm2io._data_reading import matches_time_format

# ###
# configuration
# ###
root_path = Path(__file__).parents[3].absolute()
root_path = root_path.resolve()
downloaded_data_path = root_path / "downloaded_data"
extracted_data_path = root_path / "extracted_data"


input_folder = downloaded_data_path / 'UNFCCC' / 'Thailand' / 'BUR3'
output_folder = extracted_data_path / 'UNFCCC' / 'Thailand'
if not output_folder.exists():
    output_folder.mkdir()

inventory_file = 'BUR3_Thailand_251220_.pdf'
output_filename = 'THA_BUR3_2020_'

compression = dict(zlib=True, complevel=9)

# inventory tables
pages_inventory = '68,69'
header_inventory = ['Greenhouse gas source and sink categories',
                   'CO2 emissions', 'CO2 removals',
                   'CH4', 'N2O', 'NOx', 'CO', 'NMVOCs',
                   'SO2', 'HFCs', 'PFCs', 'SF6']
unit_inventory = ['Gg'] * len(header_inventory)
unit_inventory[9] = "GgCO2eq"
unit_inventory[10] = "GgCO2eq"

year = 2016
entity_row = 0
unit_row = 1
gwp_to_use = "AR4GWP100"

index_cols = "Greenhouse gas source and sink categories"
# special header as category code and name in one column
header_long = ["orig_cat_name", "entity", "unit", "time", "data"]

# manual category codes
cat_codes_manual = {
    '6. Other Memo Items (not accounted in Total Emissions)': 'MEMO',
    'International Bunkers': 'MBK',
    'CO2 from Biomass': 'MBIO',
}

cat_code_regexp = r'^(?P<code>[a-zA-Z0-9]{1,4})[\s\.].*'

coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}


coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC1996_2006_THA_Inv",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "THA-GHG-Inventory",
    "provenance": "measured",
    "area": "THA",
    "scenario": "BUR3",
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        'HFCs': f"HFCS ({gwp_to_use})",
        'PFCs': f"PFCS ({gwp_to_use})",
        'NMVOCs': 'NMVOC',
    },
}


filter_remove = {
    'f_memo': {"category": "MEMO"},
}
filter_keep = {}

meta_data = {
    "references": "https://unfccc.int/documents/267629",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Thailand. Biennial update report (BUR). BUR3",
    "comment": "Read fom pdf by Johannes Gütschow",
    "institution": "UNFCCC",
}

# main sector time series
page_main_sector_ts = '70'
header_main_sector_ts = ['Year', 'Energy', 'IPPU',
                    'Agriculture', 'LULUCF', 'Waste',
                    'Net emissions (Including LULUCF)',
                    'Net emissions (Excluding LULUCF)']
unit_main_sector_ts = ['GgCO2eq'] * len(header_main_sector_ts)
unit_main_sector_ts[0] = ''

# manual category codes
cat_codes_manual_main_sector_ts = {
    'Energy': "1",
    'IPPU': "2",
    'Agriculture': "3",
    'LULUCF': "4",
    'Waste': "5",
    'Net emissions (Including LULUCF)': "0",
    'Net emissions (Excluding LULUCF)': "M0EL",
}

coords_cols_main_sector_ts = {
    "category": "category",
    "unit": "unit",
}

coords_defaults_main_sector_ts = {
    "source": "THA-GHG-Inventory",
    "provenance": "measured",
    "area": "THA",
    "scenario": "BUR3",
    "entity": f"KYOTOGHG ({gwp_to_use})"
}

# indirect gases time series
page_indirect = '72'
header_indirect = ['Year', 'NOx', 'CO',
                    'NMVOCs', 'SO2']
unit_indirect = ['Gg'] * len(header_indirect)
unit_indirect[0] = ''

cols_to_remove = ['Average Annual Growth Rate']

coords_cols_indirect = {
    "entity": "entity",
    "unit": "unit",
}

coords_defaults_indirect = {
    "source": "THA-GHG-Inventory",
    "provenance": "measured",
    "area": "THA",
    "scenario": "BUR3",
    "category": "0"
}


# ###
# read the inventory data and convert to PM2 IF
# ###

tables_inventory = camelot.read_pdf(str(input_folder / inventory_file), pages=pages_inventory,
                                    split_text=True, flavor="lattice")

df_inventory = tables_inventory[0].df[1:]
df_header = pd.DataFrame([header_inventory, unit_inventory])

df_inventory = pd.concat([df_header, df_inventory, tables_inventory[1].df.iloc[1:]], axis=0, join='outer')

df_inventory = pm2.pm2io.nir_add_unit_information(df_inventory, unit_row=unit_row, entity_row=entity_row,
                                                  regexp_entity=".*", regexp_unit=".*", default_unit="Gg")
# set index and convert to long format
df_inventory = df_inventory.set_index(index_cols)
df_inventory_long = pm2.pm2io.nir_convert_df_to_long(df_inventory, year, header_long)
df_inventory_long["orig_cat_name"] = df_inventory_long["orig_cat_name"].str[0]

# prep for conversion to PM2 IF and native format
# make a copy of the categories row
df_inventory_long["category"] = df_inventory_long["orig_cat_name"]

# replace cat names by codes in col "category"
# first the manual replacements
df_inventory_long["category"] = df_inventory_long["category"].replace(cat_codes_manual)
# then the regex replacements
repl = lambda m: m.group('code')
df_inventory_long["category"] = df_inventory_long["category"].str.replace(cat_code_regexp, repl, regex=True)
df_inventory_long = df_inventory_long.reset_index(drop=True)

# replace "," with "" in data
repl = lambda m: m.group('part1') + m.group('part2')
df_inventory_long.loc[:, "data"] = df_inventory_long.loc[:, "data"].str.replace('(?P<part1>[0-9]+),(?P<part2>[0-9\.]+)$', repl, regex=True)
df_inventory_long.loc[:, "data"] = df_inventory_long.loc[:, "data"].str.replace(' ','', regex=False)

# make sure all col headers are str
df_inventory_long.columns = df_inventory_long.columns.map(str)

df_inventory_long = df_inventory_long.drop(columns=["orig_cat_name"])

data_inventory_IF = pm2.pm2io.convert_long_dataframe_if(
    df_inventory_long,
    coords_cols=coords_cols,
    #add_coords_cols=add_coords_cols,
    coords_defaults=coords_defaults,
    coords_terminologies=coords_terminologies,
    coords_value_mapping=coords_value_mapping,
    #coords_value_filling=coords_value_filling,
    filter_remove=filter_remove,
    #filter_keep=filter_keep,
    meta_data=meta_data,
    convert_str=True
    )

# ###
# read the main sector time series and convert to PM2 IF
# ###
tables_main_sector_ts = camelot.read_pdf(str(input_folder / inventory_file), pages=page_main_sector_ts,
                                    split_text=True, flavor="lattice")

df_main_sector_ts = tables_main_sector_ts[0].df.iloc[2:]
#df_header = pd.DataFrame([header_main_sector_ts, unit_main_sector_ts])
#df_main_sector_ts = pd.concat([df_header, df_main_sector_ts], axis=0, join='outer')
df_main_sector_ts.columns = [header_main_sector_ts, unit_main_sector_ts]

df_main_sector_ts = df_main_sector_ts.transpose()
df_main_sector_ts = df_main_sector_ts.reset_index(drop=False)
cols = df_main_sector_ts.iloc[0].copy(deep=True)
cols.iloc[0] = "category"
cols.iloc[1] = "unit"
df_main_sector_ts.columns = cols
df_main_sector_ts = df_main_sector_ts.drop(0)

# replace cat names by codes in col "category"
df_main_sector_ts["category"] = df_main_sector_ts["category"].replace(cat_codes_manual_main_sector_ts)

repl = lambda m: m.group('part1') + m.group('part2')
year_cols = list(set(df_main_sector_ts.columns) - set(['category', 'unit']))
for col in year_cols:
    df_main_sector_ts.loc[:, col] = df_main_sector_ts.loc[:, col].str.replace('(?P<part1>[0-9]+),(?P<part2>[0-9\.]+)$', repl, regex=True)
    df_main_sector_ts.loc[:, col] = df_main_sector_ts.loc[:, col].str.replace(' ','', regex=False)

data_main_sector_ts_IF = pm2.pm2io.convert_wide_dataframe_if(
    df_main_sector_ts,
    coords_cols=coords_cols_main_sector_ts,
    #add_coords_cols=add_coords_cols,
    coords_defaults=coords_defaults_main_sector_ts,
    coords_terminologies=coords_terminologies,
    coords_value_mapping=coords_value_mapping,
    #coords_value_filling=coords_value_filling,
    filter_remove=filter_remove,
    #filter_keep=filter_keep,
    meta_data=meta_data,
    convert_str=True
    )


# ###
# read the indirect gases time series and convert to PM2 IF
# ###
tables_indirect = camelot.read_pdf(str(input_folder / inventory_file), pages=page_indirect,
                                    split_text=True, flavor="lattice")

df_indirect = tables_indirect[0].df.iloc[2:]
#df_header = pd.DataFrame([header_main_sector_ts, unit_main_sector_ts])
#df_main_sector_ts = pd.concat([df_header, df_main_sector_ts], axis=0, join='outer')
df_indirect.columns = [header_indirect, unit_indirect]

df_indirect = df_indirect.transpose()
df_indirect = df_indirect.reset_index(drop=False)
cols = df_indirect.iloc[0].copy(deep=True)
cols.iloc[0] = "entity"
cols.iloc[1] = "unit"
df_indirect.columns = cols
df_indirect = df_indirect.drop(0)
df_indirect = df_indirect.drop(columns=cols_to_remove)

repl = lambda m: m.group('part1') + m.group('part2')
year_cols = list(set(df_indirect.columns) - set(['entity', 'unit']))
for col in year_cols:
    df_indirect.loc[:, col] = df_indirect.loc[:, col].str.replace('(?P<part1>[0-9]+),(?P<part2>[0-9\.]+)$', repl, regex=True)
    df_indirect.loc[:, col] = df_indirect.loc[:, col].str.replace(' ','', regex=False)

data_indirect_IF = pm2.pm2io.convert_wide_dataframe_if(
    df_indirect,
    coords_cols=coords_cols_indirect,
    #add_coords_cols=add_coords_cols,
    coords_defaults=coords_defaults_indirect,
    coords_terminologies=coords_terminologies,
    coords_value_mapping=coords_value_mapping,
    #coords_value_filling=coords_value_filling,
    #filter_remove=filter_remove,
    #filter_keep=filter_keep,
    meta_data=meta_data,
    convert_str=True
    )

# ###
# merge the three datasets
# ###
data_inventory_pm2 = pm2.pm2io.from_interchange_format(data_inventory_IF)
data_main_sector_ts_pm2 = pm2.pm2io.from_interchange_format(data_main_sector_ts_IF)
data_indirect_pm2 = pm2.pm2io.from_interchange_format(data_indirect_IF)

data_all = data_inventory_pm2.pr.merge(data_main_sector_ts_pm2)
data_all = data_all.pr.merge(data_indirect_pm2)

# combine CO2 emissions and absorptions
data_CO2 = data_all[['CO2 emissions', 'CO2 removals']].\
    to_array().pr.sum("variable", skipna=True, min_count=1)
data_all["CO2"] = data_CO2

data_all_if = data_all.pr.to_interchange_format()



# ###
# convert to IPCC2006 categories
# ###

cat_mapping = {
    '3': 'M.AG',
    '3.A': '3.A.1',
    '3.B': '3.A.2',
    '3.C': 'M.3.C.1.AG',  # field burning of agricultural residues
    '3.D': '3.C.2',  # Liming
    '3.E': '3.C.3',  # urea application
    '3.F': '3.C.4',  # direct N2O from agri soils
    '3.G': '3.C.5',  # indirect N2O from agri soils
    '3.H': '3.C.6',  # indirect N2O from manure management
    '3.I': '3.C.7',  # rice
    '4': 'M.LULUCF',
    '4.A': '3.B.1.a',  # forest remaining forest
    '4.B': '3.B.2.a',  # cropland remaining cropland
    '4.C': '3.B.2.b',  # land converted to cropland
    '4.D': '3.B.6.b',  # land converted to other land
    '4.E': 'M.3.C.1.LU',  # biomass burning (LULUCF)
    '5': '4',
    '5.A': '4.A',
    '5.B': '4.B',
    '5.C': '4.C',
    '5.D': '4.D',
}

aggregate_cats = {
    '2.A.4': {'sources': ['2.A.4.b', '2.A.4.d'],
              'name': 'Other Process uses of Carbonates'},
    '3.A': {'sources': ['3.A.1', '3.A.2'], 'name': 'Livestock'},
    '3.C.1': {'sources': ['M.3.C.1.AG', 'M.3.C.1.LU'],
              'name': 'Emissions from Biomass Burning'},
    '3.C': {'sources': ['3.C.1', '3.C.2', '3.C.3', '3.C.4', '3.C.5', '3.C.6', '3.C.7'],
            'name': 'Aggregate sources and non-CO2 emissions sources on land'},
    'M.3.C.AG': {
        'sources': ['M.3.C.1.AG', '3.C.2', '3.C.3', '3.C.4', '3.C.5', '3.C.6', '3.C.7'],
        'name': 'Aggregate sources and non-CO2 emissions sources on land (Agriculture)'},
    'M.3.C.LU': {'sources': ['M.3.C.1.LU'],
                 'name': 'Aggregate sources and non-CO2 emissions sources on land (Land use)'},
    '3': {'sources': ['M.AG', 'M.LULUCF'], 'name': 'AFOLU'},
    '3.B.1': {'sources': ['3.B.1.a'], 'name': 'Forest Land'},
    '3.B.2': {'sources': ['3.B.2.a', '3.B.2.b'], 'name': 'Cropland'},
    '3.B.6': {'sources': ['3.B.6.b'], 'name': 'Other Land'},
    '3.B': {'sources': ['3.B.1', '3.B.2', '3.B.6'], 'name': 'Land'},
    'M.AG.ELV': {'sources': ['M.3.C.AG'],
                 'name': 'Agriculture excluding livestock emissions'},
}

data_if_2006 = copy.deepcopy(data_all_if)
data_if_2006.attrs = copy.deepcopy(data_all_if.attrs)

# map categories
data_if_2006 = data_if_2006.replace({'category (IPCC1996_2006_THA_Inv)': cat_mapping})
data_if_2006["category (IPCC1996_2006_THA_Inv)"].unique()

# rename the category col
data_if_2006.rename(
    columns={'category (IPCC1996_2006_THA_Inv)': 'category (IPCC2006_PRIMAP)'},
    inplace=True)
data_if_2006.attrs['attrs']['cat'] = 'category (IPCC2006_PRIMAP)'
data_if_2006.attrs['dimensions']['*'] = [
    'category (IPCC2006_PRIMAP)' if item == 'category (IPCC1996_2006_THA_Inv)'
    else item for item in data_if_2006.attrs['dimensions']['*']]
# aggregate categories
for cat_to_agg in aggregate_cats:
    mask = data_if_2006["category (IPCC2006_PRIMAP)"].isin(
        aggregate_cats[cat_to_agg]["sources"])
    df_test = data_if_2006[mask]
    # print(df_test)

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

        data_if_2006 = pd.concat([data_if_2006, df_combine], axis=0, join='outer')
        data_if_2006 = data_if_2006.reset_index(drop=True)
    else:
        print(f"no data to aggregate category {cat_to_agg}")

# conversion to PRIMAP2 native format
data_pm2_2006 = pm2.pm2io.from_interchange_format(data_if_2006)

# convert back to IF to have units in the fixed format
data_if_2006 = data_pm2_2006.pr.to_interchange_format()


# ###
# save data to IF and native format
# ###
# data in original categories
pm2.pm2io.write_interchange_format(output_folder / (output_filename + coords_terminologies["category"]), data_all_if)

encoding = {var: compression for var in data_all.data_vars}
data_all.pr.to_netcdf(output_folder / (output_filename + coords_terminologies["category"] + ".nc"), encoding=encoding)

# data in 2006 categories
pm2.pm2io.write_interchange_format(output_folder / (output_filename + "IPCC2006_PRIMAP"), data_if_2006)

encoding = {var: compression for var in data_pm2_2006.data_vars}
data_pm2_2006.pr.to_netcdf(output_folder / (output_filename + "IPCC2006_PRIMAP" + ".nc"), encoding=encoding)