# this script reads data from Chile's 2020 national inventory which is underlying BUR4
# Data is read from the xlsx file

import os
import sys
import pandas as pd
import primap2 as pm2
from pathlib import Path

from config_CHL_BUR4 import cat_mapping, filter_remove_IPCC2006, aggregate_cats
from primap2.pm2io._data_reading import matches_time_format
from primap2.pm2io._data_reading import filter_data

# ###
# configuration
# ###

input_folder = Path('..') / '..' / '..' / 'downloaded_data' / 'UNFCCC' / 'Chile' / 'BUR4'
output_folder = Path('..') / '..' / '..' / 'extracted_data' / 'UNFCCC', 'Chile'

output_filename = 'CHL_BUR4_2021_'

inventory_file = 'Inventario_Nacional_de_GEI-1990-2018.xlsx'
years_to_read = range(1990, 2018 + 1)

# configuration for conversion to PRIMAP2 data format
unit_row = "header"
unit_info = {
    'regexp_entity': r'(.*)\s\(.*\)$',
    'regexp_unit': r'.*\s\((.*)\)$',
    'default_unit': 'kt',
    'manual_repl_unit': {
        'kt CO₂ eq': 'ktCO2eq',
        'HFC (kt CO₂ eq)': 'ktCO2eq',
        'PFC (kt CO₂ eq)': 'ktCO2eq',
        'SF₆ (kt CO₂ eq)': 'ktCO2eq',
    },
    'manual_repl_entity': {
        'kt CO₂ eq': 'KYOTOGHG (AR4GWP100)',
        'HFC (kt CO₂ eq)': 'HFCS (AR4GWP100)',
        'PFC (kt CO₂ eq)': 'PFCS (AR4GWP100)',
        'SF₆ (kt CO₂ eq)': 'SF6 (AR4GWP100)',
    }
}
cols_to_drop = ['Unnamed: 14', 'Unnamed: 16', 'Código IPCC.1',
                'Categorías de fuente y sumidero de gases de efecto invernadero.1']
# columns for category code and original category name
index_cols = ['Código IPCC', 'Categorías de fuente y sumidero de gases de efecto invernadero']

# operations on long format DF
cols_for_space_stripping = ['category', 'orig_cat_name', 'entity']

time_format = "%Y"

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
    "category": "IPCC2006_1996_Chile_NIR",
    "scenario": "PRIMAP",
}

coords_terminologies_2006 = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "CHL-GHG-Inventory",
    "provenance": "measured",
    "area": "CHL",
    "scenario": "BUR4"
}

coords_value_mapping = {
    "entity": {
        "COVDM": "NMVOC",
        "CO₂ neto": "CO2",
        "CH₄": "CH4",
        # "HFC": "HFCS",
        "HFC-125": "HFC125",
        "HFC-134a": "HFC134a",
        "HFC-143a": "HFC143a",
        "HFC-152a": "HFC152a",
        "HFC-227ea": "HFC227ea",
        "HFC-23": "HFC23",
        "HFC-236fa": "HFC236fa",
        "HFC-245fa": "HFC245fa",
        "HFC-32": "HFC32",
        "HFC-365mfc": "HFC365mfc",
        "HFC-43-10mee": "HFC4310mee",
        "N₂O": "N2O",
        # "PFC": "PFCS",
        "PFC-116": "C2F6",
        "PFC-14": "CF4",
        "PFC-218": "C3F8",
        # "SF₆": "SF6",
        "SO₂": "SO2",
    },
    "unit": "PRIMAP1",
}

coords_value_filling = {
    'category': {  # col to fill
        'orig_cat_name': {  # col to fill from
            'Todas las emisiones y las absorciones nacionales': '0',  # from value: to value
            'Tanque internacional': 'M.BK',
            'Aviación internacional': 'M.BK.A',
            'Navegación internacional': 'M.BK.M',
            'Operaciones multilaterales': 'M.MULTIOP',
            'Emisiones de CO2 de la biomasa': 'M.BIO',
        }
    }
}

filter_remove = {
    "f1": {
        "entity": ["Absorciones CO₂", "Emisiones CO₂"],
    },
    "f2": {
        "orig_cat_name": ["Partidas informativas"],
    },
}

filter_keep = {}

meta_data = {
    "references": "https://unfccc.int/documents/267936, https://snichile.mma.gob.cl/wp-content/uploads/2021/03/Inventario_Nacional_de_GEI-1990-2018.xlsx",
    "rights": "",
    "contact": "mail@johannes-guetschow.de.de",
    "title": "Chile: BUR4",
    "comment": "Read fom xlsx file by Johannes Gütschow",
    "institution": "United Nations Framework Convention on Climate Change (UNFCCC)",
}

