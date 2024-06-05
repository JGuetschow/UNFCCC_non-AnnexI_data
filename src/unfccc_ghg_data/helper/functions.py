"""common functions for unfccc_ghg_data

Functions used by the different readers and downloaders in the unfccc_ghg_data package
"""
from __future__ import annotations

import copy
import json
import re
import warnings
from collections.abc import Hashable
from copy import deepcopy
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import pycountry
import xarray as xr

from .definitions import (
    GWP_factors,
    code_path,
    custom_country_mapping,
    custom_folders,
    downloaded_data_path,
    extracted_data_path,
    legacy_data_path,
    root_path,
)


def process_data_for_country(  # noqa PLR0913, PLR0912, PLR0915
    data_country: xr.Dataset,
    entities_to_ignore: list[str],
    gas_baskets: dict[str, list[str]],
    filter_dims: dict[str, list[str]] | None = None,
    cat_terminology_out: str | None = None,
    category_conversion: dict[str, dict] | None = None,
    sectors_out: list[str] | None = None,
    processing_info_country: dict | None = None,
) -> xr.Dataset:
    """
    Process data from DI interface (where necessary).

    * Downscaling including subtraction of time series
    * country specific sector aggregation
    * Conversion to IPCC2006 categories
    * general sector and gas basket aggregation (in new categories)

    Parameters
    ----------
    data_country: xr.Dataset
        data to process
    entities_to_ignore: list[str]
        Which entities should be ignored. They will not be in the returned dataset
    gas_baskets: dict[str, list[str]
        Gas baskets to create. Each entry consists of the basket as key and a list of
        gases that make up the basket as value
    filter_dims: Optional[dict[str, list[str]]] = None
        filter data before processing. Filter is in the format taken by PRIMAP2's
        ds.pr.loc[] functionality
    cat_terminology_out: Optional[str] = None
        Category terminology for the output dataset
    category_conversion: dict[str, dict] = None
        Definition of category conversion. The dict has two possible fields:
        * "conversion" where the value is a dict[str, str] with 1 to 1 category code
        mapping (key is category from and value is category to)
        * "aggregation" TODO
    sectors_out: list[str] = None
        Categories to return
    processing_info_country
        more detailed processing info TODO: explain format
        The "aggregate_cats" flag is deprecated and will be removed in a future
        version. Please use "aggregate_coord" with key "category" instead

    Returns
    -------
    xr.Dataset: processed dataset

    """
    # 0: gather information
    countries = list(data_country.coords[data_country.attrs["area"]].values)
    if len(countries) > 1:
        raise ValueError(  # noqa: TRY003
            f"Found {len(countries)} countries. Only single country data "
            f"can be processed by this function. countries: {countries}"
        )
    else:
        country_code = countries[0]

    # get category terminology
    cat_col = data_country.attrs["cat"]
    temp = re.findall(r"\((.*)\)", cat_col)
    cat_terminology_in = temp[0]

    # get scenario
    scenarios = list(data_country.coords[data_country.attrs["scen"]].values)
    if len(scenarios) > 1:
        raise ValueError(  # noqa: TRY003
            f"Found {len(scenarios)} scenarios. Only single scenario data "
            f"can be processed by this function. Scenarios: {scenarios}"
        )
    scenario = scenarios[0]

    # get source
    sources = list(data_country.coords["source"].values)
    if len(sources) > 1:
        raise ValueError(  # noqa: TRY003
            f"Found {len(sources)} sources. Only single source data "
            f"can be processed by this function. Sources: {sources}"
        )
    source = sources[0]

    # check if category name column present
    # TODO: replace 'name' in config by  'additional_cols' dict that defines the cols
    #  and the values
    if "orig_cat_name" in data_country.coords:
        cat_name_present = True
    else:
        cat_name_present = False

    # 1: general processing
    # remove unused cats
    data_country = data_country.dropna(f"category ({cat_terminology_in})", how="all")
    # remove unused years
    data_country = data_country.dropna("time", how="all")
    # remove variables only containing nan
    nan_vars_country = [
        var
        for var in data_country.data_vars
        if bool(data_country[var].isnull().all().data) is True  # noqa: PD003
    ]
    print(f"removing all-nan variables: {nan_vars_country}")
    data_country = data_country.drop_vars(nan_vars_country)

    # remove unnecessary variables
    entities_ignore_present = [
        entity for entity in entities_to_ignore if entity in data_country.data_vars
    ]
    data_country = data_country.drop_vars(entities_ignore_present)

    # filter ()
    if filter_dims is not None:
        data_country = data_country.pr.loc[filter_dims]

    # 2: country specific processing
    if processing_info_country is not None:
        if "tolerance" in processing_info_country:
            tolerance = processing_info_country["tolerance"]
        else:
            tolerance = 0.01

        # remove entities if needed
        if "ignore_entities" in processing_info_country:
            entities_to_ignore_country = processing_info_country["ignore_entities"]
            entities_ignore_present = [
                entity
                for entity in entities_to_ignore_country
                if entity in data_country.data_vars
            ]
            data_country = data_country.drop_vars(entities_ignore_present)

        # take only desired years
        if "years" in processing_info_country:
            data_country = data_country.pr.loc[
                {"time": processing_info_country["years"]}
            ]

        # remove timeseries if desired
        if "remove_ts" in processing_info_country:
            for case in processing_info_country["remove_ts"]:
                remove_info = copy.deepcopy(processing_info_country["remove_ts"][case])
                entities = remove_info.pop("entities")
                for entity in entities:
                    data_country[entity].pr.loc[remove_info] = (
                        data_country[entity].pr.loc[remove_info] * np.nan
                    )

        # remove all data for given years if necessary
        if "remove_years" in processing_info_country:
            data_country = data_country.drop_sel(
                time=processing_info_country["remove_years"]
            )

        # subtract categories
        if "subtract_cats" in processing_info_country:
            subtract_cats_current = processing_info_country["subtract_cats"]
            print(f"Subtracting categories for country {country_code}")
            for cat_to_generate in subtract_cats_current:
                if "entities" in subtract_cats_current[cat_to_generate].keys():
                    entities_current = subtract_cats_current[cat_to_generate][
                        "entities"
                    ]
                else:
                    entities_current = list(data_country.data_vars)

                cats_to_subtract = subtract_cats_current[cat_to_generate]["subtract"]
                data_sub = (
                    data_country[entities_current]
                    .pr.loc[{"category": cats_to_subtract}]
                    .pr.sum(dim="category", skipna=True, min_count=1)
                )
                data_parent = data_country[entities_current].pr.loc[
                    {"category": subtract_cats_current[cat_to_generate]["parent"]}
                ]
                data_agg = data_parent - data_sub
                nan_vars = [
                    var
                    for var in data_agg.data_vars
                    if data_agg[var].isnull().all().data is True  # noqa: PD003
                ]
                data_agg = data_agg.drop(nan_vars)
                if len(data_agg.data_vars) > 0:
                    print(f"Generating {cat_to_generate} through subtraction")
                    data_agg = data_agg.expand_dims(
                        [f"category (" f"{cat_terminology_in})"]
                    )

                    data_agg = data_agg.assign_coords(
                        coords={
                            f"category ({cat_terminology_in})": (
                                f"category ({cat_terminology_in})",
                                [cat_to_generate],
                            )
                        }
                    )
                    if cat_name_present:
                        cat_name = subtract_cats_current[cat_to_generate]["name"]
                        data_agg = data_agg.assign_coords(
                            coords={
                                "orig_cat_name": (
                                    f"category ({cat_terminology_in})",
                                    [cat_name],
                                )
                            }
                        )
                    data_country = data_country.pr.merge(data_agg, tolerance=tolerance)
                else:
                    print(f"no data to generate category {cat_to_generate}")

        # downscaling
        if "downscale" in processing_info_country:
            if "sectors" in processing_info_country["downscale"]:
                sector_downscaling = processing_info_country["downscale"]["sectors"]
                for case in sector_downscaling.keys():
                    print(f"Downscaling for {case}.")
                    sector_downscaling_current = sector_downscaling[case]
                    entities = sector_downscaling_current.pop("entities")
                    for entity in entities:
                        data_country[entity] = data_country[
                            entity
                        ].pr.downscale_timeseries(**sector_downscaling_current)
                        # , skipna_evaluation_dims=None)

            if "entities" in processing_info_country["downscale"]:
                entity_downscaling = processing_info_country["downscale"]["entities"]
                for case in entity_downscaling.keys():
                    print(f"Downscaling for {case}.")
                    # print(data_country.coords[f'category ('
                    #                          f'{cat_terminology_in})'].values)
                    data_country = data_country.pr.downscale_gas_timeseries(
                        **entity_downscaling[case],
                        skipna=True,
                        skipna_evaluation_dims=None,
                    )

        # aggregate categories
        if "aggregate_cats" in processing_info_country:
            warnings.warn(
                'The "aggregate_cats" flag is deprecated and will '
                "be removed in a future version. Please use "
                '"aggregate_coord" with key "category" instead',
                category=DeprecationWarning,
            )
            print(
                f"Aggregating categories for country {country_code}, source {source}, "
                f"scenario {scenario}"
            )

            # prep input to add_aggregates_coordinates
            agg_info = {"category": processing_info_country["aggregate_cats"]}

            if "agg_tolerance" in processing_info_country:
                agg_tolerance = processing_info_country["agg_tolerance"]
            else:
                agg_tolerance = tolerance

            data_country = data_country.pr.add_aggregates_coordinates(
                agg_info=agg_info,
                tolerance=agg_tolerance,
                skipna=True,
                min_count=1,
            )

        if "aggregate_coord" in processing_info_country:
            print(
                f"Aggregating data for country {country_code}, source {source}, "
                f"scenario {scenario}"
            )
            data_country = data_country.pr.add_aggregates_coordinates(
                agg_info=processing_info_country["aggregate_coords"],
                skipna=True,
                min_count=1,
            )

        # copy HFCs and PFCs with default factors
        if "basket_copy" in processing_info_country:
            GWPs_to_add = processing_info_country["basket_copy"]["GWPs_to_add"]
            entities = processing_info_country["basket_copy"]["entities"]
            source_GWP = processing_info_country["basket_copy"]["source_GWP"]
            for entity in entities:
                data_source = data_country[f"{entity} ({source_GWP})"]
                for GWP in GWPs_to_add:
                    data_GWP = (
                        data_source * GWP_factors[f"{source_GWP}_to_{GWP}"][entity]
                    )
                    data_GWP.attrs["entity"] = entity
                    data_GWP.attrs["gwp_context"] = GWP
                    data_country[f"{entity} ({GWP})"] = data_GWP

        # aggregate gases if desired
        if "aggregate_gases" in processing_info_country:
            data_country = data_country.pr.add_aggregates_variables(
                gases=processing_info_country["aggregate_gases"],
            )

    # 3: map categories
    if category_conversion is not None:
        data_country = convert_categories(
            data_country,
            category_conversion,
            cat_terminology_out,
            debug=False,
            tolerance=0.01,
        )
    else:
        cat_terminology_out = cat_terminology_in

    # more general processing
    # reduce categories to output cats
    if sectors_out is not None:
        cats_to_keep = [
            cat
            for cat in data_country.coords[
                f"category ({cat_terminology_out})"
            ].to_numpy()
            if cat in sectors_out
        ]
        data_country = data_country.pr.loc[{"category": cats_to_keep}]

    # create gas baskets
    if gas_baskets:
        data_country = data_country.pr.add_aggregates_variables(
            gas_baskets=gas_baskets, skipna=True, min_count=1
        )

    # amend title and comment
    data_country.attrs["comment"] = (
        data_country.attrs["comment"] + f" Processed on " f"{date.today()}"
    )
    data_country.attrs["title"] = (
        data_country.attrs["title"] + f" Processed on " f"{date.today()}"
    )

    return data_country


