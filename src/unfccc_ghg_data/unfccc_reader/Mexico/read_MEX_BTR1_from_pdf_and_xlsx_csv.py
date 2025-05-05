"""
Read Mexico's BUR3 from pdf

This script reads data from Mexico's BTR1 and national inventory
Data are read from pdf using camelot for 2022 and from inventory
xlsx and csv files for 1990-2021 where consistent witht the BTR1

Source for the inventory:
https://www.datos.gob.mx/busca/dataset/inventario-nacional-de-emisiones-
de-gases-y-compuestos-de-efecto-invernadero-inegycei

TODO: code currently just a copy of BUR3 code
"""

# TODO: download all fies using datalad download-url (only two xlsx files needed)
# read from pdf: pages 79-81 from BTR_libro_24DIC2024.pdf
# read from xls: 2020-2021, 1990-2019 That covers all years. csv files not needed


import camelot
import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import downloaded_data_path, extracted_data_path, fix_rows
from unfccc_ghg_data.unfccc_reader.Mexico.config_mex_btr1 import (
    add_coords_cols,
    cat_code_regexp,
    cat_codes_manual,
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    filter_remove,
    header_long,
    meta_data,
    page_defs,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = downloaded_data_path / "UNFCCC" / "Mexico" / "BTR1"
    output_folder = extracted_data_path / "UNFCCC" / "Mexico"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "MEX_BTR1_2025_"
    compression = dict(zlib=True, complevel=9)
    inventory_file_pdf = "BTR_libro_24DIC2024.pdf"

    year = 2022
    entity_row = 1
    unit_row = 0
    default_unit = "kt CO2 / yr"
    manual_repl_unit = {"Kt CO₂e": default_unit}

    index_cols = ("Categorías de fuentes y sumideros de GEI", default_unit)

    # ###
    # read the data from pdf into one long format dataframe
    # ###
    df_pdf = None
    for page in page_defs:
        print(f"Working on page {page}")
        page_def = page_defs[page]
        tables = camelot.read_pdf(
            str(input_folder / inventory_file_pdf), pages=page, **page_def["camelot"]
        )
        df_this_table = tables[0].df

        # fix rows
        for n_rows in page_def["rows_to_fix"].keys():
            # replace line breaks, long hyphens, double, and triple spaces in category
            # names
            df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("\n", " ")
            df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("   ", " ")
            df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("  ", " ")
            df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("-", "-")
            # replace double space in entity
            df_this_table.iloc[0, :] = df_this_table.iloc[0, :].str.replace("  ", " ")
            df_this_table = fix_rows(
                df_this_table, page_def["rows_to_fix"][n_rows], 0, n_rows
            )

        # add units

        # bring in right format for conversion to long format
        df_this_table = pm2.pm2io.nir_add_unit_information(
            df_this_table,
            unit_row=unit_row,
            entity_row=entity_row,
            regexp_unit=".+",
            regexp_entity=".+",
            manual_repl_unit=manual_repl_unit,
            default_unit=default_unit,
        )

        # set index and convert to long format
        df_this_table = df_this_table.set_index(index_cols)
        df_this_table_long = pm2.pm2io.nir_convert_df_to_long(
            df_this_table, year, header_long
        )

        # combine with tables for other sectors (merge not append)
        if df_pdf is None:
            df_pdf = df_this_table_long
        else:
            df_pdf = pd.concat([df_pdf, df_this_table_long], axis=0, join="outer")

    # ###
    # conversion to PM2 IF
    # ###
    # make a copy of the categories row
    df_pdf["category"] = df_pdf["orig_cat_name"]

    # replace cat names by codes in col "category"
    # first the manual replacements
    df_pdf["category"] = df_pdf["category"].replace(cat_codes_manual, regex=True)

    # then the regex replacements
    def repl(m):  # noqa: D103
        return m.group("code")

    df_pdf["category"] = df_pdf["category"].str.replace(
        cat_code_regexp, repl, regex=True
    )
    df_pdf = df_pdf.reset_index(drop=True)

    # replace "," and " " with "" in data
    df_pdf.loc[:, "data"] = df_pdf.loc[:, "data"].str.replace(",", "", regex=False)
    df_pdf.loc[:, "data"] = df_pdf.loc[:, "data"].str.replace(" ", "", regex=False)

    # make sure all col headers are str
    df_pdf.columns = df_pdf.columns.map(str)

    # ###
    # convert to PRIMAP2 interchange format
    # ###
    data_pdf_if = pm2.pm2io.convert_long_dataframe_if(
        df_pdf,
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

    cat_label = f"category ({coords_terminologies['category']})"
    # fix error cats
    data_pdf_if[cat_label] = data_pdf_if[cat_label].str.replace("error_", "")

    data_pdf_pm2 = pm2.pm2io.from_interchange_format(data_pdf_if)

    ###########
    ### data from xlsx files
    ###########

    # # convert back to IF to have units in the fixed format
    # data_if = data_pm2.pr.to_interchange_format()
    #
    # # ###
    # # save data to IF and native format
    # # ###
    # if not output_folder.exists():
    #     output_folder.mkdir()
    # pm2.pm2io.write_interchange_format(
    #     output_folder / (output_filename + coords_terminologies["category"]), data_if
    # )
    #
    # encoding = {var: compression for var in data_pm2.data_vars}
    # data_pm2.pr.to_netcdf(
    #     output_folder / (output_filename + coords_terminologies["category"] + ".nc"),
    #     encoding=encoding,
    # )
