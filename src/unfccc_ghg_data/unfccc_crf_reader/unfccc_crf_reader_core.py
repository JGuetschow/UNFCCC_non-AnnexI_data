"""
Core functions for the CRF / CRT reader

This file holds the core functions of the CRF reader.
Core function are used both for reading for final datasets as
well as for test-reading to check for new categories etc.
"""

import json
import os
import re
from collections import Counter
from collections.abc import Generator
from copy import deepcopy
from datetime import datetime, timedelta
from operator import itemgetter
from pathlib import Path
from typing import Optional, Union

import datalad as dl
import numpy as np
import pandas as pd
import primap2 as pm2
from treelib import Tree

from unfccc_ghg_data.helper import downloaded_data_path_UNFCCC, root_path

from . import crf_specifications as crf
from .util import BTR_urls, NoCRFFilesError

pd.set_option("future.no_silent_downcasting", True)


### reading functions
def convert_crf_table_to_pm2if(  # noqa: PLR0912, PLR0913, PLR0915
    df_table: pd.DataFrame,
    submission_year: int,
    entity_mapping: dict[str, str] | None = None,
    coords_defaults_input: dict[str, str] | None = None,
    filter_remove_input: dict[str, dict[str, str | list]] | None = None,
    filter_keep_input: dict[str, dict[str, str | list]] | None = None,
    meta_data_input: dict[str, str] | None = None,
    submission_type: str = "CRF",
    decimal_sep: str = ".",
    thousands_sep: str = ",",
) -> pd.DataFrame:
    """
    Convert a given pandas long format crf table to PRIMAP2 interchange format

    Parameters
    ----------
    df_table: pd.DataFrame
        Data to convert
    submission_year: int
        Year of submission
    entity_mapping: Optional[Dict[str,str]]
        Mapping of entities to PRIMAP2 format. Not necessary for all tables
    coords_defaults_input: Optional[Dict[str,str]],
        Additional default values for coordinates. (e.g. "Total" for `type`)
    filter_remove_input: Optional[Dict[str,Dict[str,Union[str,List]]]]
        Filter to remove data during conversion. The format is as in
        PRIMAP2
    filter_keep_input: Optional[Dict[str,Dict[str,Union[str,List]]]]
        Filter to keep only specified data during conversion.
        The format is as in PRIMAP2
    meta_data_input: Optional[Dict[str,str]]
        Meta data information. If values filled by this function automatically
        are given as input the automatic values are overwritten.
    submission_type: str default = "CRF"
        read CRF or CRF data
    decimal_sep: str default = '.'
        decimal separator to use to interpret the data.
    thousands_sep: str default = ','
        thousands separator to use to interpret the data.

    Returns
    -------
    pd.DataFrame:
        Pandas DataFrame containing the data in PRIMAP2 interchange format
        Metadata is stored as attrs in the DataFrame
    """
    # check type
    if submission_type not in ["CRF", "CRT", "CRTAI"]:
        raise ValueError("Type must be CRF, CRT, or CRTAI")  # noqa: TRY003

    coords_cols = {
        "category": "category",
        "entity": "entity",
        "unit": "unit",
        "sec_cats__class": "class",
        "area": "country",
        "data": "data",
    }

    # set scenario and terminologies
    if submission_type == "CRF":
        category_terminology = f"CRF2013_{submission_year}"
        class_terminology = "CRF2013"
        scenario = f"CRF{submission_year}"
        title = f"Data submitted in {submission_year} to the UNFCCC in the common "
        "reporting format (CRF)"
    else:
        category_terminology = f"CRT{submission_year}"
        class_terminology = f"CRT{submission_year}"
        scenario = f"CRT{submission_year}"
        title = (
            f"Data submitted in {submission_year} to the UNFCCC using the "
            f"common reporting tables (CRT)"
        )

    add_coords_cols = {
        #    "orig_cat_name": ["orig_cat_name", "category"],
    }

    coords_terminologies = {
        "area": "ISO3",
        "category": category_terminology,
        "scenario": "PRIMAP",
        "class": class_terminology,
    }

    coords_defaults = {
        "source": "UNFCCC",
        "provenance": "measured",
        "scenario": scenario,
    }
    if coords_defaults_input is not None:
        for key in coords_defaults_input.keys():
            coords_defaults[key] = coords_defaults_input[key]

    coords_value_mapping = {
        "unit": "PRIMAP1",
        "entity": "PRIMAP1",
    }
    if entity_mapping is not None:
        coords_value_mapping["entity"] = entity_mapping

    # coords_value_filling_template = {
    # }

    filter_remove = {
        "f1": {
            "category": ["\\IGNORE"],
        }
    }
    if filter_remove_input is not None:
        for key in filter_remove_input.keys():
            filter_remove[key] = filter_remove_input[key]

    filter_keep = {}
    if filter_keep_input is not None:
        for key in filter_keep_input.keys():
            filter_keep[key] = filter_keep_input[key]

    meta_data = {
        "rights": "",
        "contact": "mail@johannes-guetschow.de",
        "title": title,
        "comment": "Read fom xlsx file by Johannes Gütschow",
        "institution": "United Nations Framework Convention on Climate Change "
        "(www.unfccc.int)",
    }
    if submission_type in ["CRF", "CRTAI"]:
        meta_data[
            "references"
        ] = f"https://unfccc.int/ghg-inventories-annex-i-parties/{submission_year}"
    elif submission_year in BTR_urls.keys():
        meta_data["references"] = BTR_urls[submission_year]
    elif meta_data_input is not None:
        if "references" not in meta_data_input.keys():
            raise ValueError(  # noqa: TRY003
                f"Submission round {submission_year} unknown, please add metadata."
            )
    else:
        raise ValueError(  # noqa: TRY003
            f"Submission round {submission_year} unknown, please add metadata."
        )

    if meta_data_input is not None:
        for key in meta_data_input.keys():
            meta_data[key] = meta_data_input[key]

    # fix decimal separator
    sep_regexp_special = ["."]

    if decimal_sep != ".":
        if thousands_sep in sep_regexp_special:
            regex_thousands = f"([0-9]+)\\{thousands_sep}([0-9,]+)"
        else:
            regex_thousands = f"([0-9]+){thousands_sep}([0-9,]+)"
        if decimal_sep in sep_regexp_special:
            regex_decimal = f"([0-9]+)\\{decimal_sep}([0-9]+)"
        else:
            regex_decimal = f"([0-9]+){decimal_sep}([0-9]+)"
        # first remove thousand sep
        df_table = df_table.replace(
            to_replace=regex_thousands, value=r"\1\2", regex=True
        )
        # now replace the decimal sep by a dot
        df_table = df_table.replace(
            to_replace=regex_decimal, value=r"\1.\2", regex=True
        )

    df_table_if = pm2.pm2io.convert_long_dataframe_if(
        df_table,
        coords_cols=coords_cols,
        add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        # coords_value_filling=coords_value_filling,
        filter_remove=filter_remove,
        filter_keep=filter_keep,
        meta_data=meta_data,
        time_format="%Y",
    )
    return df_table_if