def convert_categories(
    ds_input: xr.Dataset,
    conversion: dict[str, dict[str, str]],
    # terminology_from: str,
    terminology_to: str,
    debug: bool = False,
    tolerance: float = 0.01,
) -> xr.Dataset:
    """
    convert data from one category terminology to another

    """
    print(f"converting categories to {terminology_to}")

    ds_converted = ds_input.copy(deep=True)
    ds_converted.attrs = deepcopy(ds_input.attrs)
    # TODO: change attrs for additional coordinates

    # change category terminology
    cat_dim = ds_converted.attrs["cat"]
    ds_converted.attrs["cat"] = f"category ({terminology_to})"
    ds_converted = ds_converted.rename({cat_dim: ds_converted.attrs["cat"]})

    # find categories present in dataset
    cats_present = list(ds_converted.coords[f"category ({terminology_to})"])

    # restrict categories and map category names
    if "mapping" in conversion.keys():
        mapping_cats_present = [
            cat for cat in list(conversion["mapping"].keys()) if cat in cats_present
        ]
        ds_converted = ds_converted.pr.loc[{"category": mapping_cats_present}]

        from_cats = ds_converted.coords[f"category ({terminology_to})"].to_numpy()
        to_cats = pd.Series(from_cats).replace(conversion["mapping"])
        ds_converted = ds_converted.assign_coords(
            {f"category ({terminology_to})": (f"category ({terminology_to})", to_cats)}
        )

    # aggregate categories
    if "aggregate" in conversion:
        agg_info = {
            "category": conversion["aggregate"],
        }
        ds_converted = ds_converted.pr.add_aggregates_coordinates(
            agg_info=agg_info,
            tolerance=tolerance,
            skipna=True,
            min_count=1,
        )
    return ds_converted


