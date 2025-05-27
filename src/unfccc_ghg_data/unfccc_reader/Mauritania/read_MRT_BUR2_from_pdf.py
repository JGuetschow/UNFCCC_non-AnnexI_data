"""
Read data from Mauritania's BUR2.

Data are read from pdf. The file contains a detailed inventory for
1990, 1995, 2000, 2010, 2012, 2015, 1018.

"""

import camelot
import numpy as np
import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import (
    compression,
    downloaded_data_path,
    extracted_data_path,
    fix_rows,
    gas_baskets,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.Mauritania.config_mrt_bur2 import (
    area_fgases,
    cat_code_regexp,
    cat_codes_manual,
    cats_remove,
    cats_remove_fgases,
    cols_fgases,
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    entities_to_remove_fgases,
    entity_row,
    entity_row_fgases,
    filter_remove,
    first_ignore_cat_fgases,
    fix_cat_using_preceeding,
    fix_cat_values,
    gwp_to_use,
    header_long,
    index_cols,
    meta_data,
    pages_fgases,
    proc_info_country,
    remove_per_table,
    rows_to_fix_fgases,
    table_defs,
    table_defs_fgases,
    table_reading_defs,
    terminology_proc,
    unit_entity_rows,
    unit_entity_rows_fgases,
    unit_info_fgases,
    unit_row,
    unit_row_fgases,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = downloaded_data_path / "UNFCCC" / "Mauritania" / "BUR2"
    output_folder = extracted_data_path / "UNFCCC" / "Mauritania"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "MRT_BUR2_2020_"
    inventory_file = "Mauritania_BUR_2_-_NIR_Annexes_-_May_2020.pdf"

    # ###
    # read the tables from pdf
    # ###

    ## main tables
    # empty dataframe
    df_all = None
    for year in table_defs.keys():
        print(f"Working on year {year}")

        # join the tables which need combining
        df_this_year = None
        for table_parts, cats_remove_this_table in zip(
            table_defs[year], remove_per_table
        ):
            new_table = camelot.read_pdf(
                str(input_folder / inventory_file),
                pages=table_reading_defs[table_parts[0]]["page"],
                table_areas=[
                    table_reading_defs[table_parts[0]]["page_def"]["area"][
                        table_reading_defs[table_parts[0]]["table"]
                    ]
                ],
                columns=[
                    table_reading_defs[table_parts[0]]["page_def"]["cols"][
                        table_reading_defs[table_parts[0]]["table"]
                    ]
                ],
                flavor="stream",
                split_text=True,
            )
            df_this_table = new_table[0].df
            if "fix_rows" in table_reading_defs[table_parts[0]].keys():
                rows_to_fix = table_reading_defs[table_parts[0]]["fix_rows"]
                for n_rows in rows_to_fix:
                    df_this_table = fix_rows(
                        df_this_table,
                        rows_to_fix=rows_to_fix[n_rows],
                        col_to_use=0,
                        n_rows=n_rows,
                    )
            if len(table_parts) > 1:
                parts_remaining = table_parts[1:]
                for part in parts_remaining:
                    new_table = camelot.read_pdf(
                        str(input_folder / inventory_file),
                        pages=table_reading_defs[part]["page"],
                        table_areas=[
                            table_reading_defs[part]["page_def"]["area"][
                                table_reading_defs[part]["table"]
                            ]
                        ],
                        columns=[
                            table_reading_defs[part]["page_def"]["cols"][
                                table_reading_defs[part]["table"]
                            ]
                        ],
                        flavor="stream",
                        split_text=True,
                    )
                    df_new_table_part = new_table[0].df
                    if "fix_rows" in table_reading_defs[part].keys():
                        rows_to_fix = table_reading_defs[part]["fix_rows"]
                        for n_rows in rows_to_fix:
                            df_new_table_part = fix_rows(
                                df_new_table_part,
                                rows_to_fix=rows_to_fix[n_rows],
                                col_to_use=0,
                                n_rows=n_rows,
                            )
                    df_this_table = pd.concat([df_this_table, df_new_table_part])

            df_this_table = df_this_table.reset_index(drop=True)

            df_this_table = df_this_table.drop(
                df_this_table.index[
                    : table_reading_defs[table_parts[0]]["header"]["rows"]
                ],
            )
            df_this_table.columns = [
                table_reading_defs[table_parts[0]]["header"]["entity"],
                table_reading_defs[table_parts[0]]["header"]["unit"],
            ]

            # replace '' by nan for filling
            df_this_table.iloc[unit_entity_rows] = df_this_table.iloc[
                unit_entity_rows
            ].replace("", np.nan)
            # fill the units to the right as for merged cells the unit is only
            # in the first cell
            df_this_table.iloc[unit_row] = df_this_table.iloc[unit_row].ffill(axis=0)
            # fill entity from unit if empty
            df_this_table.iloc[unit_entity_rows] = df_this_table.iloc[
                unit_entity_rows
            ].ffill()

            # fix values in category col
            df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].replace(fix_cat_values)

            # replace line breaks, double, and triple spaces in category names
            df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("\n", " ")
            df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("   ", " ")
            df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("  ", " ")

            # fix category values using preceding categories
            for cat in fix_cat_using_preceeding:
                mask = df_this_table.iloc[:, 0] == cat
                if any(mask):
                    print(f"Found occurence of category to fix {cat}")
                    indices = np.where(mask)[0]
                    for idx in indices:
                        if (
                            df_this_table.iloc[idx - 1, 0]
                            in fix_cat_using_preceeding[cat].keys()
                        ):
                            df_this_table.iloc[idx, 0] = fix_cat_using_preceeding[cat][
                                df_this_table.iloc[idx - 1, 0]
                            ]
                            print(
                                f"Replaced {cat} by {fix_cat_using_preceeding[cat][df_this_table.iloc[idx - 1, 0]]}"  # noqa: E501
                            )

            # reindex because we have double indices
            df_this_table = df_this_table.reset_index(drop=True)

            # remove given rows
            for cat in cats_remove_this_table:
                # old_len = len(df_this_table)
                df_this_table = df_this_table.drop(
                    df_this_table[df_this_table[index_cols[0]] == cat].index
                )
                # new_len = len(df_this_table)
                # print(f"Removed {old_len - new_len} rows from table for year {year}
                # and category {cat}.")

            # set index and convert to long format
            df_this_table = df_this_table.set_index(index_cols)
            # df_before_convert = df_this_table.copy(deep=True)
            df_this_table_long = pm2.pm2io.nir_convert_df_to_long(
                df_this_table, year, header_long
            )

            # combine with tables for other sectors (merge not append)
            if df_this_year is None:
                df_this_year = df_this_table_long
            else:
                df_this_year = pd.concat([df_this_year, df_this_table_long])

        # aggregate years to df_all
        if df_all is None:
            df_all = df_this_year
        else:
            df_all = pd.concat([df_all, df_this_year])

    df_all = df_all.reset_index(drop=True)

    ## fgases ##############

    df_all_fgases = None
    for year in table_defs_fgases.keys():
        print(f"Working on fgases year {year}")

        # join the tables which need combining
        table_parts = table_defs_fgases[year]
        tables_fgases = camelot.read_pdf(
            str(input_folder / inventory_file),
            pages=pages_fgases[table_parts[0]],
            table_areas=[area_fgases[table_parts[0]]],
            columns=cols_fgases,
            flavor="stream",
            split_text=True,
        )
        df_this_year = tables_fgases[0].df.copy(deep=True)
        if len(table_parts) > 1:
            parts_remaining = table_parts[1:]
            for part in parts_remaining:
                tables_fgases = camelot.read_pdf(
                    str(input_folder / inventory_file),
                    pages=pages_fgases[part],
                    table_areas=[area_fgases[part]],
                    columns=cols_fgases,
                    flavor="stream",
                    split_text=True,
                )
                df_this_year = pd.concat([df_this_year, tables_fgases[0].df])

        # reindex because we have double indices
        df_this_year = df_this_year.reset_index(drop=True)

        for n_rows in rows_to_fix_fgases:
            df_this_year = fix_rows(
                df_this_year,
                rows_to_fix=rows_to_fix_fgases[n_rows],
                col_to_use=0,
                n_rows=n_rows,
            )

        # remove additional header rows
        for cat in cats_remove_fgases:
            df_this_year = df_this_year.drop(df_this_year[df_this_year[0] == cat].index)

        # add category col label if missing
        if (df_this_year.iloc[entity_row][0] == "") & (
            str(df_this_year.iloc[unit_row][0]) == ""
        ):
            print(f"Add category header for table {table_parts[0]}")
            df_this_year.iloc[entity_row][0] = index_cols[0]

        # replace '' by nan for filling
        df_this_year.iloc[unit_entity_rows_fgases] = df_this_year.iloc[
            unit_entity_rows_fgases
        ].replace("", np.nan)
        # fill the units to the right as for merged cells the unit is only in
        # the first cell
        df_this_year.iloc[unit_row_fgases] = df_this_year.iloc[unit_row_fgases].fillna(
            axis=0, method="ffill"
        )

        # replace line breaks in units and entities
        df_this_year.iloc[entity_row_fgases] = df_this_year.iloc[
            entity_row_fgases
        ].str.replace("\n", "")
        df_this_year.iloc[unit_row_fgases] = df_this_year.iloc[
            unit_row_fgases
        ].str.replace("\n", "")
        df_this_year.iloc[entity_row_fgases] = df_this_year.iloc[
            entity_row_fgases
        ].str.replace("   ", " ")
        df_this_year.iloc[unit_row_fgases] = df_this_year.iloc[
            unit_row_fgases
        ].str.replace("   ", " ")
        df_this_year.iloc[entity_row_fgases] = df_this_year.iloc[
            entity_row_fgases
        ].str.replace("  ", " ")
        df_this_year.iloc[unit_row_fgases] = df_this_year.iloc[
            unit_row_fgases
        ].str.replace("  ", " ")
        df_this_year.iloc[entity_row_fgases] = df_this_year.iloc[
            entity_row_fgases
        ].str.strip()
        df_this_year.iloc[unit_row_fgases] = df_this_year.iloc[
            unit_row_fgases
        ].str.strip()

        # replace line breaks, double, and triple spaces in category names
        df_this_year.iloc[:, 0] = df_this_year.iloc[:, 0].str.replace("\n", " ")
        df_this_year.iloc[:, 0] = df_this_year.iloc[:, 0].str.replace("   ", " ")
        df_this_year.iloc[:, 0] = df_this_year.iloc[:, 0].str.replace("  ", " ")

        # set unit row cat label to nan
        df_this_year.iloc[unit_row_fgases, 0] = np.nan

        # remove second part of table with GWP weighted data
        idx = df_this_year[
            df_this_year.iloc[:, 0] == first_ignore_cat_fgases
        ].index.tolist()[0]
        df_this_year = df_this_year.loc[: idx - 1]

        df_this_year = pm2.pm2io.nir_add_unit_information(
            df_this_year,
            unit_row=unit_row_fgases,
            entity_row=entity_row_fgases,
            **unit_info_fgases,
        )

        # remove entities
        df_this_year = df_this_year.drop(columns=entities_to_remove_fgases)

        # set index and convert to long format
        df_this_year = df_this_year.set_index(index_cols)
        df_this_year_long = pm2.pm2io.nir_convert_df_to_long(
            df_this_year, year, header_long
        )

        # aggregate years to df_all
        if df_all_fgases is None:
            df_all_fgases = df_this_year_long
        else:
            df_all_fgases = pd.concat([df_all_fgases, df_this_year_long])

    # combine with other data
    df_all = pd.concat([df_all, df_all_fgases])

    # drop the rows with memo items etc
    for cat in cats_remove:
        df_all = df_all.drop(df_all[df_all["orig_cat_name"] == cat].index)

        # make a copy of the categories row
    df_all["category"] = df_all["orig_cat_name"]

    # temp: drop NOx and CO as the data is not read properly
    # df_all = df_all.drop(df_all[df_all["entity"] == "CO"].index)
    # df_all = df_all.drop(df_all[df_all["entity"] == "NOx"].index)

    # replace cat names by codes in col "category"
    # first the manual replacements
    df_all["category"] = df_all["category"].replace(cat_codes_manual)

    # then the regex repalcements
    def repl(m):  # noqa: D103
        return m.group("code")

    df_all["category"] = df_all["category"].str.replace(
        cat_code_regexp, repl, regex=True
    )
    df_all = df_all.reset_index(drop=True)

    # replace "," with "." in data and remove space in number
    df_all.loc[:, "data"] = df_all.loc[:, "data"].str.replace(",", ".", regex=False)
    df_all.loc[:, "data"] = df_all.loc[:, "data"].str.replace(". ", ".", regex=False)

    # make sure all col headers are str
    df_all.columns = df_all.columns.map(str)

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

    data_if = data_if.drop(columns="orig_cat_name")
    data_if.attrs["dimensions"]["*"].remove("orig_cat_name")

    # conversion to PRIMAP2 native format
    data_pm2 = pm2.pm2io.from_interchange_format(data_if)

    # ###
    # save data to IF and native format
    # ###
    data_if = data_pm2.pr.to_interchange_format()
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"] + "_raw"),
        data_if,
    )

    encoding = {var: compression for var in data_pm2.data_vars}
    data_pm2.pr.to_netcdf(
        output_folder
        / (output_filename + coords_terminologies["category"] + "_raw.nc"),
        encoding=encoding,
    )

    ### processing
    data_proc_pm2 = data_pm2  # copy not needed data_pm2 is not needed any more
    # fix HFC values (code is more general than needed as prep for transfer
    # into a function
    HFC_fix = {  # SAR GWP while rest uses AR4
        "dim": "category",
        "source_value": "2",
        "target_values": ["2.F", "2.F.1", "2.F.1.a"],
        "filter": {
            "variable": [f"HFCS ({gwp_to_use})"],
            "time": ["2000", "2010"],
        },
    }
    filter = HFC_fix["filter"]
    variables = data_proc_pm2.data_vars
    if "variable" in filter:
        filter_vars = filter.pop("variable")
        variables = [var for var in filter_vars if var in variables]

    filter_source = filter.copy()
    filter_source[HFC_fix["dim"]] = HFC_fix["source_value"]
    for var in variables:
        source_data = data_proc_pm2[var].pr.loc[filter_source]
        for value in HFC_fix["target_values"]:
            data_proc_pm2[var] = data_proc_pm2[var].pr.set(
                HFC_fix["dim"], value, source_data, existing="overwrite"
            )

    # actual processing
    data_proc_pm2 = process_data_for_country(
        data_pm2,
        entities_to_ignore=[],
        gas_baskets=gas_baskets,
        processing_info_country=proc_info_country,
        cat_terminology_out=terminology_proc,
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
