"""
Read Iraq's BUR1 from pdf

This script reads data from Iraq's BUR3
Data are read from pdf using camelot

"""

import camelot
import numpy as np
import pandas as pd
import primap2 as pm2
import primap2.pm2io

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.Iraq.config_irq_bur1 import (
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_terminologies_1996,
    coords_value_mapping,
    country_processing_step1,
    def_inv_config,
    filter_remove,
    gas_baskets,
    meta_data,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = downloaded_data_path / "UNFCCC" / "Iraq" / "BUR1"
    output_folder = extracted_data_path / "UNFCCC" / "Iraq"
    if not output_folder.exists():
        output_folder.mkdir()

    inventory_file = "IRAQ_SNCBUR_-ENGLISH.pdf"
    output_filename = "IRQ_BUR1_2024_"

    compression = dict(zlib=True, complevel=9)

    # fugitive emissions are zero for 2000 in the tables. They are non-zero in the
    # IPCC 1996 tables in pages 55-56 and the small table on page 179
    # inventory tables
    inventories = {
        "energy_2000": {
            "year": 2000,
            "pages": "180",
            "entity_row": 1,
            "unit_row": 0,
            "regexp_unit": "\\n(.*)",
            "fix_index": False,
        },
        "ippu_2000": {
            "year": 2000,
            "pages": "185",
            "entity_row": 1,
            "unit_row": 0,
            "regexp_unit": ".*",
            "fix_index": True,
        },
        "agri_2000": {
            "year": 2000,
            "pages": "186,187",
            "entity_row": 1,
            "unit_row": 0,
            "regexp_unit": ".*",
            "fix_index": True,
            "merge_header": [1, 2],
        },
        "waste_2000": {
            "year": 2000,
            "pages": "188",
            "entity_row": 1,
            "unit_row": 0,
            "regexp_unit": r".*",
            "fix_index": True,
            "header": [["Categories", "Gg", "Gg", "Gg"], ["", "CO2", "CH4", "N2O"]],
        },
        "main_2000": {  # read last because of lower detail and sign. digits
            "year": 2000,
            "pages": "175,176,177,178",
            "entity_row": 1,
            "unit_row": 0,
            "regexp_unit": "\\n(.*)",
            "fix_index": False,
            "drop_rows": [10, 11, 12, 13],
        },
        "energy_2019": {
            "year": 2019,
            "pages": "210,211",
            "entity_row": 1,
            "unit_row": 0,
            "regexp_unit": r"\((.*)\)",
            "fix_index": False,
        },
        "bunkers_2019": {
            "year": 2019,
            "pages": "214",
            "entity_row": 1,
            "unit_row": 0,
            "regexp_unit": r"\((.*)\)",
            "fix_index": False,
        },
        "ippu_2019": {
            "year": 2019,
            "pages": "218",
            "entity_row": 1,
            "unit_row": 0,
            "regexp_unit": ".*",
            "fix_index": True,
        },
        "agri_2019": {
            "year": 2019,
            "pages": "219,220",
            "entity_row": 1,
            "unit_row": 0,
            "regexp_unit": ".*",
            "fix_index": True,
            "merge_header": [1, 2],
        },
        "waste_2019": {
            "year": 2019,
            "pages": "221",
            "entity_row": 1,
            "unit_row": 0,
            "regexp_unit": r"\[(.*)\]",
            "fix_index": False,
        },
        "main_2019": {  # read last because of lower detail and sign. digits
            "year": 2019,
            "pages": "206,208",
            "entity_row": 1,
            "unit_row": 0,
            "regexp_unit": "\\n(.*)",
            "fix_index": False,
        },
    }

    inventory_1996 = {
        "year": 2000,
        "pages": "55,56",
        "entity_row": 0,
        "unit_row": 0,
        "regexp_unit": r"\((.*)\)",
        "regexp_entity": r"(.*)\s\(",
        "fix_index": False,
        "index_cols": "GHG source and sink categories: Inventory Year: 2000",
        "str_conversions": {
            "NE NO": 0,
            "NO NE": 0,
        },
    }

    # ###
    # read the inventory data and convert to PM2 IF
    # ###
    data_all_pm2 = None
    for inv_label, inv_config in inventories.items():
        print(f"reading tables for inventory tables {inv_label}")
        tables_inventory = camelot.read_pdf(
            str(input_folder / inventory_file),
            pages=inv_config["pages"],
            split_text=False,
            flavor="lattice",
        )

        df_inventory = tables_inventory[0].df  # [1:]
        # df_header = pd.DataFrame([inv_conf["header"], inv_conf["unit"]])
        for table in tables_inventory[1:]:
            df_inventory = pd.concat([df_inventory, table.df])

        # reset the index because we have double valuesa fter concatenation
        df_inventory = df_inventory.reset_index(drop=True)

        # merge header rows where necessary
        if "merge_header" in inv_config:
            new_row = df_inventory.iloc[inv_config["merge_header"][0]]
            for rowidx in inv_config["merge_header"][1:]:
                new_row = new_row + df_inventory.iloc[rowidx]
            df_inventory.iloc[inv_config["merge_header"][0]] = new_row
            # drop other rows
            index_to_drop = df_inventory.iloc[inv_config["merge_header"][1:]].index
            df_inventory = df_inventory.drop(index_to_drop)
        elif "header" in inv_config:
            for i, row in enumerate(inv_config["header"]):
                df_inventory.iloc[i] = row

        # drop rows where necessary
        if "drop_rows" in inv_config:
            index_to_drop = df_inventory.iloc[inv_config["drop_rows"]].index
            df_inventory = df_inventory.drop(index_to_drop)

        # fill empty unit values
        df_inventory.iloc[0] = df_inventory.iloc[0].replace(
            r"^\s*$", np.nan, regex=True
        )
        df_inventory.iloc[0] = df_inventory.iloc[0].ffill()
        df_inventory.iloc[1] = df_inventory.iloc[1].replace(
            r"^\s*$", np.nan, regex=True
        )
        # remove line breaks from entity names
        df_inventory.iloc[1] = df_inventory.iloc[1].str.replace(r"\n", "", regex=True)

        # if category col (first col) is empty for entity row, copy value from unit row
        if pd.isna(df_inventory.iloc[inv_config["entity_row"], 0]):
            df_inventory.iloc[inv_config["entity_row"], 0] = df_inventory.iloc[
                inv_config["unit_row"], 0
            ]

        # bring header in default format
        df_inventory = pm2.pm2io.nir_add_unit_information(
            df_inventory,
            unit_row=inv_config["unit_row"],
            entity_row=inv_config["entity_row"],
            regexp_entity=".*",
            regexp_unit=inv_config["regexp_unit"],
            default_unit="",
        )
        # set index and convert to long format
        df_inventory = df_inventory.set_index(def_inv_config["index_cols"])
        df_inventory_long = pm2.pm2io.nir_convert_df_to_long(
            df_inventory, inv_config["year"], def_inv_config["header_long"]
        )
        if inv_config["fix_index"]:
            df_inventory_long["orig_cat_name"] = df_inventory_long["orig_cat_name"].str[
                0
            ]

        # remove line breaks from category names
        df_inventory_long["orig_cat_name"] = df_inventory_long[
            "orig_cat_name"
        ].str.replace(r"\n", "", regex=True)

        # prep for conversion to PM2 IF and native format
        # make a copy of the categories row
        df_inventory_long["category"] = df_inventory_long["orig_cat_name"]

        # replace cat names by codes in col "category"
        # first the manual replacements
        df_inventory_long["category"] = df_inventory_long["category"].replace(
            def_inv_config["cat_codes_manual"]
        )

        # then the regex replacements
        def repl(m):  # noqa: D103
            return m.group("code")

        df_inventory_long["category"] = df_inventory_long["category"].str.replace(
            def_inv_config["cat_code_regexp"], repl, regex=True
        )

        # replace units
        df_inventory_long["unit"] = df_inventory_long["unit"].replace(
            def_inv_config["unit_replace"]
        )

        df_inventory_long = df_inventory_long.reset_index(drop=True)

        # make sure all col headers are str
        df_inventory_long.columns = df_inventory_long.columns.map(str)

        df_inventory_long = df_inventory_long.drop(columns=["orig_cat_name"])

        data_inventory_IF = pm2.pm2io.convert_long_dataframe_if(
            df_inventory_long,
            coords_cols=coords_cols,
            # add_coords_cols=add_coords_cols,
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

        data_inventory = primap2.pm2io.from_interchange_format(data_inventory_IF)

        if data_all_pm2 is None:
            data_all_pm2 = data_inventory
        else:
            data_all_pm2 = data_all_pm2.pr.merge(data_inventory, tolerance=0.02)

    # remove energy and Totals for year 2000 from IPCC2006 data (fugitive missing)
    variables = data_all_pm2.data_vars
    for var in variables:
        data_all_pm2[var].pr.loc[
            {
                "time": "2000",
                "category": ["0", "1", "1.B"],
            }
        ] *= np.nan

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
    # read the IPCC1996 inventory data and convert to PM2 IF
    # ###
    print("reading tables for IPCC1996 inventory")
    tables_inventory = camelot.read_pdf(
        str(input_folder / inventory_file),
        pages=inventory_1996["pages"],
        split_text=False,
        flavor="lattice",
    )

    data_1996_pm2 = None
    for table in tables_inventory[0:2]:
        df_inventory = table.df

        # remove line breaks from entity names
        df_inventory = df_inventory.replace(r"\n", "", regex=True)
        df_inventory = df_inventory.replace("  ", " ", regex=True)
        df_inventory = df_inventory.replace("/", "", regex=True)
        df_inventory = df_inventory.replace("  ", " ", regex=True)  # noqa: RUF001

        # bring header in default format
        df_inventory = pm2.pm2io.nir_add_unit_information(
            df_inventory,
            unit_row=inventory_1996["unit_row"],
            entity_row=inventory_1996["entity_row"],
            regexp_entity=inventory_1996["regexp_entity"],
            regexp_unit=inventory_1996["regexp_unit"],
            default_unit="Gg",
        )
        # set index and convert to long format
        df_inventory = df_inventory.set_index(inventory_1996["index_cols"])
        df_inventory_long = pm2.pm2io.nir_convert_df_to_long(
            df_inventory, inventory_1996["year"], def_inv_config["header_long"]
        )
        df_inventory_long["orig_cat_name"] = df_inventory_long["orig_cat_name"].str[0]

        # prep for conversion to PM2 IF and native format
        # make a copy of the categories row
        df_inventory_long["category"] = df_inventory_long["orig_cat_name"]

        # replace cat names by codes in col "category"
        # first the manual replacements
        df_inventory_long["category"] = df_inventory_long["category"].replace(
            def_inv_config["cat_codes_manual"]
        )

        # then the regex replacements
        def repl(m):  # noqa: D103
            return m.group("code")

        df_inventory_long["category"] = df_inventory_long["category"].str.replace(
            def_inv_config["cat_code_regexp"], repl, regex=True
        )

        df_inventory_long = df_inventory_long.reset_index(drop=True)

        # make sure all col headers are str
        df_inventory_long.columns = df_inventory_long.columns.map(str)

        df_inventory_long = df_inventory_long.drop(columns=["orig_cat_name"])

        data_inventory_IF = pm2.pm2io.convert_long_dataframe_if(
            df_inventory_long,
            coords_cols=coords_cols,
            coords_defaults=coords_defaults,
            coords_terminologies=coords_terminologies_1996,
            coords_value_mapping=coords_value_mapping,
            filter_remove=filter_remove,
            meta_data=meta_data,
            convert_str=inventory_1996["str_conversions"],
            time_format="%Y",
        )

        data_inventory = primap2.pm2io.from_interchange_format(data_inventory_IF)

        if data_1996_pm2 is None:
            data_1996_pm2 = data_inventory
        else:
            data_1996_pm2 = data_1996_pm2.pr.merge(data_inventory)

    data_1996_if = data_1996_pm2.pr.to_interchange_format()

    # ###
    # save raw data to IF and native format
    # ###
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder
        / (output_filename + coords_terminologies_1996["category"] + "_raw"),
        data_1996_if,
    )

    encoding = {var: compression for var in data_1996_pm2.data_vars}
    data_1996_pm2.pr.to_netcdf(
        output_folder
        / (output_filename + coords_terminologies_1996["category"] + "_raw.nc"),
        encoding=encoding,
    )

    # ###
    # ## process the data
    # ###
    data_proc_pm2 = data_all_pm2

    # # remove fugitive emissions for year 2000 from IPCC2006 data and replace by
    # # IPCC1996 data as they are zero in 1996 data
    # variables = data_proc_pm2.data_vars
    # for var in variables:
    #     data_proc_pm2[var].pr.loc[{
    #         "time": "2000",
    #         "category": ["0", "1", "1.B", "1.B.1", "1.B.2"],
    #     }] *= np.nan
    #
    # data_to_fill = data_1996_pm2.pr.loc[{
    #     "time": "2000",
    #     "category": ["1.B", "1.B.1", "1.B.2"],
    # }]
    # # change category terminology
    # cat_dim = data_to_fill.attrs["cat"]
    # data_to_fill.attrs["cat"] = f"category ({coords_terminologies['category']})"
    # data_to_fill = data_to_fill.rename({cat_dim: data_to_fill.attrs["cat"]})
    #
    # data_proc_pm2 = data_proc_pm2.merge(data_to_fill)

    # actual processing
    data_proc_pm2 = process_data_for_country(
        data_proc_pm2,
        gas_baskets=gas_baskets,
        entities_to_ignore=[],
        processing_info_country=country_processing_step1,
    )

    data_proc_if = data_proc_pm2.pr.to_interchange_format()

    # ###
    # save raw data to IF and native format
    # ###
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