def get_country_name(
    country_code: str,
) -> str:
    """Get country name from code"""
    if country_code in custom_country_mapping:
        country_name = custom_country_mapping[country_code]
    else:
        try:
            country = pycountry.countries.get(alpha_3=country_code)
            country_name = country.name
        except:  # noqa: E722
            raise ValueError(  # noqa: TRY003, TRY200
                f"Country code {country_code} can not be mapped to " f"any country"
            )

    return country_name


def get_country_code(
    country_name: str,
) -> str:
    """
    Obtain country code.

    If the input is a code it will be returned,
    if the input is not a three letter code a search will be performed

    Parameters
    ----------
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
            # check if it's a 3 letter code
            country = pycountry.countries.get(alpha_3=country_name)
            country_code = country.alpha_3
        except:  # noqa: E722
            try:
                country = pycountry.countries.search_fuzzy(
                    country_name.replace("_", " ")
                )
            except:  # noqa: E722
                raise ValueError(  # noqa: TRY200, TRY003
                    f"Country name {country_name} can not be mapped to "
                    f"any country code. Try using the ISO3 code directly."
                )
            if len(country) > 1:
                country_code = None
                for current_country in country:
                    if current_country.name == country_name:
                        country_code = current_country.alpha_3
                if country_code is None:
                    raise ValueError(  # noqa: TRY200, TRY003
                        f"Country name {country_name} has {len(country)} "
                        f"possible results for country codes."
                    )

            country_code = country[0].alpha_3

    return country_code


def create_folder_mapping(  # noqa: PLR0912
    folder: str, extracted: bool = False
) -> None:
    """
    Create a mapping of iso codes to folder names

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
    # if not extracted:
    known_folders = custom_folders
    # else:
    #    known_folders = {}

    for item in folder.iterdir():
        if item.is_dir() and not item.match("__pycache__"):
            if item.name in known_folders:
                ISO3 = known_folders[item.name]
            else:
                try:
                    country = pycountry.countries.search_fuzzy(
                        item.name.replace("_", " ")
                    )
                    if len(country) > 1:
                        ISO3 = None
                        for current_country in country:
                            if current_country.name == item.name.replace("_", " "):
                                ISO3 = current_country.alpha_3
                    else:
                        ISO3 = country[0].alpha_3
                except:  # noqa: E722
                    ISO3 = None

            if ISO3 is None:
                print(f"No match for {item.name}")
            elif ISO3 in folder_mapping.keys():
                folder_mapping[ISO3] = [folder_mapping[ISO3], item.name]
            else:
                folder_mapping[ISO3] = item.name

    with open(folder / "folder_mapping.json", "w") as mapping_file:
        json.dump(dict(sorted(folder_mapping.items())), mapping_file, indent=4)


