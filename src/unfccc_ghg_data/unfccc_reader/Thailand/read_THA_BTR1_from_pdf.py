"""
Read Thailand's BTR1 from pdf

This script reads data from Thailand's BTR1
Data is partly read directly from pdf and partly from data manually entered
in the config file and paths from the plots for additional data points that
were obtained using inkscape.

GHG precursors have mostly been omitted to save time and focus on gases relevant
for PRIMAP-hist.

"""

import camelot
import numpy as np
import pandas as pd
import primap2 as pm2
from primap2.pm2io import (
    convert_long_dataframe_if,
    convert_wide_dataframe_if,
    nir_add_unit_information,
    nir_convert_df_to_long,
)
from primap2.pm2io._data_reading import matches_time_format

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    fix_rows,
    gas_baskets,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.Thailand.config_tha_btr1 import (
    LULUCF_graph_data,
    cat_code_regexp,
    cat_codes_manual,
    cat_conversion,
    coords_cols,
    coords_defaults,
    coords_terminologies,
    country_processing_step1,
    country_processing_step2,
    graph_data,
    gwp_to_use,
    header_long,
    meta_data,
    page_defs_inventory,
    page_defs_trends,
    path_to_values,
    path_to_values_bargraph,
    terminology_proc,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = downloaded_data_path / "UNFCCC" / "Thailand" / "BTR1"
    output_folder = extracted_data_path / "UNFCCC" / "Thailand"
    if not output_folder.exists():
        output_folder.mkdir()

    inventory_file = "THAILAND%E2%80%99S_BTR1.pdf"
    output_filename = "THA_BTR1_2024_"

    compression = dict(zlib=True, complevel=9)

    # ###
    # Read inventories from pdf
    # ###
    def repl(m):  # noqa: D103
        return m.group("code")

    data_inventory_pm2 = None

    for page in page_defs_inventory:
        print(f"Reading from page: {page}")
        table_def = page_defs_inventory[page]
        if "columns" in table_def:
            tables_current_inv_table = camelot.read_pdf(
                str(input_folder / inventory_file),
                pages=page,
                table_areas=table_def["table_areas"],
                split_text=table_def["split_text"],
                flavor=table_def["flavor"],
                columns=table_def["columns"],
            )
        else:
            tables_current_inv_table = camelot.read_pdf(
                str(input_folder / inventory_file),
                pages=page,
                table_areas=table_def["table_areas"],
                split_text=table_def["split_text"],
                flavor=table_def["flavor"],
            )

        df_current_inv_table = tables_current_inv_table[0].df

        if "drop_rows" in table_def:
            df_current_inv_table = df_current_inv_table.drop(table_def["drop_rows"])

        # fix rows
        if "rows_to_fix" in table_def:
            for n_rows in table_def["rows_to_fix"].keys():
                print(f"Fixing split rows: {n_rows}")
                df_current_inv_table = fix_rows(
                    df_current_inv_table, table_def["rows_to_fix"][n_rows], 0, n_rows
                )
            df_current_inv_table = df_current_inv_table.reset_index(drop=True)

        # fill unit:
        if table_def["unit_info"]["unit_row"] != table_def["unit_info"]["entity_row"]:
            df_current_inv_table.loc[
                table_def["unit_info"]["unit_row"]
            ] = df_current_inv_table.loc[table_def["unit_info"]["unit_row"]].replace(
                "", np.nan
            )
            df_current_inv_table.loc[table_def["unit_info"]["unit_row"]] = (
                df_current_inv_table.loc[table_def["unit_info"]["unit_row"]]
                .ffill()
                .bfill()
            )

        # fill entity:
        df_current_inv_table.loc[
            table_def["unit_info"]["entity_row"]
        ] = df_current_inv_table.loc[table_def["unit_info"]["entity_row"]].replace(
            "", np.nan
        )
        df_current_inv_table.loc[table_def["unit_info"]["entity_row"]] = (
            df_current_inv_table.loc[table_def["unit_info"]["entity_row"]]
            .bfill()
            .ffill()
        )

        df_current_inv_table = nir_add_unit_information(
            df_current_inv_table, **table_def["unit_info"]
        )

        df_current_inv_table = df_current_inv_table.set_index(
            df_current_inv_table.columns[0]
        )

        df_current_inv_table_long = nir_convert_df_to_long(
            df_current_inv_table,
            year=table_def["year"],
            header_long=header_long,
        )

        # remove ',', '\n'
        df_current_inv_table_long.loc[:, "data"] = df_current_inv_table_long.loc[
            :, "data"
        ].str.replace(",", "", regex=False)
        df_current_inv_table_long.loc[:, "data"] = df_current_inv_table_long.loc[
            :, "data"
        ].str.replace("\n", "", regex=False)
        df_current_inv_table_long.loc[:, "data"] = df_current_inv_table_long.loc[
            :, "data"
        ].str.strip()
        df_current_inv_table_long.loc[:, "data"] = df_current_inv_table_long.loc[
            :, "data"
        ].str.replace("/", ",", regex=False)

        # replace cat names by codes in col "category"
        # first the manual replacements
        df_current_inv_table_long["category"] = df_current_inv_table_long[
            "category"
        ].replace(cat_codes_manual)

        # then the regex replacements
        df_current_inv_table_long["category"] = df_current_inv_table_long[
            "category"
        ].str.replace(cat_code_regexp, repl, regex=True)
        df_current_inv_table_long = df_current_inv_table_long.reset_index(drop=True)

        # ready for conversion to IF

        if "filter_remove" in table_def:
            filter_remove = table_def["filter_remove"]
        else:
            filter_remove = None
        current_inv_table_if = convert_long_dataframe_if(
            df_current_inv_table_long,
            coords_cols=coords_cols,
            # add_coords_cols=add_coords_cols,
            coords_defaults=coords_defaults,
            coords_terminologies=coords_terminologies,
            coords_value_mapping=table_def["coords_value_mapping"],
            # coords_value_filling=coords_value_filling,
            filter_remove=filter_remove,
            # filter_keep=filter_keep,
            meta_data=meta_data,
            convert_str=True,
            time_format="%Y",
        )

        current_inv_table_pm2 = pm2.pm2io.from_interchange_format(current_inv_table_if)
        if data_inventory_pm2 is None:
            data_inventory_pm2 = current_inv_table_pm2
        else:
            data_inventory_pm2 = data_inventory_pm2.merge(current_inv_table_pm2)

    # ###
    # Read time series from pdf
    # ###
    data_time_series_pm2 = None

    for page in page_defs_trends:
        print(f"Reading from page: {page}")
        table_def = page_defs_trends[page]
        tables_current_trend_table = camelot.read_pdf(
            str(input_folder / inventory_file),
            pages=page,
            table_areas=table_def["table_areas"],
            split_text=table_def["split_text"],
            flavor=table_def["flavor"],
        )

        df_current_trend_table = tables_current_trend_table[0].df

        if "drop_rows" in table_def:
            df_current_trend_table = df_current_trend_table.drop(table_def["drop_rows"])

        # fix rows
        if "rows_to_fix" in table_def:
            for n_rows in table_def["rows_to_fix"].keys():
                print(f"Fixing split rows: {n_rows}")
                df_current_trend_table = fix_rows(
                    df_current_trend_table, table_def["rows_to_fix"][n_rows], 0, n_rows
                )
            df_current_trend_table = df_current_trend_table.reset_index(drop=True)

        # fill unit:
        if table_def["unit_info"]["unit_row"] != table_def["unit_info"]["entity_row"]:
            # df_current_trend_table.loc[table_def["unit_info"]["unit_row"], 0] = "unit"
            df_current_trend_table.loc[
                table_def["unit_info"]["unit_row"]
            ] = df_current_trend_table.loc[table_def["unit_info"]["unit_row"]].replace(
                "", np.nan
            )
            df_current_trend_table.loc[table_def["unit_info"]["unit_row"]] = (
                df_current_trend_table.loc[table_def["unit_info"]["unit_row"]]
                .bfill()
                .ffill()
            )

        df_current_trend_table = nir_add_unit_information(
            df_current_trend_table, **table_def["unit_info"]
        )

        # transpose to wide format
        df_current_trend_table = df_current_trend_table.transpose()
        df_current_trend_table = df_current_trend_table.reset_index(drop=False)

        # rename columns
        df_current_trend_table.loc[0, "level_1"] = "unit"
        df_current_trend_table.loc[0, "level_0"] = "category"

        # set col index
        df_current_trend_table.columns = df_current_trend_table.iloc[0]
        df_current_trend_table = df_current_trend_table.drop(0)

        # if necessary copy the category column and rename for later mapping
        if "entity" not in table_def:
            df_current_trend_table["entity"] = df_current_trend_table["category"]
            if "category" in table_def:
                # if cat is fixed drop category column
                df_current_trend_table = df_current_trend_table.drop(
                    columns=["category"]
                )

        # remove ','
        time_format = "%Y"
        time_columns = [
            col
            for col in df_current_trend_table.columns.to_numpy()
            if matches_time_format(col, time_format)
        ]

        for col in time_columns:
            df_current_trend_table.loc[:, col] = df_current_trend_table.loc[
                :, col
            ].str.replace(",", "", regex=False)

        # ready for conversion to IF
        # update configuration
        coords_cols_current = coords_cols.copy()
        coords_defaults_current = coords_defaults.copy()
        if "entity" in table_def:
            coords_cols_current.pop("entity")
            coords_defaults_current["entity"] = table_def["entity"]
        elif "category" in table_def:
            coords_cols_current.pop("category")
            coords_defaults_current["category"] = table_def["category"]

        if "filter_remove" in table_def:
            filter_remove = table_def["filter_remove"]
        else:
            filter_remove = None
        current_trend_table_if = convert_wide_dataframe_if(
            df_current_trend_table,
            coords_cols=coords_cols_current,
            coords_defaults=coords_defaults_current,
            coords_terminologies=coords_terminologies,
            coords_value_mapping=table_def["coords_value_mapping"],
            filter_remove=filter_remove,
            meta_data=meta_data,
            convert_str=True,
            time_format="%Y",
        )

        current_trend_table_pm2 = pm2.pm2io.from_interchange_format(
            current_trend_table_if
        )

        if data_time_series_pm2 is None:
            data_time_series_pm2 = current_trend_table_pm2
        else:
            data_time_series_pm2 = data_time_series_pm2.pr.merge(
                current_trend_table_pm2
            )

    # ###
    # Read data from small tables and plots from the config and process it
    # ###
    default_tolerance = (
        0.01  # 1% deviation of individual scaling factors from mean is allowed
    )

    time_format = "%Y"
    df_all = None
    for category in graph_data:
        cat_data = graph_data[category]
        if "tolerance" in cat_data:
            tolerance = cat_data["tolerance"]
        else:
            tolerance = default_tolerance
        # build dataframe with data read from table
        df_known = pd.DataFrame(cat_data["known_data"])
        df_known.columns = df_known.iloc[0]
        df_known = df_known.drop([0])
        time_columns = [
            col
            for col in df_known.columns.to_numpy()
            if matches_time_format(str(col), time_format)
        ]
        year_cols_plot = [str(year) for year in cat_data["years"]]

        df_result = df_known.copy()
        cols_to_add = [col for col in year_cols_plot if col not in time_columns]
        cols_to_add.reverse()
        for col in cols_to_add:
            df_result.insert(loc=2, column=col, value=np.nan)
        df_result = df_result.set_index("entity")

        # extend dataframe with information from path objects of the plots
        for entity in cat_data["paths"]:
            # get existing data from df_known
            if entity in df_known["entity"].to_numpy():
                entity_df = entity
            else:
                entity_df = f"{entity} ({gwp_to_use})"

            # get the values from the plot
            if isinstance(cat_data["zero"], dict):
                zero = cat_data["zero"][entity]
            elif isinstance(cat_data["zero"], str):
                zero = cat_data["zero"]
            else:
                raise TypeError(  # noqa: TRY003
                    f"Unknown data type for zero value: {cat_data['zero']}"
                )
            values = path_to_values(cat_data["paths"][entity], zero)
            # print(f"{category}, {entity}, {values}, {year_cols_plot}")
            df_plot = pd.DataFrame([values], columns=year_cols_plot)

            # transform the plot values to fit the known data
            overlap_time_cols = [col for col in time_columns if col in year_cols_plot]
            df_plot_overlap = df_plot[overlap_time_cols]
            df_known_overlap = df_known[df_known["entity"] == entity_df][
                overlap_time_cols
            ]
            df_factor = df_known_overlap.reset_index(
                drop=True
            ) / df_plot_overlap.reset_index(drop=True)
            factor = df_factor.iloc[0].mean()
            df_factor_var = abs(df_factor / factor - 1)
            if df_factor_var.iloc[0].ge(tolerance).any():
                raise ValueError(  # noqa: TRY003
                    f"Scaling factors for {category}, {entity}: "
                    f"vary too much: {df_factor}, {df_factor_var}"
                )
            df_plot = df_plot * factor
            df_plot.insert(loc=0, column="entity", value=entity_df)
            df_plot.insert(
                loc=1,
                column="unit",
                value=df_known[df_known["entity"] == entity_df]["unit"].to_numpy()[0],
            )
            df_plot = df_plot.set_index("entity")
            # merge the dataframes
            df_result = df_result.combine_first(df_plot)

        df_result.insert(loc=0, column="category", value=category)

        if df_all is None:
            df_all = df_result
        else:
            df_all = pd.concat([df_all, df_result])

    df_all = df_all.reset_index(drop=False)

    # ###
    # convert to PRIMAP2 interchange format
    # ###
    data_plots_if = pm2.pm2io.convert_wide_dataframe_if(
        df_all,
        coords_cols=coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )

    data_plots_pm2 = pm2.pm2io.from_interchange_format(data_plots_if)

    # ###
    # Read data from small tables and plots from the config and process it - LULUCF
    # ###

    default_tolerance = (
        0.01  # 1% deviation of individual scaling factors from mean is allowed
    )

    time_format = "%Y"
    df_all = None
    for category in LULUCF_graph_data:
        cat_data = LULUCF_graph_data[category]
        if "tolerance" in cat_data:
            tolerance = cat_data["tolerance"]
        else:
            tolerance = default_tolerance
        # build dataframe with data read from table
        df_known = pd.DataFrame(cat_data["known_data"])
        df_known.columns = df_known.iloc[0]
        df_known = df_known.drop([0])
        time_columns = [
            col
            for col in df_known.columns.to_numpy()
            if matches_time_format(str(col), time_format)
        ]
        year_cols_plot = [str(year) for year in cat_data["years"]]

        df_result = df_known.copy()
        cols_to_add = [col for col in year_cols_plot if col not in time_columns]
        cols_to_add.reverse()
        for col in cols_to_add:
            df_result.insert(loc=2, column=col, value=np.nan)
        df_result = df_result.set_index("entity")

        # extend dataframe with information from path objects of the plots
        for entity in cat_data["paths"]:
            # get existing data from df_known
            if entity in df_known["entity"].to_numpy():
                entity_df = entity
            else:
                entity_df = f"{entity} ({gwp_to_use})"

            # get the values from the plot
            values = path_to_values_bargraph(cat_data["paths"][entity])
            # print(f"{category}, {entity}, {values}, {year_cols_plot}")
            df_plot = pd.DataFrame([values], columns=year_cols_plot)

            # transform the plot values to fit the known data
            overlap_time_cols = [col for col in time_columns if col in year_cols_plot]
            df_plot_overlap = df_plot[overlap_time_cols]
            df_known_overlap = df_known[df_known["entity"] == entity_df][
                overlap_time_cols
            ]
            df_factor = df_known_overlap.reset_index(
                drop=True
            ) / df_plot_overlap.reset_index(drop=True)
            factor = df_factor.iloc[0].mean()
            df_factor_var = abs(df_factor / factor - 1)
            if df_factor_var.iloc[0].ge(tolerance).any():
                raise ValueError(  # noqa: TRY003
                    f"Scaling factors for {category}, {entity}: "
                    f"vary too much: {df_factor}, {df_factor_var}"
                )
            df_plot = df_plot * factor
            df_plot.insert(loc=0, column="entity", value=entity_df)
            df_plot.insert(
                loc=1,
                column="unit",
                value=df_known[df_known["entity"] == entity_df]["unit"].to_numpy()[0],
            )
            df_plot = df_plot.set_index("entity")
            # merge the dataframes
            df_result = df_result.combine_first(df_plot)

        df_result.insert(loc=0, column="category", value=category)

        if df_all is None:
            df_all = df_result
        else:
            df_all = pd.concat([df_all, df_result])

    df_all = df_all.reset_index(drop=False)

    # ###
    # convert to PRIMAP2 interchange format
    # ###
    data_LULUCF_if = pm2.pm2io.convert_wide_dataframe_if(
        df_all,
        coords_cols=coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )

    data_LULUCF_pm2 = pm2.pm2io.from_interchange_format(data_LULUCF_if)

    # ###
    # merge the four datasets
    # ###

    data_all_pm2 = data_inventory_pm2.pr.merge(data_time_series_pm2)
    data_all_pm2 = data_all_pm2.pr.merge(data_plots_pm2)
    data_all_pm2 = data_all_pm2.pr.merge(data_LULUCF_pm2)

    data_all_if = data_all_pm2.pr.to_interchange_format()

    # ###
    # save raw data to IF and native format
    # ###
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"] + "_raw"),
        data_all_if,
    )

    encoding = {var: compression for var in data_all_pm2.data_vars}
    data_all_pm2.pr.to_netcdf(
        output_folder
        / (output_filename + coords_terminologies["category"] + "_raw.nc"),
        encoding=encoding,
    )

    # ###
    # ## process the data
    # ###
    data_proc_pm2 = data_all_pm2

    # combine CO2 emissions and removals
    data_temp_CO2 = data_proc_pm2[["CO2 emissions", "CO2 removals"]].pr.sum(
        dim="entity", skipna=True, min_count=1
    )
    data_proc_pm2["CO2"] = data_proc_pm2["CO2"].fillna(data_temp_CO2)
    # data_proc_pm2["CO2"].attrs["entity"] = "CO2"

    # actual processing
    data_proc_pm2 = process_data_for_country(
        data_proc_pm2,
        entities_to_ignore=["CO2 emissions", "CO2 removals", f"PFCS ({gwp_to_use})"],
        gas_baskets={},  # gas_baskets,
        processing_info_country=country_processing_step1,
    )

    data_proc_pm2 = process_data_for_country(
        data_proc_pm2,
        entities_to_ignore=[],
        gas_baskets=gas_baskets,
        processing_info_country=country_processing_step2,
        cat_terminology_out=terminology_proc,
        category_conversion=cat_conversion,
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
        output_folder / (output_filename + terminology_proc), data_proc_if
    )

    encoding = {var: compression for var in data_proc_pm2.data_vars}
    data_proc_pm2.pr.to_netcdf(
        output_folder / (output_filename + terminology_proc + ".nc"), encoding=encoding
    )
