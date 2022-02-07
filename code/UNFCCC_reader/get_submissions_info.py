# helper functions to get information on available submissions
# and data reading functions for a given country

from typing import Union, List, Dict
from pathlib import Path
import json
import countrynames
import os


def get_country_submissions(
        country_name: str,
        print_sub: bool = True,
) -> Dict[str, List[str]]:
    """
    Input is a three letter ISO code for a country, or the countries name.
    The function tries to map the country name to an ISO code and then
    queries the folder mapping files for folders.

    Parameters
    ----------
        country_name: str
            String containing the country name or ISO 3 letter code

        print_sub: bool
            If True information on submissions will be written to stdout

    Returns
    -------
        returns a dict with keys for the dataset classes (e.g. UNFCCC, non-UNFCCC)
        Each value is a list of folders

    """

    codepath = Path(__file__).parent
    data_folder = codepath / ".." / ".." / "downloaded_data"

    # obtain country code
    country_code = countrynames.to_code_3(country_name)
    if country_code is None:
        raise ValueError(f"Country name {country_name} can not be mapped to "
                         f"any country code")

    if print_sub:
        print(f"Country name {country_name} maps to ISO code {country_code}")

    country_submissions = {}
    for item in data_folder.iterdir():
        if item.is_dir():
            if print_sub:
                print("")
                print("#" * 80)
                print(f"Data folder {item.name}")
            with open(item / "folder_mapping.json", "r") as mapping_file:
                folder_mapping = json.load(mapping_file)
            country_folders = folder_mapping[country_code]
            if isinstance(country_folders, str):
                # only one folder
                country_folders = [country_folders]

            submission_folders = []
            for country_folder in country_folders:
                current_folder = item / country_folder
                if print_sub:
                    print("-" * 80)
                    print(f"Submissions in folder {country_folder}:")

                for submission_folder in current_folder.iterdir():
                    if submission_folder.is_dir():
                        if print_sub:
                            print(submission_folder.name)
                        submission_folders.append(submission_folder.name)

            country_submissions[item.name] = submission_folders

    return country_submissions



def create_folder_mapping(
        folder: str,
        extracted: bool = False
) -> None:
    """
    Create a mapping from 3 letter ISO country codes to folders
    based on the subfolders of the given folder. The mapping is
    stored in 'folder_mapping.json' in the given folder.

    Parameters
    ----------
        folder: str
            folder to create the mapping for
        extracted: bool = False
            If true treat the folder as extracted data, where we
            only have one folder per country and no typos in the
            names

    Returns
    -------
        Nothing

    """
    if extracted:
        folder_mapping = {}
    else:
        folder_mapping = {
            'VEN': 'Venezeula_(Bolivarian_Republic_of)',
            'FSM': 'Micronesia_(Federated_State_of)',
            'MKD': 'The_Republic_of_North_Macedonia',
        }
    known_folders = list(folder_mapping.values())

    for item in folder.iterdir():
        if item.is_dir():
            ISO3 = countrynames.to_code_3(item.name)
            if ISO3 is None:
                if item.name not in known_folders:
                    print(folder_mapping.values())
                    print(f"No match for {item.name}")
            else:
                known_folders.append(item.name)
                if ISO3 in folder_mapping.keys():
                    folder_mapping[ISO3] = [folder_mapping[ISO3], item.name]
                else:
                    folder_mapping[ISO3] = item.name

    with open(folder / "folder_mapping.json", "w") as mapping_file:
        json.dump(folder_mapping, mapping_file, indent=4)
