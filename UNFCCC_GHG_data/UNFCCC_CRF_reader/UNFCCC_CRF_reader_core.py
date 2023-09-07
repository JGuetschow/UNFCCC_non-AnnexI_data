"""
This file holds the core functions of the CRF reader.
Core function are used both for reading for final datasets as
well as for test-reading to check for new categories etc.
"""

import re
import os
import json
import numpy as np
import pandas as pd
import primap2 as pm2
from pathlib import Path
from treelib import Tree
from operator import itemgetter
from collections import Counter
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime, timedelta
from . import crf_specifications as crf
from .util import NoCRFFilesError
from UNFCCC_GHG_data.helper import downloaded_data_path_UNFCCC

### reading functions
def convert_crf_table_to_pm2if(
        df_table: pd.DataFrame,
        submission_year: int,
        entity_mapping: Optional[Dict[str,str]]=None,
        coords_defaults_input: Optional[Dict[str,str]]=None,
        filter_remove_input: Optional[Dict[str,Dict[str,Union[str,List]]]]=None,
        filter_keep_input: Optional[Dict[str,Dict[str,Union[str,List]]]]=None,
        meta_data_input: Optional[Dict[str,str]]=None,
) -> pd.DataFrame:
    """
    Converts a given pandas long format crf table to PRIMAP2 interchange format

    Parameters
    __________
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

    Returns
    _______
        pd.DataFrame:
            Pandas DataFrame containing the data in PRIMAP2 interchange format
            Metadata is stored as attrs in the DataFrame
    """

    coords_cols = {
        "category": "category",
        "entity": "entity",
        "unit": "unit",
        "sec_cats__class": "class",
        "area": "country",
        "data": "data",
    }

    add_coords_cols = {
    #    "orig_cat_name": ["orig_cat_name", "category"],
    }

    coords_terminologies = {
        "area": "ISO3",
        "category": f"CRF2013_{submission_year}",
        "scenario": "PRIMAP",
        "class": "CRF2013",
    }

    coords_defaults = {
        "source": "UNFCCC",
        "provenance": "measured",
        "scenario": f"CRF{submission_year}",
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

    #coords_value_filling_template = {
    #}

    filter_remove = {
        "f1": {
            "category": ["\IGNORE"],
        }
    }
    if filter_remove_input is not None:
        for key in filter_remove_input.keys():
            filter_remove[key] = filter_remove_input[key]

    filter_keep = {
    }
    if filter_keep_input is not None:
        for key in filter_keep_input.keys():
            filter_keep[key] = filter_keep_input[key]


    meta_data = {
        "references": f"https://unfccc.int/ghg-inventories-annex-i-parties/{submission_year}",
        "rights": "",
        "contact": "mail@johannes-guetschow.de",
        "title": f"Data submitted in {submission_year} to the UNFCCC in the common reporting format (CRF)",
        "comment": "Read fom xlsx file by Johannes Gütschow",
        "institution": "United Nations Framework Convention on Climate Change (www.unfccc.int)",
    }
    if meta_data_input is not None:
        for key in meta_data_input.keys():
            meta_data[key] = meta_data_input[key]

    df_table_if = pm2.pm2io.convert_long_dataframe_if(
        df_table,
        coords_cols=coords_cols,
        add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        #coords_value_filling=coords_value_filling,
        filter_remove=filter_remove,
        filter_keep=filter_keep,
        meta_data=meta_data,
        time_format="%Y",
    )
    return df_table_if


def read_crf_table(
        country_codes: Union[str, List[str]],
        table: str,
        submission_year: int,
        data_year: Optional[Union[int, List[int]]]=None,
        date: Optional[str]=None,
        folder: Optional[str]=None,
) -> Tuple[pd.DataFrame, List[List], List[List]]:
    """
    Read CRF table for given submission year and country / or countries
    This function can read for multiple years and countries but only a single
    table. The reason is that combining data from different tables needs
    consistency checks while combining for different years and countries does not.

    The folder can either be given explicitly or if not given folders are determined
    from the submission_year and country_code variables

    Parameters
    __________

    country_codes: str or list[str]
        ISO 3-letter country UNFCCC_GHG_data or list of country codes

    table: str
        name of the table sheet in the CRF xlsx file

    submission_year: int
        Year of the submission of the data

    data_year: int or List of int (optional)
        if int a single data year will be read. if a list of ints is given these
        years will be read. If no nothing is given all data years will be read

    date: str (optional, default is "latest")
        readonly submission from the given date

    folder: str (optional)
        Folder that contains the xls files. If not given fodlers are determined by the
        submissions_year and country_code variables

    Returns
    _______
        Tuple[pd.DataFrame, List[List], List[List]]:
        * First return parameter is the data as a pandas DataFrame in long format
        * Second return parameter is a list of unknown categories / row headers
        * Third return parameter holds information on data found in the last read row.
          This is used as a hint to check if table specifications might have to be adapted
          as country submitted tables are longer than expected.

    """
    if isinstance(country_codes, str):
        country_codes = [country_codes]

    # get file names and locations
    input_files = get_crf_files(country_codes=country_codes,
                                submission_year=submission_year,
                                data_year=data_year,
                                date=date,
                                folder=folder)
    # nasty fix for cases where exporting ran overnight and not all files have the same date
    if (date is not None) and (len(country_codes)==1):
        if isinstance(data_year, list):
            expected_files = len(data_year)
        elif isinstance(data_year, int):
            expected_files = 1
        else:
            expected_files = submission_year - 1990 - 1
        if len(input_files) < expected_files:
            print(f"Found only {len(input_files)} input files for {country_codes}. "
                  f"Expected {expected_files}.")
            print(f"Possibly exporting run overnight and some files have the previous day as date.")
            date_datetime = datetime.strptime(date, "%d%m%Y")
            date_datetime = date_datetime - timedelta(days=1)
            prv_date = date_datetime.strftime("%d%m%Y")
            more_input_files = get_crf_files(country_codes=country_codes,
                                             submission_year=submission_year,
                                             data_year=data_year,
                                             date=prv_date,
                                             folder=folder)
            if len(more_input_files) > 0:
                print(f"Found {len(more_input_files)} additional input files.")
                input_files = input_files + more_input_files
            else:
                print(f"Found no additional input files")

    if input_files == []:
        raise NoCRFFilesError(f"No files found for {country_codes}, "
                              f"submission_year={submission_year}, "
                              f"data_year={data_year}, "
                              f"date={date}, "
                              f"folder={folder}.")

    # get specification
    # if we only have a single country check if we might have a country specific
    # specification (currently only Australia, 2023)
    if len(country_codes) == 1:
        try:
            crf_spec = getattr(crf, f"CRF{submission_year}_{country_codes[0]}")
            print(f"Using country specific specification: " 
                  f"CRF{submission_year}_{country_codes[0]}")
        except:
            # no country specific specification, check for general specification
            try:
                crf_spec = getattr(crf, f"CRF{submission_year}")
            except:
                raise ValueError(f"No terminology exists for submission year "
                                 f"{submission_year}")
    else:
        try:
            crf_spec = getattr(crf, f"CRF{submission_year}")
        except:
            raise ValueError(f"No terminology exists for submission year "
                             f"{submission_year}")

    # now loop over files and read them
    df_all = None
    unknown_rows = []
    last_row_info = []
    for file in input_files:
        file_info = get_info_from_crf_filename(file.name)
        try:
            int(file_info["data_year"])
            df_this_file, unknown_rows_this_file, last_row_info_this_file = \
                read_crf_table_from_file(file, table, crf_spec[table])
            if df_all is None:
                df_all = df_this_file.copy(deep=True)
                unknown_rows = unknown_rows_this_file
                last_row_info = last_row_info_this_file
            else:
                df_all = pd.concat([df_this_file, df_all])
                unknown_rows = unknown_rows + unknown_rows_this_file
                last_row_info = last_row_info + last_row_info_this_file
        except Exception as e:
            print(f"Error when reading file {file}. Skipping file. Exception: {e}")

    return df_all, unknown_rows, last_row_info


def read_crf_table_from_file(
        file: Path,
        table: str,
        table_spec: Dict[str, Dict],
) -> Tuple[pd.DataFrame, List[List], List[List]]:
    """
    Read a single CRF table from a given file. This is the core function of the CRF
    reading process as it reads the data from xls and performs the category mapping.

    Parameters
    __________
    file: Path
        file to read from

    table: str
        table to read (name of the sheet in the xlsx file)

    table_spec: Dict[str, Dict]
        Specification for the given table, e.g. CRF2021["Table4"]

    Returns
    _______
        Tuple[pd.DataFrame, List[List], List[List]]:
        * First return parameter is the data as a pandas DataFrame in long format
        * Second return parameter is a list of unknown categories / row headers
        * Third return parameter holds information on data found in the last read row.
          This is used as a hint to check if table specifications might have to be adapted
          as country submitted tables are longer than expected.

    TODO: add verbosity option for debugging?
    """

    table_properties = table_spec["table"]
    file_info = get_info_from_crf_filename(file.name)

    # find non-unique categories in mapping
    all_cats_mapping = table_spec["sector_mapping"]
    all_cats = [cat[0] for cat in all_cats_mapping]

    unique_cats = [cat for (cat, count) in Counter(all_cats).items() if count == 1]
    unique_cat_tuples = [mapping for mapping in all_cats_mapping if mapping[0] in unique_cats]
    unique_mapping = dict(zip([tup[0] for tup in unique_cat_tuples],
                              [tup[1] for tup in unique_cat_tuples]))
    non_unique_cats = [cat for (cat, count) in Counter(all_cats).items() if count > 1]

    # prepare the sector hierarchy
    if non_unique_cats:
        # if we have non-unique categories present we need the information on
        # levels within the category hierarchy
        category_tree = create_category_tree(all_cats_mapping, table, file_info["party"])

    # prepare index colum information
    cat_col = table_properties["col_for_categories"]
    index_cols = table_properties["categories"] + [cat_col]
    cols_for_space_stripping = [table_properties["col_for_categories"]]

    # read the data
    print(f"Reading table {table} for year {file_info['data_year']} from {file.name}.")
    skiprows = table_properties["firstrow"] - 1
    nrows = table_properties["lastrow"] - skiprows + 1 # read one row more to check if we reached the end
    # we read with user specific NaN treatment as the NaN treatment is part of the conversion to
    # PRIMAP2 format.
    df_raw = pd.read_excel(file, sheet_name=table, skiprows=skiprows , nrows=nrows, engine="openpyxl",
                               na_values=['-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN',
                                          'NULL', 'NaN', ''], keep_default_na=False)

    if len(df_raw) < nrows:
        #print(f"read data truncated because of all-nan rows")
        last_row_nan = True
    else:
        last_row_nan = False
    
    # remove empty columns (for Australia tables start with an empty column)
    df_raw = df_raw.dropna(how='all', axis=1)
    
    #### prepare the header (2 row header, first entity, then unit)
    # We do this before removing columns and any other processing to
    # have consistent column names in the configuration and to avoid
    # "Unnamed: X" column names which appear after reading of merged
    # cells
    # the filling leads to long and a bit confusing headers, but as long
    # as pandas can not fill values of merged cells in all individual cells
    # we have to use some filling algorithm.
    df_header = df_raw.iloc[0:len(table_properties["header"])-1].copy(deep=True)
    df_header.loc[-1] = df_header.columns.values
    df_header.index = df_header.index + 1
    # replace "Unnamed: X" colum names by nan to fill from left in next step
    df_header = df_header.sort_index()
    df_header = df_header.replace(r"Unnamed: [0-9]{1,2}", np.nan, regex=True)
    header = []
    # fill nans with the last value from the left
    if "header_fill" in table_properties:
        for row in range(0, len(df_header)):
            if table_properties["header_fill"][row]:
                header.append(list(df_header.iloc[row].fillna(method="ffill")))
            else:
                header.append(list(df_header.iloc[row]))
    else:
        for row in range(0, len(df_header)):
            header.append(list(df_header.iloc[row].fillna(method="ffill")))

    # combine all non-unit rows into one
    entities = None
    units = None
    for idx, row in enumerate(header):
        if table_properties["header"][idx] == "unit":
            units = row
        else:
            if entities is None:
                entities = row
            else:
                for col, value in enumerate(row):
                    if str(value) != "nan":
                        entities[col] = f"{entities[col]} {value}"

    if units is None:
        raise ValueError(f"Specification for table {table} does not contain unit information.")

    # remove double spaces
    entities = [entity.strip() for entity in entities]
    entities = [re.sub('\s+', ' ', entity) for entity in entities]

    # replace the old header
    if len(header) > 2:
        df_current = df_raw.drop(index=df_raw.iloc[0:len(header)-2].index)
    else:
        df_current = df_raw

    df_current.iloc[0] = units
    df_current.columns = entities
    # remove all columns to ignore
    df_current = df_current.drop(columns=table_properties["cols_to_ignore"])

    # remove double spaces
    for col in cols_for_space_stripping:
        df_current[col] = df_current[col].str.strip()
        df_current[col] = df_current[col].replace('\s+', ' ', regex=True)

    # prepare for sector mapping by initializing result lists and
    # variables
    new_cats = [[''] * len(table_properties["categories"])] * len(df_current)

    # copy the header rows which are not part of the index (unit)
    new_cats[0] = [df_current.iloc[0][cat_col]] * len(table_properties["categories"])

    # do the sector mapping here as we need to keep track of unmapped categories
    # and also need to consider the order of elements for the mapping
    unknown_categories = []
    info_last_row = []
    if non_unique_cats:
        # need to initialize the tree parsing.
        last_parent = category_tree.get_node("root")
        all_nodes = set([category_tree.get_node(node).tag for node in category_tree.nodes])

        for idx in range(1, len(df_current)):
            current_cat = df_current.iloc[idx][cat_col]
            if current_cat in table_properties["stop_cats"]:
                # we've reached the end of the table, so stop processing
                # and remove all further rows
                df_current = df_current.drop(df_current.index[idx:])
                new_cats = new_cats[0:idx]
                break

            # check if current category is a child of the last node
            children = dict([[child.tag, child.identifier]
                        for child in category_tree.children(last_parent.identifier)])
            if current_cat in children.keys():
                # the current category is a child of the current parent
                # do the mapping
                node = category_tree.get_node(children[current_cat])
                new_cats[idx] = node.data[1]
                # check if the node has children
                new_children = category_tree.children(node.identifier)
                if new_children:
                    last_parent = node
            else:
                # two possibilities
                # 1. The category is at a higher point in the hierarchy
                # 2. It's missing in the hierarchy
                # we have to first move up the hierarchy
                # first check if category is present at all
                if current_cat in all_nodes:
                    old_parent = last_parent

                    while (current_cat not in children.keys()) and \
                            (last_parent.identifier != "root"):
                        last_parent = category_tree.get_node(
                            last_parent.predecessor(category_tree.identifier))
                        children = dict([[child.tag, child.identifier]
                                    for child in category_tree.children(last_parent.identifier)])

                    if (last_parent.identifier == "root") and \
                        (current_cat not in children.keys()):
                        # we have not found the category as direct child of any of the
                        # predecessors. Thus it is missing in the specification in
                        # that place
                        print(f"Unknown category '{current_cat}' found in {table} for {file_info['party']}, "
                              f"{file_info['data_year']} (last parent: {old_parent.tag}).")
                        unknown_categories.append([table, file_info["party"], current_cat, file_info['data_year']])
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
                    print(f"Unknown category '{current_cat}' found in {table} for {file_info['party']}, {file_info['data_year']}.")
                    unknown_categories.append([table, file_info["party"], current_cat, file_info['data_year']])
    else:
        for idx in range(1, len(df_current)):
            current_cat = df_current.iloc[idx][cat_col]
            if current_cat in table_properties["stop_cats"]:
                # we've reached the end of the table, so stop processing
                # and remove all further rows
                df_current = df_current.drop(df_current.index[idx:])
                new_cats = new_cats[0:idx]
                break
            if current_cat in all_cats:
                new_cats[idx] = unique_mapping[current_cat]
                if (idx == len(df_current) - 1) and not last_row_nan:
                    print(f"found information in last row: category {current_cat}, row {idx}")
                    info_last_row.append([table, file_info["party"], current_cat, file_info['data_year']])
            else:
                print(f"Unknown category '{current_cat}' found in {table} for {file_info['party']}, {file_info['data_year']}.")
                unknown_categories.append([table, file_info["party"], current_cat, file_info['data_year']])

    for idx, col in enumerate(table_properties["categories"]):
        df_current.insert(loc=idx, column=col, value=
                          [cat[idx] for cat in new_cats])

    # set index
    df_current = df_current.set_index(index_cols)
    # process the unit information using the primap2 functions
    df_current = pm2.pm2io.nir_add_unit_information(df_current, **table_properties["unit_info"])

    # convert to long format
    header_long = table_properties["categories"] + \
        ["orig_cat_name", "entity", "unit", "time", "data"]
    df_long = pm2.pm2io.nir_convert_df_to_long(
        df_current, file_info["data_year"], header_long=header_long)

    # add country information
    df_long.insert(0, column="country", value=file_info["party"])
    #df_long.insert(1, column="submission", value=f"CRF{file_info['submission_year']}")
    if "coords_defaults" in table_spec.keys():
        for col in table_spec["coords_defaults"]:
            df_long.insert(2, column=col, value=table_spec["coords_defaults"][col])

    return df_long, unknown_categories, info_last_row


def get_crf_files(
        country_codes: Union[str, List[str]],
        submission_year: int,
        data_year: Optional[Union[int, List[int]]] = None,
        date: Optional[str] = None,
        folder: Optional[str] = None,
) -> List[Path]:
    """
    Finds all files according to given parameters

    Parameters
    __________

    country_codes: str or list[str]
        ISO 3-letter country UNFCCC_GHG_data or list of country codes

    submission_year: int
        Year of the submission of the data

    data_year: int or List of int (optional)
        if int a single data year will be read. if a list of ints is given these
        years will be read. If no nothing is given all data years will be read

    date: str (optional, default is "latest")
        readonly submission from the given date

    folder: str (optional)
        Folder that contains the xls files. If not given fodlers are determined by the
        submissions_year and country_code variables

    Returns
    _______
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
        data_folder = downloaded_data_path_UNFCCC
        submission_folder = f"CRF{submission_year}"

        with open(data_folder / "folder_mapping.json", "r") as mapping_file:
            folder_mapping = json.load(mapping_file)

        # use country default folders
        country_folders = []
        for country_code in country_codes:
            if country_code in folder_mapping:
                new_country_folders = folder_mapping[country_code]
                if isinstance(new_country_folders, str):
                    # only one folder
                    country_folders = country_folders + \
                                      [data_folder / new_country_folders / submission_folder]
                else:
                    country_folders = country_folders + \
                                      [data_folder / folder / submission_folder
                                       for folder in new_country_folders]
            else:
                raise ValueError(f"No data folder found for country {country_code}. "
                                 f"Check if folder mapping is up to date.")
    else:
        country_folders = [folder]

    file_filter_template = {}
    file_filter_template["submission_year"] = submission_year
    file_filter_template["party"] = country_codes
    if data_year is not None:
        file_filter_template["data_year"] = data_year

    for input_folder in country_folders:
        input_folder = Path(input_folder)
        if input_folder.exists():
            # if desired find the latest date and only read that
            # has to be done per country
            if date == "latest":
                for country in country_codes:
                    file_filter = file_filter_template.copy()
                    file_filter["party"] = country
                    dates = get_submission_dates(folder, file_filter)
                    file_filter["date"] = find_latest_date(dates)
                    input_files = input_files + \
                                  filter_filenames(input_folder.glob("*.xlsx"),
                                                   **file_filter)
            else:
                file_filter = file_filter_template.copy()
                if date is not None:
                    file_filter["date"] = date
                input_files = input_files + \
                              filter_filenames(input_folder.glob("*.xlsx"),
                                               **file_filter)
        else:
            raise ValueError(f"Folder {input_folder} does not exist")

    # make sure no files is in the list twice (happens when multiple input folder
    # contain the same submission which is possible when the country name is changed)
    files_added = set()
    unique_files = []
    for file in input_files:
        if file.name not in files_added:
            unique_files.append(file)
            files_added.add(file.name)

    return unique_files


def get_info_from_crf_filename(
        filename: str,
) -> Dict[str, Union[int, str]]:
    """
    Parse given file name and return a dict with information
    on the contained data.

    Parameters
    __________

    filename: str
        The file to analyze (without path)

    Returns
    _______
    dict with fields:
        party: the party that submitted the data (3 letter UNFCCC_GHG_data)
        submission_year: year of submission
        data_year: year in which the emissions took place
        date: date of the submission
        extra: rest of the file name
    """
    filename = os.path.splitext(filename)[0]
    name_parts = filename.split("_")
    file_info = {}
    file_info["party"] = name_parts[0]
    file_info["submission_year"] = int(name_parts[1])
    try:
        file_info["data_year"] = int(name_parts[2])
    except:
        print(f"Data year string {name_parts[2]} "
              "could not be converted to int.")
        file_info["data_year"] = name_parts[2]
    file_info["date"] = name_parts[3]
    # the last part (time code) is missing for Australia since 2023
    if len(name_parts) > 4:
        file_info["extra"] = name_parts[4]
    else:
        file_info["extra"] = ""
    return file_info


def filter_filenames(
        files_to_filter: List[Path],
        party: Optional[Union[str, List[str]]] = None,
        data_year: Optional[Union[int, List[int]]] = None,
        submission_year: Optional[str] = None,
        date: Optional[str] = None,
) -> List[Path]:
    """ Filter a list of filenames of CRF files

    Parameters
    __________
    files_to_filter: List[Path]
        List with pathlib.Path objects for the filenames to filter

    party: Optional[Union[str, List[str]]] (default: None)
        List of country codes or single country UNFCCC_GHG_data. If given only files
        for this(these) country-UNFCCC_GHG_data(s) will be returned.

    data_year: Optional[Union[int, List[int]]] (default: None)
        List of data years or single year. If given only files for this
        (these) year(s) will be returned

    submission_year: Optional[str] (default: None)
        List of submission years or single year. If given only files with the
        given submission year(s) will be returned

    date: Optional[str] (default: None)
        Date. If given only files with the given submission date will be returned

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

    filtered_files = []
    for file in files_to_filter:
        if not file.is_dir():
            file_info = get_info_from_crf_filename(file.name)
            if check_crf_file_info(file_info, file_filter):
                filtered_files.append(file)

    return filtered_files


def check_crf_file_info(
        file_info: Dict,
        file_filter: Dict,
) -> bool:
    """
    Check if a CRF file has given properties

    Parameters
    __________
    file_info: Dict
        the file info dict of a CRF xlsx file as returned by
        `get_info_from_crf_filename`

    file_filter: Dict
        possible keys are `party`, `data_year`, `submission_year` and `date`
        with functionality as in `filter_filenames`

    Returns
    _______
        bool: `True` if the file info matches the filter and `False` if not

    """
    if "submission_year" in file_filter.keys():
        if file_info["submission_year"] != file_filter["submission_year"]:
            return False
    if "date" in file_filter.keys():
        if file_info["date"] != file_filter["date"]:
            return False
    if "data_year" in file_filter.keys():
        if isinstance(file_filter["data_year"], int):
            if file_info["data_year"] != file_filter["data_year"]:
                return False
        else:
            if file_info["data_year"] not in file_filter["data_year"]:
                return False
    if "party" in file_filter.keys():
        if isinstance(file_filter["party"], str):
            if file_info["party"] != file_filter["party"]:
                return False
        else:
            if file_info["party"] not in file_filter["party"]:
                return False
    return True


def create_category_tree(
        specification: List[List],
        table: str,
        country: Optional[str] = None,
) -> Tree:
    """
    Create a treelib Tree for the categorical hierarchy from a CRF
    table specification.

    The tree is used to parse the row headers in CRF xlsx files and assign the
    correct categories to non-unique row headers.

    Parameters
    __________

    specification: List[List]
        The `sector_mapping` dict of a table specification

    table: str
        Name of the table. Mainly used for output so error messages can
        be linked to tables

    country: str (optional)
        Country name to build the table for. Some categories are country dependent.
        To include them in the tree the country name has to be specified. If no country name
        is given the generic tree will be built.

    """
    # small sanity check on the specification
    if len(specification[0]) < 3:
        raise ValueError(f"Error: Specification for Table {table} has non-unique "
                         "categories and need level specifications")

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

    # filter categories in case country is given
    if country is not None:
        # remove country tags from categories and mark categories
        # for other countries for removal
        specification = [filter_category(mapping, country)
                         for mapping in specification]
        # remove the categories for other countries
        specification = [mapping for mapping in specification
                         if mapping[0] != "\REMOVE"]

    # build a tree from specification
    # when looping over the categories present in the table
    # to read data from we walk along this tree
    for idx, mapping in enumerate(specification):
        current_cat = mapping[0]
        current_cat_level = mapping[2]
        if current_cat_level == last_cat_info["level"]:
            # cat has the same level as preceeding on, so no change to
            # parent node
            category_tree.create_node(current_cat, idx, parent=parent_info[-1]["id"], data=mapping)
        elif current_cat_level == last_cat_info["level"] + 1:
            # the current category is one level further away from
            # the trunk of the tree. This means that
            # * the previous category is its parent
            # add it to parent info
            parent_info.append(
                {
                    "id": last_cat_info["id"],
                    "tag": last_cat_info["category"],
                    "level": last_cat_info["level"]
                }
            )
            # add the category as new node
            category_tree.create_node(current_cat, idx, parent=parent_info[-1]["id"], data=mapping)

        elif current_cat_level < last_cat_info["level"]:
            # the new level is smaller (closer to the trunk)
            # than the last one. Thus we remove all parents
            # from this level on
            parent_info = parent_info[0: current_cat_level + 1]
            category_tree.create_node(current_cat, idx, parent=parent_info[-1]["id"], data=mapping)
        else:
            # increase in levels of more than one is not allowed
            raise ValueError(f"Error in sector hierarchy for table {table}, category {current_cat}: "
                             f"Category level is {current_cat_level} and parent level is "
                             f"{parent_info[-1]['level']}")

        # set last_cat_info
        last_cat_info["category"] = current_cat
        last_cat_info["level"] = current_cat_level
        last_cat_info["id"] = idx

    return category_tree


def filter_category(
        mapping: List,
        country: str,
) -> List[str]:
    """
    This function checks if a category mapping is suitable for the given country.
    If it is the country information will be removed and the new mapping returned.
    If it is not suitable it will be returned with category name "\REMOVE" such that
    it can be removed from the mapping by the calling function.

    Parameters
    __________
        mapping: List
            mapping for a single category
        country: str
            iso 3-letter UNFCCC_GHG_data of the country

    Returns
    _______
        List: updated mapping

    """
    string_exclude = f"\C!-"
    regex_exclude = r"\\C!-([A-Z\-]+)\\"
    regex_exclude_full = r"(\\C!-[A-Z\-]+\\)"
    string_country = f"\C-{country}\\"
    regex_countries = r"^\\C-[A-Z]{3}\\"
    new_mapping = mapping.copy()
    if mapping[0].startswith(string_exclude):
        re_result = re.search(regex_exclude, mapping[0])
        countries_ex = re_result.group(1)
        countries_ex = countries_ex.split("-")
        if country in countries_ex:
            new_mapping[0] = "\REMOVE"
        else:
            re_result = re.search(regex_exclude_full, mapping[0])
            new_mapping[0] = mapping[0][len(re_result.group(1)) + 1:]
    elif mapping[0].startswith(string_country):
        new_mapping[0] = mapping[0][len(string_country) + 1:]
    elif re.match(regex_countries, mapping[0]):
        new_mapping[0] = "\REMOVE"

    return new_mapping


def get_latest_date_for_country(
        country_code: str,
        submission_year: int,
)->str:
    """
    Find the latest submission date for a country

    Parameters
    __________
    country: str
        3-letter country UNFCCC_GHG_data

    submission_year: int
        Year of the submission to find the l;atest date for

    Returns
    _______
        str: string with date
    """

    with open(downloaded_data_path_UNFCCC / "folder_mapping.json", "r") as mapping_file:
        folder_mapping = json.load(mapping_file)

    if country_code in folder_mapping:
        file_filter = {}
        file_filter["party"] = country_code
        file_filter["submission_year"] = submission_year
        country_folders = folder_mapping[country_code]
        if isinstance(country_folders, str):
            # only one folder
            submission_date = find_latest_date(get_submission_dates(
                downloaded_data_path_UNFCCC / country_folders / f"CRF{submission_year}", file_filter))
        else:
            dates = []
            for folder in country_folders:
                dates = dates + get_submission_dates(
                    downloaded_data_path_UNFCCC / folder / f"CRF{submission_year}", file_filter)
            submission_date = find_latest_date(dates)
    else:
        raise ValueError(f"No data folder found for country {country_code}. "
                         f"Check if folder mapping is up to date.")

    return submission_date


def get_submission_dates(
        folder: Path,
        file_filter: Dict[str, Union[str, int, List]],
)->List[str]:
    """
    Returns all submission dates available in a folder

    Parameters
    __________
    folder: Path
        Folder to analyze

    file_filter: Dict[str, Union[str, int, List]]
        Dict with possible fields "party", "submission_year", "data_year"

    Returns
    _______
        List[str]:
            List of dates as str
    """

    if "date" in file_filter:
        raise ValueError(f"'date' present in 'file_filter'. This makes no sense as "
                         f"the function's purpose is to return available dates.")

    if folder.exists():
        files = filter_filenames(folder.glob("*.xlsx"), **file_filter)
    else:
        raise ValueError(f"Folder {folder} does not exist")

    dates = [get_info_from_crf_filename(file.name)["date"] for file in files]
    dates = list(set(dates))

    return dates


def get_submission_parties(
        folder: Path,
        file_filter: Dict[str, Union[str, int, List]],
)->List[str]:
    """
    Returns all submission dates available in a folder

    Parameters
    __________
    folder: Path
        Folder to analyze

    file_filter: Dict[str, Union[str, int, List]]
        Dict with possible fields "submission_year", "data_year", "date"

    Returns
    _______
        List[str]:
            List of parties as str
    """

    if "party" in file_filter:
        raise ValueError(f"'party' present in 'file_filter'. This makes no sense as "
                         f"the function's purpose is to return available parties.")

    if folder.exists():
        files = filter_filenames(list(folder.glob("*.xlsx")), **file_filter)
    else:
        raise ValueError(f"Folder {folder} does not exist")

    parties = [get_info_from_crf_filename(file.name)["party"] for file in files]
    parties = list(set(parties))

    return parties


def find_latest_date(
        dates: List[str],
        date_format: str='%d%m%Y',
)-> str:
    """
    Returns the latest date in a list of dates as str in the format
    ddmmyyyy

    Parameters
    __________
    dates: List[str]
        List of dates

    Returns
    _______
        str: latest date
    """

    if len(dates) > 0:
        dates_datetime = [[date, datetime.strptime(date, date_format)] for date in
                          dates]
        dates_datetime = sorted(dates_datetime, key=itemgetter(1))
    else:
        raise ValueError(f"Passed list of dates is empty")

    return dates_datetime[-1][0]

