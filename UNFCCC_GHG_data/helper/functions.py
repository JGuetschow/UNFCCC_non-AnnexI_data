import pycountry
import json
import xarray as xr
from copy import deepcopy
from typing import Dict, List
from pathlib import Path
from .definitions import custom_country_mapping, custom_folders
from .definitions import root_path, downloaded_data_path, extracted_data_path
from .definitions import legacy_data_path, code_path


def convert_categories(
        ds_input: xr.Dataset,
        conversion: Dict[str, Dict[str, str]],
        #terminology_from: str,
        terminology_to: str,
        debug: bool=False,
        tolerance: float=0.01,
)->xr.Dataset:
    """
    convert data from one category terminology to another
    """
    ds_converted = ds_input.copy(deep=True)
    ds_converted.attrs = deepcopy(ds_input.attrs)

    # change category terminology
    cat_dim = ds_converted.attrs["cat"]
    ds_converted.attrs["cat"] = f"category ({terminology_to})"
    ds_converted = ds_converted.rename({cat_dim: ds_converted.attrs["cat"]})

    # find categories present in dataset
    cats_present = list(ds_converted.coords[f'category ({terminology_to})'])

    # restrict categories and map category names
    if 'mapping' in conversion.keys():
        mapping_cats_present = [cat for cat in list(conversion['mapping'].keys()) if
                                cat in cats_present]
        ds_converted = ds_converted.pr.loc[
            {'category': mapping_cats_present}]

        from_cats = ds_converted.coords[f'category ({terminology_to})'].values
        to_cats = pd.Series(from_cats).replace(conversion['mapping'])
        ds_converted = ds_converted.assign_coords({f'category ({terminology_to})':
                                                   (f'category ({terminology_to})',
                                                    to_cats)})

    # redo the list of present cats after mapping, as we have new categories in the
    # target terminology now
    cats_present_mapped = list(ds_converted.coords[f'category ({terminology_to})'])
    # aggregate categories
    if 'aggregate' in conversion:
        aggregate_cats = conversion['aggregate']
        for cat_to_agg in aggregate_cats:
            if debug:
                print(f"Category: {cat_to_agg}")
            source_cats = [cat for cat in aggregate_cats[cat_to_agg]['sources'] if
                           cat in cats_present_mapped]
            data_agg = ds_converted.pr.loc[{'category': source_cats}].pr.sum(
                dim='category', skipna=True, min_count=1)
            nan_vars = [var for var in data_agg.data_vars if
                        data_agg[var].isnull().all().data == True]
            data_agg = data_agg.drop(nan_vars)
            if len(data_agg.data_vars) > 0:
                data_agg = data_agg.expand_dims([f'category ({terminology_to})'])
                data_agg = data_agg.assign_coords(
                    coords={f'category ({terminology_to})':
                                (f'category ({terminology_to})', [cat_to_agg])})
                ds_converted = ds_converted.pr.merge(data_agg, tolerance=tolerance)
            else:
                print(f"no data to aggregate category {cat_to_agg}")

    return ds_converted


def get_country_name(
        country_code: str,
) -> str:
    """get country name from code """
    if country_code in custom_country_mapping:
        country_name = custom_country_mapping[country_code]
    else:
        try:
            country = pycountry.countries.get(alpha_3=country_code)
            country_name = country.name
        except:
            raise ValueError(f"Country code {country_code} can not be mapped to "
                             f"any country")

    return country_name


def get_country_code(
        country_name: str,
)->str:
    """
    obtain country code. If the input is a code it will be returned,
    if the input
    is not a three letter code a search will be performed

    Parameters
    __________
    country_name: str
        Country code or name to get the three-letter code for.

    Returns
    -------
        country_code: str

    """
    # First check if it's in the list of custom codes
    if country_name in custom_country_mapping:
        country_code = country_name
    else:
        try:
            # check if it's a 3 letter UNFCCC_GHG_data
            country = pycountry.countries.get(alpha_3=country_name)
            country_code = country.alpha_3
        except:
            try:
                country = pycountry.countries.search_fuzzy(country_name.replace("_", " "))
            except:
                raise ValueError(f"Country name {country_name} can not be mapped to "
                                 f"any country UNFCCC_GHG_data. Try using the ISO3 UNFCCC_GHG_data directly.")
            if len(country) > 1:
                country_code = None
                for current_country in country:
                    if current_country.name == country_name:
                        country_code = current_country.alpha_3
                if country_code is None:
                    raise ValueError(f"Country name {country_name} has {len(country)} "
                                     f"possible results for country codes.")

            country_code = country[0].alpha_3

    return country_code


