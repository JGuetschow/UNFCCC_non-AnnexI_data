"""
Read Democratic Republic of the Congo's BUR1 from pdf

This script reads data from Democratic Republic of the Congo,'s BUR1
Data are read from pdf using camelot

"""

from copy import deepcopy

import camelot
import pandas as pd
import primap2 as pm2
import primap2.pm2io
from primap2.pm2io._data_reading import matches_time_format

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
)
from unfccc_ghg_data.unfccc_reader.Democratic_Republic_of_the_Congo.config_cod_bur1 import (  # noqa: E501
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    filter_remove,
    meta_data,
    page_defs,
    table_defs,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = (
        downloaded_data_path / "UNFCCC" / "Democratic_Republic_of_the_Congo" / "BUR1"
    )
    output_folder = extracted_data_path / "UNFCCC" / "Democratic_Republic_of_the_Congo"
    if not output_folder.exists():
        output_folder.mkdir()

    inventory_file = "RDC_NIR_Final.pdf"
    output_filename = "COD_BUR1_2024_"

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
            **page_def,
        )
        for table in new_tables:
            all_tables.append(table.df)

    # ###
    # process the tables and convert to PM2 IF
    # ###
    data_pm2 = None
    for table_name, table_def in table_defs.items():
        print(f"Working on table: {table_name}")

        # process all raw tables
        # individual tables as they all have headers

        for table in table_def["tables"]:
            df_this_table = all_tables[table].copy(deep=True)

            # set category label
            if "category_cell" in table_def.keys():
                df_this_table.iloc[
                    table_def["category_cell"][0], table_def["category_cell"][1]
                ] = "category"

            # drop rows if necessary
            if "drop_rows" in table_def.keys():
                index_to_drop = df_this_table.iloc[table_def["drop_rows"]].index
                df_this_table = df_this_table.drop(index_to_drop)

            # remove line breaks
            df_this_table = df_this_table.replace("\n", " ")

            # add new header
            if "header" in table_def.keys():
                df_this_table = pd.concat(
                    [pd.DataFrame(table_def["header"]), df_this_table]
                )

            # transpose
            df_this_table = df_this_table.transpose()
            df_this_table = df_this_table.reset_index(drop=True)

            # set column index
            df_this_table.columns = df_this_table.iloc[0]
            # idx_to_drop = df_this_table.iloc[0].index
            df_this_table = df_this_table.drop(0)

            # add unit
            if "unit" in table_def.keys():
                df_this_table["unit"] = table_def["unit"]

            # replace cat names by codes in col "category"
            if "cat_codes_mapping" in table_def:
                df_this_table["category"] = df_this_table["category"].replace(
                    table_def["cat_codes_mapping"]
                )
                # the

            # fix spaces in numbers
            time_format = "%Y"
            time_columns = [
                col
                for col in df_this_table.columns.to_numpy()
                if matches_time_format(col, time_format)
            ]

            for col in time_columns:
                df_this_table.loc[:, col] = df_this_table.loc[:, col].str.replace(
                    " ", "", regex=False
                )
                df_this_table.loc[:, col] = df_this_table.loc[:, col].str.replace(
                    ",", ".", regex=False
                )

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
                data_pm2 = data_pm2.pr.merge(this_table_pm2)

            print("done")

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

    ### TODO processing ###
    # The data is very inconsistent we have to deal with theis before processing
