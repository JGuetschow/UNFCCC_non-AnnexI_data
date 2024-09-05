"""
Read Uzbekistans's BTR1 inventory from pdf

Most tables are read, but not all.
Some tables are ignored due to inconsistencies (precursors)

"""
import camelot
import numpy as np
import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    fix_rows,
    make_long_table,
    set_to_nan_in_ds,
)
from unfccc_ghg_data.unfccc_reader.Uzbekistan.config_uzb_btr1 import (
    cat_code_regexp,
    config_general,
    page_def_inventory,
    page_def_trends,
    table_def_inventory,
    table_def_trends,
)

# NIR tables for 1990, 2010, 2021 on page 187-208
# trend tables:
# precursors not listed, but also available
# mot all detail tables listed
# [X] Total for main gases: 21
# [X] KyotoGHG for main sectors: 23
# [X] gases for energy sector totals: 29
# [X] Kyotoghg for energy sector main subsectors: 30
# [X] Bunkers, gases: 36
# [X] 1.A gases: 38
# [X] KyotoGHG for main sectors: 40, 41
# [X] CO2 for 1.A.X sectors: 42
# [X] CH4 for 1.A.X sectors: 43,44
# [X] N2O for 1.A.X sectors: 44, 45
# [] KyotoGHG 1.A.3 subsectors: 51
# [X] 1.B gases: 55
# [X] 1.B.x KyotoGHG: 56
# [x] CH4 from coal mining: 58, 59 (check if that covers 1.B.1)
# [x] gases from oil (1.B.2.a?): 61
# [X] KyotoGHG for oil subsectors: 62
# [X] gases from oil production: 63
# [] KyotoGHG oil production subsectors: 64
# [X] gases from oil transportation: 66, 67
# [x] gases for natural gas: 69
# [x] precursors for natural gas: 69
# [] KyotoGHG for natural gas subsectors
# [X] IPPU gases: 76
# [X] IPPU precursors: 76
# [X] KyotoGHG IPPU subsectors: 78
# [x] CO2 2.A: 81
# [X] CO2, SO2 in 2.A.1
# [] Skip the other 2.A.x tables as contained in table on page 81
# [X] 2.B gases: 92, 93
# [] KyotoGHG 2.B.x: 94
# [] Detail tables for individual chemicals (95, 98, 101, 103, 105)
# [X] 2.C gases: 107
# [] Metal industry detail tables (108, 109, 111, 112, 113)
# [X] 2.D.1 CO2: 115 (other sectors NE)
# [X] 2.F gases: 116
# [X] 2.H NMVOC only
##########################
# [X] M.AG, gases: 123
# [X] KyotoGHG M.AG subcategories: 124
# [X] CH4 3.A.1.x : 127
# [] manure management gases: 131 (not needed)
# [X] 3.A.2.x, CH4: 132
# [X] direct + indirect N2O manure management: 133, 134
# [X] direct N2O mm, subsectors: 134, 135
# [X] crop residues burning gases: 137 (all other burning NO)
# [] Liming: NO, Urea: NO, but text reads like NE
# [X] N2O from soils: 140
# [X] CH4 from rice: 144
# [X] KyotoGHG Land+subsectors: 148 (CO2 only)
# [] CO2 removals in Forest land remaining forest land (fires included): 151
# [X] gases for forest fires (read for non-CO2): 152
# [] CO2 from cropland remaining cropland: 158
# [] CO2 from grassland remaining grassland: 163
# [X] Waste by gas: 166
# [X] Waste by sector: 167
# [X] CH4 from solid waste: 169
# [X] Wastewater CH4, N2O: 176
# [X] Wastewater KyotoGHG for subsectors: 177
# [X] Domestic wastewater, gases: 179
# [X] Industrial wastewater CH$: 183
# []
# []


