"""
Read South Korea's 2024 Inventory from Excel file
"""

import os
import sys

import pandas as pd
import primap2 as pm2
from primap2.pm2io._data_reading import filter_data

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    gas_baskets,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.Republic_of_Korea.config_KOR_INV2024 import (
    cat_codes,
    cat_name_translations,
    category_conversion,
    fix_rows,
    gwp_to_use,
    processing_info_country,
    terminology_proc,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = (
        downloaded_data_path / "non-UNFCCC" / "Republic_of_Korea" / "2024-Inventory"
    )
    output_folder = extracted_data_path / "non-UNFCCC" / "Republic_of_Korea"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "KOR_2024-Inventory_2024_"

    inventory_file = (
        "Republic_of_Korea_National_GHG_Inventory_(1990_2022)(IPCC2006).xlsx"
    )
    years_to_read = range(1990, 2022 + 1)

    sheets_to_read = ["온실가스", "CO2", "CH4", "N2O", "HFCs", "PFCs", "SF6", "NF3"]
    cols_to_read = range(1, 2022 - 1990 + 3)

    # columns for category UNFCCC_GHG_data and original category name
    index_cols = ["분야·부문/연도"]

    sheet_metadata = {
        "entity": {
            "온실가스": f"KYOTOGHG ({gwp_to_use})",
            "CO2": "CO2",
            "CH4": f"CH4 ({gwp_to_use})",
            "N2O": f"N2O ({gwp_to_use})",
            "HFCs": f"HFCS ({gwp_to_use})",
            "PFCs": f"PFCS ({gwp_to_use})",
            "SF6": f"SF6 ({gwp_to_use})",
            "NF3": f"NF3 ({gwp_to_use})",
        },
        "unit": {
            "온실가스": "Gg CO2 / yr",
            "CO2": "Gg CO2 / yr",
            "CH4": "Gg CO2 / yr",
            "N2O": "Gg CO2 / yr",
            "HFCs": "Gg CO2 / yr",
            "PFCs": "Gg CO2 / yr",
            "SF6": "Gg CO2 / yr",
            "NF3": "Gg CO2 / yr",
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
        "category": "IPCC2006_KOR_INV",
        "scenario": "PRIMAP",
    }

    coords_defaults = {
        "source": "KOR-GHG-Inventory",
        "provenance": "measured",
        "area": "KOR",
        "scenario": "INV2024",
    }

    coords_value_mapping = {
        "cat_name_translation": cat_name_translations,
        "category": cat_codes,
    }

    # filtering after IF creation to be able to use the IPCC codes
    filter_remove = {
        "f1": {
            "category (IPCC2006_KOR_INV)": "\\IGNORE",
        },
    }

    filter_keep = {}

    meta_data = {
        "references": "https://www.gir.go.kr/home/board/read.do?pagerOffset="
        "0&maxPageItems=10&maxIndexPages=10&searchKey=&searchValue"
        "=&menuId=36&boardId=79&boardMasterId=2&boardCategoryId=",
        "rights": "",
        "contact": "mail@johannes-guetschow.de",
        "title": "Republic of Korea: National Greenhouse Gas Inventory Report 2024",
        "comment": "Read fom xlsx file by Johannes Gütschow",
        "institution": "Republic of Korea, Ministry of Environment, Greenhouse "
        "Gas Inventory and Research Center",
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
        print(f"Reading sheet {sheet}.")
        # read current sheet (one sheet per gas)
        df_current = pd.read_excel(
            input_folder / inventory_file,
            sheet_name=sheet,
            skiprows=3,
            nrows=146,
            usecols=cols_to_read,
            engine="openpyxl",
        )
        # drop all rows where the index cols (category UNFCCC_GHG_data and name)
        # are both NaN
        # as without one of them there is no category information
        df_current = df_current.dropna(axis=0, how="all", subset=index_cols)
        # make sure all col headers are str
        df_current.columns = df_current.columns.map(str)

        # fix the double category issue in livestock
        lastrow = None
        for i, row in df_current.iterrows():
            cat_to_fix = row["분야·부문/연도"]
            if cat_to_fix in fix_rows:
                if lastrow in fix_rows[cat_to_fix]:
                    row[
                        "분야·부문/연도"
                    ] = f"{fix_rows[cat_to_fix][lastrow]}{cat_to_fix}"
                    df_current.iloc[i] = row
                else:
                    raise ValueError(  # noqa: TRY003
                        f"Row to fix, but no fix defined {lastrow}, "
                        f"{row['분야·부문/연도']}"
                    )
            else:
                lastrow = row["분야·부문/연도"]
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
        copy_df=True,  # we need the unchanged DF for the conversion step
    )

    filter_data(data_if, filter_remove=filter_remove)

    # conversion to PRIMAP2 native format
    data_pm2 = pm2.pm2io.from_interchange_format(data_if)
    # convert back to IF to have units in the fixed format
    data_pm2 = data_pm2.reset_coords(
        ["orig_cat_name", "cat_name_translation"], drop=True
    )
    data_if = data_pm2.pr.to_interchange_format()

    # ###
    # save data to IF and native format
    # ###
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"]), data_if
    )

    data_pm2 = pm2.pm2io.from_interchange_format(data_if)
    encoding = {var: compression for var in data_pm2.data_vars}
    data_pm2.pr.to_netcdf(
        output_folder / (output_filename + coords_terminologies["category"] + ".nc"),
        encoding=encoding,
    )

    # ###
    # conversion to ipcc 2006 categories
    # ###

    ### processing
    # aggregate gas baskets (some KYOTOGHG time seres were removed because of errors)
    # this also checks for inconsistencies
    data_proc_pm2 = process_data_for_country(
        data_pm2,
        entities_to_ignore=[],
        gas_baskets=gas_baskets,
        processing_info_country=processing_info_country,
        cat_terminology_out=terminology_proc,
        category_conversion=category_conversion,
    )

    # adapt source and metadata
    current_source = data_proc_pm2.coords["source"].to_numpy()[0]
    data_temp = data_proc_pm2.pr.loc[{"source": current_source}]
    data_proc_pm2 = data_proc_pm2.pr.set("source", "BUR_NIR", data_temp)
    data_proc_pm2 = data_proc_pm2.pr.loc[{"source": ["BUR_NIR"]}]

    # ###
    # save data to IF and native format
    # ###
    data_proc_if = data_proc_pm2.pr.to_interchange_format()
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + terminology_proc),
        data_proc_if,
    )

    encoding = {var: compression for var in data_proc_pm2.data_vars}
    data_proc_pm2.pr.to_netcdf(
        output_folder / (output_filename + terminology_proc + ".nc"),
        encoding=encoding,
    )
