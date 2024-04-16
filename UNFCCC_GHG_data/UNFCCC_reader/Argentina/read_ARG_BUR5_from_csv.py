# this script reads data from Argentina's 2023 national inventory which is underlying BUR5
# https://ciam.ambiente.gob.ar/repositorio.php?tid=9&stid=36&did=394#
# Data is read from the csv file available for download at the above URL
# license probably CC-BY 4.0 (see https://datos.gob.ar/dataset/ambiente-emisiones-gases-efecto-invernadero-gei)

import sys
import camelot
import primap2 as pm2
from primap2.pm2io._conversion import convert_ipcc_code_primap_to_primap2
from UNFCCC_GHG_data.helper import downloaded_data_path, extracted_data_path, \
    process_data_for_country
from UNFCCC_GHG_data.UNFCCC_DI_reader.UNFCCC_DI_reader_config import gas_baskets


# TODO
# data is in long format. Columns needed are
# 'año' 'id_ipcc' 'tipo_de_gas' 'valor_en_toneladas_de_gas'
# columns to irgnore are
columns_to_ignore = ['sector', 'actividad', 'subactividad', 'categoria', 'valor_en_toneladas_de_co2e']
# sector codes are in primap1 format (no dots), reading should be possible directly from CSV into interchange format
# postprocessing needed is aggregation of gas baskets and categories as only the highest detail categories are present


# ###
# configuration
# ###

# TODO: lot's of empty lines are written in csv file. check if solved with new
#  PRIMAP2 version

# folders and files
input_folder = downloaded_data_path / 'UNFCCC' / 'Argentina' / \
               'BUR5'
output_folder = extracted_data_path / 'UNFCCC' / 'Argentina'
if not output_folder.exists():
    output_folder.mkdir()

output_filename = 'ARG_BUR5_2023_'

csv_file = 'emisiones_gei_inventario_datos_totales_1990_2020.csv'


# cats = ['1A1a', '1A1b', '1A1cii', '1A2a', '1A2b', '1A2c', '1A2d', '1A2e',
#        '1A2f', '1A2g', '1A2j', '1A2l', '1A2m', '1A3aii', '1A3biii',
#        '1A3bvii', '1A3c', '1A3dii', '1A3ei', '1A4ai', '1A4aii', '1A4aiii',
#        '1A4b', '1A4c', '1B1ai1', '1B1ai2', '1B1ci', '1B2ai', '1B2aii',
#        '1B2aiii', '1B2aiv', '1B2bi', '1B2bii', '1B2biii', '1B2biv',
#        '1B2bv', '1B2bvi', '2A1', '2A2', '2A4a', '2A4b', '2A4d', '2B1',
#        '2B2', '2B5', '2B7', '2B8a', '2B8b', '2B8c', '2B8f', '2B9a', '2C1',
#        '2C2', '2C3', '2C6', '2D1', '2D2', '2F1a', '2F1b', '2F2', '2F3',
#        '2F4', '3A1ai', '3A1aii', '3A1b', '3A1c', '3A1d', '3A1e', '3A1f',
#        '3A1g', '3A1h', '3A2ai', '3A2aii', '3A2b', '3A2c', '3A2d', '3A2e',
#        '3A2f', '3A2g', '3A2h', '3A2i', '3B1ai1', '3B1ai2', '3B1aii1',
#        '3B1aii2', '3B2bi', '3B2bii', '3B3bi', '3B3bii', '3B7', '3C1ai',
#        '3C1aii', '3C1bi', '3C1bii', '3C1ci', '3C1cii', '3C3', '3C4a',
#        '3C4b', '3C4c', '3C4di', '3C4dii', '3C4diii', '3C4div', '3C4dv',
#        '3C4dvi', '3C4dvii', '3C4e', '3C4f', '3C4gi', '3C4gii', '3C4n',
#        '3C4o', '3C5ai', '3C5aii', '3C5bi', '3C5bii', '3C5ci', '3C5cii',
#        '3C5di1', '3C5di2', '3C5dii1', '3C5dii2', '3C5diii1', '3C5diii2',
#        '3C5div1', '3C5div2', '3C5dv1', '3C5dv2', '3C5dvi1', '3C5dvi2',
#        '3C5dvii1', '3C5dvii2', '3C5e', '3C5fii', '3C5gi1', '3C5gi2',
#        '3C5gii1', '3C5gii2', '3C5ni', '3C5nii', '3C5oi', '3C5oii',
#        '3C6ai1', '3C6aii1', '3C6aii2', '3C6hi', '3C6hii', '3C6ii', '3C7',
#        '3D1', '4A1', '4A3', '4B', '4C1', '4D1', '4D2a', '4D2b', '4D2c',
#        '4D2d', '4D2e']

