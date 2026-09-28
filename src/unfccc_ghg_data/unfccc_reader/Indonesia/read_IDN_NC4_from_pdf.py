"""
Read Indonesia's NC4 from pdf

This script reads data from Indonesia's NC4
Data are read from pdf using camelot.

TODO: elaborate on processing

"""

from copy import deepcopy

import camelot
import primap2 as pm2
import primap2.pm2io
from primap2.pm2io._data_reading import matches_time_format

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    fix_rows,
    merge_rows,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.Indonesia.config_idn_nc4 import (
    cat_code_regexp,
    cat_codes_manual,
    cat_conversion,
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    country_processing_step1,
    filter_remove,
    gas_baskets,
    meta_data,
    page_defs,
    table_defs_timeseries,
    terminology_proc,
    tolerance,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = downloaded_data_path / "UNFCCC" / "Indonesia" / "NC4"
    output_folder = extracted_data_path / "UNFCCC" / "Indonesia"
    if not output_folder.exists():
        output_folder.mkdir()

    inventory_file = "The_Final_Fourth_National_Communication.pdf"
    output_filename = "IDN_NC4_2026_"

    compression = dict(zlib=True, complevel=9)

    # ###
    # read the tables from pdf
    # ###

    all_tables = []
    for page, page_def in page_defs.items():
        print(f"Reading from page {page}")
        new_tables = camelot.read_pdf(
            str(input_folder / inventory_file),
            pages=page,
            flavor="stream",
            **page_def,
        )
        for table in new_tables:
            all_tables.append(table.df)

    # ###
    # process the tables and convert to PM2 IF
    # part 1: trend tables
    # ###
    data_pm2 = None
    for table_name, table_def in table_defs_timeseries.items():
        print(f"Working on table: {table_name}")

        # process all raw tables
        # individual tables as they all have headers

        for table in table_def["tables"]:
            df_this_table = all_tables[table].copy(deep=True)
            indices_to_drop = []

            # combine header rows
            if "rows_to_merge" in table_def.keys():
                df_this_table, new_indices_to_drop = merge_rows(
                    df_this_table, table_def["rows_to_merge"]
                )
                indices_to_drop = indices_to_drop + list(new_indices_to_drop)

            # drop rows if necessary
            if "rows_to_drop" in table_def.keys():
                new_indices_to_drop = df_this_table.iloc[
                    table_def["rows_to_drop"]
                ].index
                indices_to_drop = indices_to_drop + list(new_indices_to_drop)

            if indices_to_drop:
                df_this_table = df_this_table.drop(indices_to_drop)

            # drop cols if necessary
            if "cols_to_drop" in table_def.keys():
                df_this_table = df_this_table.drop(table_def["cols_to_drop"], axis=1)

            # # replace non breaking spaces
            # df_this_table.loc[:, 0] = df_this_table.loc[:, 0].str.replace(
            #     " ", " ", regex=False
            # )

            # fix content that spreads across multiple rows
            if "rows_to_fix" in table_def.keys():
                for n_rows in table_def["rows_to_fix"].keys():
                    print(f"Merge content for {n_rows=}")
                    df_this_table = fix_rows(
                        df_this_table,
                        rows_to_fix=table_def["rows_to_fix"][n_rows],
                        col_to_use=0,
                        n_rows=n_rows,
                    )

            # remove line breaks
            df_this_table = df_this_table.replace("\n", " ")

            # set column index
            df_this_table.columns = df_this_table.iloc[0]
            df_this_table = df_this_table.drop(0)

            # add unit
            if "unit" in table_def.keys():
                df_this_table["unit"] = table_def["unit"]

            # add entity
            if "entity" in table_def.keys():
                df_this_table["entity"] = table_def["entity"]

            # replace cat names by codes in col "category"
            # first the manual replacements
            cat_col = table_def["cat_col"]
            df_this_table[cat_col] = df_this_table[cat_col].replace(
                cat_codes_manual, regex=False
            )

            # then the regex replacements
            def repl(m):  # noqa: D103
                return m.group("code")

            df_this_table[cat_col] = df_this_table[cat_col].str.replace(
                cat_code_regexp, repl, regex=True
            )
            df_this_table = df_this_table.reset_index(drop=True)

            # fix thousands separators in numbers
            time_format = "%Y"
            time_columns = [
                col
                for col in df_this_table.columns.to_numpy()
                if matches_time_format(col, time_format)
            ]

            for col in time_columns:
                df_this_table.loc[:, col] = df_this_table.loc[:, col].str.replace(
                    ",", "", regex=False
                )
                df_this_table.loc[:, col] = df_this_table.loc[:, col].str.replace(
                    " ", "", regex=False
                )

            # rename category columns
            df_this_table = df_this_table.rename({f"{cat_col}": "category"}, axis=1)

            if "add_coords_defaults" in table_def.keys():
                coords_defaults_this_table = deepcopy(table_def["add_coords_defaults"])
                coords_defaults_this_table.update(coords_defaults)
                coords_cols_this_table = deepcopy(coords_cols)
                for coord in table_def["add_coords_defaults"].keys():
                    coords_cols_this_table.pop(coord)
            else:
                coords_defaults_this_table = coords_defaults
                coords_cols_this_table = coords_cols

            if "filter_remove" in table_def.keys():
                filter_remove_this_table = deepcopy(table_def["filter_remove"])
                filter_remove_this_table.update(filter_remove)
            else:
                filter_remove_this_table = filter_remove

            df_this_table_if = pm2.pm2io.convert_wide_dataframe_if(
                df_this_table,
                coords_cols=coords_cols_this_table,
                # add_coords_cols=add_coords_cols,
                coords_defaults=coords_defaults_this_table,
                coords_terminologies=coords_terminologies,
                coords_value_mapping=coords_value_mapping,
                # coords_value_filling=coords_value_filling,
                filter_remove=filter_remove_this_table,
                # filter_keep=filter_keep,
                meta_data=meta_data,
            )

            this_table_pm2 = pm2.pm2io.from_interchange_format(df_this_table_if)

            if data_pm2 is None:
                data_pm2 = this_table_pm2
            else:
                data_pm2 = data_pm2.pr.merge(this_table_pm2, tolerance=tolerance)

            print("done")

    # # ###
    # # process the tables and convert to PM2 IF
    # # part 2: 2024 tables
    # # ###
    # for table_name, table_def in table_defs_detail.items():
    #     print(f"Working on table: {table_name}")
    #
    #     # process all raw tables
    #     # individual tables as they all have headers
    #
    #     for table in table_def["tables"]:
    #         df_this_table = all_tables[table].copy(deep=True)
    #         indices_to_drop = []
    #
    #         # combine header rows
    #         if "rows_to_merge" in table_def.keys():
    #             df_this_table, new_indices_to_drop = (
    #                 merge_rows(df_this_table, table_def["rows_to_merge"]))
    #             indices_to_drop = indices_to_drop + list(new_indices_to_drop)
    #
    #
    #         # drop rows if necessary
    #         if "rows_to_drop" in table_def.keys():
    #             new_indices_to_drop
    #               = df_this_table.iloc[table_def["rows_to_drop"]].index
    #             indices_to_drop = indices_to_drop + list(new_indices_to_drop)
    #
    #         if indices_to_drop:
    #             df_this_table = df_this_table.drop(indices_to_drop)
    #
    #         # drop cols if necessary
    #         if "cols_to_drop" in table_def.keys():
    #             df_this_table = df_this_table.drop(table_def["cols_to_drop"], axis=1)
    #
    #         # fix content that spreads across multiple rows
    #         if "rows_to_fix" in table_def.keys():
    #             for n_rows in table_def["rows_to_fix"].keys():
    #                 print(f"Merge content for {n_rows=}")
    #                 df_this_table = fix_rows(
    #                     df_this_table,
    #                     rows_to_fix=table_def["rows_to_fix"][n_rows],
    #                     col_to_use=0,
    #                     n_rows=n_rows,
    #                 )
    #
    #         # remove line breaks
    #         df_this_table = df_this_table.replace("\n", " ")
    #
    #         # add units
    #         # add new header
    #         if "units" in table_def.keys():
    #             df_this_table = pd.concat([
    #                 pd.DataFrame([[""] + table_def["units"]],
    #                              columns=df_this_table.columns),
    #                 df_this_table]
    #             )
    #
    #         # set column index
    #         df_this_table.columns = [df_this_table.iloc[1],df_this_table.iloc[0]]
    #         df_this_table = df_this_table.drop([0,1])
    #
    #         # replace cat names by codes in col "category"
    #         # first the manual replacements
    #         cat_col = table_def["cat_col"]
    #         df_this_table[(cat_col, "")] = df_this_table[(cat_col, "")].replace(
    #             cat_codes_manual,
    #             regex=False
    #         )
    #
    #         # then the regex replacements
    #         def repl(m):
    #             return m.group("code")
    #
    #         df_this_table[cat_col] = df_this_table[cat_col].str.replace(
    #             cat_code_regexp_2024, repl, regex=True
    #         )
    #         df_this_table = df_this_table.reset_index(drop=True)
    #
    #         # rename category columns
    #         df_this_table = df_this_table.rename({f"{cat_col}": "category"}, axis=1)
    #
    #         # fix thousands separators in numbers
    #         entity_columns = [
    #             col
    #             for col in df_this_table.columns
    #             if col != ("category", "")
    #         ]
    #
    #         for col in entity_columns:
    #             df_this_table.loc[:, col] = df_this_table.loc[:, col].str.replace(
    #                 ",", "", regex=False
    #             )
    #             df_this_table.loc[:, col] = df_this_table.loc[:, col].str.replace(
    #                 " ", "", regex=False
    #             )
    #
    #         # TODO: the following fail sbecause of an index problem
    #         # set index and convert to long format
    #         df_this_table = df_this_table.set_index("category")
    #         # df_this_table_long = pm2.pm2io.nir_convert_df_to_long(
    #         #     df_this_table, table_def["time"], header_long
    #         # )
    #
    #         df_this_table_long = (
    #             df_this_table.stack([0, 1], future_stack=True).to_frame())
    #         df_this_table_long.insert(0, "year", table_def["time"])
    #         df_this_table_long = df_this_table_long.reset_index()
    #         df_this_table_long.columns = header_long
    #
    #
    #         if "add_coords_defaults" in table_def.keys():
    #             coords_defaults_this_table
    #               = deepcopy(table_def["add_coords_defaults"])
    #             coords_defaults_this_table.update(coords_defaults)
    #             coords_cols_this_table = deepcopy(coords_cols)
    #             for coord in table_def["add_coords_defaults"].keys():
    #                 coords_cols_this_table.pop(coord)
    #         else:
    #             coords_defaults_this_table = coords_defaults
    #             coords_cols_this_table = coords_cols
    #
    #         if "filter_remove" in table_def.keys():
    #             filter_remove_this_table = deepcopy(table_def["filter_remove"])
    #             filter_remove_this_table.update(filter_remove)
    #         else:
    #             filter_remove_this_table = filter_remove
    #
    #         df_this_table_if = pm2.pm2io.convert_long_dataframe_if(
    #             df_this_table,
    #             coords_cols=coords_cols_this_table,
    #             # add_coords_cols=add_coords_cols,
    #             coords_defaults=coords_defaults_this_table,
    #             coords_terminologies=coords_terminologies,
    #             coords_value_mapping=coords_value_mapping,
    #             # coords_value_filling=coords_value_filling,
    #             filter_remove=filter_remove_this_table,
    #             # filter_keep=filter_keep,
    #             meta_data=meta_data,
    #         )
    #
    #         this_table_pm2 = pm2.pm2io.from_interchange_format(df_this_table_if)
    #
    #         if data_pm2 is None:
    #             data_pm2 = this_table_pm2
    #         else:
    #             data_pm2 = data_pm2.pr.merge(this_table_pm2, tolerance=tolerance)
    #
    #         print("done")

    # convert back to interchange format for saving
    data_if = data_pm2.pr.to_interchange_format()

    # ###
    # save raw data to IF and native format
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
        / (output_filename + coords_terminologies["category"] + "_raw.nc"),
        encoding=encoding,
    )

    # ###
    # ## process the data
    # ###
    data_proc_pm2 = data_pm2

    # actual processing
    data_proc_pm2 = process_data_for_country(
        data_proc_pm2,
        entities_to_ignore=[],
        gas_baskets=gas_baskets,
        processing_info_country=country_processing_step1,
        category_conversion=cat_conversion,
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
