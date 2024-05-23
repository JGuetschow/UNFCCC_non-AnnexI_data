"""
Read Korea's BUR4 from xlsx

This script reads data from Korea's 2020 national inventory which is underlying BUR4
Data are read from the xlsx file

"""

import os
import sys

import pandas as pd
import primap2 as pm2
from primap2.pm2io._data_reading import filter_data

from unfccc_ghg_data.helper import downloaded_data_path, extracted_data_path
from unfccc_ghg_data.unfccc_reader.Republic_of_Korea.config_kor_bur4 import (
    cat_codes,
    cat_name_translations,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = (
        downloaded_data_path / "non-UNFCCC" / "Republic_of_Korea" / "2020-Inventory"
    )
    output_folder = extracted_data_path / "UNFCCC" / "Republic_of_Korea"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "KOR_BUR4_2021_"

    inventory_file = "Republic_of_Korea_National_GHG_Inventory_(1990_2018).xlsx"
    years_to_read = range(1990, 2018 + 1)

    sheets_to_read = ["온실가스", "CO2", "CH4", "N2O", "HFCs", "PFCs", "SF6"]
    cols_to_read = range(1, 2018 - 1990 + 3)

    # columns for category code and original category name
    index_cols = ["분야·부문/연도"]

    sheet_metadata = {
        "entity": {
            "온실가스": "KYOTOGHG (SARGWP100)",
            "CO2": "CO2",
            "CH4": "CH4 (SARGWP100)",
            "N2O": "N2O (SARGWP100)",
            "HFCs": "HFCS (SARGWP100)",
            "PFCs": "PFCS (SARGWP100)",
            "SF6": "SF6 (SARGWP100)",
        },
        "unit": {
            "온실가스": "Gg CO2 / yr",
            "CO2": "Gg CO2 / yr",
            "CH4": "Gg CO2 / yr",
            "N2O": "Gg CO2 / yr",
            "HFCs": "Gg CO2 / yr",
            "PFCs": "Gg CO2 / yr",
            "SF6": "Gg CO2 / yr",
        },
    }

    # definitions for conversion to interchange format
    time_format = "%Y"

    coords_cols = {
        "category": "category",
        "entity": "entity",
        "unit": "unit",
    }

    add_coords_cols = {
        "orig_cat_name": ["orig_cat_name", "category"],
        "cat_name_translation": ["cat_name_translation", "category"],
    }

    coords_terminologies = {
        "area": "ISO3",
        "category": "IPCC1996_KOR_INV",
        "scenario": "PRIMAP",
    }

    coords_defaults = {
        "source": "KOR-GHG-Inventory",
        "provenance": "measured",
        "area": "KOR",
        "scenario": "BUR4",
    }

    coords_value_mapping = {
        "cat_name_translation": cat_name_translations,
        "category": cat_codes,
    }

    # filtering after IF creation to be able to use the IPCC codes
    filter_remove = {
        "f1": {
            "category (IPCC1996_KOR_INV)": "\\IGNORE",
        },
        "livestock": {  # temp until double cat name problem is solved
            "category (IPCC1996_KOR_INV)": [
                "4.B.1",
                "4.B.10",
                "4.B.2",
                "4.B.3",
                "4.B.4",
                "4.B.5",
                "4.B.6",
                "4.B.7",
                "4.B.8",
                "4.B.9",
            ]
        },
    }

    filter_keep = {}

    meta_data = {
        "references": "https://unfccc.int/documents/418616, "
        "http://www.gir.go.kr/home/file/readDownloadFile.do?"
        "fileId=4856&fileSeq=2",
        "rights": "",
        "contact": "mail@johannes-guetschow.de.de",
        "title": "Republic of Korea: BUR4 / National Greenhouse Gas Inventory Report "
        "2020",
        "comment": "Read fom xlsx file by Johannes Gütschow",
        "institution": "United Nations Framework Convention on Climate Change (UNFCCC)",
    }

    cols_for_space_stripping = []

    compression = dict(zlib=True, complevel=9)

    # ###
    # start data reading
    # ###

    # change working directory to script directory for proper folder names
    script_path = os.path.abspath(sys.argv[0])
    script_dir_name = os.path.dirname(script_path)
    os.chdir(script_dir_name)

    df_all = None

    for sheet in sheets_to_read:
        # read current sheet (one sheet per gas)
        df_current = pd.read_excel(
            input_folder / inventory_file,
            sheet_name=sheet,
            skiprows=3,
            nrows=144,
            usecols=cols_to_read,
            engine="openpyxl",
        )
        # drop all rows where the index cols (category code and name) are both NaN
        # as without one of them there is no category information
        df_current = df_current.dropna(axis=0, how="all", subset=index_cols)
        # set index. necessary for the stack operation in the conversion to long format
        # df_current = df_current.set_index(index_cols)
        # add columns
        for col in sheet_metadata.keys():
            df_current.insert(1, col, sheet_metadata[col][sheet])
        # aggregate to one df
        if df_all is None:
            df_all = df_current
        else:
            df_all = pd.concat([df_all, df_current])

    df_all = df_all.reset_index(drop=True)
    # rename category col because filtering produces problems with korean col names
    df_all = df_all.rename(columns={"분야·부문/연도": "category"})

    # create copies of category col for further processing
    df_all["orig_cat_name"] = df_all["category"]
    df_all["cat_name_translation"] = df_all["category"]

    # make sure all col headers are str
    df_all.columns = df_all.columns.map(str)

    # ###
    # convert to PRIMAP2 interchange format
    # ###
    data_if = pm2.pm2io.convert_wide_dataframe_if(
        df_all,
        coords_cols=coords_cols,
        add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        # coords_value_filling=coords_value_filling,
        # filter_remove=filter_remove,
        # filter_keep=filter_keep,
        meta_data=meta_data,
        convert_str=True,
    )

    filter_data(data_if, filter_remove=filter_remove)

    data_pm2 = pm2.pm2io.from_interchange_format(data_if)
    # convert back to IF to have units in the fixed format
    data_if = data_pm2.pr.to_interchange_format()

    # ###
    # save data to IF and native format
    # ###
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"]), data_if
    )

    encoding = {var: compression for var in data_pm2.data_vars}
    data_pm2.pr.to_netcdf(
        output_folder / (output_filename + coords_terminologies["category"] + ".nc"),
        encoding=encoding,
    )