# read the data

######
cat_codes_manual = {  # conversion to PRIMAP1 format
    '1A6': 'MBIO',
    '1A3di': 'MBKM',
    '1A3ai': 'MBKA',
    '1A3di Navegación marítima y fluvial internacional': 'MBKM',
    'S/N': 'MMULTIOP',
}

cat_code_regexp = r'(?P<UNFCCC_GHG_data>^[A-Z0-9]{1,8}).*'

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
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "ARG-GHG-Inventory",
    "provenance": "measured",
    "area": "ARG",
    "scenario": "BUR5",
    "unit": "tonnes" # this might not work as he entity has to be specified
}

coords_value_mapping = {
    "category": "PRIMAP1",
    "entity": {
        'HFC_23': 'HFC23',
        'HFC_32': 'HFC32',
        'HFC_125': 'HFC125',
        'HFC_134a': 'HFC134a',
        'HFC_152a': 'HFC152a',
        'HFC_143a': 'HFC143a',
        'HFC_227ea': 'HFC227ea',
        'HFC_236fa': 'HFC236fa',
        'HFC_365mfc': 'HFC365mfc',
        'HFC_245fa': 'HFC245fa',
        'PFC_143_CF4': 'CF4',
        'PFC_116-C2F6': 'C2F6',
    },
}

coords_value_filling = {
}

filter_remove = {
}

filter_keep = {}

meta_data = {
    "references": "",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "",
    "comment": "Read fom pcsv file by Johannes Gütschow",
    "institution": "United Nations Framework Convention on Climate Change (UNFCCC)",
}
#####

data_IF = pm2.pm2io.read_long_csv_file_if(
    csv_file,

    #coords_value_filling=coords_value_filling,
    filter_remove=filter_remove,
    filter_keep=filter_keep,

)




# definitions part 1: reading data from pdf and preprocessing for conversion to PRIMAP2 format
# part 1.1 KyotoGHG, CO2, CH4, N2O tables
#
pages_to_read = range(232, 244)
data_start_keyword = "Id#"
data_end_keyword = "Fuente: Elaboración propia"
index_cols = ['Id#', 'Nombre']
col_rename = {
    index_cols[0]: "category",
    index_cols[1]: "orig_cat_name"
}
metadata = {
    "entity": [0, 1],
    "unit": [0, 2]
}

rows_to_drop = [0]

metadata_mapping = {
    'unit': {
        '(GgCO2e)': 'GgCO2e',
        '(GgCO2)': 'Gg',
        '(GgN2O)': 'Gg',
        '(GgCH4)': 'Gg',
        '(GgGas)': 'Gg',
    }
}

# part 1.2: fgases table
# the f-gases table is in wide format with no sectoral resolution and gases as row header
pages_to_read_fgases = range(244, 247)
data_start_keyword_fgases = "Gas"
index_cols_fgases = ['Gas']
cols_to_drop_fgases = ["Nombre"]
metadata_fgases = {
    "unit": [0, 2],
    "category": '2',
    "orig_cat_name": "PROCESOS INDUSTRIALES Y USO DE PRODUCTOS",
}
col_rename_fgases = {
    index_cols_fgases[0]: "entity",
}

## definitions for conversion to PRIMAP2 format
# rows to remove
cats_remove = ["Information Items", "Memo Items (3)"]
# manual category codes
cat_codes_manual = {  # conversion to PRIMAP1 format
    '1A6': 'MBIO',
    '1A3di': 'MBKM',
    '1A3ai': 'MBKA',
    '1A3di Navegación marítima y fluvial internacional': 'MBKM',
    'S/N': 'MMULTIOP',
}

cat_code_regexp = r'(?P<UNFCCC_GHG_data>^[A-Z0-9]{1,8}).*'

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
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "ARG-GHG-Inventory",
    "provenance": "measured",
    "area": "ARG",
    "scenario": "BUR4",
}

