# helper functions to get information on available submissions
# and data reading functions for a given country

from typing import List, Dict
from pathlib import Path
import json
import pycountry

from UNFCCC_GHG_data.helper import root_path, downloaded_data_path, extracted_data_path
from UNFCCC_GHG_data.helper import get_country_code

code_path = root_path / "UNFCCC_GHG_data" / "UNFCCC_reader"


def get_possible_inputs(
        country_name: str,
        submission: str,
        print_info: bool = False,
) -> List[Path]:

    """
    For given country name and submission find the possible input files

    Parameters
    ----------
        country_name: str
            String containing the country name or ISO 3 letter UNFCCC_GHG_data

        submission: str
            String of the submission

        print_info: bool = False
            If True print information on UNFCCC_GHG_data found

    Returns
    -------
        returns a list pathlib Path objects for the input files
    """

    data_folder = downloaded_data_path

    # obtain country UNFCCC_GHG_data
    country_code = get_country_code(country_name)

    if print_info:
        print(f"Country name {country_name} maps to ISO UNFCCC_GHG_data {country_code}")

    input_files = []
    for item in data_folder.iterdir():
        if item.is_dir():
            with open(item / "folder_mapping.json", "r") as mapping_file:
                folder_mapping = json.load(mapping_file)

            if country_code in folder_mapping:
                country_folders = folder_mapping[country_code]
                if isinstance(country_folders, str):
                    # only one folder
                    country_folders = [country_folders]

                for country_folder in country_folders:
                    input_folder = item / country_folder / submission
                    if input_folder.exists():
                        for filepath in input_folder.glob("*"):
                            input_files.append(filepath.relative_to(root_path))

    if print_info:
        if input_files:
            print(f"Found possible input files:")
            for file in input_files:
                print(file)
        else:
            print(f"No input files found")

    return input_files


def get_possible_outputs(
        country_name: str,
        submission: str,
        print_info: bool = False,
)-> List[Path]:

    """
    For given country name and submission find the possible output files

    Parameters
    ----------
        country_name: str
            String containing the country name or ISO 3 letter UNFCCC_GHG_data

        submission: str
            String of the submission

        print_info: bool = False
            If True print information on outputs found

    Returns
    -------
        returns a list pathlib Path objects for the input files
    """

    data_folder = extracted_data_path

    # obtain country UNFCCC_GHG_data
    country_code = get_country_code(country_name)
    if print_info:
        print(f"Country name {country_name} maps to ISO UNFCCC_GHG_data {country_code}")

    output_files = []
    for item in data_folder.iterdir():
        if item.is_dir():
            with open(item / "folder_mapping.json", "r") as mapping_file:
                folder_mapping = json.load(mapping_file)

            if country_code in folder_mapping:
                country_folder = folder_mapping[country_code]
                if not isinstance(country_folder, str):
                    raise ValueError("Wrong data type in folder mapping json file. Should be str.")

                output_folder = item / country_folder
                if output_folder.exists():
                    for filepath in output_folder.glob(country_code + "_" + submission + "*"):
                        output_files.append(filepath.relative_to(root_path))

    if print_info:
        if output_files:
            print(f"Found possible output files:")
            for file in output_files:
                print(file)
        else:
            print(f"No output files found")

    return output_files






