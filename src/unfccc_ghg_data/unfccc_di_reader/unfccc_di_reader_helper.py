"""
Helper functions for the DI reader

The helper functions find the latest read data, determine the filename from country
code and other parameters of a dataset, find present data based on hashes etc.
"""
import json
import re
from datetime import date
from pathlib import Path
from typing import Optional, Union

from unfccc_ghg_data.helper import (
    custom_country_mapping,
    dataset_path_UNFCCC,
    extracted_data_path_UNFCCC,
    get_country_code,
    get_country_name,
    root_path,
)
from unfccc_ghg_data.unfccc_crf_reader.unfccc_crf_reader_core import find_latest_date

from .util import DI_date_format, regex_date


## helper functions
def determine_filename(
    country_code: str,
    date_or_hash: str,
    raw: bool = False,
    hash: bool = False,
) -> Path:
    """
    Determine the filename for a dataset from given country code and date string.

    Parameters
    ----------
    country_code: str
        ISO 3 letter code of the country
    date_or_hash:
        formatted date string
    raw: bool
        bool specifying if filename fow raw or processed data should be returned
    hash: str

    Returns
    -------
    _______
        pathlib Path object for the file name (without suffix)

    """
    # get the country folder
    with open(extracted_data_path_UNFCCC / "folder_mapping.json") as mapping_file:
        folder_mapping = json.load(mapping_file)

    if country_code in folder_mapping:
        file_filter = {}
        file_filter["party"] = country_code
        country_folders = folder_mapping[country_code]
        if isinstance(country_folders, str):
            # only one folder
            country_folder = extracted_data_path_UNFCCC / country_folders
        else:
            raise ValueError(  # noqa: TRY003
                "More than one output folder for country "
                f"{country_code}. This should not happen."
            )
    else:
        # folder not in mapping. It will be created if not present yet
        country_name = get_country_name(country_code)
        country_folder = extracted_data_path_UNFCCC / country_name.replace(" ", "_")

        if country_folder.exists():
            print(
                f"Output folder {country_name.replace(' ', '_')} for country "
                f"{country_code} exists but is not in folder mapping. Update "
                "folder mapping"
            )
        else:
            country_folder.mkdir()

    filename = f"{country_code}_DI_{date_or_hash}"
    if raw:
        filename = f"{filename}_raw"
    elif not hash:
        today = date.today()
        date_str_today = today.strftime(DI_date_format)
        filename = f"{filename}_{date_str_today}"
    if hash:
        filename = f"{filename}_hash"
    filename = country_folder / filename

    return filename.relative_to(root_path)


def determine_dataset_filename(
    date_or_hash: str,
    raw: bool = False,
    annexI: bool = False,
    hash: bool = False,
) -> Path:
    """
    Determine the filename for a dataset from given country group and date string.

    Parameters
    ----------
    date_or_hash:
        formatted date string
    raw: bool
        bool specifying if filename fow raw or processed data should be returned
    annexI: bool, default False
        True if AnnexI data, False if non-AnnexI data
    hash: str

    Returns
    -------
    _______
        pathlib Path object for the file name (without suffix)
    """
    # get the country folder
    if annexI:
        current_dataset_path = dataset_path_UNFCCC / "DI_AnnexI"
        filename = f"DI_AnnexI_{date_or_hash}"
    else:
        current_dataset_path = dataset_path_UNFCCC / "DI_non_AnnexI"
        filename = f"DI_non_AnnexI_{date_or_hash}"

    if not current_dataset_path.exists():
        current_dataset_path.mkdir()

    if raw:
        filename = f"{filename}_raw"
    if hash:
        filename = f"{filename}_hash"
    filename = current_dataset_path / filename

    return filename.relative_to(root_path)