coords_value_mapping = {
    #    "category": "PRIMAP1",
    "entity": {
        'HFC-23': 'HFC23',
        'HFC-32': 'HFC32',
        'HFC-41': 'HFC41',
        'HFC-43-10mee': 'HFC4310mee',
        'HFC-125': 'HFC125',
        'HFC-134': 'HFC134',
        'HFC-134a': 'HFC134a',
        'HFC-152a': 'HFC152a',
        'HFC-143': 'HFC143',
        'HFC-143a': 'HFC143a',
        'HFC-227ea': 'HFC227ea',
        'HFC-236fa': 'HFC236fa',
        'HFC-245ca': 'HFC245ca',
        'HFC-365mfc': 'HFC365mfc',
        'HFC-245fa': 'HFC245fa',
        'PFC-143 (CF4)': 'CF4',
        'PFC-116 (C2F6)': 'C2F6',
        'PFC-218 (C3F8)': 'C3F8',
        'PFC-31-10 (C4F10)': 'C4F10',
        'c-C4F8': 'cC4F8',
        'PFC-51-144 (C6F14)': 'C6F14',
    },
    "unit": "PRIMAP1",
    "orig_cat_name": {
        "1A3di Navegación marítima y fluvial internacional": "Navegación marítima y fluvial internacional",
    }
}

coords_value_filling = {
    "category": {
        "orig_cat_name": {
            "Total de emisiones y absorciones nacionales": "0",
            "Navegación marítima y fluvial internacional": "M.BK.M",
            "Operaciones Multilaterales": "M.MULTIOP",
            "Emisiones de CO2 provenientes del uso de biomasa como combustible": "M.BIO",
        },
    },
    "orig_cat_name": {
        "category": {
            "M.BK.M": "Navegación marítima y fluvial internacional",
        },
    },
}

filter_remove = {
    "f1": {
        "orig_cat_name": ["Elementos Recordatorios"],
    },
}

filter_keep = {}

