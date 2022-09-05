# this script reads data from Morocco's BUR3
# Data is read from pdf

import camelot
import primap2 as pm2
import pandas as pd
import numpy as np
from pathlib import Path

# ###
# configuration
# ###
root_path = Path(__file__).parents[3].absolute()
root_path = root_path.resolve()
downloaded_data_path = root_path / "downloaded_data"
extracted_data_path = root_path / "extracted_data"


input_folder = downloaded_data_path / 'UNFCCC' / 'Morocco' / 'BUR3'
output_folder = extracted_data_path / 'UNFCCC' / 'Morocco'
if not output_folder.exists():
    output_folder.mkdir()

output_filename = 'MAR_BUR3_2022_'

inventory_file = 'Morocco_BUR3_Fr.pdf'

gwp_to_use = 'AR4GWP100'

# years to read
years = [2010, 2012, 2014, 2016, 2018]
pages_to_read = range(104, 138)

compression = dict(zlib=True, complevel=9)

header_defs = {
    'Energy': [['Catégories', 'CO2', 'CH4', 'N2O', 'NOx', 'CO', 'COVNM', 'SO2'],
        ['', 'Gg', 'Gg', 'Gg', 'Gg', 'Gg', 'Gg', 'Gg']],
    'Agriculture': [['Catégories', 'CO2', 'CH4', 'N2O', 'NOx', 'CO', 'COVNM', 'SO2'],
        ['', 'Gg', 'Gg', 'Gg', 'Gg', 'Gg', 'Gg', 'Gg']],
    'IPPU': [['Catégories', 'CO2', 'CH4', 'N2O', 'HFCs', 'PFCs', 'SF6', 'NOx', 'CO', 'COVNM', 'SO2'],
        ['', 'GgCO2eq', 'GgCO2eq', 'GgCO2eq', 'GgCO2eq', 'GgCO2eq', 'GgCO2eq', 'Gg', 'Gg', 'Gg', 'Gg']],
    'LULUCF': [['Catégories', 'CO2', 'CH4', 'N2O', 'NOx', 'CO', 'COVNM', 'SO2'],
        ['', 'GgCO2eq', 'GgCO2eq', 'GgCO2eq', 'Gg', 'Gg', 'Gg', 'Gg']],
    'Waste': [['Catégories', 'CO2', 'CH4', 'N2O', 'NOx', 'CO', 'COVNM', 'SO2'],
        ['', 'GgCO2eq', 'GgCO2eq', 'GgCO2eq', 'Gg', 'Gg', 'Gg', 'Gg']],
}

# define which raw tables to combine
table_defs = {
    2010: {
        'Energy': [0, 1],
        'Agriculture': [10],
        'IPPU': [15, 16, 17],
        'LULUCF': [30],
        'Waste': [35],
    },
    2012: {
        'Energy': [2, 3],
        'Agriculture': [11],
        'IPPU': [18, 19, 20],
        'LULUCF': [31],
        'Waste': [36],
    },
    2014: {
        'Energy': [4, 5],
        'Agriculture': [10],
        'IPPU': [21, 22, 23],
        'LULUCF': [32],
        'Waste': [37],
    },
    2016: {
        'Energy': [6, 7],
        'Agriculture': [10],
        'IPPU': [24, 25, 26],
        'LULUCF': [33],
        'Waste': [38],
    },
    2018: {
        'Energy': [8, 9],
        'Agriculture': [14],
        'IPPU': [27, 28, 29],
        'LULUCF': [34],
        'Waste': [39],
    },
}

# special header as category code and name in one column
header_long = ["orig_cat_name", "entity", "unit", "time", "data"]

index_cols = ['Catégories']

# rows to remove
cats_remove = []

# manual category codes
cat_codes_manual = {
    '1.A.2.e -Industries agro-alimentaires et du tabac': '1.A.2.e',
    '1.A.2.f -Industries des minéraux non- métalliques': '1.A.2.f',
    'Agriculture': 'M.AG',
    '2. PIUP': '2',
    'UTCATF': 'M.LULUCF',
    '3.B.1 Terres forestières': '3.B.1',
    '3.B.2 Terres cultivées': '3.B.2',
    '3.B.3 Prairies': '3.B.3',
    '3.B.4 Terres humides': '3.B.4',
    '3.B.5 Etablissements': '3.B.5',
    '3.B.6 Autres terres': '3.B.6',
    '1.B.1.a.i.1 -Exploitation minière': '1.A.1.a.i.1',
}

cat_code_regexp = r'(?P<code>^[a-zA-Z0-9\.]{1,14})\s-\s.*'

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "MAR-GHG-inventory ",
    "provenance": "measured",
    "area": "MAR",
    "scenario": "BUR3"
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "entity": {
        'HFCs (AR4GWP100)': 'HFCS (AR4GWP100)',
        'PFCs (AR4GWP100)': 'PFCS (AR4GWP100)',
        'COVNM': 'NMVOC',
    }
}


coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit"
}

