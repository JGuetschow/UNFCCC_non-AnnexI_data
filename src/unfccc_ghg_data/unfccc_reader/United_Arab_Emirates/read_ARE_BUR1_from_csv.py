"""
Read data from United Arab Emirates' BUR!.

Data are read a csv file which contains data manually copied from the pdf,
which was necessary as multiple tables are not machine readable.
The file contains an inventory for 2021.

"""

import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import (
    compression,
    downloaded_data_path,
    extracted_data_path,
    gas_baskets,
    process_data_for_country,
    set_to_nan_in_ds,
)
from unfccc_ghg_data.unfccc_reader.United_Arab_Emirates.config_are_bur1 import (
    category_conversion,
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    filter_remove,
    gwp_to_use,
    meta_data,
    processing_info_country,
    terminology_proc,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = downloaded_data_path / "UNFCCC" / "United_Arab_Emirates" / "BUR1"
    output_folder = extracted_data_path / "UNFCCC" / "United_Arab_Emirates"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "ARE_BUR1_2023_"
    inventory_file = "all_data_manual.csv"

    year = 2021
    time_format = "%Y"

    # ###
    # read the tables from csv
    # ###
    data_pd = pd.read_csv(input_folder / inventory_file)

    data_pd = pm2.pm2io.nir_add_unit_information(
        data_pd,
        unit_row=0,
        entity_row="header",
        regexp_entity=".*",
        regexp_unit=".*",
        default_unit="",
    )
    data_pd = data_pd.set_index(data_pd.columns[0])
    table_long = pm2.pm2io.nir_convert_df_to_long(
        data_pd,
        year=year,
        header_long=["category", "entity", "unit", "time", "data"],
    )

    # drop CH4, N2O with GWP
    idx_gwp = table_long[table_long["entity"].isin(["CH4.1", "N2O.1"])].index
    table_long = table_long.drop(index=idx_gwp)

    data_if = pm2.pm2io.convert_long_dataframe_if(
        table_long,
        coords_cols=coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        filter_remove=filter_remove,
        meta_data=meta_data,
        time_format=time_format,
    )

    data_pm2 = pm2.pm2io.from_interchange_format(data_if)

    # ###
    # save data to IF and native format
    # ###
    data_if = data_pm2.pr.to_interchange_format()
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

    ### processing
    data_proc_pm2 = data_pm2.copy()

    # move HFCs from energy to IPPU as their use in electrical
    # equipment is reported there
    da_HFCs = data_proc_pm2[f"HFCS ({gwp_to_use})"].pr.loc[{"category": "1"}]
    ds_HFCs = data_proc_pm2[f"HFCS ({gwp_to_use})"].pr.set(
        "category", "2.G", da_HFCs, existing="overwrite"
    )
    data_proc_pm2 = data_proc_pm2.pr.merge(ds_HFCs)
    data_proc_pm2 = set_to_nan_in_ds(
        data_proc_pm2,
        entities=[f"HFCS ({gwp_to_use})"],
        filter={"category": ["1", "2"]},
    )
    data_proc_pm2 = set_to_nan_in_ds(
        data_proc_pm2,
        entities=[f"KYOTOGHG ({gwp_to_use})"],
        filter={"category": ["1", "2"]},
    )

    # actual processing
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