def read_crf_table(  # noqa: PLR0913, PLR0912, PLR0915
    country_codes: str | list[str],
    table: str,
    submission_year: int,
    data_year: int | list[int] | None = None,
    date_or_version: str | None = None,
    folder: str | None = None,
    submission_type: str = "CRF",
    debug: bool = False,
) -> tuple[pd.DataFrame, list[list], list[list], bool]:
    """
    Read CRF table for given year and country/countries

    Read CRF table for given submission year and country / or countries
    This function can read for multiple years and countries but only a single
    table. The reason is that combining data from different tables needs
    consistency checks while combining for different years and countries does not.

    The folder can either be given explicitly or if not given folders are determined
    from the submission_year and country_code variables

    Parameters
    ----------
    country_codes: str or list[str]
        ISO 3-letter country code or list of country codes
    table: str
        name of the table sheet in the CRF xlsx file
    submission_year: int
        Year of the submission of the data
    data_year: int or List of int (optional)
        if int a single data year will be read. if a list of ints is given these
        years will be read. If no nothing is given all data years will be read
    date_or_version: str (optional, default is None)
        readonly submission from the given date (CRF) or version (CRT/BTR)
        use "latest" to read the latest submissions
    folder: str (optional)
        Folder that contains the xls files. If not given folders are determined by the
        submissions_year and country_code variables
    submission_type: str default = "CRF"
        read CRF or CRT/BTR data
    debug: bool (optional)
        if true print some debug information like column headers

    Returns
    -------
    Tuple of parameters
        * First return parameter is the data as a pandas DataFrame in long format.
        * Second return parameter is a list of unknown categories / row headers.
        * Third return parameter holds information on data found in the last read row.
          This is used as a hint to check if table specifications might have to
          be adapted as country submitted tables are longer than expected.
        * The fourth return parameter is true if the worksheet to read in the file

    """
    # check type
    if submission_type not in ["CRF", "CRT", "CRTAI"]:
        raise ValueError("Type must be CRF, CRT, or CRTAI")  # noqa: TRY003

    if isinstance(country_codes, str):
        country_codes = [country_codes]

    # get file names and locations
    try:
        input_files = get_crf_files(
            country_codes=country_codes,
            submission_year=submission_year,
            data_year=data_year,
            date_or_version=date_or_version,
            folder=folder,
            submission_type=submission_type,
        )
        # nasty fix for cases where exporting ran overnight and not all files have
        # the same date_or_version. This is only applied for CRF as for CRT we use the
        # version as main identifier
        if submission_type == "CRF":
            if (date_or_version is not None) and (len(country_codes) == 1):
                if isinstance(data_year, list):
                    expected_files = len(data_year)
                elif isinstance(data_year, int):
                    expected_files = 1
                else:
                    expected_files = submission_year - 1990 - 1
                if len(input_files) < expected_files:
                    print(
                        f"Found only {len(input_files)} input files for "
                        f"{country_codes}. "
                        f"Expected {expected_files}."
                    )
                    print(
                        "Possibly exporting run overnight and some files have the "
                        "previous day as date."
                    )
                    date_datetime = datetime.strptime(date_or_version, "%d%m%Y")
                    date_datetime = date_datetime - timedelta(days=1)
                    prv_date = date_datetime.strftime("%d%m%Y")
                    more_input_files = get_crf_files(
                        country_codes=country_codes,
                        submission_year=submission_year,
                        data_year=data_year,
                        date_or_version=prv_date,
                        folder=folder,
                        submission_type=submission_type,
                    )
                    if len(more_input_files) > 0:
                        print(f"Found {len(more_input_files)} additional input files.")
                        input_files = input_files + more_input_files
                    else:
                        print("Found no additional input files")
    except Exception as ex:
        raise NoCRFFilesError(  # noqa: TRY003
            f"No files found for {country_codes}, "
            f"submission_year={submission_year}, "
            f"data_year={data_year}, "
            f"date/version={date_or_version}, "
            f"folder={folder}."
        ) from ex

    # get specification
    # if we only have a single country check if we might have a country specific
    # specification (currently only Australia, 2023)
    if len(country_codes) == 1:
        try:
            crf_spec = getattr(
                crf, f"{submission_type}{submission_year}_{country_codes[0]}"
            )
            print(
                f"Using country specific specification: "
                f"{submission_type}{submission_year}_{country_codes[0]}"
            )
        except:  # noqa: E722
            # no country specific specification, check for general specification
            try:
                crf_spec = getattr(crf, f"{submission_type}{submission_year}")
            except Exception as ex:
                raise ValueError(  # noqa: TRY003
                    f"No terminology exists for submission year " f"{submission_year}"
                ) from ex
    else:
        try:
            crf_spec = getattr(crf, f"{submission_type}{submission_year}")
        except Exception as ex:
            raise ValueError(  # noqa: TRY003
                f"No terminology exists for submission year " f"{submission_year}"
            ) from ex

    # now loop over files and read them
    df_all = None
    unknown_rows = []
    last_row_info = []
    not_present = False
    for file in input_files:
        file_info = get_info_from_crf_filename(file.name)
        try:
            int(file_info["data_year"])
            (
                df_this_file,
                unknown_rows_this_file,
                last_row_info_this_file,
            ) = read_crf_table_from_file(file, table, crf_spec[table], debug=debug)
            if df_all is None:
                df_all = df_this_file.copy(deep=True)
                unknown_rows = unknown_rows_this_file
                last_row_info = last_row_info_this_file
            else:
                df_all = pd.concat([df_this_file, df_all])
                unknown_rows = unknown_rows + unknown_rows_this_file
                last_row_info = last_row_info + last_row_info_this_file
        except ValueError as e:
            if e.args[0] == f"Worksheet named '{table}' not found":
                print(f"Table {table} not present")
                not_present = True
                pass
            else:
                print(f"Error when reading file {file}. Skipping file. Exception: {e}")
        except Exception as e:
            print(f"Error when reading file {file}. Skipping file. Exception: {e}")

    return df_all, unknown_rows, last_row_info, not_present


