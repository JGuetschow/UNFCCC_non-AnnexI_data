"""
Read Democratic Republic of the Congo's BUR1 from pdf

This script reads data from Democratic Republic of the Congo,'s BUR1
Data are read from pdf using camelot.

Data in the different tables are highly inconsistent. We mostly use the main
overview tables as the reference. For LULUCF data we make an exception, because the
data in the main tables only includes emissions and removals from forestry (and
cropland, though the data from cropland are also reported as emissions from forests
in some tables.).

GWP values are not consistent between the tables and in case ot table 29 even within
the table. Table 5 uses AR5 GWPs, Table 16 uses AR4 GWPS, Table 29 uses AR4 GWPs for
livestock CH4 and SAR GWPs for livestock N2O. Table 30 probably uses SAR GWPs for CH4
and AR5 GWPs for N2O (as the data are inconsistent with other tables it is not
completely clear)

We use table 3 and 5 for the main sectors with the exception of 3.C from table 3
and M.AGG from table 5 as the data do not contain emissions from biomass burning.
LULUCF data from both tables only contain forestry data so we don't use the data from
tables 3 and 5. We use table 16 for energy sector data.
Table 27 is our main source for detailed AFOLU data.
Table 29 has inconsistencies for N2O from livestock for a few years. The 3.C.x data
are the sum of 3.C x 1000 and other 3.C subsectors, so they are not usable at all.
Table 30 is not consistent with any other tables for CH4 but consistent for N2O.
Table 31 is consistent with table 27 for 3.A.1  except for 2017 and 2018 and
inconsistent for 3.A.2.
Table 32 is used for enteric fermentation details and consistent with Table 27.
Table 33 contains details for CH4 from manure management but is not consistent with
table 27.
Table 34 contains details for N2O from manure management but is inconsistent with table
27 for 2017 and 2018.
Table 39 is used for biomass buning details and consistent with other tables after
correcting the unit to tonnes.
Table 40 is consistent with other tables for most sectors except indirect emissions
from manure management and N2O total emissions.

We read the inconsistent data into custom categories M.XXX.TYY where XXX is the proper
sector code and YY is the table number. The data are available in the raw data.

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
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.Democratic_Republic_of_the_Congo.config_cod_bur1 import (  # noqa: E501
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    country_processing_step1,
    filter_remove,
    gas_baskets,
    meta_data,
    page_defs,
    sectors_proc,
    table_defs,
    tolerance,
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
                data_pm2 = data_pm2.pr.merge(this_table_pm2, tolerance=tolerance)

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

    # ###
    # ## process the data
    # ###
    data_proc_pm2 = data_pm2

    # actual processing
    data_proc_pm2 = process_data_for_country(
        data_proc_pm2,
        entities_to_ignore=["CO2 emissions", "CO2 removals"],
        gas_baskets=gas_baskets,
        processing_info_country=country_processing_step1,
        sectors_out=sectors_proc,
    )

    # adapt source and metadata
    # TODO: processing info is present twice
    current_source = data_proc_pm2.coords["source"].to_numpy()[0]
    data_temp = data_proc_pm2.pr.loc[{"source": current_source}]
    data_proc_pm2 = data_proc_pm2.pr.set("source", "BUR_NIR", data_temp)

    # ###
    # save data to IF and native format
    # ###
    data_proc_if = data_proc_pm2.pr.to_interchange_format()
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"]),
        data_proc_if,
    )

    encoding = {var: compression for var in data_proc_pm2.data_vars}
    data_proc_pm2.pr.to_netcdf(
        output_folder / (output_filename + coords_terminologies["category"] + ".nc"),
        encoding=encoding,
    )
