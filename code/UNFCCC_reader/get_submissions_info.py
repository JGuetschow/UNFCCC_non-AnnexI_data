# helper functions to get information on available submissions
# and data reading functions for a given country

from typing import List, Dict
from pathlib import Path
import json
import countrynames
#import os


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
    if print_sub:
        print(f"#" * 80)
        print(f"The following submissions are available for {country_name}")
    for item in data_folder.iterdir():
        if item.is_dir():
            if print_sub:
                print("")
                print("-" * 80)
                print(f"Data folder {item.name}")
                print("-" * 80)
            with open(item / "folder_mapping.json", "r") as mapping_file:
                folder_mapping = json.load(mapping_file)
            if country_code in folder_mapping:
                country_folders = folder_mapping[country_code]
                if isinstance(country_folders, str):
                    # only one folder
                    country_folders = [country_folders]

                submission_folders = []
                for country_folder in country_folders:
                    current_folder = item / country_folder
                    if print_sub:
                        print(f"Submissions in folder {country_folder}:")

                    for submission_folder in current_folder.iterdir():
                        if submission_folder.is_dir():
                            if print_sub:
                                print(submission_folder.name)
                            submission_folders.append(submission_folder.name)

                country_submissions[item.name] = submission_folders
            else:
                print(f"No submissions available for {country_name}.")

    return country_submissions


def get_country_datasets(
        country_name: str,
        print_ds: bool = True,
) -> Dict[str, List[str]]:
    """
    Input is a three letter ISO code for a country, or the country's name.
    The function tries to map the country name to an ISO code and then
    checks the code and data folders for content on the country.

    Parameters
    ----------
        country_name: str
            String containing the country name or ISO 3 letter code

        print_ds: bool
            If True information on submissions will be written to stdout

    Returns
    -------
        returns a dict with keys for the dataset classes (e.g. UNFCCC, non-UNFCCC)
        Each value is a list of folders

    """

    codepath = Path(__file__).parent
    #codepath = Path(os.getcwd()) / ".." / "code" / "UNFCCC_reader"
    rootpath = codepath / ".." / ".."
    rootpath = rootpath.resolve()
    data_folder = rootpath / "extracted_data"
    data_folder_legacy = rootpath / "legacy_data"


    # obtain country code
    country_code = countrynames.to_code_3(country_name)
    if country_code is None:
        raise ValueError(f"Country name {country_name} can not be mapped to "
                         f"any country code")

    if print_ds:
        print(f"Country name {country_name} maps to ISO code {country_code}")

    rep_data = {}
    # data
    if print_ds:
        print(f"#" * 80)
        print(f"The following datasets are available for {country_name}")
    for item in data_folder.iterdir():
        if item.is_dir():
            cleaned_datasets_current_folder = {}
            if print_ds:
                print("-" * 80)
                print(f"Data folder {item.name}")
                print("-" * 80)
            with open(item / "folder_mapping.json", "r") as mapping_file:
                folder_mapping = json.load(mapping_file)
            if country_code not in folder_mapping:
                if print_ds:
                    print("No data available")
                    print("")
            else:
                country_folder = folder_mapping[country_code]
                if not isinstance(country_folder, str):
                    raise ValueError("Wrong data type in folder mapping json file. Should be str.")

                datasets_current_folder = {}
                current_folder = item / country_folder

                for data_file in current_folder.iterdir():
                    if data_file.suffix in ['.nc', '.yaml', '.csv']:
                        if data_file.stem in datasets_current_folder:
                            datasets_current_folder[data_file.stem].append(data_file.suffix)
                        else:
                            datasets_current_folder[data_file.stem] = [data_file.suffix]

                for dataset in datasets_current_folder:
                    # process filename to get submission
                    parts = dataset.split('_')
                    if parts[0] != country_code:
                        cleaned_datasets_current_folder[f'Wrong code: {parts[0]}'] = dataset
                    else:
                        terminology = "_".join(parts[3 : ])
                        key = f"{parts[1]} ({parts[2]}, {terminology})"
                        data_info = ""
                        if '.nc' in datasets_current_folder[dataset]:
                            data_info = data_info + "NF (.nc), "
                        if ('.csv' in datasets_current_folder[dataset]) and ('.yaml' in datasets_current_folder[dataset]):
                            data_info = data_info + "IF (.yaml + .csv), "
                        elif '.csv' in datasets_current_folder[dataset]:
                            data_info = data_info + "incomplete IF? (.csv), "
                        elif '.yaml' in datasets_current_folder[dataset]:
                            data_info = data_info + "incomplete IF (.yaml), "

                        code_file = get_code_file(country_code, parts[1])
                        if code_file:
                            data_info = data_info + f"code: {code_file.name}"
                        else:
                            data_info = data_info + f"code: not found"

                        cleaned_datasets_current_folder[key] = data_info

                if print_ds:
                    if cleaned_datasets_current_folder:
                        for country_ds in cleaned_datasets_current_folder:
                            print(f"{country_ds}: {cleaned_datasets_current_folder[country_ds]}")
                    else:
                        print("No data available")
                    print("")

            rep_data[item.name] = cleaned_datasets_current_folder

    # legacy data
    if print_ds:
        print(f"#" * 80)
        print(f"The following legacy datasets are available for {country_name}")
    legacy_data = {}
    for item in data_folder_legacy.iterdir():
        if item.is_dir():
            cleaned_datasets_current_folder = {}
            if print_ds:
                print("-" * 80)
                print(f"Data folder {item.name}")
                print("-" * 80)
            with open(item / "folder_mapping.json", "r") as mapping_file:
                folder_mapping = json.load(mapping_file)
            if country_code not in folder_mapping:
                if print_ds:
                    print("No data available")
                    print("")
            else:
                country_folder = folder_mapping[country_code]
                if not isinstance(country_folder, str):
                    raise ValueError("Wrong data type in folder mapping json file. Should be str.")

                datasets_current_folder = {}
                current_folder = item / country_folder

                for data_file in current_folder.iterdir():
                    if data_file.suffix in ['.nc', '.yaml', '.csv']:
                        if data_file.stem in datasets_current_folder:
                            datasets_current_folder[data_file.stem].append(data_file.suffix)
                        else:
                            datasets_current_folder[data_file.stem] = [data_file.suffix]

                for dataset in datasets_current_folder:
                    # process filename to get submission
                    parts = dataset.split('_')
                    if parts[0] != country_code:
                        cleaned_datasets_current_folder[f'Wrong code: {parts[0]}'] = dataset
                    else:
                        terminology = "_".join(parts[3 : ])
                        key = f"{parts[1]} ({parts[2]}, {terminology}, legacy)"
                        data_info = ""
                        if '.nc' in datasets_current_folder[dataset]:
                            data_info = data_info + "NF (.nc), "
                        if ('.csv' in datasets_current_folder[dataset]) and ('.yaml' in datasets_current_folder[dataset]):
                            data_info = data_info + "IF (.yaml + .csv), "
                        elif '.csv' in datasets_current_folder[dataset]:
                            data_info = data_info + "incomplete IF? (.csv), "
                        elif '.yaml' in datasets_current_folder[dataset]:
                            data_info = data_info + "incomplete IF (.yaml), "

                        cleaned_datasets_current_folder[key] = data_info

                if print_ds:
                    if cleaned_datasets_current_folder:
                        for country_ds in cleaned_datasets_current_folder:
                            print(f"{country_ds}: {cleaned_datasets_current_folder[country_ds]}")
                    else:
                        print("No data available")
                    print("")

                legacy_data[item.name] = cleaned_datasets_current_folder

    all_data = {
        "rep_data": rep_data,
        "legacy_data": legacy_data,
    }

    return all_data


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
            String containing the country name or ISO 3 letter code

        submission: str
            String of the submission

        print_info: bool = False
            If True print information on code found

    Returns
    -------
        returns a list pathlib Path objects for the input files
    """

    codepath = Path(__file__).parent
    #codepath = Path(os.getcwd()) / ".." / "code" / "UNFCCC_reader"
    rootpath = codepath / ".." / ".."
    rootpath = rootpath.resolve()
    data_folder = rootpath / "downloaded_data"

    # obtain country code
    country_code = countrynames.to_code_3(country_name)
    if country_code is None:
        raise ValueError(f"Country name {country_name} can not be mapped to "
                         f"any country code")

    if print_info:
        print(f"Country name {country_name} maps to ISO code {country_code}")

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
                            input_files.append(filepath.relative_to(rootpath))

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
            String containing the country name or ISO 3 letter code

        submission: str
            String of the submission

        print_info: bool = False
            If True print information on outputs found

    Returns
    -------
        returns a list pathlib Path objects for the input files
    """

    codepath = Path(__file__).parent
    #codepath = Path(os.getcwd()) / ".." / "code" / "UNFCCC_reader"
    rootpath = codepath / ".." / ".."
    rootpath = rootpath.resolve()
    data_folder = rootpath / "extracted_data"

    # obtain country code
    country_code = countrynames.to_code_3(country_name)
    if country_code is None:
        raise ValueError(f"Country name {country_name} can not be mapped to "
                         f"any country code")

    if print_info:
        print(f"Country name {country_name} maps to ISO code {country_code}")

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
                        output_files.append(filepath.relative_to(rootpath))

    if print_info:
        if output_files:
            print(f"Found possible output files:")
            for file in output_files:
                print(file)
        else:
            print(f"No output files found")

    return output_files