def read_crf_table_from_file(  # noqa: PLR0912, PLR0915
    file: Path,
    table: str,
    table_spec: dict[str, dict],
    debug: bool = False,
) -> tuple[pd.DataFrame, list[list], list[list]]:
    """
    Read single crf table from file

    Read a single CRF table from a given file. This is the core function of the CRF
    reading process as it reads the data from xls and performs the category mapping.

    Parameters
    ----------
    file: Path
        file to read from
    table: str
        table to read (name of the sheet in the xlsx file)
    table_spec: Dict[str, Dict]
        Specification for the given table, e.g. CRF2021["Table4"]
    debug: bool (optional)
        if true print some debug information like column headers

    Returns
    -------
    Tuple of parameters
        * First return parameter is the data as a pandas DataFrame in long format
        * Second return parameter is a list of unknown categories / row headers
        * Third return parameter holds information on data found in the last read row.
          This is used as a hint to check if table specifications might have to
          be adapted as country submitted tables are longer than expected.

    """
    # check if file exists and if not download
    # TODO: fix such that it also follows links (if the target of the link is a link
    #  check if that exists and if not download)
    if file.is_symlink():
        if not file.exists():
            dlds = dl.api.Dataset(root_path)
            dlds.get(file.relative_to(root_path))

    table_properties = table_spec["table"]
    file_info = get_info_from_crf_filename(file.name)

    # find non-unique categories in mapping
    all_cats_mapping = deepcopy(table_spec["sector_mapping"])
    # prep specification
    all_cats_mapping = prep_specification(
        specification=all_cats_mapping, country=file_info["party"]
    )
    all_cats = [cat[0][0] for cat in all_cats_mapping]

    unique_cats = [cat for (cat, count) in Counter(all_cats).items() if count == 1]
    unique_cat_tuples = [
        mapping for mapping in all_cats_mapping if mapping[0][0] in unique_cats
    ]
    unique_mapping = dict(
        zip(
            [tup[0][0] for tup in unique_cat_tuples],
            [tup[1] for tup in unique_cat_tuples],
        )
    )
    non_unique_cats = [cat for (cat, count) in Counter(all_cats).items() if count > 1]

    # prepare the sector hierarchy
    if non_unique_cats:
        # if we have non-unique categories present we need the information on
        # levels within the category hierarchy
        category_tree = create_category_tree(
            all_cats_mapping, table, file_info["party"]
        )

    # prepare index colum information
    cat_col = table_properties["col_for_categories"]
    index_cols = table_properties["categories"] + [cat_col]
    cols_for_space_stripping = [table_properties["col_for_categories"]]

    # read the data
    print(f"Reading table {table} for year {file_info['data_year']} from {file.name}.")
    skiprows = table_properties["firstrow"] - 1
    nrows = (
        table_properties["lastrow"] - skiprows + 1
    )  # read one row more to check if we reached the end
    # we read with user specific NaN treatment as the NaN treatment is part of
    # the conversion to PRIMAP2 format.
    df_raw = pd.read_excel(
        file,
        sheet_name=table,
        skiprows=skiprows,
        nrows=nrows,
        engine="openpyxl",
        na_values=[
            "-1.#IND",
            "-1.#QNAN",
            "-NaN",
            "-nan",
            "1.#IND",
            "1.#QNAN",
            "NULL",
            "NaN",
            "",
            " ",
        ],
        keep_default_na=False,
    )

    cols_to_drop = []
    # remove empty first column (because CRTables start with an empty column)
    # df_raw = df_raw.dropna(how="all", axis=1)
    if df_raw.iloc[:, 0].isna().all():
        cols_to_drop.append(df_raw.columns.to_numpy()[0])
    # select only first table by cutting everything after a all-nan column (unless
    # it's the first column)
    if debug:
        print(f"Header before table end detection: {df_raw.columns.to_numpy()}")
    for colIdx in range(1, len(df_raw.columns.values)):
        if (df_raw.iloc[:, colIdx].isna().all()) & (
            df_raw.columns[colIdx].startswith("Unnamed")
        ):
            cols_to_drop = cols_to_drop + list(df_raw.columns.to_numpy()[colIdx:])
            if debug:
                print(f"cols_to_drop: {cols_to_drop}")
            break

    if cols_to_drop is not None:
        df_raw = df_raw.drop(columns=cols_to_drop)

    #### prepare the header (2 row header, first entity, then unit)
    # We do this before removing columns and any other processing to
    # have consistent column names in the configuration and to avoid
    # "Unnamed: X" column names which appear after reading of merged
    # cells
    # the filling leads to long and a bit confusing headers, but as long
    # as pandas can not fill values of merged cells in all individual cells
    # we have to use some filling algorithm.
    df_header = df_raw.iloc[0 : len(table_properties["header"]) - 1].copy(deep=True)
    df_header.loc[-1] = df_header.columns.to_numpy()
    df_header.index = df_header.index + 1
    # replace "Unnamed: X" colum names by nan to fill from left in next step
    df_header = df_header.sort_index()
    df_header = df_header.replace(r"Unnamed: [0-9]{1,2}", np.nan, regex=True)
    header = []
    # fill nans with the last value from the left
    if "header_fill" in table_properties:
        for row in range(0, len(df_header)):
            if table_properties["header_fill"][row]:
                header.append(list(df_header.iloc[row].ffill()))
            else:
                header.append(list(df_header.iloc[row]))
    else:
        for row in range(0, len(df_header)):
            header.append(list(df_header.iloc[row].ffill()))

    # combine all non-unit rows into one
    entities = None
    units = None
    for idx, row in enumerate(header):
        if table_properties["header"][idx] == "unit":
            units = row
        elif entities is None:
            entities = row
        else:
            for col, value in enumerate(row):
                if str(value) != "nan":
                    entities[col] = f"{entities[col]} {value}"

    if units is None:
        raise ValueError(  # noqa: TRY003
            f"Specification for table {table} does not contain unit information."
        )

    # remove double spaces
    entities = [entity.strip() for entity in entities]
    entities = [re.sub("\\s+", " ", entity) for entity in entities]
    entities = [re.sub("_x000d_", "", entity) for entity in entities]
    entities = [re.sub("_x000D_", "", entity) for entity in entities]
    entities = [re.sub("\\s+", " ", entity) for entity in entities]

    # replace the old header
    if len(header) > 2:  # noqa: PLR2004
        df_current = df_raw.drop(index=df_raw.iloc[0 : len(header) - 2].index)
    else:
        df_current = df_raw

    df_current.iloc[0] = units
    df_current.columns = entities
    if debug:
        print(f"Columns present: {entities}")
    # remove all columns to ignore
    df_current = df_current.drop(columns=table_properties["cols_to_ignore"])

    # remove double spaces
    for col in cols_for_space_stripping:
        df_current[col] = df_current[col].str.strip()
        df_current[col] = df_current[col].replace("\\s+", " ", regex=True)

    # prepare for sector mapping by initializing result lists and
    # variables
    new_cats = [[""] * len(table_properties["categories"])] * len(df_current)

    # copy the header rows which are not part of the index (unit)
    new_cats[0] = [df_current.iloc[0][cat_col]] * len(table_properties["categories"])

    # do the sector mapping here as we need to keep track of unmapped categories
    # and also need to consider the order of elements for the mapping
    unknown_categories = []
    info_last_row = []
    if non_unique_cats:
        # need to initialize the tree parsing.
        last_parent = category_tree.get_node("root")
        all_nodes = set(
            [category_tree.get_node(node).tag for node in category_tree.nodes]
        )

        for idx in range(1, len(df_current)):
            current_cat = str(df_current.iloc[idx][cat_col])
            if current_cat in table_properties["stop_cats"]:
                # we've reached the end of the table, so stop processing
                # and remove all further rows
                df_current = df_current.drop(df_current.index[idx:])
                new_cats = new_cats[0:idx]
                break

            # check if current category is a child of the last node
            children = dict(
                [
                    [child.tag, child.identifier]
                    for child in category_tree.children(last_parent.identifier)
                ]
            )
            if current_cat in children.keys():
                # the current category is a child of the current parent
                # do the mapping
                node = category_tree.get_node(children[current_cat])
                new_cats[idx] = node.data[1]
                # check if the node has children
                new_children = category_tree.children(node.identifier)
                if new_children:
                    last_parent = node

            # two other possibilities
            # 1. The category is at a higher point in the hierarchy
            # 2. It's missing in the hierarchy
            # we have to first move up the hierarchy
            # first check if category is present at all
            elif current_cat in all_nodes:
                old_parent = last_parent

                while (current_cat not in children.keys()) and (
                    last_parent.identifier != "root"
                ):
                    last_parent = category_tree.get_node(
                        last_parent.predecessor(category_tree.identifier)
                    )
                    children = dict(
                        [
                            [child.tag, child.identifier]
                            for child in category_tree.children(last_parent.identifier)
                        ]
                    )

                if (last_parent.identifier == "root") and (
                    current_cat not in children.keys()
                ):
                    # we have not found the category as direct child of any of the
                    # predecessors. Thus it is missing in the specification in
                    # that place
                    print(
                        f"Unknown category '{current_cat}' found in {table} for "
                        f"{file_info['party']}, {file_info['data_year']} "
                        f"(last parent: {old_parent.tag})."
                    )
                    unknown_categories.append(
                        [
                            table,
                            file_info["party"],
                            current_cat,
                            file_info["data_year"],
                            idx,
                        ]
                    )
                    # copy back the parent info to continue with next category
                    last_parent = old_parent
                else:
                    # do the mapping
                    node = category_tree.get_node(children[current_cat])
                    new_cats[idx] = node.data[1]
                    # check if the node has children
                    new_children = category_tree.children(node.identifier)
                    if new_children:
                        last_parent = node
            else:
                print(
                    f"Unknown category '{current_cat}' found in {table} for "
                    f"{file_info['party']}, {file_info['data_year']}, {idx}."
                )
                unknown_categories.append(
                    [
                        table,
                        file_info["party"],
                        current_cat,
                        file_info["data_year"],
                        idx,
                    ]
                )
    else:
        for idx in range(1, len(df_current)):
            current_cat = str(df_current.iloc[idx][cat_col])
            if current_cat in table_properties["stop_cats"]:
                # we've reached the end of the table, so stop processing
                # and remove all further rows
                df_current = df_current.drop(df_current.index[idx:])
                new_cats = new_cats[0:idx]
                break
            else:
                if idx == len(df_current) - 1:
                    print(
                        f"found information in last row: category {current_cat}, "
                        f"row {idx}"
                    )
                    info_last_row.append(
                        [table, file_info["party"], current_cat, file_info["data_year"]]
                    )
                if current_cat in all_cats:
                    new_cats[idx] = unique_mapping[current_cat]

                else:
                    print(
                        f"Unknown category '{current_cat}' found in {table} for "
                        f"{file_info['party']}, {file_info['data_year']}."
                    )
                    unknown_categories.append(
                        [
                            table,
                            file_info["party"],
                            current_cat,
                            file_info["data_year"],
                            idx,
                        ]
                    )

    for idx, col in enumerate(table_properties["categories"]):
        df_current.insert(loc=idx, column=col, value=[cat[idx] for cat in new_cats])

    # set index
    df_current = df_current.set_index(index_cols)
    # process the unit information using the primap2 functions
    df_current = pm2.pm2io.nir_add_unit_information(
        df_current, **table_properties["unit_info"]
    )

    # convert to long format
    header_long = table_properties["categories"] + [
        "orig_cat_name",
        "entity",
        "unit",
        "time",
        "data",
    ]
    df_long = pm2.pm2io.nir_convert_df_to_long(
        df_current, file_info["data_year"], header_long=header_long
    )

    # add country information
    df_long.insert(0, column="country", value=file_info["party"])
    # df_long.insert(1, column="submission", value=f"CRF{file_info['submission_year']}")
    if "coords_defaults" in table_spec.keys():
        for col in table_spec["coords_defaults"]:
            df_long.insert(2, column=col, value=table_spec["coords_defaults"][col])

    return df_long, unknown_categories, info_last_row


