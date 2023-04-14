# this script reads data from Mexico's BUR3
# Data is read from the pdf file

import pandas as pd
import primap2 as pm2
from pathlib import Path
import camelot
from config_MEX_BUR3 import page_defs, fix_rows


# ###
# configuration
# ###
root_path = Path(__file__).parents[3].absolute()
root_path = root_path.resolve()
downloaded_data_path = root_path / "downloaded_data"
extracted_data_path = root_path / "extracted_data"


input_folder = downloaded_data_path / 'UNFCCC' / 'Mexico' / 'BUR3'
output_folder = extracted_data_path / 'UNFCCC' / 'Mexico'
if not output_folder.exists():
   output_folder.mkdir()

output_filename = 'MEX_BUR3_2022_'
compression = dict(zlib=True, complevel=9)
inventory_file = 'Mexico_3er_BUR.pdf'

gwp_to_use = 'AR5GWP100'
year = 2019
entity_row = 0
unit_row = 1

index_cols = "Categorías de fuentes y sumideros de GEI"
# special header as category code and name in one column
header_long = ["orig_cat_name", "entity", "unit", "time", "data"]

units = {
    "CO₂": "Gg",
    "CH₄": "Gg",
    "N₂O": "Gg",
    "HFC": "GgCO2eq",
    "PFC": "GgCO2eq",
    "NF₃": "GgCO2eq",
    "SF₆": "GgCO2eq",
    "EMISIONES NETAS PCG AR5": "GgCO2eq",
}

# manual category codes
cat_codes_manual = {
    'Todas las emisiones y las absorciones nacionales': '0',
    'Todas las emisiones (sin [3B] Tierra ni [3D1] Productos de madera recolectada': 'M0EL',
    '2F6 Otras aplicaciones': '2F6',
}

cat_code_regexp = r'^\[(?P<code>[a-zA-Z0-9]{1,3})\].*'

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
    "source": "MEX-GHG-Inventory",
    "provenance": "measured",
    "area": "MEX",
    "scenario": "BUR3",
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        'CH₄': 'CH4',
        'CO₂': 'CO2',
        'EMISIONES NETAS PCG AR5': 'KYOTOGHG (AR5GWP100)',
        'HFC': f"HFCS ({gwp_to_use})",
        'NF₃': f"NF3 ({gwp_to_use})",
        'N₂O': 'N2O',
        'PFC': f"PFCS ({gwp_to_use})",
        'SF₆': f"SF6 ({gwp_to_use})",
    },
}


filter_remove = {}

filter_keep = {}

meta_data = {
    "references": "https://unfccc.int/documents/512231",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Mexico. Biennial update report (BUR). BUR3",
    "comment": "Read fom pdf by Johannes Gütschow",
    "institution": "UNFCCC",
}

# convert to mass units where possible
entities_to_convert_to_mass = [
    'NF3', 'SF6'
]

# ###
# read the data from pdf into one long format dataframe
# ###
df_all = None
for page in page_defs.keys():
    print(f"Working on page {page}")
    page_def = page_defs[page]
    tables = camelot.read_pdf(str(input_folder / inventory_file), pages=page,
                              **page_def["camelot"])
    df_this_table = tables[0].df

    # fix rows
    for n_rows in page_def["rows_to_fix"].keys():
        # replace line breaks, long hyphens, double, and triple spaces in category names
        df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("\n", " ")
        df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("   ", " ")
        df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("  ", " ")
        df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("–", "-")
        # replace double space in entity
        df_this_table.iloc[0, :] = df_this_table.iloc[0, :].str.replace("  ", " ")
        df_this_table = fix_rows(df_this_table, page_def["rows_to_fix"][n_rows], 0,
                                 n_rows)

    # add units
    for col in df_this_table.columns.values:
        if df_this_table[col].iloc[0] in units.keys():
            df_this_table[col].iloc[1] = units[df_this_table[col].iloc[0]]

    # bring in right format for conversion to long format
    df_this_table = pm2.pm2io.nir_add_unit_information(df_this_table, unit_row=unit_row,
                                                       entity_row=entity_row,
                                                       regexp_unit=".*",
                                                       regexp_entity=".*",
                                                       default_unit="GgCO2eq")

    # set index and convert to long format
    df_this_table = df_this_table.set_index(index_cols)
    df_this_table_long = pm2.pm2io.nir_convert_df_to_long(df_this_table, year,
                                                          header_long)

    # combine with tables for other sectors (merge not append)
    if df_all is None:
        df_all = df_this_table_long
    else:
        df_all = pd.concat([df_all, df_this_table_long], axis=0, join='outer')

# ###
# conversion to PM2 IF
# ###
# make a copy of the categories row
df_all["category"] = df_all["orig_cat_name"]

# replace cat names by codes in col "category"
# first the manual replacements
df_all["category"] = df_all["category"].replace(cat_codes_manual)
# then the regex replacements
repl = lambda m: m.group('code')
df_all["category"] = df_all["category"].str.replace(cat_code_regexp, repl, regex=True)
df_all = df_all.reset_index(drop=True)

# replace "," and " " with "" in data
df_all.loc[:, "data"] = df_all.loc[:, "data"].str.replace(',','', regex=False)
df_all.loc[:, "data"] = df_all.loc[:, "data"].str.replace(' ','', regex=False)

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

data_pm2 = pm2.pm2io.from_interchange_format(data_if)

# convert to mass units from CO2eq

entities_to_convert = [f"{entity} ({gwp_to_use})" for entity in
                       entities_to_convert_to_mass]

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