add_coords_cols = {
    "orig_cat_name": ["orig_cat_name", "category"],
}

filter_remove = {
    "f1": {
        "entity": ['Other halogenated gases without CO2 equivalent conversion factors (2)'],
    },
}

meta_data = {
    "references": "https://unfccc.int/documents/470340",
    "rights": "XXXX",
    "contact": "mail@johannes-guetschow.de",
    "title": "Morocco. Biennial update report (BUR). BUR 3.",
    "comment": "Read fom pdf file by Johannes Gütschow.",
    "institution": "United Nations Framework Convention on Climate Change (UNFCCC)",
}

##### read the raw data from pdf #####
tables = camelot.read_pdf(
    str(input_folder / inventory_file),
    pages=','.join([str(page) for page in pages_to_read]),
    flavor='lattice')

##### combine tables and convert to long format #####
df_all = None
for year in table_defs.keys():
    current_def = table_defs[year]
    for sector in current_def.keys():
        sector_tables = current_def[sector]
        # print(f"{year}, {sector}")
        df_first = tables[sector_tables[0]].df
        if len(sector_tables) > 1:
            for table in sector_tables[1:]:
                df_this_table = pd.concat([df_first, tables[table].df], axis=0,
                                          join='outer')
        else:
            df_this_table = df_first

        # fix the header
        df_this_table = df_this_table.drop(df_this_table.iloc[0:2].index)
        df_this_table.columns = header_defs[sector]

        # replace line breaks, long hyphens, double, and triple spaces in category names
        df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("\n", " ")
        df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("   ", " ")
        df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("  ", " ")
        df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("–", "-")

        # set index and convert to long format
        df_this_table = df_this_table.set_index(index_cols)
        df_this_table_long = pm2.pm2io.nir_convert_df_to_long(df_this_table, year,
                                                              header_long)

        # print(df_this_table_long.head())
        if df_all is None:
            df_all = df_this_table_long
        else:
            df_all = pd.concat([df_all, df_this_table_long], axis=0, join='outer')

df_all = df_all.reset_index(drop=True)

##### conversion to PRIMAP2 interchange format #####
# drop the rows with memo items etc
for cat in cats_remove:
    df_all = df_all.drop(df_all[df_all["orig_cat_name"] == cat].index)

# make a copy of the categories row
df_all["category"] = df_all["orig_cat_name"]

# replace cat names by codes in col "category"
# first the manual replacements
df_all["category"] = df_all["category"].replace(cat_codes_manual)
# then the regex replacements
repl = lambda m: m.group('code')
df_all["category"] = df_all["category"].str.replace(cat_code_regexp, repl, regex=True)
df_all = df_all.reset_index(drop=True)

# prepare numbers for pd.to_numeric
df_all.loc[:, "data"] = df_all.loc[:, "data"].str.replace(' ', '')
repl = lambda m: m.group('part1') + m.group('part2')
df_all.loc[:, 'data'] = df_all.loc[:, 'data'].str.replace(
    '(?P<part1>[0-9]+),(?P<part2>[0-9\.]+)$', repl, regex=True)
df_all['data'][df_all['data'].isnull()] = 'NaN'

# add GWP information to entity
for entity in df_all["entity"].unique():
    df_all["entity"][(df_all["entity"] == entity) & (
                df_all["unit"] == "GgCO2eq")] = f"{entity} ({gwp_to_use})"

data_if = pm2.pm2io.convert_long_dataframe_if(
    df_all,
    coords_cols=coords_cols,
    coords_defaults=coords_defaults,
    coords_terminologies=coords_terminologies,
    coords_value_mapping=coords_value_mapping,
    filter_remove=filter_remove,
    meta_data=meta_data,
    convert_str=True
)

# make sure all col headers are str
df_all.columns = df_all.columns.map(str)

# conversion to PRIMAP2 native format
data_pm2 = pm2.pm2io.from_interchange_format(data_if)

entities_to_convert = ['N2O', 'SF6', 'CO2', 'CH4']
entities_to_convert = [f"{entity} (AR4GWP100)" for entity in entities_to_convert]

# convert GWP units to mass units
for entity in entities_to_convert:
    converted = data_pm2[entity].pr.convert_to_mass()
    basic_entity = entity.split(" ")[0]
    converted = converted.to_dataset(name=basic_entity)
    data_pm2 = data_pm2.pr.merge(converted)
    data_pm2[basic_entity].attrs["entity"] = basic_entity

# drop the GWP data
data_pm2 = data_pm2.drop_vars(entities_to_convert)

# convert back to IF to have units in the fixed format
data_if = data_pm2.pr.to_interchange_format()

##### save data to IF and native format ####
if not output_folder.exists():
    output_folder.mkdir()
pm2.pm2io.write_interchange_format(
    output_folder / (output_filename + coords_terminologies["category"]), data_if)

encoding = {var: compression for var in data_pm2.data_vars}
data_pm2.pr.to_netcdf(
    output_folder / (output_filename + coords_terminologies["category"] + ".nc"),
    encoding=encoding)