def get_crf_files(  # noqa: PLR0912, PLR0913
    country_codes: Union[str, list[str]],
    submission_year: int,
    data_year: Optional[Union[int, list[int]]] = None,
    date_or_version: Optional[str] = None,
    folder: Optional[str] = None,
    submission_type: str = "CRF",
) -> list[Path]:
    """
    Find all files according to given parameters

    Parameters
    ----------
    country_codes: str or list[str]
        ISO 3-letter country code or list of country codes
    submission_year: int
        Year of the submission of the data for CRF and submission round for CRT/BTR
    data_year: int or List of int (optional)
        if int a single data year will be read. if a list of ints is given these
        years will be read. If no nothing is given all data years will be read
    date_or_version: str (optional, default is None)
        get files only for submission from the given date (CRF) or version (CRT/BTR)
        Use "latest" to get files for the latest submission
    folder: str (optional)
        Folder that contains the xls files. If not given folders are determined by the
        submissions_year and country_code variables
    submission_type: str default = "CRF"
        read CRF, CRT, or CRTAI data

    Returns
    -------
        List[Path]: list of Path objects for the files
    """
    if isinstance(country_codes, str):
        country_codes = [country_codes]
    input_files = []
    # get file names and locations
    # we're filtering for country and submission year here but in the repository setup
    # we should only have files for one country and submission in the folder. But the
    # function can also be used on a given folder and then the filter is useful.
    if folder is None:
        # use country default folders
        country_folders = get_country_folders(
            country_codes,
            submission_year=submission_year,
            submission_type=submission_type,
        )
    else:
        country_folders = [folder]

    file_filter_template = {}
    if submission_type in ["CRF", "CRTAI"]:
        file_filter_template["submission_year"] = submission_year
    # don't filter for submission year in BTR as it's the actual year and
    # not the submissions round (and we don't know yet if it will be the same
    # for all submission in one submission round)
    file_filter_template["party"] = country_codes
    if data_year is not None:
        file_filter_template["data_year"] = data_year

    for input_folder in country_folders:
        input_folder_path = Path(input_folder)
        if input_folder_path.exists():
            # if desired find the latest date_or_version and only read that
            # has to be done per country
            if submission_type == "CRF":
                if date_or_version == "latest":
                    for country in country_codes:
                        file_filter = file_filter_template.copy()
                        file_filter["party"] = country
                        dates = get_submission_dates(folder, file_filter)
                        file_filter["date"] = find_latest_date(dates)
                        input_files = input_files + filter_filenames(
                            input_folder_path.glob("*.xlsx"), **file_filter
                        )
                else:
                    file_filter = file_filter_template.copy()
                    if date_or_version is not None:
                        file_filter["date"] = date_or_version
                    input_files = input_files + filter_filenames(
                        input_folder_path.glob("*.xlsx"), **file_filter
                    )
            elif submission_type in ["CRT", "CRTAI"]:
                if date_or_version == "latest":
                    for country in country_codes:
                        file_filter = file_filter_template.copy()
                        file_filter["party"] = country
                        versions = get_submission_versions(folder, file_filter)
                        file_filter["version"] = find_latest_version(versions)
                        input_files = input_files + filter_filenames(
                            input_folder_path.glob("*.xlsx"), **file_filter
                        )
                else:
                    file_filter = file_filter_template.copy()
                    if date_or_version is not None:
                        file_filter["version"] = date_or_version
                    input_files = input_files + filter_filenames(
                        input_folder_path.glob("*.xlsx"), **file_filter
                    )
            else:
                raise ValueError(  # noqa: TRY003
                    f"Unknown submissions type: {submission_type}."
                    "Only CRF and CRT are allowed."
                )
    if len(input_files) == 0:
        raise ValueError(f"No input files found in {country_folders}")  # noqa: TRY003

    # make sure no files is in the list twice (happens when multiple input folder
    # contain the same submission which is possible when the country name is changed)
    files_added = set()
    unique_files = []
    for file in input_files:
        if file.name not in files_added:
            unique_files.append(file)
            files_added.add(file.name)

    return unique_files