if __name__ == "__main__":
    pd.set_option("future.no_silent_downcasting", True)

    # ###
    # configuration
    # ###

    # folders and files
    input_folder = downloaded_data_path / "UNFCCC" / "Uzbekistan" / "BTR1"
    output_folder = extracted_data_path / "UNFCCC" / "Uzbekistan"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "UZB_BTR1NIR_"

    inventory_file = "NIR_Uzb_eng_26_06_2024_%D1%84%D0%B8%D0%BD%D0%B0%D0%BB.pdf"

    compression = dict(zlib=True, complevel=9)

    # ###
    # start data reading
    # ###

    exceptions = {}
    # trend tables
    data_trend = None
    tables_to_read = table_def_trends.keys()
    # tables_to_read = ["bunkers_gases"]

    for table in tables_to_read:
        print(f"Reading {table}")
        table_def_current = table_def_trends[table].copy()
        data_table = None
        for page in table_def_current["tables"]:
            # prep parameters
            if "rows_to_fix" in table_def_current:
                rows_to_fix = table_def_current["rows_to_fix"]
            else:
                rows_to_fix = {}
            # read the page
            tables_read = camelot.read_pdf(
                str(input_folder / inventory_file), pages=page, **page_def_trends[page]
            )
            table_df = tables_read[table_def_current["tables"][page]].df

            # fill empty strings in rows
            if "ffill_rows" in table_def_current.keys():
                for row in table_def_current["ffill_rows"]:
                    table_df.iloc[row] = (
                        table_df.iloc[row].replace(r"^\s*$", np.nan, regex=True).ffill()
                    )

            # fix split rows
            if rows_to_fix:
                for n_rows in rows_to_fix.keys():
                    table_df = fix_rows(table_df, rows_to_fix[n_rows], 0, n_rows)

            # remove additional header rows
            if "header_remove" in table_def_current.keys():
                idx_to_drop = table_df.index[table_def_current["header_remove"]]
                table_df = table_df.drop(idx_to_drop)

            # remove unwanted characters in header
            table_df.iloc[0] = table_df.iloc[0].str.replace("\n", " ")
            table_df.iloc[0] = table_df.iloc[0].str.replace("  ", " ")
            table_df.iloc[0] = table_df.iloc[0].str.strip()

            # stack table if necessary
            if "split_kw" in table_def_current:
                split_kw = table_def_current["split_kw"]
                if isinstance(split_kw, list):
                    for kw in split_kw[1:]:
                        table_df.iloc[0] = table_df.iloc[0].str.replace(kw, split_kw[0])
                    long_kw = split_kw[0]
                else:
                    long_kw = split_kw
                table_df = make_long_table(table_df, keyword=long_kw)

            else:
                long_kw = table_def_current["long_kw"]
                table_df.columns = table_df.iloc[0]
                idx_to_drop = table_df.index[0]
                table_df = table_df.drop(idx_to_drop)

            # remove unwanted characters in first column
            table_df[long_kw] = table_df[long_kw].str.replace("м", "")
            table_df[long_kw] = table_df[long_kw].str.replace("\n", " ")
            table_df[long_kw] = table_df[long_kw].str.replace("  ", " ")

            # stack header variable
            table_df.index = table_df[long_kw]
            table_df = table_df.drop(columns=[long_kw])
            table_df.columns.name = table_def_current["header"]
            table_long = table_df.stack()  # noqa: PD013
            table_long.name = "data"
            table_long = table_long.reset_index()
            table_long = table_long.rename(
                columns={long_kw: table_def_current["long_var"]}
            )

            # replace str in data
            if "replace_str_data" in table_def_current.keys():
                for str_to_replace in table_def_current["replace_str_data"].keys():
                    table_long["data"] = table_long["data"].str.replace(
                        str_to_replace,
                        table_def_current["replace_str_data"][str_to_replace],
                    )

            # prepare parameters for conversion to PRIMAP2 IF
            coords_defaults = config_general["coords_defaults"].copy()
            coords_defaults.update(table_def_current["coords_defaults"])

            data_if = pm2.pm2io.convert_long_dataframe_if(
                table_long,
                coords_cols=table_def_current["coords_cols"],
                coords_defaults=coords_defaults,
                coords_terminologies=config_general["coords_terminologies"],
                coords_value_mapping=table_def_current["coords_value_mapping"],
                filter_remove=table_def_current["filter_remove"],
                meta_data=config_general["meta_data"],
                time_format=config_general["time_format"],
            )
            data_pm2 = pm2.pm2io.from_interchange_format(data_if)
            if data_table is None:
                data_table = data_pm2
            else:
                data_table = data_table.pr.merge(data_pm2)

        if "remove_vals" in table_def_current:
            for case in table_def_current["remove_vals"]:
                data_table = set_to_nan_in_ds(
                    data_table, **table_def_current["remove_vals"][case]
                )

        if data_trend is None:
            data_trend = data_table
        else:
            data_trend = data_trend.pr.merge(data_table)

    # inventories for 1990, 2010, 2021
    data_inv = None
    tables_to_read = table_def_inventory.keys()

    def repl(m):  # noqa: D103
        return m.group("code")

    for table in tables_to_read:
        print(f"Reading {table}")
        table_def_current = table_def_inventory[table].copy()
        data_table = None
        for page in table_def_current["tables"]:
            table_number = table_def_current["tables"][page]
            print(f"page {page}, {table_number}")
            # prep
            if "manual_repl_unit" in table_def_current:
                manual_repl_unit = table_def_current["manual_repl_unit"]
            else:
                manual_repl_unit = None

            if "unit" in table_def_current.keys():
                default_unit = table_def_current["unit"]
            else:
                default_unit = "Gg"

            page_def = page_def_inventory[page].copy()
            if "table_config" in page_def.keys():
                table_config = page_def.pop("table_config")[table_number]
            else:
                table_config = {}

            if "rows_to_fix" in table_config:
                rows_to_fix = table_config["rows_to_fix"]
            else:
                rows_to_fix = None

            if "bfill_header" in table_config:
                bfill_header = table_config["bfill_header"]
            else:
                bfill_header = None

            # read the page
            tables_read = camelot.read_pdf(
                str(input_folder / inventory_file), pages=page, **page_def
            )
            table_df = tables_read[table_def_current["tables"][page]].df

            # fix split rows if necessary
            if rows_to_fix is not None:
                for n_rows in rows_to_fix.keys():
                    table_df = fix_rows(table_df, rows_to_fix[n_rows], 0, n_rows)

            if bfill_header is not None:
                table_df.iloc[bfill_header] = (
                    table_df.iloc[bfill_header]
                    .replace(r"^\s*$", np.nan, regex=True)
                    .bfill()
                )

                # remove unwanted characters in header
            table_df.iloc[table_def_current["unit_row"]] = table_df.iloc[
                table_def_current["unit_row"]
            ].str.replace("\n", " ")
            table_df.iloc[table_def_current["unit_row"]] = table_df.iloc[
                table_def_current["unit_row"]
            ].str.replace("  ", " ")
            table_df.iloc[table_def_current["unit_row"]] = table_df.iloc[
                table_def_current["unit_row"]
            ].str.strip()
            table_df.iloc[table_def_current["entity_row"]] = table_df.iloc[
                table_def_current["entity_row"]
            ].str.replace("\n", " ")
            table_df.iloc[table_def_current["entity_row"]] = table_df.iloc[
                table_def_current["entity_row"]
            ].str.replace("  ", " ")
            table_df.iloc[table_def_current["entity_row"]] = table_df.iloc[
                table_def_current["entity_row"]
            ].str.strip()

            # fill empty strings in rows
            if "ffill_rows" in table_def_current.keys():
                for row in table_def_current["ffill_rows"]:
                    table_df.iloc[row] = (
                        table_df.iloc[row].replace(r"^\s*$", np.nan, regex=True).ffill()
                    )

            table_df = pm2.pm2io.nir_add_unit_information(
                table_df,
                unit_row=table_def_current["unit_row"],
                entity_row=table_def_current["entity_row"],
                regexp_entity=".*",
                default_unit=default_unit,
                manual_repl_unit=manual_repl_unit,
            )
            table_df = table_df.set_index(table_df.columns[0])
            table_long = pm2.pm2io.nir_convert_df_to_long(
                table_df,
                year=table_def_current["time"],
                header_long=["category", "entity", "unit", "time", "data"],
            )

            # replace special characters in category column
            table_long["category"] = table_long["category"].str.replace("\n", " ")
            table_long["category"] = table_long["category"].str.replace("  ", " ")
            table_long["category"] = table_long["category"].str.strip()

            # replace cat names by codes in col "category"
            # first the manual replacements
            table_long["category"] = table_long["category"].replace(
                table_def_current["cat_codes_manual"]
            )

            # then the regex replacements
            table_long["category"] = table_long["category"].str.replace(
                cat_code_regexp, repl, regex=True
            )

            # # prepare parameters for conversion to PRIMAP2 IF
            coords_defaults = config_general["coords_defaults"].copy()
            # coords_defaults.update(table_def_current['coords_defaults'])
            coords_cols = {
                "category": "category",
                "entity": "entity",
                "unit": "unit",
            }

            data_if = pm2.pm2io.convert_long_dataframe_if(
                table_long,
                coords_cols=coords_cols,
                coords_defaults=coords_defaults,
                coords_terminologies=config_general["coords_terminologies"],
                coords_value_mapping=table_def_current["coords_value_mapping"],
                filter_remove=table_def_current["filter_remove"],
                meta_data=config_general["meta_data"],
                time_format=config_general["time_format"],
            )
            data_pm2 = pm2.pm2io.from_interchange_format(data_if)
            if data_table is None:
                data_table = data_pm2
            else:
                data_table = data_table.pr.merge(data_pm2)

        # if "remove_vals" in table_def_current:
        #     for case in table_def_current['remove_vals']:
        #         data_table = set_to_nan_in_ds(data_table,
        #         **table_def_current['remove_vals'][case])

        if data_inv is None:
            data_inv = data_table
        else:
            data_inv = data_inv.pr.merge(data_table)

    # remove SO2, NOx from trends as there are inconsistencies with the inventory
    # SO2: 2, 2.B, 2.C, 1.A
    # NOx: 1.A.3, 2.C
    vars_to_remove = ["SO2", "NOx"]
    vars_trends = data_trend.data_vars
    vars_to_keep = [var for var in vars_trends if var not in vars_to_remove]
    data_trend = data_trend[vars_to_keep]

    # merge trends and inventory
    data_pm2 = data_inv.pr.merge(data_trend)

    # convert back to IF to have units in the fixed format
    data_if = data_pm2.pr.to_interchange_format()

    # ###
    # save data to IF and native format
    # ###
    pm2.pm2io.write_interchange_format(
        output_folder
        / (output_filename + config_general["coords_terminologies"]["category"]),
        data_if,
    )

    encoding = {var: compression for var in data_pm2.data_vars}
    data_pm2.pr.to_netcdf(
        output_folder
        / (
            output_filename + config_general["coords_terminologies"]["category"] + ".nc"
        ),
        encoding=encoding,
    )

    #################################

    # # ###
    # # conversion to ipcc 2006 categories
    # # ###
    #
    # data_pm2_2006 = data_pm2.copy()
    #
    # # actual processing
    #
    # country_processing = {
    #     "basket_copy": basket_copy,
    # }
    #
    # data_pm2_2006 = process_data_for_country(
    #     data_pm2_2006,
    #     entities_to_ignore=[],
    #     gas_baskets=gas_baskets,
    #     processing_info_country=country_processing,
    #     cat_terminology_out=terminology_proc,
    #     category_conversion=cat_conversion,
    #     # sectors_out=sectors_to_save,
    # )
    #
    # # adapt source and metadata
    # current_source = data_pm2_2006.coords["source"].to_numpy()[0]
    # data_temp = data_pm2_2006.pr.loc[{"source": current_source}]
    # data_pm2_2006 = data_pm2_2006.pr.set("source", "AI_INV", data_temp)
    # data_pm2_2006 = data_pm2_2006.pr.loc[{"source": ["AI_INV"]}]
    #
    # # convert back to IF to have units in the fixed format
    # data_if_2006 = data_pm2_2006.pr.to_interchange_format()
    #
    # pm2.pm2io.write_interchange_format(
    #     output_folder / (output_filename + terminology_proc),
    #     data_if_2006,
    # )
    #
    # encoding = {var: compression for var in data_pm2_2006.data_vars}
    # data_pm2_2006.pr.to_netcdf(
    #     output_folder / (output_filename + terminology_proc + ".nc"),
    #     encoding=encoding,
    # )