def get_code_file(
        country_name: str,
        submission: str,
        print_info: bool = False,
) -> Path:
    """
    For given country name and submission find the script that creates the data

    Parameters
    ----------
        country_name: str
            String containing the country name or ISO 3 letter code

        submission: str
            String of the submission

        print_info: bool = False
            If True print information on code found

    Returns
    -------
        returns a pathlib Path object for the code file
    """

    codepath = Path(__file__).parent
    #codepath = Path(os.getcwd()) / ".." / "code" / "UNFCCC_reader"
    rootpath = codepath / ".." / ".."
    rootpath = rootpath.resolve()
    code_file_path = None

    # obtain country code
    country_code = countrynames.to_code_3(country_name)
    if country_code is None:
        raise ValueError(f"Country name {country_name} can not be mapped to "
                         f"any country code")

    if print_info:
        print(f"Country name {country_name} maps to ISO code {country_code}")

    with open(codepath / "folder_mapping.json", "r") as mapping_file:
        folder_mapping = json.load(mapping_file)

    if country_code not in folder_mapping:
        if print_info:
            print("No code available")
            print("")
    else:
        country_folder = codepath / folder_mapping[country_code]
        code_file_name_candidate = "read_" + country_code + "_" + submission + "*"

        for file in country_folder.iterdir():
            if file.match(code_file_name_candidate):
                if code_file_path is not None:
                    raise ValueError(f"Found multiple code candidates: "
                                     f"{code_file_path} and file.name. "
                                     f"Please use only one file with name "
                                     f"'read_ISO3_submission_XXX.YYY'.")
                else:
                    if print_info:
                        print(f"Found code file {file.relative_to(rootpath)}")
                code_file_path = file

    if code_file_path is not None:
        return code_file_path.relative_to(rootpath)
    else:
        return None

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