def get_country_folders(
    country_codes: Union[str, list[str]],
    submission_year: int,
    submission_type: str = "CRF",
) -> list[Path]:
    """
    get folders which contain CRF or BTR/CRT submissions for given countries

    Parameters
    ----------
    country_codes :
        ISO 3-letter country code or list of country codes
    submission_year :
        Year of the submission of the data for CRF and submission round for CRT/BTR
    submission_type :
        read CRF, CRT, or CRTAI data

    Returns
    -------
        List[Path]: list of Path objects for the folders

    """
    if submission_type == "CRT":
        type_folder = "BTR"
    elif submission_type == "CRTAI":
        type_folder = "CRT"
    elif submission_type == "CRF":
        type_folder = submission_type
    else:
        raise ValueError("Type must be CRF, CRT, or CRTAI")  # noqa: TRY003
    data_folder = downloaded_data_path_UNFCCC
    submission_folder = f"{type_folder}{submission_year}"

    with open(data_folder / "folder_mapping.json") as mapping_file:
        folder_mapping = json.load(mapping_file)

    country_folders = []
    for country_code in country_codes:
        if country_code in folder_mapping:
            new_country_folders = folder_mapping[country_code]
            if isinstance(new_country_folders, str):
                # only one folder
                country_folders = [
                    *country_folders,
                    data_folder / new_country_folders / submission_folder,
                ]
            else:
                country_folders = country_folders + [
                    data_folder / folder / submission_folder
                    for folder in new_country_folders
                ]
        else:
            raise ValueError(  # noqa: TRY003
                f"No data folder found for country {country_code}. "
                f"Check if folder mapping is up to date_or_version."
            )
    return country_folders