def create_folder_mapping(
        folder: str,
        extracted: bool = False
) -> None:
    """
    Create a mapping from 3 letter ISO country codes to folders
    based on the subfolders of the given folder. The mapping is
    stored in 'folder_mapping.json' in the given folder. Folder
    must be given relative to the repository root

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

    folder = root_path / folder
    folder_mapping = {}
    #if not extracted:
    known_folders = custom_folders
    #else:
    #    known_folders = {}

    for item in folder.iterdir():
        if item.is_dir() and not item.match("__pycache__"):
            if item.name in known_folders:
                ISO3 = known_folders[item.name]
            else:
                try:
                    country = pycountry.countries.search_fuzzy(item.name.replace("_", " "))
                    if len(country) > 1:
                        ISO3 = None
                        for current_country in country:
                            if current_country.name == item.name.replace("_", " "):
                                ISO3 = current_country.alpha_3
                    else:
                        ISO3 = country[0].alpha_3
                except:
                    ISO3 = None

            if ISO3 is None:
                print(f"No match for {item.name}")
            else:
                if ISO3 in folder_mapping.keys():
                    folder_mapping[ISO3] = [folder_mapping[ISO3], item.name]
                else:
                    folder_mapping[ISO3] = item.name

    with open(folder / "folder_mapping.json", "w") as mapping_file:
        json.dump(folder_mapping, mapping_file, indent=4)


# TODO add crf
def get_country_submissions(
        country_name: str,
        print_sub: bool = True,
) -> Dict[str, List[str]]:
    """
    Input is a three letter ISO UNFCCC_GHG_data for a country, or the countries name.
    The function tries to map the country name to an ISO UNFCCC_GHG_data and then
    queries the folder mapping files for folders.

    Parameters
    ----------
        country_name: str
            String containing the country name or ISO 3 letter UNFCCC_GHG_data

        print_sub: bool
            If True information on submissions will be written to stdout

    Returns
    -------
        returns a dict with keys for the dataset classes (e.g. UNFCCC, non-UNFCCC)
        Each value is a list of folders

    """

    data_folder = downloaded_data_path

    country_code = get_country_code(country_name)

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
    The function tries to map the country name to an ISO UNFCCC_GHG_data and then
    checks the UNFCCC_GHG_data and data folders for content on the country.

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

    data_folder = extracted_data_path
    data_folder_legacy = legacy_data_path

    # obtain country UNFCCC_GHG_data
    country_code = get_country_code(country_name)

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
                        cleaned_datasets_current_folder[f'Wrong code: {parts[0]}'] =\
                            dataset
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
                        cleaned_datasets_current_folder[f'Wrong UNFCCC_GHG_data: {parts[0]}'] = dataset
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
            String containing the country name or ISO 3 letter UNFCCC_GHG_data

        submission: str
            String of the submission

        print_info: bool = False
            If True print information on UNFCCC_GHG_data found

    Returns
    -------
        returns a pathlib Path object for the UNFCCC_GHG_data file
    """

    code_file_path = None
    UNFCCC_reader_path = code_path / "UNFCCC_reader"

    # CRF is an exception as it's read using the UNFCCC_CRF_reader module
    # so we return the path to that.
    if submission[0:3] == "CRF":
        return root_path / "UNFCCC_CRF_reader"

    if submission[0:2] == "DI":
        return root_path / "UNFCCC_DI_reader"

    # obtain country UNFCCC_GHG_data
    country_code = get_country_code(country_name)

    if print_info:
        print(f"Country name {country_name} maps to ISO UNFCCC_GHG_data {country_code}")

    with open(UNFCCC_reader_path / "folder_mapping.json", "r") as mapping_file:
        folder_mapping = json.load(mapping_file)

    if country_code not in folder_mapping:
        if print_info:
            print("No UNFCCC_GHG_data available")
            print("")
    else:
        country_folder = UNFCCC_reader_path / folder_mapping[country_code]
        code_file_name_candidate = "read_" + country_code + "_" + submission + "*"

        for file in country_folder.iterdir():
            if file.match(code_file_name_candidate):
                if code_file_path is not None:
                    raise ValueError(f"Found multiple UNFCCC_GHG_data candidates: "
                                     f"{code_file_path} and file.name. "
                                     f"Please use only one file with name "
                                     f"'read_ISO3_submission_XXX.YYY'.")
                else:
                    if print_info:
                        print(f"Found UNFCCC_GHG_data file {file.relative_to(root_path)}")
                code_file_path = file

    if code_file_path is not None:
        return code_file_path.relative_to(root_path)
    else:
        return None