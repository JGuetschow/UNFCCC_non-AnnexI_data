"""
Read Bangladesh's BTR1 from pdf

This script reads data from Bangladesh's BTR1
As the data is spread over multiple tables we collect data from small tables manually
in a xlsx file which we then read using pandas. The origin of the data points is
specified in the xls files. Additionally, we read the key category analysis (Annex-IX)
which contains detailed information for 2019 and 2022 using camelot.

"""

from copy import deepcopy

import camelot
import numpy as np
import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import (
    auto_fix_rows,
    downloaded_data_path,
    extracted_data_path,
    merge_rows,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.Bangladesh.config_bgd_btr1 import (
    cols_to_drop_individual,
    cols_to_drop_key_cat,
    cols_to_rename_key_cat,
    coords_cols_individual,
    coords_cols_key_cat,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping_individual,
    coords_value_mapping_key_cat,
    country_processing_step1,
    country_processing_step2,
    filter_remove,
    meta_data,
    page_defs,
    # table_defs,
    unit_key_cat,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = downloaded_data_path / "UNFCCC" / "Bangladesh" / "BTR1"
    output_folder = extracted_data_path / "UNFCCC" / "Bangladesh"
    if not output_folder.exists():
        output_folder.mkdir()

    inventory_file = "Bangladesh_BTR1_Interim.pdf"
    inventory_csv_file = "data_BGD_BTR1.csv"
    output_filename = "BGD_BTR1_2024_"

    compression = dict(zlib=True, complevel=9)

    # ###
    # read the csv file with data from the individual tables and convert to primap2
    # format
    # ###

    # read the data
    data_individual_df = pd.read_csv(input_folder / inventory_csv_file)

    data_individual_pm2 = None
    # split the table by source as some values are present from different sources
    # and we need to merge to avoid duplicate indices
    all_sources = data_individual_df["source"].unique()

    for source in all_sources:
        data_this_source = data_individual_df[data_individual_df["source"] == source]

        # drop the extra cols
        data_this_source = data_this_source.drop(columns=cols_to_drop_individual)

        # convert to primap2 if
        data_this_source_if = pm2.pm2io.convert_wide_dataframe_if(
            data_this_source,
            coords_cols=coords_cols_individual,
            # add_coords_cols=add_coords_cols,
            coords_defaults=coords_defaults,
            coords_terminologies=coords_terminologies,
            coords_value_mapping=coords_value_mapping_individual,
            # coords_value_filling=coords_value_filling,
            filter_remove=filter_remove,
            # filter_keep=filter_keep,
            meta_data=meta_data,
        )

        data_this_source_pm2 = pm2.pm2io.from_interchange_format(data_this_source_if)

        if data_individual_pm2 is None:
            data_individual_pm2 = data_this_source_pm2
        else:
            data_individual_pm2 = data_individual_pm2.pr.merge(data_this_source_pm2)

    # ###
    # read the key category analysis tables from pdf
    # ###

    # read and process
    data_key_cat_pm2 = None
    # data_key_cat_if = None
    col_for_row_fixing = 0
    for page, page_def in page_defs.items():
        print(f"Reading from page {page}")
        new_tables = camelot.read_pdf(
            str(input_folder / inventory_file),
            pages=page,
            **page_def,
        )
        data_this_table = new_tables[0].df

        data_this_table = auto_fix_rows(data_this_table, col_for_row_fixing)

        # combine header rows
        data_this_table, indices_to_drop = merge_rows(data_this_table, [0, 1, 2, 3])
        data_this_table = data_this_table.drop(indices_to_drop)

        index_to_drop = data_this_table.iloc[[0]].index
        data_this_table.columns = data_this_table.iloc[0]
        data_this_table = data_this_table.drop(index=index_to_drop)

        # drop the extra cols
        data_this_table = data_this_table.drop(columns=cols_to_drop_key_cat)

        # insert a unit col (don't use coords_defaults because the unit needs
        # processing as it's entity dependent)
        data_this_table["unit"] = unit_key_cat

        # rename year columns
        data_this_table = data_this_table.rename(columns=cols_to_rename_key_cat)

        # convert to primap2 if
        data_this_table_if = pm2.pm2io.convert_wide_dataframe_if(
            data_this_table,
            coords_cols=coords_cols_key_cat,
            coords_defaults=coords_defaults,
            coords_terminologies=coords_terminologies,
            coords_value_mapping=coords_value_mapping_key_cat,
            # coords_value_filling=coords_value_filling,
            filter_remove=filter_remove,
            # filter_keep=filter_keep,
            meta_data=meta_data,
        )

        data_this_table_pm2 = pm2.pm2io.from_interchange_format(data_this_table_if)

        if data_key_cat_pm2 is None:
            data_key_cat_pm2 = data_this_table_pm2
        else:
            data_key_cat_pm2 = data_key_cat_pm2.pr.merge(data_this_table_pm2)
        # if data_key_cat_if is None:
        #     data_key_cat_if = data_this_table_if
        # else:
        #     data_key_cat_if = pd.concat([data_key_cat_if, data_this_table_if])

    agg_fuel_type = {
        "fuel_type": {
            "all": {
                "sources": [
                    "bio_gas",
                    "bio_liquid",
                    "bio_other",
                    "bio_solid",
                    "gaseous",
                    "liquid",
                    "other_fossil",
                    "peat",
                    "solid",
                ],
            }
        }
    }

    # data to drop because it is inconsistent between fuel types and aggregates
    data_to_remove = {
        "1A1": {
            "entities": ["CO2", "CH4"],
            "category (IPCC2006_PRIMAP)": ["1.A.1"],
            "time": ["2019", "2022"],
            "fuel_type": ["all"],
        },
        "2C1": {
            "entities": ["CO2", "CH4"],
            "category (IPCC2006_PRIMAP)": ["2.C.1"],
            "time": ["2019", "2022"],
            "fuel_type": ["solid"],
        },
        "1A3b": {
            "entities": ["CO2"],
            "category (IPCC2006_PRIMAP)": ["1.A.3.b"],
            "time": ["2019", "2022"],
            "fuel_type": ["all"],
        },
    }

    for case in data_to_remove.items():
        remove_info = deepcopy(case[1])
        if "entities" in remove_info:
            entities = remove_info.pop("entities")
        else:
            entities = data_key_cat_pm2.data_vars
        for entity in entities:
            data_key_cat_pm2[entity].pr.loc[remove_info] *= np.nan

        # remove all-nan time-series
        for coord in remove_info.keys():
            data_key_cat_pm2 = data_key_cat_pm2.dropna(dim=coord, how="all")

    # aggregate fuel types
    data_key_cat_pm2 = data_key_cat_pm2.pr.add_aggregates_coordinates(
        agg_info=agg_fuel_type
    )

    data_key_cat_pm2 = data_key_cat_pm2.pr.loc[{"fuel_type": "all"}]
    data_key_cat_pm2 = data_key_cat_pm2.drop_vars("fuel_type")

    ###
    # merge data from individual tables and key category analysis
    ###
    data_all_pm2 = data_individual_pm2.pr.merge(data_key_cat_pm2)

    # convert back to interchange format for saving
    data_if = data_all_pm2.pr.to_interchange_format()

    # ###
    # save raw data to IF and native format
    # ###
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"] + "_raw"),
        data_if,
    )

    encoding = {var: compression for var in data_all_pm2.data_vars}
    data_all_pm2.pr.to_netcdf(
        output_folder
        / (output_filename + coords_terminologies["category"] + "_raw.nc"),
        encoding=encoding,
    )

    ###
    # processing
    ###

    data_proc_pm2 = data_all_pm2.copy(deep=True)

    # aggregate some gases for the individual data
    data_proc_pm2 = process_data_for_country(
        data_proc_pm2,
        entities_to_ignore=[],
        gas_baskets=[],
        # cat_terminology_out=terminology_proc,
        # category_conversion=cat_conversion_trends,
        processing_info_country=country_processing_step1,
    )

    # aggregate some gases for the individual data
    data_proc_pm2 = process_data_for_country(
        data_proc_pm2,
        entities_to_ignore=[],
        gas_baskets=[],  # TODO
        # cat_terminology_out=terminology_proc,
        # category_conversion=cat_conversion_trends,
        processing_info_country=country_processing_step2,
    )

    data_proc_if = data_proc_pm2.pr.to_interchange_format()
    # aggregation of categories and gases

    # downscaling of categories and gases for

    ### TODO processing ###
    # The data is very inconsistent we have to deal with theis before processing