def get_info_from_crf_filename(  # noqa: PLR0912
    filename: str,
) -> dict[str, Union[int, str]]:
    """
    Parse given file name and return a dict with information on contained data.

    Parameters
    ----------
    filename: str
        The file to analyze (without path)

    Returns
    -------
    dict with fields
        * party: the party that submitted the data (3 letter code)
        * submission_year: year of submission
        * data_year: year in which the emissions took place
        * date: date of the submission
        * version: version of the submission. if not given filled with V0.0
        * extra: rest of the file name

    """
    filename = os.path.splitext(filename)[0]
    name_parts = filename.split("_")
    file_info = {}
    if len(name_parts) >= 4:  # noqa: PLR2004
        # CRF file name convention (unfortunately also used for some CRT files)
        file_info["party"] = name_parts[0]
        file_info["submission_year"] = int(name_parts[1])
        try:
            file_info["data_year"] = int(name_parts[2])
        except:  # noqa: E722
            print(f"Data year string {name_parts[2]} could not be converted to int.")
            file_info["data_year"] = name_parts[2]
        file_info["date"] = name_parts[3]
        # the last part (time code) is missing for CRT tables in CRF sile format
        if len(name_parts) > 4:  # noqa: PLR2004
            file_info["extra"] = name_parts[4]
        else:
            file_info["extra"] = ""
        file_info["version"] = "V0.0"
    else:
        # not enough parts, we probably have a CRT file with different separator
        name_parts = filename.split("-")
        if len(name_parts) >= 6 and "DataEntry" not in name_parts:  # noqa: PLR2004
            if name_parts[1] == "CRT":
                file_info["party"] = name_parts[0]
                file_info["submission_year"] = int(name_parts[2])
                file_info["version"] = name_parts[3]
                try:
                    file_info["data_year"] = int(name_parts[4])
                except:  # noqa: E722
                    print(
                        f"Data year string {name_parts[4]} "
                        "could not be converted to int."
                    )
                    file_info["data_year"] = name_parts[4]
                file_info["date"] = name_parts[5]
                # treat time code and note as optional
                if len(name_parts) > 6:  # noqa: PLR2004
                    file_info["extra"] = name_parts[6]
                else:
                    file_info["extra"] = ""
            else:
                message = f"File {filename} is not a valid CRF or CRT file."
                raise ValueError(message)
        else:
            message = f"File {filename} is not a valid CRF or CRT file."
            raise ValueError(message)

    return file_info


def filter_filenames(  # noqa: PLR0913
    files_to_filter: list[Path] | Generator[Path, None, None],
    party: Optional[Union[str, list[str]]] = None,
    data_year: Optional[Union[int, list[int]]] = None,
    submission_year: Optional[str] = None,
    date: Optional[str] = None,
    version: Optional[str] = None,
) -> list[Path]:
    """Filter a list of filenames of CRF/CRT files

    Parameters
    ----------
    files_to_filter: List[Path]
        List with pathlib.Path objects for the filenames to filter
    party: Optional[Union[str, List[str]]] (default: None)
        List of country codes or single country code. If given only files
        for this(these) country-code(s) will be returned.
    data_year: Optional[Union[int, List[int]]] (default: None)
        List of data years or single year. If given only files for this
        (these) year(s) will be returned
    submission_year: Optional[str] (default: None)
        List of submission years or single year. If given only files with the
        given submission year(s) will be returned
    date: Optional[str] (default: None)
        Date. If given only files with the given submission date will be returned
    version: Optional[str] (default: None)
        Date. If given only files with the given submission version (CRT/BTR)

    Returns
    -------
        list with pathlib Path objects for the files matching the filter

    """
    file_filter = {}
    if party is not None:
        file_filter["party"] = party
    if submission_year is not None:
        file_filter["submission_year"] = submission_year
    if data_year is not None:
        file_filter["data_year"] = data_year
    if date is not None:
        file_filter["date"] = date
    if version is not None:
        file_filter["version"] = version

    filtered_files = []
    for file in files_to_filter:
        if not file.is_dir():
            try:
                file_info = get_info_from_crf_filename(file.name)
                if check_crf_file_info(file_info, file_filter):
                    filtered_files.append(file)
            except ValueError:
                pass

    return filtered_files


def check_crf_file_info(  # noqa: PLR0911, PLR0912
    file_info: dict,
    file_filter: dict,
) -> bool:
    """
    Check if a CRF file has given properties

    Parameters
    ----------
    file_info: Dict
        the file info dict of a CRF xlsx file as returned by
        `get_info_from_crf_filename`

    file_filter: Dict
        possible keys are `party`, `data_year`, `submission_year` and `date_or_version`
        with functionality as in `filter_filenames`

    Returns
    -------
        bool: `True` if the file info matches the filter and `False` if not

    """
    if "submission_year" in file_filter.keys():
        if file_info["submission_year"] != file_filter["submission_year"]:
            return False
    if "date" in file_filter.keys():
        if file_info["date"] != file_filter["date"]:
            return False
    if "version" in file_filter.keys():
        if file_info["version"] != file_filter["version"]:
            return False
    if "data_year" in file_filter.keys():
        if isinstance(file_filter["data_year"], int):
            if file_info["data_year"] != file_filter["data_year"]:
                return False
        elif file_info["data_year"] not in file_filter["data_year"]:
            return False
    if "party" in file_filter.keys():
        if isinstance(file_filter["party"], str):
            if file_info["party"] != file_filter["party"]:
                return False
        elif file_info["party"] not in file_filter["party"]:
            return False
    return True


def create_category_tree(
    specification: list[list],
    table: str,
    country: Optional[str] = None,
) -> Tree:
    """
    Create a category hierarchy tree from a CRF table specification

    Create a treelib Tree for the categorical hierarchy from a CRF
    table specification.

    The tree is used to parse the row headers in CRF xlsx files and assign the
    correct categories to non-unique row headers.

    Parameters
    ----------
    specification: List[List]
        The `sector_mapping` dict of a table specification

    table: str
        Name of the table. Mainly used for output so error messages can
        be linked to tables

    country: str (optional)
        Country name to build the table for. Some categories are country dependent.
        To include them in the tree the country name has to be specified. If no
        country name is given the generic tree will be built.

    """
    # small sanity check on the specification
    if len(specification[0]) < 3:  # noqa: PLR2004
        raise ValueError(  # noqa: TRY003
            f"Error: Specification for Table {table} has non-unique "
            "categories and need level specifications"
        )

    # initialize variables for tree building
    parent_info = [
        {
            "level": -1,
            "id": "root",
        }
    ]
    category_tree = Tree()
    category_tree.create_node(table, "root")
    last_cat_info = {
        "level": 0,
        "category": "",
        "id": "root",
    }

    # prep mappings
    specification_list = prep_specification(
        specification=specification, country=country
    )

    # build a tree from specification
    # when looping over the categories present in the table
    # to read data from we walk along this tree
    for idx, mapping in enumerate(specification_list):
        current_cat = mapping[0]
        current_cat_level = mapping[2]
        if len(current_cat) > 1:
            message = (
                "More than one category names in mapping rule. "
                "This is currently not supported. "
                "Use country specific mappings to incorporte differences in "
                f"category names. Rule: {mapping}, Country: {country}"
            )
            print(message)
            raise ValueError(message)
        current_cat = current_cat[0]

        if current_cat_level == last_cat_info["level"]:
            # cat has the same level as preceeding one, so no change to
            # parent node
            category_tree.create_node(
                current_cat, idx, parent=parent_info[-1]["id"], data=mapping
            )
        elif current_cat_level == last_cat_info["level"] + 1:
            # the current category is one level further away from
            # the trunk of the tree. This means that
            # * the previous category is its parent
            # add it to parent info
            parent_info.append(
                {
                    "id": last_cat_info["id"],
                    "tag": last_cat_info["category"],
                    "level": last_cat_info["level"],
                }
            )
            # add the category as new node
            category_tree.create_node(
                current_cat, idx, parent=parent_info[-1]["id"], data=mapping
            )

        elif current_cat_level < last_cat_info["level"]:
            # the new level is smaller (closer to the trunk)
            # than the last one. Thus, we remove all parents
            # from this level on
            parent_info = parent_info[0 : current_cat_level + 1]
            category_tree.create_node(
                current_cat, idx, parent=parent_info[-1]["id"], data=mapping
            )
        else:
            # increase in levels of more than one is not allowed
            raise ValueError(  # noqa: TRY003
                f"Error in sector hierarchy for table {table}, category {current_cat}: "
                f"Category level is {current_cat_level} and parent level is "
                f"{parent_info[-1]['level']}"
            )

        # set last_cat_info
        last_cat_info["category"] = current_cat
        last_cat_info["level"] = current_cat_level
        last_cat_info["id"] = idx

    return category_tree