meta_data = {
    "references": "https://unfccc.int/documents/419772",
    "rights": "XXXX",
    "contact": "mail@johannes-guetschow.de",
    "title": "Cuarto Informe Bienal de Actualización de la República Argentina a la Convención Marco delas Naciones Unidas Sobre el Cambio Climático",
    "comment": "Read fom pdf file by Johannes Gütschow",
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

# read data for KyotoGHG, CO2, CH4, N2O
data_all = None
for page in pages_to_read:
    # read current page
    tables = camelot.read_pdf(str(input_folder / pdf_file), pages=str(page),
                              flavor='stream')
    df_current = tables[0].df
    rows_to_drop = []
    for index, data in df_current.iterrows():
        if data[0] == data_start_keyword:
            break
        else:
            rows_to_drop.append(index)

    end_of_data = False
    for index, data in df_current.iterrows():
        if data_end_keyword in list(data):
            end_of_data = True
        if end_of_data:
            rows_to_drop.append(index)

    df_current = df_current.drop(rows_to_drop)
    idx_header = df_current.index[df_current[0] == index_cols[0]].tolist()
    df_current = df_current.rename(
        dict(zip(df_current.columns, list(df_current.loc[idx_header[0]]))), axis=1)
    df_current = df_current.drop(idx_header)

    # for sheet "Aggregate GHGs" fill entity cell
    if page in range(232, 235):
        df_current.iloc[
            metadata["entity"][0], metadata["entity"][1]] = "KYOTOGHG (SARGWP100)"
    # drop all rows where the index cols (category UNFCCC_GHG_data and name) are both NaN
    # as without one of them there is no category information
    df_current.dropna(axis=0, how='all', subset=index_cols, inplace=True)
    # set index. necessary for the stack operation in the conversion to long format
    # df_current = df_current.set_index(index_cols)
    # add columns
    inserted = 0
    for col in metadata.keys():
        # print(f"coordinates: {metadata[col][0]}, {metadata[col][1]}")
        value = df_current.iloc[metadata[col][0], metadata[col][1] + inserted]
        if col in metadata_mapping.keys():
            if value in metadata_mapping[col].keys():
                value = metadata_mapping[col][value]
        # print(f"Inserting column {col} with value {value}")
        df_current.insert(2, col, value)
        inserted += 1

    # drop unit row
    # for row in rows_to_drop:
    #    df_current = df_current.drop(df_current.iloc[row].name)
    df_current = df_current.drop(df_current.index[0])

    # fix number format
    df_current = df_current.apply(lambda x: x.str.replace('.', '', regex=False), axis=1)
    df_current = df_current.apply(lambda x: x.str.replace(',', '.', regex=False),
                                  axis=1)

    df_current.rename(columns=col_rename, inplace=True)

    # reindex
    df_current.reset_index(inplace=True, drop=True)

    df_current["category"] = df_current["category"].replace(cat_codes_manual)
    # then the regex replacements
    repl = lambda m: convert_ipcc_code_primap_to_primap2('IPC' + m.group('UNFCCC_GHG_data'))
    df_current["category"] = df_current["category"].str.replace(cat_code_regexp, repl,
                                                                regex=True)

    df_current = df_current.reset_index(drop=True)

    # make sure all col headers are str
    df_current.columns = df_current.columns.map(str)

    # convert to PRIMAP2 interchange format
    data_if = pm2.pm2io.convert_wide_dataframe_if(
        df_current,
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

    # convert to PRIMAP2 native format
    data_pm2 = pm2.pm2io.from_interchange_format(data_if)

    # aggregate to one df
    if data_all is None:
        data_all = data_pm2
    else:
        data_all = data_all.pr.merge(data_pm2)

# read fgases
for page in pages_to_read_fgases:
    # read current page
    tables = camelot.read_pdf(str(input_folder / pdf_file), pages=str(page),
                              flavor='stream')
    df_current = tables[0].df
    rows_to_drop = []
    for index, data in df_current.iterrows():
        if data[0] == data_start_keyword_fgases:
            break
        else:
            rows_to_drop.append(index)

    end_of_data = False
    for index, data in df_current.iterrows():
        if data_end_keyword in list(data):
            end_of_data = True
        if end_of_data:
            rows_to_drop.append(index)

    df_current = df_current.drop(rows_to_drop)
    idx_header = df_current.index[df_current[0] == index_cols_fgases[0]].tolist()
    df_current = df_current.rename(
        dict(zip(df_current.columns, list(df_current.loc[idx_header[0]]))), axis=1)
    df_current = df_current.drop(idx_header)

    # drop all rows where the index cols (category UNFCCC_GHG_data and name) are both NaN
    # as without one of them there is no category information
    df_current.dropna(axis=0, how='all', subset=index_cols_fgases, inplace=True)
    # set index. necessary for the stack operation in the conversion to long format
    # df_current = df_current.set_index(index_cols)
    # add columns
    inserted = 0
    for col in metadata_fgases.keys():
        # print(f"coordinates: {metadata[col][0]}, {metadata[col][1]}")
        if isinstance(metadata_fgases[col], str):
            value = metadata_fgases[col]
        else:
            value = df_current.iloc[
                metadata_fgases[col][0], metadata_fgases[col][1] + inserted]
            if col in metadata_mapping.keys():
                if value in metadata_mapping[col].keys():
                    value = metadata_mapping[col][value]
        # print(f"Inserting column {col} with value {value}")
        df_current.insert(2, col, value)
        inserted += 1

    # remove unnecessary columns
    df_current = df_current.drop(columns=cols_to_drop_fgases)

    # drop unit row
    df_current = df_current.drop(df_current.index[0])

    # fix number format
    df_current = df_current.apply(lambda x: x.str.replace('.', '', regex=False), axis=1)
    df_current = df_current.apply(lambda x: x.str.replace(',', '.', regex=False),
                                  axis=1)

    df_current.rename(columns=col_rename_fgases, inplace=True)

    # reindex
    df_current.reset_index(inplace=True, drop=True)

    df_current["category"] = df_current["category"].replace(cat_codes_manual)
    # then the regex repalcements
    repl = lambda m: convert_ipcc_code_primap_to_primap2('IPC' + m.group('UNFCCC_GHG_data'))
    df_current["category"] = df_current["category"].str.replace(cat_code_regexp, repl,
                                                                regex=True)

    df_current = df_current.reset_index(drop=True)

    # make sure all col headers are str
    df_current.columns = df_current.columns.map(str)

    # convert to PRIMAP2 interchange format
    data_if = pm2.pm2io.convert_wide_dataframe_if(
        df_current,
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

    # convert to PRIMAP2 native format
    data_pm2 = pm2.pm2io.from_interchange_format(data_if)

    # aggregate to one df
    data_all = data_all.pr.merge(data_pm2)

# ###
# process (aggregate fgases)
# ###
data_all = process_data_for_country(
    data_all,
    entities_to_ignore=[],
    gas_baskets=gas_baskets,
    processing_info_country=None,
)


# ###
# save data to IF and native format
# ###

encoding = {var: compression for var in data_all.data_vars}
data_all.pr.to_netcdf(output_folder / (output_filename + coords_terminologies[
    "category"] + ".nc"), encoding=encoding)

data_if = data_all.pr.to_interchange_format()
pm2.pm2io.write_interchange_format(output_folder / (output_filename + coords_terminologies["category"]), data_if)





