import copy

import pycountry
import json
import re
import xarray as xr
import pandas as pd
import numpy as np
from datetime import date
from copy import deepcopy
from typing import Dict, List, Optional
from pathlib import Path
from .definitions import custom_country_mapping, custom_folders
from .definitions import root_path, downloaded_data_path, extracted_data_path
from .definitions import legacy_data_path, code_path
from .definitions import GWP_factors


def process_data_for_country(
    data_country: xr.Dataset,
    entities_to_ignore: List[str],
    gas_baskets: Dict[str, List[str]],
    filter_dims: Optional[Dict[str, List[str]]] = None,
    cat_terminology_out: Optional[str] = None,
    category_conversion: Dict[str, Dict] = None,
    sectors_out: List[str] = None,
    processing_info_country: Dict = None,
) -> xr.Dataset:
    """
    Process data from DI interface (where necessary).
    * Downscaling including subtraction of time series
    * country specific sector aggregation
    * Conversion to IPCC2006 categories
    * general sector and gas basket aggregation (in new categories)
    """

    # 0: gather information
    countries = list(data_country.coords[data_country.attrs["area"]].values)
    if len(countries) > 1:
        raise ValueError(
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
        raise ValueError(
            f"Found {len(scenarios)} scenarios. Only single scenario data "
            f"can be processed by this function. Scenarios: {scenarios}"
        )
    scenario = scenarios[0]

    # get source
    sources = list(data_country.coords["source"].values)
    if len(sources) > 1:
        raise ValueError(
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
    data_country = data_country.dropna(f"time", how="all")
    # remove variables only containing nan
    nan_vars_country = [
        var
        for var in data_country.data_vars
        if bool(data_country[var].isnull().all().data) is True
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
                    if data_agg[var].isnull().all().data is True
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
            data_country = data_country.pr.dequantify()
            if "agg_tolerance" in processing_info_country:
                agg_tolerance = processing_info_country["agg_tolerance"]
            else:
                agg_tolerance = tolerance
            aggregate_cats_current = processing_info_country["aggregate_cats"]
            print(
                f"Aggregating categories for country {country_code}, source {source}, "
                f"scenario {scenario}"
            )
            for cat_to_agg in aggregate_cats_current:
                print(f"Category: {cat_to_agg}")
                source_cats = aggregate_cats_current[cat_to_agg]["sources"]
                data_agg = data_country.pr.loc[{"category": source_cats}].pr.sum(
                    dim="category", skipna=True, min_count=1
                )
                nan_vars = [
                    var
                    for var in data_agg.data_vars
                    if data_agg[var].isnull().all().data is True
                ]
                data_agg = data_agg.drop(nan_vars)
                if len(data_agg.data_vars) > 0:
                    data_agg = data_agg.expand_dims(
                        [f"category (" f"{cat_terminology_in})"]
                    )
                    data_agg = data_agg.assign_coords(
                        coords={
                            f"category ({cat_terminology_in})": (
                                f"category ({cat_terminology_in})",
                                [cat_to_agg],
                            )
                        }
                    )
                    if cat_name_present:
                        cat_name = aggregate_cats_current[cat_to_agg]["name"]
                        data_agg = data_agg.assign_coords(
                            coords={
                                "orig_cat_name": (
                                    f"category ({cat_terminology_in})",
                                    [cat_name],
                                )
                            }
                        )
                    data_country = data_country.pr.merge(
                        data_agg, tolerance=agg_tolerance
                    )
                else:
                    print(f"no data to aggregate category {cat_to_agg}")
            data_country = data_country.pr.quantify()

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
            # TODO: why use different code here than below. Can this fill non-existen
            #  gas baskets?
            for case in processing_info_country["aggregate_gases"].keys():
                case_info = processing_info_country["aggregate_gases"][case]
                data_country[
                    case_info["basket"]
                ] = data_country.pr.fill_na_gas_basket_from_contents(**case_info)

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
            for cat in data_country.coords[f"category ({cat_terminology_out})"].values
            if cat in sectors_out
        ]
        data_country = data_country.pr.loc[{"category": cats_to_keep}]

    # create gas baskets
    entities_present = set(data_country.data_vars)
    for basket in gas_baskets.keys():
        basket_contents_present = [
            gas for gas in gas_baskets[basket] if gas in entities_present
        ]
        if len(basket_contents_present) > 0:
            if basket in list(data_country.data_vars):
                data_country[basket] = data_country.pr.fill_na_gas_basket_from_contents(
                    basket=basket,
                    basket_contents=basket_contents_present,
                    skipna=True,
                    min_count=1,
                )
            else:
                try:
                    # print(data_country.data_vars)
                    data_country[basket] = xr.full_like(
                        data_country["CO2"], np.nan
                    ).pr.quantify(units="Gg CO2 / year")
                    data_country[basket].attrs = {
                        "entity": basket.split(" ")[0],
                        "gwp_context": basket.split(" ")[1][1:-1],
                    }
                    data_country[basket] = data_country.pr.gas_basket_contents_sum(
                        basket=basket,
                        basket_contents=basket_contents_present,
                        min_count=1,
                    )
                    entities_present.add(basket)
                except Exception as ex:
                    print(
                        f"No gas basket created for {country_code}, {source}, "
                        f"{scenario}: {ex}"
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
    conversion: Dict[str, Dict[str, str]],
    # terminology_from: str,
    terminology_to: str,
    debug: bool = False,
    tolerance: float = 0.01,
) -> xr.Dataset:
    """
    convert data from one category terminology to another
    """
    print(f"converting categories to {terminology_to}")

    if "orig_cat_name" in ds_input.coords:
        cat_name_present = True
    else:
        cat_name_present = False
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

        from_cats = ds_converted.coords[f"category ({terminology_to})"].values
        to_cats = pd.Series(from_cats).replace(conversion["mapping"])
        ds_converted = ds_converted.assign_coords(
            {f"category ({terminology_to})": (f"category ({terminology_to})", to_cats)}
        )

    # redo the list of present cats after mapping, as we have new categories in the
    # target terminology now
    cats_present_mapped = list(
        ds_converted.coords[f"category (" f"{terminology_to})"].values
    )
    # aggregate categories
    if "aggregate" in conversion:
        aggregate_cats = conversion["aggregate"]
        for cat_to_agg in aggregate_cats:
            if debug:
                print(f"Category: {cat_to_agg}")
            source_cats = [
                cat
                for cat in aggregate_cats[cat_to_agg]["sources"]
                if cat in cats_present_mapped
            ]
            if debug:
                print(source_cats)
            data_agg = ds_converted.pr.loc[{"category": source_cats}].pr.sum(
                dim="category", skipna=True, min_count=1
            )
            nan_vars = [
                var
                for var in data_agg.data_vars
                if data_agg[var].isnull().all().data == True
            ]
            data_agg = data_agg.drop(nan_vars)
            if len(data_agg.data_vars) > 0:
                data_agg = data_agg.expand_dims([f"category ({terminology_to})"])
                data_agg = data_agg.assign_coords(
                    coords={
                        f"category ({terminology_to})": (
                            f"category ({terminology_to})",
                            [cat_to_agg],
                        )
                    }
                )
                if cat_name_present:
                    data_agg = data_agg.assign_coords(
                        coords={
                            "orig_cat_name": (
                                f"category ({terminology_to})",
                                [aggregate_cats[cat_to_agg]["name"]],
                            )
                        }
                    )
                ds_converted = ds_converted.pr.merge(data_agg, tolerance=tolerance)
                cats_present_mapped.append(cat_to_agg)
            else:
                print(f"no data to aggregate category {cat_to_agg}")

    return ds_converted


def get_country_name(
    country_code: str,
) -> str:
    """get country name from code"""
    if country_code in custom_country_mapping:
        country_name = custom_country_mapping[country_code]
    else:
        try:
            country = pycountry.countries.get(alpha_3=country_code)
            country_name = country.name
        except:
            raise ValueError(
                f"Country code {country_code} can not be mapped to " f"any country"
            )

    return country_name


def get_country_code(
    country_name: str,
) -> str:
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
                country = pycountry.countries.search_fuzzy(
                    country_name.replace("_", " ")
                )
            except:
                raise ValueError(
                    f"Country name {country_name} can not be mapped to "
                    f"any country code. Try using the ISO3 code directly."
                )
            if len(country) > 1:
                country_code = None
                for current_country in country:
                    if current_country.name == country_name:
                        country_code = current_country.alpha_3
                if country_code is None:
                    raise ValueError(
                        f"Country name {country_name} has {len(country)} "
                        f"possible results for country codes."
                    )

            country_code = country[0].alpha_3

    return country_code


def create_folder_mapping(folder: str, extracted: bool = False) -> None:
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

        json.dump(dict(sorted(folder_mapping.items())), mapping_file, indent=4)


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
                    raise ValueError(
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
                            data_info = data_info + f"code: not found"

                        cleaned_datasets_current_folder[key] = data_info

                if print_ds:
                    if cleaned_datasets_current_folder:
                        for country_ds in cleaned_datasets_current_folder:
                            print(
                                f"{country_ds}: {cleaned_datasets_current_folder[country_ds]}"
                            )
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
                    raise ValueError(
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
                            f"Wrong UNFCCC_GHG_data: {parts[0]}"
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
                                f"{country_ds}: {cleaned_datasets_current_folder[country_ds]}"
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
                    raise ValueError(
                        f"Found multiple UNFCCC_GHG_data candidates: "
                        f"{code_file_path} and file.name. "
                        f"Please use only one file with name "
                        f"'read_ISO3_submission_XXX.YYY'."
                    )
                else:
                    if print_info:
                        print(
                            f"Found UNFCCC_GHG_data file {file.relative_to(root_path)}"
                        )
                code_file_path = file

    if code_file_path is not None:
        return code_file_path.relative_to(root_path)
    else:
        return None


def fix_rows(
    data: pd.DataFrame, rows_to_fix: list, col_to_use: str, n_rows: int
) -> pd.DataFrame:
    """
    Function to fix rows that have been split during reading from pdf
    This is the version used for Malaysia BUR3,4. adapt for other BURs if needed

    :param data:
    :param rows_to_fix:
    :param col_to_use:
    :param n_rows:
    :return:
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
        if n_rows == -2:
            locs_to_merge = list(range(loc - 1, loc + 1))
        elif n_rows == -3:
            locs_to_merge = list(range(loc - 1, loc + 2))
        elif n_rows == -5:
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
        repl = lambda m: f"{m.group('first')}{m.group('last')}"
        new_row = new_row.str.replace(pat, repl, regex=True)
        data.loc[indices_to_merge[0]] = new_row
        data = data.drop(indices_to_merge[1:])
    return data
