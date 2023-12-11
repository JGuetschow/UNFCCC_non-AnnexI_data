"""
Read Korea's 2021 inventory from xlsx

This script reads data from Korea's 2022 national inventory
Data are read from the xlsx file

"""

import os
import sys

import pandas as pd
import primap2 as pm2
from config_kor_bur4 import (
    aggregate_after_mapping,
    aggregate_before_mapping,
    cat_codes,
    cat_mapping,
    cat_name_translations,
    coords_terminologies_2006,
    filter_remove_2006,
    filter_remove_after_agg,
)
from primap2.pm2io._data_reading import filter_data, matches_time_format

from unfccc_ghg_data.helper import downloaded_data_path, extracted_data_path

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = (
        downloaded_data_path / "non-UNFCCC" / "Republic_of_Korea" / "2022-Inventory"
    )
    output_folder = extracted_data_path / "non-UNFCCC" / "Republic_of_Korea"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "KOR_2022-Inventory_2022_"

    inventory_file = "Republic_of_Korea_National_GHG_Inventory_(1990_2020).xlsx"
    years_to_read = range(1990, 2020 + 1)

    sheets_to_read = ["온실가스", "CO2", "CH4", "N2O", "HFCs", "PFCs", "SF6"]
    cols_to_read = range(1, 2020 - 1990 + 3)

    # columns for category code and original category name
    index_cols = ["분야·부문/연도"]

    sheet_metadata = {
        "entity": {
            "온실가스": "KYOTOGHG (SARGWP100)",
            "CO2": "CO2",
            "CH4": "CH4 (SARGWP100)",
            "N2O": "N2O (SARGWP100)",
            "HFCs": "HFCS (SARGWP100)",
            "PFCs": "PFCS (SARGWP100)",
            "SF6": "SF6 (SARGWP100)",
        },
        "unit": {
            "온실가스": "Gg CO2 / yr",
            "CO2": "Gg CO2 / yr",
            "CH4": "Gg CO2 / yr",
            "N2O": "Gg CO2 / yr",
            "HFCs": "Gg CO2 / yr",
            "PFCs": "Gg CO2 / yr",
            "SF6": "Gg CO2 / yr",
        },
    }

    # definitions for conversion to interchange format
    time_format = "%Y"

    coords_cols = {
        "category": "category",
        "entity": "entity",
        "unit": "unit",
    }

    add_coords_cols = {
        "orig_cat_name": ["orig_cat_name", "category"],
        "cat_name_translation": ["cat_name_translation", "category"],
    }

    coords_terminologies = {
        "area": "ISO3",
        "category": "IPCC1996_KOR_INV",
        "scenario": "PRIMAP",
    }

    coords_defaults = {
        "source": "KOR-GHG-Inventory",
        "provenance": "measured",
        "area": "KOR",
        "scenario": "INV2022",
    }

    coords_value_mapping = {
        "cat_name_translation": cat_name_translations,
        "category": cat_codes,
    }

    # filtering after IF creation to be able to use the IPCC codes
    filter_remove = {
        "f1": {
            "category (IPCC1996_KOR_INV)": "\\IGNORE",
        },
        "livestock": {  # temp until double cat name problem is solved
            "category (IPCC1996_KOR_INV)": [
                "4.B.1",
                "4.B.10",
                "4.B.2",
                "4.B.3",
                "4.B.4",
                "4.B.5",
                "4.B.6",
                "4.B.7",
                "4.B.8",
                "4.B.9",
            ]
        },
    }

    filter_keep = {}

    meta_data = {
        "references": "http://www.gir.go.kr/home/file/readDownloadFile.do?fileId=5810&fileSeq=3",
        "rights": "",
        "contact": "mail@johannes-guetschow.de",
        "title": "Republic of Korea: National Greenhouse Gas Inventory Report 2022",
        "comment": "Read fom xlsx file by Johannes Gütschow",
        "institution": "Republic of Korea, Ministry of Environment, "
        "Greenhouse Gas Inventory and Research Center",
    }

    cols_for_space_stripping = []

    compression = dict(zlib=True, complevel=9)

    # ###
    # start data reading
    # ###

    # change working directory to script directory for proper folder names
    script_path = os.path.abspath(sys.argv[0])
    script_dir_name = os.path.dirname(script_path)
    os.chdir(script_dir_name)

    df_all = None

    for sheet in sheets_to_read:
        # read current sheet (one sheet per gas)
        df_current = pd.read_excel(
            input_folder / inventory_file,
            sheet_name=sheet,
            skiprows=3,
            nrows=146,
            usecols=cols_to_read,
            engine="openpyxl",
        )
        # drop all rows where the index cols (category code and name) are both NaN
        # as without one of them there is no category information
        df_current = df_current.dropna(axis=0, how="all", subset=index_cols)
        # set index. necessary for the stack operation in the conversion to long format
        # df_current = df_current.set_index(index_cols)
        # make sure all col headers are str
        df_current.columns = df_current.columns.map(str)
        # add columns
        for col in sheet_metadata.keys():
            df_current.insert(1, col, sheet_metadata[col][sheet])
        # aggregate to one df
        if df_all is None:
            df_all = df_current
        else:
            df_all = pd.concat([df_all, df_current])

    df_all = df_all.reset_index(drop=True)
    # rename category col because filtering produces problems with korean col names
    df_all = df_all.rename(columns={"분야·부문/연도": "category"})

    # create copies of category col for further processing
    df_all["orig_cat_name"] = df_all["category"]
    df_all["cat_name_translation"] = df_all["category"]

    # ###
    # convert to PRIMAP2 interchange format
    # ###
    data_if = pm2.pm2io.convert_wide_dataframe_if(
        df_all,
        coords_cols=coords_cols,
        add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        # coords_value_filling=coords_value_filling,
        # filter_remove=filter_remove,
        # filter_keep=filter_keep,
        meta_data=meta_data,
        convert_str=True,
        copy_df=True,  # we need the unchanged DF for the conversion step
    )

    filter_data(data_if, filter_remove=filter_remove)

    # conversion to PRIMAP2 native format
    data_pm2 = pm2.pm2io.from_interchange_format(data_if)
    # convert back to IF to have units in the fixed format
    data_pm2 = data_pm2.reset_coords(
        ["orig_cat_name", "cat_name_translation"], drop=True
    )
    data_if = data_pm2.pr.to_interchange_format()

    # ###
    # save data to IF and native format
    # ###
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"]), data_if
    )

    data_pm2 = pm2.pm2io.from_interchange_format(data_if)
    encoding = {var: compression for var in data_pm2.data_vars}
    data_pm2.pr.to_netcdf(
        output_folder / (output_filename + coords_terminologies["category"] + ".nc"),
        encoding=encoding,
    )

    # ###
    # conversion to ipcc 2006 categories
    # ###

    data_if_2006 = pm2.pm2io.convert_wide_dataframe_if(
        df_all,
        coords_cols=coords_cols,
        add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies_2006,
        coords_value_mapping=coords_value_mapping,
        meta_data=meta_data,
        convert_str=True,
        copy_df=True,  # don't mess up the dataframe when testing
    )

    cat_label = "category (" + coords_terminologies_2006["category"] + ")"
    # agg before mapping

    for cat_to_agg in aggregate_before_mapping:
        mask = data_if_2006[cat_label].isin(
            aggregate_before_mapping[cat_to_agg]["sources"]
        )
        df_test = data_if_2006[mask]

        if len(df_test) > 0:
            print(f"Aggregating category {cat_to_agg}")
            df_combine = df_test.copy(deep=True)

            time_format = "%Y"
            time_columns = [
                col
                for col in df_combine.columns.to_numpy()
                if matches_time_format(col, time_format)
            ]

            for col in time_columns:
                df_combine[col] = pd.to_numeric(df_combine[col], errors="coerce")

            df_combine = df_combine.groupby(
                by=[
                    "source",
                    "scenario (PRIMAP)",
                    "provenance",
                    "area (ISO3)",
                    "entity",
                    "unit",
                ]
            ).sum()

            df_combine = df_combine.drop(
                columns=[
                    "category (IPCC2006_PRIMAP)",
                    "orig_cat_name",
                    "cat_name_translation",
                ]
            )
            df_combine.insert(0, cat_label, cat_to_agg)
            df_combine.insert(
                1, "orig_cat_name", aggregate_before_mapping[cat_to_agg]["name"]
            )

            df_combine = df_combine.reset_index()

            if cat_to_agg in aggregate_before_mapping[cat_to_agg]["sources"]:
                filter_this_cat = {"f": {cat_label: cat_to_agg}}
                filter_data(data_if_2006, filter_remove=filter_this_cat)

            data_if_2006 = pd.concat([data_if_2006, df_combine])
        else:
            print(f"no data to aggregate category {cat_to_agg}")

    # filtering
    filter_data(data_if_2006, filter_remove=filter_remove_2006)

    # map 1 to 1 categories
    data_if_2006 = data_if_2006.replace({cat_label: cat_mapping})
    data_if_2006[cat_label].unique()

    # agg after mapping

    for cat_to_agg in aggregate_after_mapping:
        mask = data_if_2006[cat_label].isin(
            aggregate_after_mapping[cat_to_agg]["sources"]
        )
        df_test = data_if_2006[mask]

        if len(df_test) > 0:
            print(f"Aggregating category {cat_to_agg}")
            df_combine = df_test.copy(deep=True)

            time_format = "%Y"
            time_columns = [
                col
                for col in df_combine.columns.to_numpy()
                if matches_time_format(col, time_format)
            ]

            for col in time_columns:
                df_combine[col] = pd.to_numeric(df_combine[col], errors="coerce")

            df_combine = df_combine.groupby(
                by=[
                    "source",
                    "scenario (PRIMAP)",
                    "provenance",
                    "area (ISO3)",
                    "entity",
                    "unit",
                ]
            ).sum()

            df_combine = df_combine.drop(
                columns=[
                    "category (IPCC2006_PRIMAP)",
                    "orig_cat_name",
                    "cat_name_translation",
                ]
            )
            df_combine.insert(0, cat_label, cat_to_agg)
            df_combine.insert(
                1, "orig_cat_name", aggregate_after_mapping[cat_to_agg]["name"]
            )

            df_combine = df_combine.reset_index()

            if cat_to_agg in aggregate_after_mapping[cat_to_agg]["sources"]:
                filter_this_cat = {"f": {cat_label: cat_to_agg}}
                filter_data(data_if_2006, filter_remove=filter_this_cat)

            data_if_2006 = pd.concat([data_if_2006, df_combine])
        else:
            print(f"no data to aggregate category {cat_to_agg}")

    # conversion to PRIMAP2 native format
    data_pm2_2006 = pm2.pm2io.from_interchange_format(data_if_2006)
    # convert back to IF to have units in the fixed format
    data_pm2_2006 = data_pm2_2006.reset_coords(
        ["orig_cat_name", "cat_name_translation"], drop=True
    )
    data_if_2006 = data_pm2_2006.pr.to_interchange_format()
    # save IPCC2006 data

    filter_data(data_if_2006, filter_remove=filter_remove_after_agg)
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies_2006["category"]),
        data_if_2006,
    )

    encoding = {var: compression for var in data_pm2_2006.data_vars}
    data_pm2_2006.pr.to_netcdf(
        output_folder
        / (output_filename + coords_terminologies_2006["category"] + ".nc"),
        encoding=encoding,
    )
