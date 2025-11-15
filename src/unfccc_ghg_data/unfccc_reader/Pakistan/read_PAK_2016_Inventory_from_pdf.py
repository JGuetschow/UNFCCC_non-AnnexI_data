"""
Read Pakistan's 2016 Invetory from pdf


"""

import camelot
import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    fix_rows,
    gas_baskets,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.Pakistan.config_pak_INV2016 import (
    cat_codes_manual,
    category_conversion,
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    filter_remove,
    fix_cat_names,
    header_long,
    meta_data,
    page_defs,
    processing_info_country,
    terminology_proc,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = downloaded_data_path / "non-UNFCCC" / "Pakistan" / "2016-Inventory"
    output_folder = extracted_data_path / "non-UNFCCC" / "Pakistan"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "PAK_2026-Inventory_2016_"
    compression = dict(zlib=True, complevel=9)
    inventory_file_pdf = "GHGINVENTORY2011-2012_FINAL_GCISCRR19.pdf"

    # year_inventory = 2021
    entity_row = 0
    unit_row = 0
    default_unit = "Gg"
    regexp_unit = r"\((A-Za-z\))"
    regexp_entity = r"^([A-za-z0-9\s]+)\s\("
    # manual_repl_unit = {"Kt CO₂e": default_unit}
    # drop_rows = range(0, 6)

    index_cols = ("Greenhouse gas source and sink categories", default_unit)

    # ###
    # read the 2021 data from pdf into one long format dataframe
    # ###
    df_all = None
    for page in page_defs:
        print(f"Working on page {page}")
        page_def = page_defs[page]
        tables = camelot.read_pdf(
            str(input_folder / inventory_file_pdf), pages=page, **page_def["camelot"]
        )

        df_this_table = tables[0].df
        # replace line breaks, long hyphens, double, and triple spaces in
        # category names
        df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("\n", " ")
        df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("   ", " ")
        df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("  ", " ")
        df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("-", "-")

        # fix rows
        for n_rows in page_def["rows_to_fix"].keys():
            print(f"Fixing {n_rows}")
            df_this_table = fix_rows(
                df_this_table, page_def["rows_to_fix"][n_rows], 0, n_rows
            )

        # fix the double category name issue
        col_to_use = 0
        lastrow = None
        for i, row in df_this_table.iterrows():
            cat_to_fix = row[col_to_use]
            if cat_to_fix in fix_cat_names:
                if lastrow in fix_cat_names[cat_to_fix]:
                    row[
                        col_to_use
                    ] = f"{fix_cat_names[cat_to_fix][lastrow]}{cat_to_fix}"
                    df_this_table.loc[i] = row
                else:
                    raise ValueError(  # noqa: TRY003
                        f"Category to fix, but no fix defined {lastrow}, "
                        f"{row[col_to_use]}"
                    )
            else:
                lastrow = row[col_to_use]

        # add units

        # bring in right format for conversion to long format
        df_this_table = pm2.pm2io.nir_add_unit_information(
            df_this_table,
            unit_row=unit_row,
            entity_row=entity_row,
            regexp_unit=regexp_unit,
            regexp_entity=regexp_entity,
            # manual_repl_unit=manual_repl_unit,
            default_unit=default_unit,
        )

        # set index and convert to long format
        df_this_table = df_this_table.set_index(index_cols)
        df_this_table_long = pm2.pm2io.nir_convert_df_to_long(
            df_this_table, page_def["year"], header_long
        )

        if df_all is None:
            df_all = df_this_table_long
        else:
            df_all = pd.concat([df_all, df_this_table_long])

    # ###
    # conversion to PM2 IF
    # ###

    # make a copy of the categories row
    df_all["category"] = df_all["orig_cat_name"]

    # replace cat names by codes in col "category"
    # first the manual replacements
    df_all["category"] = df_all["category"].replace(cat_codes_manual, regex=False)

    df_all = df_all.reset_index(drop=True)

    # make sure all col headers are str
    df_all.columns = df_all.columns.map(str)

    # remove ','
    df_all.loc[:, "data"] = df_all.loc[:, "data"].str.replace(",", "", regex=False)

    # drop orig_cat_name as it's not unique per category
    df_all = df_all.drop(columns="orig_cat_name")

    # ###
    # convert to PRIMAP2 interchange format
    # ###
    data_if = pm2.pm2io.convert_long_dataframe_if(
        df_all,
        coords_cols=coords_cols,
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

    # convert back to IF to have units in the fixed format
    data_if = data_pm2.pr.to_interchange_format()

    # ###
    # save data to IF and native format
    # ###
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"]),
        data_if,
    )

    encoding = {var: compression for var in data_pm2.data_vars}
    data_pm2.pr.to_netcdf(
        output_folder / (output_filename + coords_terminologies["category"] + ".nc"),
        encoding=encoding,
    )

    # ###
    # process data (add sectors and gas baskets)
    # ###
    data_proc_pm2 = data_pm2.copy()
    ### processing
    # combine CO2 emissions and removals
    data_proc_pm2["CO2"] = data_proc_pm2[["CO2 emissions", "CO2 removals"]].pr.sum(
        dim="entity", skipna=True, min_count=1
    )
    data_proc_pm2["CO2"].attrs = {"entity": "CO2"}
    data_proc_pm2 = data_proc_pm2.drop_vars(["CO2 emissions", "CO2 removals"])

    # aggregate gas baskets
    # this also checks for inconsistencies
    data_proc_pm2 = process_data_for_country(
        data_proc_pm2,
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