def prep_specification(
    specification: list[list],
    country: Optional[str] = None,
) -> list[list]:
    """
    Prepare specification to build tree or use directly

    Unifies data format and filter for country

    Parameters
    ----------
    specification :
        The table specification to process
    country :
        Country to filter for

    Returns
    -------
        list with modified specification

    """
    # prep mappings (make sure first item is a list)
    specification_list = [listify(mapping) for mapping in specification]

    # filter categories in case country is given
    if country is not None:
        # remove country tags from categories and mark categories
        # for other countries for removal
        specification_list = [
            filter_category(mapping, country) for mapping in specification_list
        ]
        # remove the categories for other countries
        specification_list = [
            mapping for mapping in specification_list if mapping[0] != ["\\REMOVE"]
        ]
    return specification_list


def listify(mapping: list) -> list:
    """Make sure first item of mapping is a list"""
    if isinstance(mapping[0], str):
        mapping[0] = [mapping[0]]
    elif isinstance(mapping[0], list):
        pass
    else:
        raise TypeError(  # noqa: TRY003
            f"First element of mapping has to be str or list: {mapping}"
        )
    return mapping


def filter_category(
    mapping: list,
    country: str,
) -> list[str]:
    r"""
    Check if category mapping suitable for country

    This function checks if a category mapping is suitable for the given country.
    If it is the country information will be removed and the new mapping returned.
    If it is not suitable it will be returned with category name "\\REMOVE" such that
    it can be removed from the mapping by the calling function.

    Parameters
    ----------
    mapping: List
        mapping for a single category
    country: str
        iso 3-letter code of the country

    Returns
    -------
    List: updated mapping

    """
    string_exclude = "\\C!-"
    string_include = "\\C-"
    regex_exclude = r"\\C!-([A-Z\-]+)\\"
    regex_exclude_full = r"(\\C!-[A-Z\-]+\\)"
    regex_include = r"\\C-([A-Z\-]+)\\"
    regex_include_full = r"(\\C-[A-Z\-]+\\)"
    new_mapping = mapping.copy()
    new_items = []
    for item in mapping[0]:
        if item.startswith(string_exclude):
            re_result = re.search(regex_exclude, item)
            countries_ex = re_result.group(1)
            countries_ex = countries_ex.split("-")
            if country not in countries_ex:
                re_result = re.search(regex_exclude_full, item)
                new_items.append(item[len(re_result.group(1)) + 1 :])
        elif item.startswith(string_include):
            re_result = re.search(regex_include, item)
            countries_in = re_result.group(1)
            countries_in = countries_in.split("-")
            if country in countries_in:
                re_result = re.search(regex_include_full, item)
                new_items.append(item[len(re_result.group(1)) + 1 :])
        else:
            new_items.append(item)

    if not new_items:
        new_items = ["\\REMOVE"]
    new_mapping[0] = new_items
    return new_mapping


def get_latest_date_for_country(
    country_code: str,
    submission_year: int,
    submission_type: str = "CRF",
) -> str:
    """
    Find the latest submission date_or_version (CRF) or version (CRT) for a country

    Parameters
    ----------
    country_code: str
        3-letter country code
    submission_year: int
        Year of the submission to find the l;atest date_or_version for
    submission_type: str, default CRF
        Check for CRF, CRT, or CRTAI tables

    Returns
    -------
        str: string with date_or_version / version
    """
    with open(downloaded_data_path_UNFCCC / "folder_mapping.json") as mapping_file:
        folder_mapping = json.load(mapping_file)

    if country_code in folder_mapping:
        file_filter = {
            "party": country_code,
        }
        if submission_type == "CRF":
            type_folder = submission_type
            date_format = "%d%m%Y"
            file_filter["submission_year"] = submission_year
        elif submission_type == "CRT":
            type_folder = "BTR"
            if country_code == "AUS" and submission_year == 1:
                date_format = "%d%m%Y"
            else:
                date_format = "%Y%m%d"
            # don't filter for submission year in BTR as it's the actual year and
            # not the submissions round (and we don't know yet if it will be the same
            # for all submission in one submission round)
        elif submission_type == "CRTAI":
            type_folder = "CRT"
            date_format = "%Y%m%d"
            file_filter["submission_year"] = submission_year
        else:
            raise ValueError("Type must be CRF, CRT, or CRTAI")  # noqa: TRY003

        country_folders = folder_mapping[country_code]
        if isinstance(country_folders, str):
            # only one folder
            submission_date = find_latest_date(
                get_submission_dates(
                    downloaded_data_path_UNFCCC
                    / country_folders
                    / f"{type_folder}{submission_year}",
                    file_filter,
                ),
                date_format=date_format,
            )
        else:
            dates = []
            for folder in country_folders:
                folder_submission = (
                    downloaded_data_path_UNFCCC
                    / folder
                    / f"{type_folder}{submission_year}"
                )
                if folder_submission.exists():
                    dates = dates + get_submission_dates(folder_submission, file_filter)
            submission_date = find_latest_date(dates, date_format=date_format)
    else:
        raise ValueError(  # noqa: TRY003
            f"No data folder found for country {country_code}. "
            f"Check if folder mapping is up to date_or_version."
        )

    return submission_date


