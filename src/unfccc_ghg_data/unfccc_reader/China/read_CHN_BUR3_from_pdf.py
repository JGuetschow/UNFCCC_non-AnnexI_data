"""
Read data from China's BUR3.

Data are read from pdf. The file contains a detailed inventory for 2018 and
recalculated 2005 data for the main sectors and gases.

Inventories for mainland China (CHN), Hong Kong (HKG) and Macau (MAC) are reported in
individual inventories.
"""


from copy import deepcopy

import camelot
import primap2 as pm2

from unfccc_ghg_data.helper import (
    compression,
    downloaded_data_path,
    extracted_data_path,
    fix_rows,
    gas_baskets,
    process_data_for_country,
    set_to_nan_in_ds,
)
from unfccc_ghg_data.unfccc_reader.China.config_chn_bur3_nc4 import (
    category_conversion,
    config_bur3,
    config_general,
    gwp_to_use,
    terminology_proc,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = downloaded_data_path / "UNFCCC" / "China" / "BUR3"
    output_folder = extracted_data_path / "UNFCCC" / "China"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "CHN_BUR3_2023_"
    inventory_file = "China_BUR3_English.pdf"

    def repl(m):  # noqa: D103
        return m.group("code")

    # ###
    # read the tables from pdf
    # ###
    all_data = None
    for table_group in config_bur3["table_groups"].keys():
        current_group = config_bur3["table_groups"][table_group]
        for country in current_group["pages"].keys():
            for page in current_group["pages"][country]:
                print(f"Reading {country}, {table_group}, page {page}")
                page_str = str(page)
                page_def = config_bur3["page_def"][page_str]
                if "rows_to_fix" in page_def:
                    rows_to_fix = page_def.pop("rows_to_fix")
                else:
                    rows_to_fix = {}
                if "unit_correction" in page_def:
                    unit_correction = page_def.pop("unit_correction")
                else:
                    unit_correction = None
                unit = page_def.pop("unit")
                if "manual_repl_unit" in page_def:
                    manual_repl_unit = page_def.pop("manual_repl_unit")
                else:
                    manual_repl_unit = None

                tables_read = camelot.read_pdf(
                    str(input_folder / inventory_file), pages=page_str, **page_def
                )
                table_df = tables_read[0].df
                # fix split rows
                if rows_to_fix:
                    for n_rows in rows_to_fix.keys():
                        table_df = fix_rows(table_df, rows_to_fix[n_rows], 0, n_rows)
                # remove unwanted characters
                table_df[0] = table_df[0].str.replace("\n", " ")
                table_df[0] = table_df[0].str.replace("⎯ ", "")
                table_df[0] = table_df[0].str.replace("♦", "")
                table_df.iloc[0] = table_df.iloc[0].str.strip()

                table_df = pm2.pm2io.nir_add_unit_information(
                    table_df,
                    unit_row=0,
                    entity_row=0,
                    regexp_entity=".*",
                    default_unit=unit,
                    manual_repl_unit=manual_repl_unit,
                )
                table_df = table_df.set_index(table_df.columns[0])
                table_long = pm2.pm2io.nir_convert_df_to_long(
                    table_df,
                    year=current_group["year"],
                    header_long=["category", "entity", "unit", "time", "data"],
                )
                # clean data and metadata
                table_long["entity"] = table_long["entity"].str.strip()
                table_long["data"] = table_long["data"].str.strip()
                table_long["data"] = table_long["data"].str.replace(",", "")
                table_long["data"] = table_long["data"].str.replace(" ", "")

                # convert to primap2 format
                coords_defaults = config_general["coords_defaults"].copy()
                coords_defaults.update(config_bur3["coords_defaults"])
                coords_defaults.update({"area": country})
                coords_value_mapping = deepcopy(config_general["coords_value_mapping"])
                if "CO2eq" in unit:
                    coords_value_mapping["entity"].update(
                        {
                            "CH4": f"CH4 ({gwp_to_use})",
                            "N2O": f"N2O ({gwp_to_use})",
                            "SF6": f"SF6 ({gwp_to_use})",
                        }
                    )

                meta_data = config_general["meta_data"].copy()
                meta_data.update(config_bur3["meta_data"])
                data_if = pm2.pm2io.convert_long_dataframe_if(
                    table_long,
                    coords_cols=config_general["coords_cols"],
                    coords_defaults=coords_defaults,
                    coords_terminologies=config_general["coords_terminologies"],
                    coords_value_mapping=coords_value_mapping,
                    filter_remove=config_general["filter_remove"],
                    meta_data=meta_data,
                    time_format=config_general["time_format"],
                )
                print(data_if["entity"].unique())
                data_pm2 = pm2.pm2io.from_interchange_format(data_if)
                if unit_correction is not None:
                    for entity in data_pm2.data_vars:
                        data_pm2[entity].data = data_pm2[entity].data * unit_correction

                if all_data is None:
                    all_data = data_pm2
                else:
                    all_data = all_data.pr.merge(data_pm2)

    # ###
    # save data to IF and native format
    # ###
    all_data_if = all_data.pr.to_interchange_format()
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder
        / (output_filename + config_general["coords_terminologies"]["category"]),
        all_data_if,
    )

    encoding = {var: compression for var in all_data.data_vars}
    all_data.pr.to_netcdf(
        output_folder
        / (
            output_filename + config_general["coords_terminologies"]["category"] + ".nc"
        ),
        encoding=encoding,
    )

    ### processing
    data_proc_pm2 = None
    remove_data = config_bur3["remove_data"]

    # actual processing
    for country in all_data.coords["area (ISO3)"].to_numpy():
        print(f"Processing data for {country}")
        data_country = all_data.pr.loc[{"area (ISO3)": [country]}]
        # remove wrong and conflicting data
        if country in remove_data:
            for filter_name in remove_data[country]:
                filter = remove_data[country][filter_name].copy()
                entities = data_country.data_vars
                if "entity" in filter:
                    entities_current = filter.pop("entity")
                    entities = [
                        entity for entity in entities if entity in entities_current
                    ]

                data_country = set_to_nan_in_ds(
                    data_country,
                    entities=entities,
                    filter=filter,
                )
                # ds_mask = xr.zeros_like(
                #     data_country[entities].pr.loc[filter]
                # ).combine_first(xr.ones_like(data_country))
                #
                # data_country = data_country.where(ds_mask)

        data_proc_pm2_new = process_data_for_country(
            data_country,
            entities_to_ignore=[],
            gas_baskets=gas_baskets,
            processing_info_country=config_bur3["processing_info_country"][country],
            cat_terminology_out=terminology_proc,
            category_conversion=category_conversion[country],
        )
        if data_proc_pm2 is None:
            data_proc_pm2 = data_proc_pm2_new
        else:
            data_proc_pm2 = data_proc_pm2.pr.merge(data_proc_pm2_new)

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
