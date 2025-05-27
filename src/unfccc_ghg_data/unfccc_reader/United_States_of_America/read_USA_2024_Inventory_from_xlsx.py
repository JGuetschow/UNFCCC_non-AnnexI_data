"""
Read USA's 2024 inventory from xlsx

Files available here: https://www.epa.gov/ghgemissions/
inventory-us-greenhouse-gas-emissions-and-sinks-1990-2022

Only the overview tables are read as details are in several individual tables and
overview is sufficient for PRIMAP-hist

"""

import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.United_States_of_America.config_usa_inv2024 import (
    basket_copy,
    cat_conversion,
    category_col,
    coords_cols_template,
    coords_defaults_template,
    coords_terminologies,
    filter_remove,
    gas_baskets,
    inventory_files,
    meta_data,
    terminology_proc,
    time_format,
)

if __name__ == "__main__":
    pd.set_option("future.no_silent_downcasting", True)

    # ###
    # configuration
    # ###

    # folders and files
    input_folder = (
        downloaded_data_path
        / "non-UNFCCC"
        / "United_States_of_America"
        / "2024-Inventory"
        / "main-text-tables"
        / "trends"
    )
    output_folder = extracted_data_path / "non-UNFCCC" / "United_States_of_America"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "USA_2024-Inventory_"
    compression = dict(zlib=True, complevel=9)

    # ###
    # start data reading
    # ###

    data_pm2 = None

    for file in inventory_files.keys():
        data_current_pd = pd.read_csv(input_folder / file, header=[1])
        # remove the thousands separators (can't be done during reading as data is
        # stored as string)
        all_cols = data_current_pd.columns
        data_cols = [col for col in all_cols if col != category_col]
        for col in data_cols:
            if data_current_pd.dtypes[col] == "object":
                data_current_pd[col] = data_current_pd[col].str.replace(",", "")

        section_keys = inventory_files[file].keys()
        key_info = {}
        last_key = None
        for i, row in data_current_pd.iterrows():
            if row[category_col] in section_keys:
                key_info[row[category_col]] = {}
                key_info[row[category_col]]["start"] = i
                if last_key is not None:
                    key_info[last_key]["end"] = i
                last_key = row[category_col]

        for section_key in section_keys:
            current_config = inventory_files[file][section_key]
            if current_config is not None:
                # get the data
                if "end" in key_info[section_key].keys():
                    data_section = data_current_pd.iloc[
                        key_info[section_key]["start"] : key_info[section_key]["end"]
                    ].copy()
                else:
                    data_section = data_current_pd.iloc[
                        key_info[section_key]["start"] :
                    ].copy()

                # convert to primap2 IF
                coords_defaults = coords_defaults_template.copy()
                coords_defaults.update(current_config["coords_defaults"])
                coords_value_mapping = current_config["coords_value_mapping"]
                coords_cols = coords_cols_template.copy()
                if "entity" in coords_value_mapping:
                    # make a copy of the category column as we also need if for entity
                    data_section["entity"] = data_section[category_col]
                    coords_cols["entity"] = "entity"

                data_section_if = pm2.pm2io.convert_wide_dataframe_if(
                    data_section,
                    coords_cols=coords_cols,
                    coords_terminologies=coords_terminologies,
                    coords_defaults=coords_defaults,
                    coords_value_mapping=coords_value_mapping,
                    filter_remove=filter_remove,
                    meta_data=meta_data,
                    time_format=time_format,
                )
                # convert to primap2 native format
                data_section_pm2 = pm2.pm2io.from_interchange_format(data_section_if)

                # merge with other data
                if data_pm2 is None:
                    data_pm2 = data_section_pm2
                else:
                    data_pm2 = data_pm2.pr.merge(data_section_pm2)

    # convert back to IF to have units in the fixed format
    data_if = data_pm2.pr.to_interchange_format()

    # ###
    # save data to IF and native format
    # ###
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"]), data_if
    )

    encoding = {var: compression for var in data_pm2.data_vars}
    data_pm2.pr.to_netcdf(
        output_folder / (output_filename + coords_terminologies["category"] + ".nc"),
        encoding=encoding,
    )

    # ###
    # conversion to ipcc 2006 categories
    # ###

    data_pm2_2006 = data_pm2.copy()

    # actual processing

    country_processing = {
        "basket_copy": basket_copy,
    }

    data_pm2_2006 = process_data_for_country(
        data_pm2_2006,
        entities_to_ignore=[],
        gas_baskets=gas_baskets,
        processing_info_country=country_processing,
        cat_terminology_out=terminology_proc,
        category_conversion=cat_conversion,
        # sectors_out=sectors_to_save,
    )

    # adapt source and metadata
    current_source = data_pm2_2006.coords["source"].to_numpy()[0]
    data_temp = data_pm2_2006.pr.loc[{"source": current_source}]
    data_pm2_2006 = data_pm2_2006.pr.set("source", "AI_INV", data_temp)
    data_pm2_2006 = data_pm2_2006.pr.loc[{"source": ["AI_INV"]}]

    # convert back to IF to have units in the fixed format
    data_if_2006 = data_pm2_2006.pr.to_interchange_format()

    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + terminology_proc),
        data_if_2006,
    )

    encoding = {var: compression for var in data_pm2_2006.data_vars}
    data_pm2_2006.pr.to_netcdf(
        output_folder / (output_filename + terminology_proc + ".nc"),
        encoding=encoding,
    )