def get_latest_version_for_country(
    country_code: str,
    submission_round: int,
    submission_type: str = "CRT",
) -> str:
    """
    Find the latest submission version (CRT) for a country

    Parameters
    ----------
    country_code: str
        3-letter country code
    submission_round: int
        Submission round to find the latest version for
    submission_type: str, default CRT
        Type of submission: CRT (from BRT) or CRTAI (from AnnexI National
        Inventory Submission)

    Returns
    -------
        str: string with date_or_version / version
    """
    with open(downloaded_data_path_UNFCCC / "folder_mapping.json") as mapping_file:
        folder_mapping = json.load(mapping_file)

    if country_code in folder_mapping:
        file_filter = {
            "party": country_code,
        }

        country_folders = folder_mapping[country_code]
        if submission_type == "CRT":
            subfolder = f"BTR{submission_round}"
        elif submission_type == "CRTAI":
            subfolder = f"CRT{submission_round}"
        else:
            raise ValueError("Type must be CRT or CRTAI")  # noqa: TRY003
        if isinstance(country_folders, str):
            # only one folder
            submission_version = find_latest_version(
                get_submission_versions(
                    downloaded_data_path_UNFCCC / country_folders / subfolder,
                    file_filter,
                ),
            )
        else:
            versions = []
            for folder in country_folders:
                folder_submission = downloaded_data_path_UNFCCC / folder / subfolder
                if folder_submission.exists():
                    versions = versions + get_submission_versions(
                        folder_submission, file_filter
                    )
            submission_version = find_latest_version(versions)
    else:
        raise ValueError(  # noqa: TRY003
            f"No data folder found for country {country_code}. "
            f"Check if folder mapping is up to date_or_version."
        )

    return submission_version


def get_submission_dates(
    folder: Path,
    file_filter: dict[str, Union[str, int, list]],
) -> list[str]:
    """
    Return all submission dates available in a folder

    Parameters
    ----------
    folder: Path
        Folder to analyze

    file_filter: Dict[str, Union[str, int, List]]
        Dict with possible fields "party", "submission_year", "data_year"

    Returns
    -------
        List[str]:
            List of dates as str
    """
    if "date" in file_filter:
        raise ValueError(  # noqa: TRY003
            "'date' present in 'file_filter'. This makes no sense as "
            "the function's purpose is to return available dates."
        )

    if folder.exists():
        files = filter_filenames(folder.glob("*.xlsx"), **file_filter)
    else:
        raise ValueError(f"Folder {folder} does not exist")  # noqa: TRY003

    dates = [get_info_from_crf_filename(file.name)["date"] for file in files]
    dates = list(set(dates))

    return dates


def get_submission_versions(
    folder: Path,
    file_filter: dict[str, Union[str, int, list]],
) -> list[str]:
    """
    Return all submission versions available in a folder.

    This function only works for CRT files as CRF files do not contain a version and
    the field is filled with 0.0 for all CRF files.

    There is one BTR submission where the CRT files use the CRF naming convention
    and don't have a version number (Australia BTR1). It uses 0.0 as version number.

    Parameters
    ----------
    folder: Path
        Folder to analyze

    file_filter: Dict[str, Union[str, int, List]]
        Dict with possible fields "party", "submission_year", "data_year"

    Returns
    -------
        List[str]:
            List of versions as str
    """
    if "version" in file_filter:
        raise ValueError(  # noqa: TRY003
            "'version' present in 'file_filter'. This makes no sense as "
            "the function's purpose is to return available versions."
        )

    if "CRF" in folder.name:
        raise ValueError(  # noqa: TRY003
            "'CRF' present in 'folder_name'. Function only works on CRT files"
        )

    if folder.exists():
        files = filter_filenames(folder.glob("*.xlsx"), **file_filter)
    else:
        raise ValueError(f"Folder {folder} does not exist")  # noqa: TRY003

    dates = [get_info_from_crf_filename(file.name)["version"] for file in files]
    dates = list(set(dates))

    return dates


def get_submission_parties(
    folder: Path,
    file_filter: dict[str, Union[str, int, list]],
) -> list[str]:
    """
    Return all submission parties available in a folder

    Parameters
    ----------
    folder: Path
        Folder to analyze

    file_filter: Dict[str, Union[str, int, List]]
        Dict with possible fields "submission_year", "data_year", "date", "version"

    Returns
    -------
    List[str]:
        List of parties as str
    """
    if "party" in file_filter:
        raise ValueError(  # noqa: TRY003
            "'party' present in 'file_filter'. This makes no sense as "
            "the function's purpose is to return available parties."
        )

    if folder.exists():
        files = filter_filenames(list(folder.glob("*.xlsx")), **file_filter)
    else:
        raise ValueError(f"Folder {folder} does not exist")  # noqa: TRY003

    parties = [get_info_from_crf_filename(file.name)["party"] for file in files]
    parties = list(set(parties))

    return parties


def find_latest_date(
    dates: list[str],
    date_format: str = "%d%m%Y",
) -> str:
    """
    Return the latest date_or_version in a list of dates as str in the format ddmmyyyy

    Parameters
    ----------
    dates: List[str]
        List of dates
    date_format: str, default "%d%m%Y"
        Format for the date_or_version. Unfortunately CRF uses %d%m%Y while CRT uses
        %Y%m%d with some exceptions for early submissions which use the CRF file namig
        scheme

    Returns
    -------
        str: latest date_or_version
    """
    if len(dates) > 0:
        dates_datetime = [
            [date, datetime.strptime(date, date_format)] for date in dates
        ]
        dates_datetime = sorted(dates_datetime, key=itemgetter(1))
    else:
        raise ValueError("Passed list of dates is empty")  # noqa: TRY003

    return dates_datetime[-1][0]


def find_latest_version(
    versions: list[str],
) -> str:
    """
    Return the latest version in a list of versions as str

    Parameters
    ----------
    versions: List[str]
        List of versions

    Returns
    -------
        str: latest date_or_version
    """
    # TODO: use mayor and minor version numbers. currently 0.11 will be judged as
    #  lower than 0.2
    if len(versions) > 0:
        versions_float = [[version, float(version[1:])] for version in versions]
        versions_float = sorted(versions_float, key=itemgetter(1))
    else:
        raise ValueError("Passed list of versions is empty")  # noqa: TRY003

    return versions_float[-1][0]