def get_input_and_output_files_for_country_DI(  # noqa: PLR0912
    country: str,
    date_str: str,
    raw: bool,
    verbose: Optional[bool] = True,
) -> dict[str, Union[list, str]]:
    """
    Get input and output files for a given country
    """
    country_info = {}

    if country in custom_country_mapping:
        country_code = country
    else:
        country_code = get_country_code(country)
    # now get the country name
    country_name = get_country_name(country_code)
    country_info["code"] = country_code
    country_info["name"] = country_name
    # now get the country name
    country_name = get_country_name(country_code)
    country_info["code"] = country_code
    country_info["name"] = country_name

    # determine latest data
    if raw:
        print(f"Determining output files for {country_name}")
    else:
        print(f"Determining input and output files for {country_name}")

    # get input files (only for processing)
    if raw:
        input_files = []
    else:
        # get latest dataset if no date given
        if date_str is None:
            # get the latest date
            input_file = [find_latest_DI_data(country_code, raw=True)]

        else:
            input_file = [
                determine_filename(country_code, date_str, raw=False, hash=False)
            ]
            if input_file[0].is_symlink():
                # also get the file with the actual data
                input_file.append(input_file[0].readlink())
            else:
                # DI processing input files wit date labels should always be symlinks
                # to the files with hashes holding the actual data.
                raise (
                    ValueError,
                    f"Input file {input_file[0].name} is not a symlink "
                    f" or not existent. Check if the data you want to "
                    f"process exists and if your repository is clean.",
                )

        input_files = [
            f"{file.parent / file.stem}.{suffix}"
            for suffix in ["yaml", "csv", "nc"]
            for file in input_file
        ]

        if verbose:
            print("The following files are considered as input_files:")
            for file in input_files:
                print(file)
            print("")

    # get output files
    output_file = determine_filename(country_code, date_str, raw=raw)
    output_files = [
        f"{output_file.as_posix()}.{suffix}" for suffix in ["yaml", "csv", "nc"]
    ]

    if verbose:
        print("The following files are considered as output_files:")
        for file in output_files:
            print(file)
        print("")

    # add to country info
    country_info["input"] = input_files
    country_info["output"] = []  # output_files # not used because we don't know the
    # hash in advance

    return country_info


def get_present_hashes_for_country_DI(
    country_code: str,
    raw: bool,
) -> list:
    """
    Get the hashes of outputs
    """
    regex_hash = r"_([a-f0-9]*)_"
    if raw:
        regex_hash = regex_hash + "raw_hash\\.nc"
    else:
        regex_hash = regex_hash + "hash\\.nc"

    # get the country folder
    with open(extracted_data_path_UNFCCC / "folder_mapping.json") as mapping_file:
        folder_mapping = json.load(mapping_file)

    if country_code in folder_mapping:
        file_filter = {}
        file_filter["party"] = country_code
        country_folders = folder_mapping[country_code]
        if isinstance(country_folders, str):
            # only one folder
            country_folder = extracted_data_path_UNFCCC / country_folders
        else:
            raise ValueError(  # noqa: TRY003
                "More than one output folder for country "
                f"{country_code}. This should not happen."
            )

        files_list = list(country_folder.glob("*_hash.nc"))
        # filter according to raw flag
        if raw:
            files_list = [
                file.name for file in files_list if re.search(r"_raw_hash", file.name)
            ]
        else:
            files_list = [
                file.name
                for file in files_list
                if not re.search(r"_raw_hash", file.name)
            ]

        hash_list = [re.findall(regex_hash, file)[0] for file in files_list]
        return hash_list

    else:
        # folder not in mapping.
        return []


def find_latest_DI_data(
    country_code: str,
    raw: bool = True,
) -> Union[Path, None]:
    """
    Find the path to the nc file with the latest DI data for a given country
    """
    if raw:
        regex = f"{country_code}_DI_{regex_date}" + r"_raw\.nc"
    else:
        regex = f"{country_code}_DI_{regex_date[1:-1]}_{regex_date}" + r"\.nc"
        # regex = f"{country_code}_DI_{regex_date}" + r"\.nc"

    # get the country folder
    with open(extracted_data_path_UNFCCC / "folder_mapping.json") as mapping_file:
        folder_mapping = json.load(mapping_file)

    if country_code in folder_mapping:
        file_filter = {}
        file_filter["party"] = country_code
        country_folders = folder_mapping[country_code]
        if isinstance(country_folders, str):
            # only one folder
            country_folder = extracted_data_path_UNFCCC / country_folders
        else:
            raise ValueError(  # noqa: TRY003
                "More than one output folder for country "
                f"{country_code}. This should not happen."
            )

        files_path_list = list(country_folder.glob("*.nc"))
        # remove files with hash
        files_list = [
            file.name
            for file in files_path_list
            if not re.search(r"_hash\.nc", file.name)
        ]
        # remove files that don't begin with country_code_DI
        files_list = [
            file for file in files_list if re.search(f"^{country_code}_DI_", file)
        ]
        # filter according to raw flag
        if raw:
            files_list = [file for file in files_list if re.search(r"_raw\.nc", file)]
        else:
            files_list = [
                file for file in files_list if not re.search(r"_raw\.nc", file)
            ]

        if len(files_list) > 0:
            date_list = [re.findall(regex, file)[0] for file in files_list]
            latest_date = find_latest_date(date_list, "%Y-%m-%d")
            latest_file = [  # noqa: RUF015
                file for file in files_list if re.search(latest_date, file)
            ][0]
            return country_folder / latest_file
        else:
            return None

    else:
        # folder not in mapping.
        return None
