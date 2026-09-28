"""
Read Mexico's 2026 inventory from xlsx

This script reads data from Mexico's national inventory
Data are read from the inventory
xlsx file for 1990-2024. 2024 data are marked as preliminary

Source for the inventory:
https://www.gob.mx/cms/uploads/attachment/file/1031246/INEGyCEI_1990-2024_Dif_221025.xlsx
"""

import numpy as np
import openpyxl
import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    gas_baskets,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.Mexico.config_mex_inv2026 import (
    CRT1_MEX_to_IPCC2006_mapping,
    add_coords_cols,
    cat_code_regexp,
    cat_codes_manual,
    cat_terminology_proc,
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    filter_remove,
    header_long,
    meta_data,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = downloaded_data_path / "non-UNFCCC" / "Mexico" / "2026-Inventory"
    output_folder = extracted_data_path / "non-UNFCCC" / "Mexico"
    if not output_folder.exists():
        output_folder.mkdir()

    inv_files = [
        "INEGyCEI_1990-2024_Dif_221025.xlsx",
    ]

    output_filename = "MEX_2026-Inventory_2026_"
    compression = dict(zlib=True, complevel=9)

    idx_year = 1
    idx_unit = 0
    col_year = (
        "INVENTARIO NACIONAL DE EMISIONES DE GASES Y COMPUESTOS DE "
        "EFECTO INVERNADERO (INEGYCEI)"
    )
    entity_unit_rows = range(0, 5)

    unit_mapping = {
        "Emisiones de gases de efecto invernadero (t de CO2e )": "tCO2eq",
    }

    df_xlsx = None
    for file in inv_files:
        current_wb = openpyxl.load_workbook(input_folder / file)
        sheets = current_wb.sheetnames

        df_file = None

        for sheet in sheets:
            print(f"Reading data from file {file}, sheet {sheet}")
            df_sheet = pd.read_excel(input_folder / file, sheet_name=sheet)

            # remove rows and cols which are all nan
            df_sheet = df_sheet.dropna(axis=0, how="all")
            df_sheet = df_sheet.dropna(axis=1, how="all")

            # replace line breaks, long hyphens, double, and triple spaces in category
            # names
            df_sheet.iloc[:, 0] = df_sheet.iloc[:, 0].str.strip()
            df_sheet.iloc[:, 0] = df_sheet.iloc[:, 0].str.replace("\n", " ")
            df_sheet.iloc[:, 0] = df_sheet.iloc[:, 0].str.replace("   ", " ")
            df_sheet.iloc[:, 0] = df_sheet.iloc[:, 0].str.replace("  ", " ")
            df_sheet.iloc[:, 0] = df_sheet.iloc[:, 0].str.replace("-", "-")

            year = df_sheet[col_year].loc[idx_year]
            unit_text = df_sheet[col_year].loc[idx_unit]
            unit_text = unit_text.replace("  ", " ")
            unit_text = unit_text.replace("\n", " ")
            unit = unit_mapping[unit_text]
            df_sheet.loc[idx_unit, col_year] = np.nan
            index_cols = ("CATEGORÍA / FUENTE / SUBFUENTE DE EMISIÓN", unit)
            print(f"year: {year}, unit: {unit}")
            df_sheet.loc[[0, 1, 2, 3]] = df_sheet.loc[[0, 1, 2, 3]].ffill(axis=0)
            # replace double spaces and line breaks in entities
            df_sheet.iloc[3, :] = df_sheet.iloc[3, :].str.replace("  ", " ")
            df_sheet.iloc[3, :] = df_sheet.iloc[3, :].str.replace("\n", " ")
            df_sheet.iloc[3, :] = df_sheet.iloc[3, :].str.strip()
            df_sheet.columns = df_sheet.loc[3]
            # remove columns where header is nan
            if np.nan in df_sheet.columns:
                df_sheet = df_sheet.drop(columns=np.nan)
            df_sheet = df_sheet.drop(entity_unit_rows)
            # also drop any rows where the first col is nan
            df_sheet = df_sheet.dropna(subset=df_sheet.columns[0])

            # bring in right format for conversion to long format
            df_sheet = pm2.pm2io.nir_add_unit_information(
                df_sheet,
                unit_row="header",
                regexp_unit=r"\(([A-Za-z0-9]+)\)",
                regexp_entity=".+",
                default_unit=unit,
            )

            # set index and convert to long format
            # print(df_sheet.columns[0])
            df_sheet = df_sheet.set_index(index_cols)
            # sum mixture of HFC-365mfc and HFC-227ea with HFC-365mfc
            df_sheet[("HFC-365mfc", unit)] = (df_sheet)[
                [("HFC-365mfc/227ea", unit), ("HFC-365mfc", unit)]
            ].sum(axis=1, skipna=True, min_count=1)
            df_sheet = df_sheet.drop(columns=[("HFC-365mfc/227ea", unit)])
            # annoyingly this creates None values in the data (instead of np.nan)
            # which we have to fix for later steps tow ork
            df_sheet[("HFC-365mfc", unit)] = df_sheet[("HFC-365mfc", unit)].fillna(
                value=np.nan
            )

            df_sheet_long = pm2.pm2io.nir_convert_df_to_long(
                df_sheet, year, header_long
            )

            # combine with tables for other years
            if df_file is None:
                df_file = df_sheet_long
            else:
                df_file = pd.concat([df_file, df_sheet_long], axis=0, join="outer")

        # combine with tables from other files
        if df_xlsx is None:
            df_xlsx = df_file
        else:
            df_xlsx = pd.concat([df_xlsx, df_file], axis=0, join="outer")

    # ###
    # conversion to PM2 IF
    # ###
    # make a copy of the categories row
    df_xlsx["category"] = df_xlsx["orig_cat_name"]

    # replace cat names by codes in col "category"
    # first the manual replacements
    df_xlsx["category"] = df_xlsx["category"].replace(cat_codes_manual, regex=False)

    # then the regex replacements
    def repl(m):  # noqa: D103
        return m.group("code")

    df_xlsx["category"] = df_xlsx["category"].str.replace(
        cat_code_regexp, repl, regex=True
    )
    df_xlsx = df_xlsx.reset_index(drop=True)

    # make sure all col headers are str
    df_xlsx.columns = df_xlsx.columns.map(str)

    # drop duplicate rows (national total emissions are present twice)
    df_xlsx = df_xlsx.drop_duplicates(
        keep="first", subset=["category", "entity", "time"]
    )

    # ###
    # convert to PRIMAP2 interchange format
    # ###
    data_if = pm2.pm2io.convert_long_dataframe_if(
        df_xlsx,
        coords_cols=coords_cols,
        add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        # coords_value_filling=coords_value_filling,
        filter_remove=filter_remove,
        # filter_keep=filter_keep,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )

    data_pm2 = pm2.pm2io.from_interchange_format(data_if)

    ###########
    ### data from xlsx files
    ###########

    # convert back to IF to have units in the fixed format
    data_if = data_pm2.pr.to_interchange_format()

    # ###
    # save data to IF and native format
    # ###
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"] + "_raw"),
        data_if,
    )

    encoding = {var: compression for var in data_pm2.data_vars}
    data_pm2.pr.to_netcdf(
        output_folder
        / (output_filename + coords_terminologies["category"] + "_raw" + ".nc"),
        encoding=encoding,
    )

    # ###
    # process data (add sectors and gas baskets)
    # ###

    # drop the original category name
    data_proc_pm2 = data_pm2.reset_coords(["orig_cat_name"], drop=True)

    ### processing
    # aggregate gas baskets
    # this also checks for inconsistencies
    data_proc_pm2 = process_data_for_country(
        data_proc_pm2,
        entities_to_ignore=[],
        gas_baskets=gas_baskets,
        cat_terminology_out=cat_terminology_proc,
        category_conversion=CRT1_MEX_to_IPCC2006_mapping,
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
        output_folder / (output_filename + cat_terminology_proc),
        data_proc_if,
    )

    encoding = {var: compression for var in data_proc_pm2.data_vars}
    data_proc_pm2.pr.to_netcdf(
        output_folder / (output_filename + cat_terminology_proc + ".nc"),
        encoding=encoding,
    )
