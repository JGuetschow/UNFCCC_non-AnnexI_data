"""
This file holds the core functions of the CRF reader.
Core function are used both for reading for final datasets as
well as for test-reading to check for new categories etc.
"""

import re
from typing import Dict, Union, List, Optional, Union
from pathlib import Path
from treelib import Tree

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
        party: the party that submitted the data (3 letter code)
        submission_year: year of submission
        data_year: year in which the meissions took place
        date: date of the submission
        extra: rest of the file name
    """
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
    file_info["extra"] = name_parts[4]
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
            iso 3-letter code of the country

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