# TODO add crf
def get_country_submissions(  # noqa: PLR0912
    country_name: str,
    print_sub: bool = True,
) -> dict[str, list[str]]:
    """
    Get all submissions for a country

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
    data_folder = downloaded_data_path

    country_code = get_country_code(country_name)

    if print_sub:
        print(f"Country name {country_name} maps to ISO code {country_code}")

    country_submissions = {}
    if print_sub:
        print("#" * 80)
        print(f"The following submissions are available for {country_name}")
    for item in data_folder.iterdir():
        if item.is_dir():
            if print_sub:
                print("")
                print("-" * 80)
                print(f"Data folder {item.name}")
                print("-" * 80)
            with open(item / "folder_mapping.json") as mapping_file:
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


def get_country_datasets(  # noqa: PLR0915, PLR0912
    country_name: str,
    print_ds: bool = True,
) -> dict[str, list[str]]:
    """
    Get all datasets for a country

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
    data_folder = extracted_data_path
    data_folder_legacy = legacy_data_path

    # obtain country code
    country_code = get_country_code(country_name)

    if print_ds:
        print(f"Country name {country_name} maps to ISO code {country_code}")

    rep_data = {}
    # data
    if print_ds:
        print("#" * 80)
        print(f"The following datasets are available for {country_name}")
    for item in data_folder.iterdir():
        if item.is_dir():
            cleaned_datasets_current_folder = {}
            if print_ds:
                print("-" * 80)
                print(f"Data folder {item.name}")
                print("-" * 80)
            with open(item / "folder_mapping.json") as mapping_file:
                folder_mapping = json.load(mapping_file)
            if country_code not in folder_mapping:
                if print_ds:
                    print("No data available")
                    print("")
            else:
                country_folder = folder_mapping[country_code]
                if not isinstance(country_folder, str):
                    raise ValueError(  # noqa: TRY003
                        "Wrong data type in folder mapping json file. Should be str."
                    )

                datasets_current_folder = {}
                current_folder = item / country_folder

                for data_file in current_folder.iterdir():
                    if data_file.suffix in [".nc", ".yaml", ".csv"]:
                        if data_file.stem in datasets_current_folder:
                            datasets_current_folder[data_file.stem].append(
                                data_file.suffix
                            )
                        else:
                            datasets_current_folder[data_file.stem] = [data_file.suffix]

                for dataset in datasets_current_folder:
                    # process filename to get submission
                    parts = dataset.split("_")
                    if parts[0] != country_code:
                        cleaned_datasets_current_folder[
                            f"Wrong code: {parts[0]}"
                        ] = dataset
                    else:
                        terminology = "_".join(parts[3:])
                        key = f"{parts[1]} ({parts[2]}, {terminology})"
                        data_info = ""
                        if ".nc" in datasets_current_folder[dataset]:
                            data_info = data_info + "NF (.nc), "
                        if (".csv" in datasets_current_folder[dataset]) and (
                            ".yaml" in datasets_current_folder[dataset]
                        ):
                            data_info = data_info + "IF (.yaml + .csv), "
                        elif ".csv" in datasets_current_folder[dataset]:
                            data_info = data_info + "incomplete IF? (.csv), "
                        elif ".yaml" in datasets_current_folder[dataset]:
                            data_info = data_info + "incomplete IF (.yaml), "

                        code_file = get_code_file(country_code, parts[1])
                        if code_file:
                            data_info = data_info + f"code: {code_file.name}"
                        else:
                            data_info = data_info + "code: not found"

                        cleaned_datasets_current_folder[key] = data_info

                if print_ds:
                    if cleaned_datasets_current_folder:
                        for country_ds in cleaned_datasets_current_folder:
                            print(
                                f"{country_ds}: "
                                f"{cleaned_datasets_current_folder[country_ds]}"
                            )
                    else:
                        print("No data available")
                    print("")

            rep_data[item.name] = cleaned_datasets_current_folder

    # legacy data
    if print_ds:
        print("#" * 80)
        print(f"The following legacy datasets are available for {country_name}")
    legacy_data = {}
    for item in data_folder_legacy.iterdir():
        if item.is_dir():
            cleaned_datasets_current_folder = {}
            if print_ds:
                print("-" * 80)
                print(f"Data folder {item.name}")
                print("-" * 80)
            with open(item / "folder_mapping.json") as mapping_file:
                folder_mapping = json.load(mapping_file)
            if country_code not in folder_mapping:
                if print_ds:
                    print("No data available")
                    print("")
            else:
                country_folder = folder_mapping[country_code]
                if not isinstance(country_folder, str):
                    raise ValueError(  # noqa: TRY003
                        "Wrong data type in folder mapping json file. Should be str."
                    )

                datasets_current_folder = {}
                current_folder = item / country_folder

                for data_file in current_folder.iterdir():
                    if data_file.suffix in [".nc", ".yaml", ".csv"]:
                        if data_file.stem in datasets_current_folder:
                            datasets_current_folder[data_file.stem].append(
                                data_file.suffix
                            )
                        else:
                            datasets_current_folder[data_file.stem] = [data_file.suffix]

                for dataset in datasets_current_folder:
                    # process filename to get submission
                    parts = dataset.split("_")
                    if parts[0] != country_code:
                        cleaned_datasets_current_folder[
                            f"Wrong code: {parts[0]}"
                        ] = dataset
                    else:
                        terminology = "_".join(parts[3:])
                        key = f"{parts[1]} ({parts[2]}, {terminology}, legacy)"
                        data_info = ""
                        if ".nc" in datasets_current_folder[dataset]:
                            data_info = data_info + "NF (.nc), "
                        if (".csv" in datasets_current_folder[dataset]) and (
                            ".yaml" in datasets_current_folder[dataset]
                        ):
                            data_info = data_info + "IF (.yaml + .csv), "
                        elif ".csv" in datasets_current_folder[dataset]:
                            data_info = data_info + "incomplete IF? (.csv), "
                        elif ".yaml" in datasets_current_folder[dataset]:
                            data_info = data_info + "incomplete IF (.yaml), "

                        cleaned_datasets_current_folder[key] = data_info

                if print_ds:
                    if cleaned_datasets_current_folder:
                        for country_ds in cleaned_datasets_current_folder:
                            print(
                                f"{country_ds}: "
                                f"{cleaned_datasets_current_folder[country_ds]}"
                            )
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
            String containing the country name or ISO 3 letter code

        submission: str
            String of the submission

        print_info: bool = False
            If True print information on code found

    Returns
    -------
        returns a pathlib Path object for the code file
    """
    code_file_path = None
    UNFCCC_reader_path = code_path / "unfccc_reader"

    # CRF is an exception as it's read using the unfccc_crf_reader module
    # so we return the path to that.
    if submission[0:3] in ("CRF", "CRT"):
        return root_path / "unfccc_crf_reader"

    if submission[0:2] == "DI":
        return root_path / "unfccc_di_reader"

    # replace "-" by "_" in submission
    submission = submission.replace("-", "_")

    # obtain country code
    country_code = get_country_code(country_name)

    if print_info:
        print(f"Country name {country_name} maps to ISO code {country_code}")

    with open(UNFCCC_reader_path / "folder_mapping.json") as mapping_file:
        folder_mapping = json.load(mapping_file)

    if country_code not in folder_mapping:
        if print_info:
            print("No code available")
            print("")
    else:
        country_folder = UNFCCC_reader_path / folder_mapping[country_code]
        code_file_name_candidate = "read_" + country_code + "_" + submission + "*"

        for file in country_folder.iterdir():
            if file.match(code_file_name_candidate):
                if code_file_path is not None:
                    raise ValueError(  # noqa: TRY003
                        f"Found multiple code candidates: "
                        f"{code_file_path} and file.name. "
                        f"Please use only one file with name "
                        f"'read_ISO3_submission_XXX.YYY'."
                    )
                elif print_info:
                    print(f"Found code file {file.relative_to(root_path)}")
                code_file_path = file

    if code_file_path is not None:
        return code_file_path.relative_to(root_path)
    else:
        return None


def fix_rows(
    data: pd.DataFrame, rows_to_fix: list, col_to_use: str, n_rows: int
) -> pd.DataFrame:
    """
    Fix rows that have been split during reading from pdf

    This is the version used for Malaysia BUR3,4. adapt for other BURs if needed

    Parameters
    ----------
    data
    rows_to_fix
    col_to_use
    n_rows

    Returns
    -------
    Dataframe with fixed rows

    """
    for row in rows_to_fix:
        # print(row)
        # find the row number and collect the row and the next two rows
        index = data.loc[data[col_to_use] == row].index
        # print(list(index))
        if not list(index):
            print(f"Can't merge split row {row}")
            print(data[col_to_use])
        # print(f"Merging split row {row} for table {page}")
        loc = data.index.get_loc(index[0])
        # TODO: formula for negative values
        if n_rows == -2:  # noqa: PLR2004
            locs_to_merge = list(range(loc - 1, loc + 1))
        elif n_rows == -3:  # noqa: PLR2004
            locs_to_merge = list(range(loc - 1, loc + 2))
        elif n_rows == -5:  # noqa: PLR2004
            locs_to_merge = list(range(loc - 1, loc + 4))
        else:
            locs_to_merge = list(range(loc, loc + n_rows))
        rows_to_merge = data.iloc[locs_to_merge]
        indices_to_merge = rows_to_merge.index
        # join the three rows
        new_row = rows_to_merge.agg(" ".join)
        # replace the double spaces that are created
        # must be done here and not at the end as splits are not always
        # the same and join would produce different col values
        new_row = new_row.str.replace("  ", " ")
        new_row = new_row.str.replace("N O", "NO")
        new_row = new_row.str.replace(", N", ",N")
        new_row = new_row.str.replace("- ", "-")
        # replace spaces in numbers
        pat = r"^(?P<first>[0-9\.,]*)\s(?P<last>[0-9\.,]*)$"

        def repl(m):
            return f"{m.group('first')}{m.group('last')}"

        new_row = new_row.str.replace(pat, repl, regex=True)
        data.loc[indices_to_merge[0]] = new_row
        data = data.drop(indices_to_merge[1:])
    return data


def make_wide_table(
    data: pd.DataFrame,
    keyword: str,
    col: int | str,
    index_cols: list[int | str],
) -> pd.DataFrame:
    """
    Make a wide table from a table which is a stack of tables for different time periods

    Parameters
    ----------
    data
        Input table as pandas.DataFrame
    keyword
    col
    index_cols

    Returns
    -------
    pandas.DataFrame in wide format

    """
    index = data.loc[data[col] == keyword].index
    if not list(index):
        print("Keyword for table transformation not found")
        return data
    elif len(index) == 1:
        print("Keyword for table transformation found only once")
        return data
    else:
        df_all = None
        for i, item in enumerate(index):
            loc = data.index.get_loc(item)
            if i < len(index) - 1:
                next_loc = data.index.get_loc(index[i + 1])
            else:
                next_loc = data.index[-1] + 1
            df_to_add = data.loc[list(range(loc, next_loc))]
            # select only cols which don't have NaN, Null, or '' as header
            filter_nan = (
                (~df_to_add.iloc[0].isna())
                & (df_to_add.iloc[0] != "NaN")
                & (df_to_add.iloc[0])
            )
            df_to_add = df_to_add.loc[:, filter_nan]
            df_to_add.columns = df_to_add.iloc[0]
            # print(df_to_add.columns)
            df_to_add = df_to_add.drop(loc)
            df_to_add = df_to_add.set_index(index_cols)

            if df_all is None:
                df_all = df_to_add
            else:
                df_all = pd.concat([df_all, df_to_add], axis=1, join="outer")
        return df_all


def find_and_replace_values(
    df: pd.DataFrame,
    replace_info: list[tuple[str | float]],
    category_column: str,
    entity_column: str = "entity",
) -> pd.DataFrame:
    """
    Find values and replace single values in a dataframe.

    Parameters
    ----------
    df
        Input data frame
    replace_info
        Category, entity, year, and new value. Don't put a new value if you
        would like to replace with nan.
        For example [("3.C", "CO", "2019", 3.423)] or [("3.C", "CO", "2019")]
    category_column
        The name of the column that contains the categories.
    entity_column
        The name of the column that contains the categories.

    Output
    ------
        Data frame with updated values.

    """
    for replace_info_value in replace_info:
        category = replace_info_value[0]
        entity = replace_info_value[1]
        year = replace_info_value[2]

        if len(replace_info_value) == 4:  # noqa: PLR2004
            new_value = replace_info_value[3]
        elif len(replace_info_value) == 3:  # noqa: PLR2004
            new_value = np.nan
        else:
            raise AssertionError(  # noqa: TRY003
                f"Expected tuple of length 3 or 4. Got {replace_info_value}"
            )

        index = df.loc[
            (df[category_column] == category) & (df[entity_column] == entity),
        ].index[0]

        # pandas recommends using .at[] for changing single values
        df.loc[index, year] = new_value
        print(f"Set value for {category}, {entity}, {year} to {new_value}.")

    return df


def set_to_nan_in_ds(
    ds_in: xr.Dataset,
    entities: list[Hashable],
    filter: dict[str, any],
) -> xr.Dataset:
    """
    Set values to NaN in a data set.

    Parameters
    ----------
    ds_in:
        input dataset
    entities
        list of entities to work on
    filter
        .pr.loc type selector which selects the elements that should be replaced
        with nan

    Returns
    -------
        xr.Dataset with the desired values set to nan
    """
    ds_mask = xr.zeros_like(ds_in[entities].pr.loc[filter]).combine_first(
        xr.ones_like(ds_in)
    )

    return ds_in.where(ds_mask)


def assert_values(
    df: pd.DataFrame,
    test_case: tuple[str | float | int],
    category_column: str = "category (IPCC1996_2006_GIN_Inv)",
    entity_column: str = "entity",
) -> None:
    """
    Check if a value in a dataframe matches the expected value.

    Parameters
    ----------
    df
        The data frame to check.
    test_case
        The combination of parameters and the expected value.
        Use the format (<category>, <entity>, <year>, <expected_value>).
    category_column
        The columns where to look for the category.
    entity_column
        The column where to look for the entity.
    """
    category = test_case[0]
    entity = test_case[1]
    year = test_case[2]
    expected_value = test_case[3]

    assert isinstance(  # noqa: S101
        expected_value, (float, int)
    ), (
        "This function only works for numbers. "
        "Use assert_nan_values to check for NaNs "
        "and empty values."
    )

    arr = df.loc[
        (df[category_column] == category) & (df[entity_column] == entity), year
    ].to_numpy()

    # Assert the category exists in the data frame
    assert (  # noqa: S101
        category in df[category_column].unique()
    ), f"{category} is not a valid category. Choose from {df[category_column].unique()}"

    # Assert the entity exists in the data frame
    assert (  # noqa: S101
        entity in df[entity_column].unique()
    ), f"{entity} is not a valid entity. Choose from {df[entity_column].unique()}"

    assert (  # noqa: S101
        arr.size > 0
    ), f"No value found for category {category}, entity {entity}, year {year}!"

    assert (  # noqa: S101
        arr.size <= 1
    ), (
        f"More than one value found for category {category}, entity {entity}, "
        f"year {year}!"
    )

    assert (  # noqa: S101
        arr[0] == test_case[3]
    ), f"Expected value {expected_value}, actual value is {arr[0]}"

    print(
        f"Value for category {category}, entity {entity}, year {year} is as expected."
    )


def assert_nan_values(
    df: pd.DataFrame,
    test_case: tuple[str, ...],
    category_column: str = "category (IPCC1996_2006_GIN_Inv)",
    entity_column: str = "entity",
) -> None:
    """
    Check for empty, NE, NE1 values

    Check if values that are empty or NE or NE1 in the PDF tables
    are not present in the dataset.

    Parameters
    ----------
    df
        The data frame to check.
    test_case
        The combination of input parameters.
        Use the format (<category>, <entity>, <year>).
    category_column
        The columns where to look for the category.
    entity_column
        The column where to look for the entity.

    """
    category = test_case[0]
    entity = test_case[1]
    year = test_case[2]

    if category not in df[category_column].unique():
        warning_string = (
            f"{category} is not in the data set. Either all values "
            f"for this category are NaN or the category never "
            f"existed in the data set."
        )
        warnings.warn(warning_string)
        return

    if entity not in df[entity_column].unique():
        warning_string = (
            f"{entity} is not in the data set. Either all values "
            f"for this entity are NaN or the category never "
            f"existed in the data set."
        )
        warnings.warn(warning_string)
        return

    arr = df.loc[
        (df[category_column] == category) & (df[entity_column] == entity), year
    ].to_numpy()

    assert np.isnan(arr[0]), f"Value is {arr[0]} and not NaN."  # noqa: S101

    print(f"Value for category {category}, entity {entity}, year {year} is NaN.")