compression = dict(zlib=True, complevel=9)

# ###
# start data reading
# ###

# change working directory to script directory for proper folder names
script_path = os.path.abspath(sys.argv[0])
script_dir_name = os.path.dirname(script_path)
os.chdir(script_dir_name)

df_all = None

for year in years_to_read:
    # read sheet for the year. Each sheet contains several tables,
    # we only read the upper row as the other tables are summary tables
    df_current = pd.read_excel(input_folder / inventory_file, sheet_name=str(year), skiprows=2, nrows=442, engine="openpyxl")
    # drop the columns which are empty and repetition of the metadata for the second block
    df_current.drop(cols_to_drop, axis=1, inplace=True)
    # drop all rows where the index cols (category code and name) are both NaN
    # as without one of them there is no category information
    df_current.dropna(axis=0, how='all', subset=index_cols, inplace=True)
    # set multi-index. necessary for the stack operation in the conversion to long format
    df_current = df_current.set_index(index_cols)
    # add unit row using information from entity row and add to index
    df_current = pm2.pm2io.nir_add_unit_information(df_current, unit_row=unit_row, **unit_info)
    # actual conversion to long format
    df_current = pm2.pm2io.nir_convert_df_to_long(df_current, year)
    # aggregate to one df
    if df_all is None:
        df_all = df_current
    else:
        df_all = pd.concat([df_all, df_current])

df_all = df_all.reset_index(drop=True)

# ###
# postprocessing
# ###
# strip trailing and leading spaces
for col in cols_for_space_stripping:
    df_all[col] = df_all[col].str.strip()

df_all["category"] = df_all["category"].str.rstrip('.')

data_if = pm2.pm2io.convert_long_dataframe_if(
    df_all,
    coords_cols=coords_cols,
    add_coords_cols=add_coords_cols,
    coords_defaults=coords_defaults,
    coords_terminologies=coords_terminologies,
    coords_value_mapping=coords_value_mapping,
    coords_value_filling=coords_value_filling,
    filter_remove=filter_remove,
    filter_keep=filter_keep,
    meta_data=meta_data
)

# ###
# save data to IF and native format
# ###
pm2.pm2io.write_interchange_format(output_folder / (output_filename + coords_terminologies["category"]), data_if)

data_pm2 = pm2.pm2io.from_interchange_format(data_if)
encoding = {var: compression for var in data_pm2.data_vars}
data_pm2.pr.to_netcdf(output_folder / (output_filename + coords_terminologies["category"] + ".nc"), encoding=encoding)

# ###
# conversion to ipcc 2006 categories
# ###

data_if_2006 = pm2.pm2io.convert_long_dataframe_if(
    df_all,
    coords_cols=coords_cols,
    add_coords_cols=add_coords_cols,
    coords_defaults=coords_defaults,
    coords_terminologies=coords_terminologies_2006,
    coords_value_mapping=coords_value_mapping,
    coords_value_filling=coords_value_filling,
    filter_remove=filter_remove,
    filter_keep=filter_keep,
    meta_data=meta_data
)

cat_label = 'category (' + coords_terminologies_2006["category"] + ')'
filter_data(data_if_2006, filter_remove=filter_remove_IPCC2006)
data_if_2006 = data_if_2006.replace({cat_label: cat_mapping})

# aggregate categories
for cat_to_agg in aggregate_cats:
    mask = data_if_2006[cat_label].isin(aggregate_cats[cat_to_agg]["sources"])
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
            by=['source', 'scenario (PRIMAP)', 'provenance', 'area (ISO3)', 'entity', 'unit']).sum()

        df_combine.insert(0, cat_label, cat_to_agg)
        df_combine.insert(1, "orig_cat_name", aggregate_cats[cat_to_agg]["name"])

        df_combine = df_combine.reset_index()

        data_if_2006 = pd.concat([data_if_2006, df_combine])
    else:
        print(f"no data to aggregate category {cat_to_agg}")

pm2.pm2io.write_interchange_format(output_folder / (output_filename + coords_terminologies_2006["category"]), data_if_2006)

data_pm2_2006 = pm2.pm2io.from_interchange_format(data_if)
encoding = {var: compression for var in data_pm2_2006.data_vars}
data_pm2_2006.pr.to_netcdf(output_folder / (output_filename + coords_terminologies_2006["category"] + ".nc"), encoding=encoding)
