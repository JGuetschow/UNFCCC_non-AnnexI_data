"""
Read Argentina's BUR4 from pdf

This script reads data from Argentina's fourth Binnial Update Report (BUR4).
Data is read from the pdf file using camelot
"""

import os
import sys

import camelot
import primap2 as pm2
from primap2.pm2io._conversion import convert_ipcc_code_primap_to_primap2

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    gas_baskets,
    process_data_for_country,
)

# ###
# configuration
# ###

# TODO: lot's of empty lines are written in csv file. check if solved with new
#  PRIMAP2 version
if __name__ == "__main__":
    # folders and files
    input_folder = downloaded_data_path / "UNFCCC" / "Argentina" / "BUR4"
    output_folder = extracted_data_path / "UNFCCC" / "Argentina"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "ARG_BUR4_2022_"

    pdf_file = "4to_Informe_Bienal_de_la_Rep%C3%BAblica_Argentina.pdf"

    # definitions part 1: reading data from pdf and preprocessing for conversion to
    # PRIMAP2 format

    # part 1.1 KyotoGHG, CO2, CH4, N2O tables
    #
    pages_to_read = range(232, 244)
    data_start_keyword = "Id#"
    data_end_keyword = "Fuente: Elaboración propia"
    index_cols = ["Id#", "Nombre"]
    col_rename = {index_cols[0]: "category", index_cols[1]: "orig_cat_name"}
    metadata = {"entity": [0, 1], "unit": [0, 2]}

    rows_to_drop = [0]

    metadata_mapping = {
        "unit": {
            "(GgCO2e)": "GgCO2e",
            "(GgCO2)": "Gg",
            "(GgN2O)": "Gg",
            "(GgCH4)": "Gg",
            "(GgGas)": "Gg",
        }
    }

    # part 1.2: fgases table
    # the f-gases table is in wide format with no sectoral resolution and gases as row
    # header
    pages_to_read_fgases = range(244, 247)
    data_start_keyword_fgases = "Gas"
    index_cols_fgases = ["Gas"]
    cols_to_drop_fgases = ["Nombre"]
    metadata_fgases = {
        "unit": [0, 2],
        "category": "2",
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
        "1A6": "MBIO",
        "1A3di": "MBKM",
        "1A3ai": "MBKA",
        "1A3di Navegación marítima y fluvial internacional": "MBKM",
        "S/N": "MMULTIOP",
    }

    cat_code_regexp = r"(?P<code>^[A-Z0-9]{1,8}).*"

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
            "HFC-23": "HFC23",
            "HFC-32": "HFC32",
            "HFC-41": "HFC41",
            "HFC-43-10mee": "HFC4310mee",
            "HFC-125": "HFC125",
            "HFC-134": "HFC134",
            "HFC-134a": "HFC134a",
            "HFC-152a": "HFC152a",
            "HFC-143": "HFC143",
            "HFC-143a": "HFC143a",
            "HFC-227ea": "HFC227ea",
            "HFC-236fa": "HFC236fa",
            "HFC-245ca": "HFC245ca",
            "HFC-365mfc": "HFC365mfc",
            "HFC-245fa": "HFC245fa",
            "PFC-143 (CF4)": "CF4",
            "PFC-116 (C2F6)": "C2F6",
            "PFC-218 (C3F8)": "C3F8",
            "PFC-31-10 (C4F10)": "C4F10",
            "c-C4F8": "cC4F8",
            "PFC-51-144 (C6F14)": "C6F14",
        },
        "unit": "PRIMAP1",
        "orig_cat_name": {
            "1A3di Navegación marítima y fluvial internacional": "Navegación marítima y fluvial internacional",  # noqa: E501
        },
    }

    coords_value_filling = {
        "category": {
            "orig_cat_name": {
                "Total de emisiones y absorciones nacionales": "0",
                "Navegación marítima y fluvial internacional": "M.BK.M",
                "Operaciones Multilaterales": "M.MULTIOP",
                "Emisiones de CO2 provenientes del uso de biomasa como combustible": "M.BIO",  # noqa: E501
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
        "title": "Cuarto Informe Bienal de Actualización de la República Argentina a "
        "la Convención Marco delas Naciones Unidas Sobre el Cambio Climático",
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
        tables = camelot.read_pdf(
            str(input_folder / pdf_file), pages=str(page), flavor="stream"
        )
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
            dict(zip(df_current.columns, list(df_current.loc[idx_header[0]]))), axis=1
        )
        df_current = df_current.drop(idx_header)

        # for sheet "Aggregate GHGs" fill entity cell
        if page in range(232, 235):
            df_current.iloc[
                metadata["entity"][0], metadata["entity"][1]
            ] = "KYOTOGHG (SARGWP100)"
        # drop all rows where the index cols (category code and name) are both NaN
        # as without one of them there is no category information
        df_current = df_current.dropna(axis=0, how="all", subset=index_cols)
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
        df_current = df_current.apply(
            lambda x: x.str.replace(".", "", regex=False), axis=1
        )
        df_current = df_current.apply(
            lambda x: x.str.replace(",", ".", regex=False), axis=1
        )

        df_current = df_current.rename(columns=col_rename)

        # reindex
        df_current = df_current.reset_index(drop=True)

        df_current["category"] = df_current["category"].replace(cat_codes_manual)

        # then the regex replacements
        def repl(m):  # noqa: D103
            return convert_ipcc_code_primap_to_primap2("IPC" + m.group("code"))

        df_current["category"] = df_current["category"].str.replace(
            cat_code_regexp, repl, regex=True
        )

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
            meta_data=meta_data,
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
        tables = camelot.read_pdf(
            str(input_folder / pdf_file), pages=str(page), flavor="stream"
        )
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
            dict(zip(df_current.columns, list(df_current.loc[idx_header[0]]))), axis=1
        )
        df_current = df_current.drop(idx_header)

        # drop all rows where the index cols (category code
        df_current = df_current.dropna(axis=0, how="all", subset=index_cols_fgases)
        # set index. necessary for the stack operation in the conversion to long format
        # df_current = df_current.set_index(index_cols)
        # add columns
        inserted = 0
        for col_key, col_info in metadata_fgases.items():
            # print(f"coordinates: {metadata[col][0]}, {metadata[col][1]}")
            if isinstance(col_info, str):
                value = col_info
            else:
                value = df_current.iloc[col_info[0], col_info[1] + inserted]
                if col_key in metadata_mapping.keys():
                    if value in metadata_mapping[col_key].keys():
                        value = metadata_mapping[col_key][value]
            # print(f"Inserting column {col} with value {value}")
            df_current.insert(2, col_key, value)
            inserted += 1

        # remove unnecessary columns
        df_current = df_current.drop(columns=cols_to_drop_fgases)

        # drop unit row
        df_current = df_current.drop(df_current.index[0])

        # fix number format
        df_current = df_current.apply(
            lambda x: x.str.replace(".", "", regex=False), axis=1
        )
        df_current = df_current.apply(
            lambda x: x.str.replace(",", ".", regex=False), axis=1
        )

        df_current = df_current.rename(columns=col_rename_fgases)

        # reindex
        df_current = df_current.reset_index(drop=True)

        df_current["category"] = df_current["category"].replace(cat_codes_manual)

        # then the regex replacements
        def repl(m):  # noqa: D103
            return convert_ipcc_code_primap_to_primap2("IPC" + m.group("code"))

        df_current["category"] = df_current["category"].str.replace(
            cat_code_regexp, repl, regex=True
        )

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
            meta_data=meta_data,
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
    data_all.pr.to_netcdf(
        output_folder / (output_filename + coords_terminologies["category"] + ".nc"),
        encoding=encoding,
    )

    data_if = data_all.pr.to_interchange_format()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"]), data_if
    )
