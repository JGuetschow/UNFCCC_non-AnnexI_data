"""
Read Mexico's BTR1 from pdf

This script reads data from Mexico's BTR1
Data are read from pdf using camelot for 2022
pages 79-81 from BTR_libro_24DIC2024.pdf
"""

import camelot
import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    gas_baskets,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.Pakistan.config_pak_btr1 import (
    add_coords_cols,
    cat_code_regexp,
    cat_codes_manual,
    category_conversion,
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    filter_remove,
    header_long,
    meta_data,
    page_defs_2021,
    processing_info_country,
    terminology_proc,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = downloaded_data_path / "UNFCCC" / "Pakistan" / "BTR1"
    output_folder = extracted_data_path / "UNFCCC" / "Pakistan"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "PAK_BTR1_2025_"
    compression = dict(zlib=True, complevel=9)
    inventory_file_pdf = (
        "Pakistan%27s_Biennial_Transparency_Report_%28BTR%29_2024_to_the_UNFCCC.pdf"
    )

    year_inventory = 2021
    entity_row = 0
    unit_row = 1
    default_unit = "Mt CO2 / yr"
    # manual_repl_unit = {"Kt CO₂e": default_unit}
    drop_rows = range(0, 6)

    index_cols = ("Categories", default_unit)

    # ###
    # read the 2021 data from pdf into one long format dataframe
    # ###
    df_2021 = None
    for page in page_defs_2021:
        print(f"Working on page {page}")
        page_def = page_defs_2021[page]
        tables = camelot.read_pdf(
            str(input_folder / inventory_file_pdf), pages=page, **page_def
        )
        for table in tables:
            df_this_table = table.df
            if df_2021 is None:
                df_2021 = df_this_table
            else:
                df_2021 = pd.concat([df_2021, df_this_table])

    # fix header
    new_header = [
        ["Categories", "Net CO2 emissions / removals", "CH4", "N2O", "Total"],
        ["", default_unit, default_unit, default_unit, default_unit],
    ]

    # df_2021.columns = new_header
    # df_2021 = df_2021.drop(drop_rows)
    df_2021 = df_2021.reset_index(drop=True)
    df_2021 = df_2021.drop(range(2, 6))
    df_2021.loc[0] = new_header[0]
    df_2021.loc[1] = new_header[1]
    df_2021 = df_2021.reset_index(drop=True)
    # df_2021.loc[2,("Categories", "")] = "0 - National Total"
    df_2021.loc[2, 0] = "0 - National Total"

    # replace line breaks, long hyphens, double, and triple spaces in category
    # names
    df_2021.iloc[:, 0] = df_2021.iloc[:, 0].str.replace("\n", " ")
    df_2021.iloc[:, 0] = df_2021.iloc[:, 0].str.replace("   ", " ")
    df_2021.iloc[:, 0] = df_2021.iloc[:, 0].str.replace("  ", " ")
    df_2021.iloc[:, 0] = df_2021.iloc[:, 0].str.replace("-", "-")

    # bring in right format for conversion to long format
    df_2021 = pm2.pm2io.nir_add_unit_information(
        df_2021,
        unit_row=unit_row,
        entity_row=entity_row,
        regexp_unit=".+",
        regexp_entity=".+",
        # manual_repl_unit=manual_repl_unit,
        default_unit=default_unit,
    )

    # set index and convert to long format
    df_2021 = df_2021.set_index(index_cols)
    df_2021_long = pm2.pm2io.nir_convert_df_to_long(
        df_2021, year_inventory, header_long
    )

    # ###
    # conversion to PM2 IF
    # ###
    # make a copy of the categories row
    df_2021_long["category"] = df_2021_long["orig_cat_name"]

    # replace cat names by codes in col "category"
    # first the manual replacements
    df_2021_long["category"] = df_2021_long["category"].replace(
        cat_codes_manual, regex=False
    )

    # then the regex replacements
    def repl(m):  # noqa: D103
        return m.group("code")

    df_2021_long["category"] = df_2021_long["category"].str.replace(
        cat_code_regexp, repl, regex=True
    )
    df_2021_long = df_2021_long.reset_index(drop=True)

    # make sure all col headers are str
    df_2021_long.columns = df_2021_long.columns.map(str)

    # ###
    # convert to PRIMAP2 interchange format
    # ###
    data_2021_if = pm2.pm2io.convert_long_dataframe_if(
        df_2021_long,
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

    data_pm2 = pm2.pm2io.from_interchange_format(data_2021_if)

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

    ### processing
    # aggregate gas baskets
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
