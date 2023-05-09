import primap2 as pm2
import unfccc_di_api
import pandas as pd
import numpy as np
import pycountry
import itertools
import json
import copy
import xarray as xr
from datetime import date
from typing import Optional, Dict, List
from pathlib import Path
from copy import deepcopy

from UNFCCC_DI_reader_config import di_to_pm2if_template_nai
from UNFCCC_DI_reader_config import di_to_pm2if_template_ai
from UNFCCC_DI_reader_config import di_query_filters
from UNFCCC_DI_reader_config import cat_conversion
from util import NoDIDataError, extracted_data_path, get_country_name
from util import nAI_countries, AI_countries


def read_UNFCCC_DI_for_country(
        country_code: str,
        category_groups: Optional[Dict]=None,
        read_subsectors: bool=False,
        save_data: Optional[bool]=True,
        date_str: Optional[str]=None,
        pm2if_specifications: Optional[dict]=None,
        default_gwp: Optional[str]=None,
        debug: Optional[bool]=False,
):
    """
    reads data for a country from the UNFCCC DI interface and saves to native and
    interchange format
    """

    # read the data
    data_df = read_UNFCCC_DI_for_country_df(
        country_code=country_code,
        category_groups=category_groups,
        read_subsectors=read_subsectors,
        debug=debug,
    )

    # set date_str if not given
    if date_str is None:
        date_str = str(date.today())

    # determine filename
    if save_data:
        filename = determine_filename(country_code, date_str, True)
    else:
        filename = None

    # convert raw data to pm2 interchange format and save
    data_if = convert_DI_data_to_pm2_if(
        data=data_df,
        pm2if_specifications=pm2if_specifications,
        filename=filename,
        default_gwp=default_gwp,
        date_str=date_str,
        debug=debug,
    )

    # convert raw data to native pm2 format and save that
    data_pm2 = convert_DI_IF_data_to_pm2(
        data_di_if=data_if,
        filename=filename,
    )

    return data_pm2


def process_UNFCCC_DI_for_country(
        data_country: xr.Dataset,
        country: str,
        cat_terminology_in: str,
        entities_to_ignore: List[str],
        sectors: List[str],
        gas_baskets: Dict[str, List[str]],
        processing_info_country: Dict = None,
) -> xr.Dataset:
    """
        Process data from DI interface (where necessary).
        * Downscaling including subtraction of time series
        * country specific sector aggregation
        * Conversion to IPCC2006 categories
        * general sector and gas basket aggregation (in new categories)
    """
    #### 1: general processing
    # remove unused cats
    data_country = data_country.dropna(f'category ({cat_terminology_in})', how='all')
    # remove unused years
    data_country = data_country.dropna(f'time', how='all')
    # remove variables only containing nan
    nan_vars_country = [var for var in data_country.data_vars if
                        data_country[var].isnull().all().data == True]
    data_country = data_country.drop_vars(nan_vars_country)

    # remove unnecessary variables
    entities_ignore_present = [entity for entity in entities_to_ignore if
                               entity in data_country.data_vars]
    data_country = data_country.drop_vars(entities_ignore_present)

    #### 2: country specific processing
    if processing_info_country is not None:
        if 'tolerance' in processing_info_country:
            tolerance = processing_info_country["tolerance"]
        else:
            tolerance = 0.01

        # take only desired years
        if 'years' in processing_info_country:
            data_country = data_country.pr.loc[
                {'time': processing_info_country['years']}]

        # remove timeseries if desired
        if 'remove_ts' in processing_info_country:
            for case in processing_info_country['remove_ts']:
                remove_info = processing_info_country['remove_ts'][case]
                entities = remove_info.pop("entities")
                for entity in entities:
                    data_country[entity].pr.loc[remove_info] = \
                        data_country[entity].pr.loc[remove_info] * np.nan

        # remove all data for given years if necessary
        if 'remove_years' in processing_info_country:
            data_country.pr.loc[{'time': processing_info_country['remove_years']}] = \
                data_country.pr.loc[{'time': processing_info_country[
                    'remove_years']}] * np.nan

        # subtract categories
        if 'subtract_cats' in processing_info_country:
            subtract_cats_current = processing_info_country['subtract_cats']
            if 'entities' in subtract_cats_current.keys():
                entities_current = subtract_cats_current['entities']
            else:
                entities_current = list(data_country.data_vars)
            print(f"Subtracting categories for country {country}, entities "
                  f"{entities_current}")
            for cat_to_generate in subtract_cats_current:
                cats_to_subtract = subtract_cats_current[cat_to_generate]['subtract']
                data_sub = data_country.pr.loc[{'category': cats_to_subtract}].pr.sum(
                    dim='category', skipna=True, min_count=1)
                data_parent = data_country.pr.loc[
                    {'category': subtract_cats_current[cat_to_generate]['parent']}]
                data_agg = data_parent - data_sub
                nan_vars = [var for var in data_agg.data_vars if
                            data_agg[var].isnull().all().data == True]
                data_agg = data_agg.drop(nan_vars)
                if len(data_agg.data_vars) > 0:
                    print(f"Generating {cat_to_generate} through subtraction")
                    data_agg = data_agg.expand_dims([f'category ('
                                                     f'{cat_terminology_in})'])
                    data_agg = data_agg.assign_coords(
                        coords={f'category ({cat_terminology_in})':
                                    (f'category ({cat_terminology_in})',
                                     [cat_to_generate])})
                    data_country = data_country.pr.merge(data_agg, tolerance=tolerance)
                else:
                    print(f"no data to generate category {cat_to_generate}")

        # downscaling
        if 'downscale' in processing_info_country:
            if 'sectors' in processing_info_country['downscale']:
                sector_downscaling = processing_info_country['downscale']['sectors']
                for case in sector_downscaling.keys():
                    print(f"Downscaling for {case}.")
                    sector_downscaling_current = sector_downscaling[case]
                    entities = sector_downscaling_current.pop('entities')
                    for entity in entities:
                        data_country[entity] = data_country[
                            entity].pr.downscale_timeseries(
                            **sector_downscaling_current)  # , skipna_evaluation_dims=None)

            if 'entities' in processing_info_country['downscale']:
                entity_downscaling = processing_info_country['downscale']['entities']
                for case in entity_downscaling.keys():
                    #print(case)
                    print(data_country.coords[f'category ('
                                              f'{cat_terminology_in})'].values)
                    data_country = data_country.pr.downscale_gas_timeseries(
                        **entity_downscaling[case], skipna=True,
                        skipna_evaluation_dims=None)

        # aggregate categories
        if 'aggregate_cats' in processing_info_country:
            aggregate_cats_current = processing_info_country['aggregate_cats']
            print(
                f"Aggregating categories for country {country}")
            for cat_to_agg in aggregate_cats_current:
                print(f"Category: {cat_to_agg}")
                source_cats = aggregate_cats_current[cat_to_agg]['sources']
                data_agg = data_country.pr.loc[{'category': source_cats}].pr.sum(
                    dim='category', skipna=True, min_count=1)
                nan_vars = [var for var in data_agg.data_vars if
                            data_agg[var].isnull().all().data == True]
                data_agg = data_agg.drop(nan_vars)
                if len(data_agg.data_vars) > 0:
                    data_agg = data_agg.expand_dims([f'category ('
                                                     f'{cat_terminology_in})'])
                    data_agg = data_agg.assign_coords(
                        coords={f'category ({cat_terminology_in})':
                                    (f'category ({cat_terminology_in})', [cat_to_agg])})
                    data_country = data_country.pr.merge(data_agg, tolerance=tolerance)
                else:
                    print(f"no data to aggregate category {cat_to_agg}")

        # aggregate gases if desired
        if 'aggregate_gases' in processing_info_country:
            for case in processing_info_country['aggregate_gases'].keys():
                case_info = processing_info_country['aggregate_gases'][case]
                data_country[case_info['basket']] = \
                    data_country.pr.fill_na_gas_basket_from_contents(
                        **case_info)

    #### 3: map categories
    if country in nAI_countries:
        # conversion from BURDI to IPCC2006_PRIMAP needed
        cat_terminology_out = 'IPCC2006_PRIMAP'
        data_country = convert_categories(
            data_country,
            cat_conversion[f"{cat_terminology_in}_to_{cat_terminology_out}"],
            cat_terminology_out,
            debug=False,
            tolerance=0.01,
        )
    else:
        cat_terminology_out = cat_terminology_in

    # more general processing
    # reduce categories to output cats
    cats_to_keep = [cat for cat in
                    data_country.coords[f'category ({cat_terminology_out})'].values if
                    cat in sectors]
    data_country = data_country.pr.loc[{'category': cats_to_keep}]

    # create gas baskets
    entities_present = set(data_country.data_vars)
    for basket in gas_baskets.keys():
        basket_contents_present = [gas for gas in gas_baskets[basket] if
                                   gas in entities_present]
        if len(basket_contents_present) > 0:
            if basket in list(data_country.data_vars):
                data_country[basket] = data_country.pr.fill_na_gas_basket_from_contents(
                    basket=basket, basket_contents=basket_contents_present, min_count=1)
            else:
                try:
                    data_country[basket] = xr.full_like(data_country["CO2"],
                                                        np.nan).pr.quantify(
                        units="Gg CO2 / year")
                    data_country[basket].attrs = {"entity": basket.split(' ')[0],
                                                  "gwp_context": basket.split(' ')[1][
                                                                 1:-1]}
                    data_country[basket] = data_country.pr.gas_basket_contents_sum(
                        basket=basket, basket_contents=basket_contents_present,
                        min_count=1)
                except:
                    print(f"No gas basket created for {country}")

    # amend title and comment
    data_country.attrs["comment"] = data_country.attrs["comment"] + f" Processed on " \
                                                                    f"{date.today()}"
    data_country.attrs["title"] = data_country.attrs["title"] + f" Processed on " \
                                                                    f"{date.today()}"

    return data_country


def read_UNFCCC_DI_for_country_df(
        country_code: str,
        category_groups: Optional[Dict]=None,
        read_subsectors: bool=False,
        debug: Optional[bool]=False,
)->pd.DataFrame:
    """
    read UNFCCC DI data for a given country. All data will be read
    including all categories, gases, measures, and classifications
    Filtering is done later on conversion to PRIMAP2 format

    Parameters
    ----------
    country_code: str
        ISO3 code of the country (country names don't work, use the wrapper function)

    category_groups: dict (optional)
        define which categories to read including filters on classification, measure,
        gases

        cat_groups = {
            "4.A  Enteric Fermentation": { #4.A  Enteric Fermentation[14577]
                "measure": [
                    'Net emissions/removals',
                    'Total population',
                ],
                "gases": ["CH4"],
            },
        }

    Returns
    -------
    pd.DataFrame with read data

    """
    reader = unfccc_di_api.UNFCCCApiReader()

    # template for the query to the DI API
    query_template = {
        "party_codes": [country_code],
        "normalize_gas_names": True
    }

    # find country group
    if country_code in list(reader.non_annex_one_reader.parties["code"]):
        ai_country = False
    elif country_code in list(reader.annex_one_reader.parties["code"]):
        ai_country = True
        #di_data = reader.annex_one_reader.query(**query)
    else:
        raise ValueError(f"Country code {country_code} found neither in AnnexI nor "
                         f"non-AnnexI countrz lists.")

    if category_groups is None:
        # no category defs given, so use default which is all categories,
        # all gases, but no other data
        if debug:
            print(f"Using default config to read for country {country_code}")
        if ai_country:
            all_gases = reader.annex_one_reader.gases["name"]
            query = query_template
            query["gases"] = list(set(all_gases) - {"No gas"})
            if debug:
                print(f"Using query: {query}")
            di_data = reader.annex_one_reader.query(**query)
        else:
            all_gases = reader.non_annex_one_reader.gases["name"]
            query = query_template
            query["gases"] = list(set(all_gases) - {"No gas"})
            if debug:
                print(f"Using query: {query}")
            di_data = reader.non_annex_one_reader.query(**query)
    else:
        # detailed query per category (could also be just the top level cat)

        # read available categories and measures
        if ai_country:
            categories = reader.annex_one_reader.category_tree.all_nodes()
            measures = reader.annex_one_reader.measure_tree.all_nodes()
        else:
            categories = reader.non_annex_one_reader.category_tree.all_nodes()
            measures = reader.non_annex_one_reader.measure_tree.all_nodes()

                # set data to none so we have the variable for the first category
        di_data = None


        for category in category_groups:
            if debug:
                print(f"Working on {category}")
            this_cat_config = category_groups[category]
            # category specific query
            query = query_template.copy()
            for filter in di_query_filters:
                if filter in this_cat_config.keys():
                    query[filter] = this_cat_config[filter]

            # get the category nodes with the given tag (might be multiple)
            cat_nodes = [cat_node for cat_node in categories if cat_node.tag == category]
            if debug:
                print(f"Found fitting category nodes: {cat_nodes}")
            node_codes = []
            for node in cat_nodes:
                if "read_subsectors" in this_cat_config.keys():
                    read_subsectors_this_cat = this_cat_config["read_subsectors"]
                else:
                    read_subsectors_this_cat = read_subsectors
                if read_subsectors_this_cat:
                    # get the subcategories
                    sub_nodes = reader.non_annex_one_reader.category_tree.subtree(
                        nid=node.identifier).all_nodes()
                    node_codes = node_codes + (
                        [sub_node.identifier for sub_node in sub_nodes])
                else:
                    node_codes = node_codes + [node.identifier]
            if debug:
                print(f"Found node_codes: {node_codes}")
            # add category node_codes to query
            query["category_ids"] = node_codes

            if "measure" in this_cat_config:
                measure_nodes = [
                    measure_node for measure_node in measures if
                    measure_node.tag in this_cat_config["measure"]]
                if debug:
                    print(f"Found measure_nodes: {measure_nodes}")
                # add measure nodes to query
                query["measure_ids"] = [node.identifier for node in measure_nodes]
            if debug:
                print(query)

            # read the data. If no data is available for the query the error is caught and a message is printed
            try:
                if ai_country:
                    data_new = reader.annex_one_reader.query(**query)
                else:
                    data_new = reader.non_annex_one_reader.query(**query)

                n_points = len(data_new)
                n_countries = len(data_new["party"].unique())
                if debug:
                    print(f"Collected {n_points} data points for {n_countries} countries")
                if di_data is None:
                    di_data = data_new
                else:
                    di_data = pd.concat([di_data, data_new])
            except unfccc_di_api.NoDataError:
                print(f"No data for {category}")

    # if data has been collected print some information and save the data
    if di_data is None:
        raise ValueError(f"No data collected for country {country_code} and category "
                         f"groups "
                         f"{category_groups}")
    elif debug:
        # print some information on collected data
        print(f"Collected data for country {country_code}")
        print("### Categories ###")
        categories = di_data["category"].unique()
        categories.sort()
        print(categories)
        print("### Classifications ###")
        classifications = di_data["classification"].unique()
        classifications.sort()
        print(classifications)
        print("### Measures ###")
        measures = di_data["measure"].unique()
        measures.sort()
        print(measures)

    return di_data


def convert_DI_data_to_pm2_if(
        data: pd.DataFrame,
        pm2if_specifications: Optional[dict]=None,
        filename: Optional[Path]=None,
        default_gwp: Optional[str]=None,
        date_str: Optional[str]=None,
        debug: bool = False,
) -> pd.DataFrame:
    """
    Convert data returned from the unfccc_di_api package to primap2 interchange format

    TODO: consider moving the specification template into this function and just use the config parameter
    to overwrite certain parameters (makes sense if function is used in a broader context
    """

    print("Convert data to PRIMAP2 interchange format")

    # regular expression to match category code in category label
    cat_code_regexp = r'(?P<code>^(([0-9][A-Za-z0-9\.]{0,10}[0-9A-Za-z]))|([0-9]))[' \
                      r'\s\.].*'

    # the activity data and emissions factors have a structure that is incompatible
    # with PRIMAP2.
    # To read it into a primap2 dataframe the information in classification / measure
    # has to be put into "entity" which is currently always "No gas". I's possible,
    # but takes some time, so I have omitted it here
    filter_activity_factors = {
        "entity": {"gas": ["No gas"]},
        "unit": {"unit": [
            'no unit', 'kg/TJ', 't/TJ', '%', 'kg/t',
            'kg/kt', 't/t', 'kg/head/year', 'kg N2O/kg N handled', 'kg N2O/kg N',
            'kg N2O-N/kg N handled', 'g/m^2', 'kg N2O-N/kg N', 'kg N2O-N/ha', 'kg/t dm',
            't CO2-C/t', 't/unit', 't C/ha', 'kg CH4/ha', 'kg CO2/ha',
            'g/kg', 'kg/kg DC',
        ]
        },
    }

    # create a copy of the data to avoid data altering the original data
    # this will be done inside the *convert_to_long_dataframe* function
    # in the future. Thus it can be removed here once the category column
    # copy workaround is no longer necessary
    data_temp = data.copy(deep=True)

    # check which country group we have
    reader = unfccc_di_api.UNFCCCApiReader()
    ai_parties = list(reader.annex_one_reader.parties["code"])
    nai_parties = list(reader.non_annex_one_reader.parties["code"])
    parties_present_ai = [party for party in data_temp["party"].unique() if party
                          in ai_parties]
    parties_present_nai = [party for party in data_temp["party"].unique() if party
                          in nai_parties]
    if len(parties_present_ai) > 0:
        if len(parties_present_nai) > 0:
            raise ValueError("AnnexI and non-AnnexI parties present in one dataset. "
                             "This is not possible due to different DI category "
                             "terminologies. Convert to common categories.")
        else:
            ai_dataset = True
    else:
        ai_dataset=False

    if pm2if_specifications is None:
        if ai_dataset:
            pm2if_specifications = di_to_pm2if_template_ai.copy()
        else:
            pm2if_specifications = di_to_pm2if_template_nai.copy()

    # modify specifications
    #pm2if_specifications["filter_remove"].update(filter_activity_factors)

    # set the scenario to today's date if not given explicitly
    if date_str is None:
        date_str = str(date.today())
    pm2if_specifications["coords_defaults"]["scenario"] = f"DI{date_str}"

    # set metadata
    countries = data["party"].unique()
    if len(countries) > 1:
        pm2if_specifications["meta_data"]["title"] = "Data submitted to the UNFCCC " \
                                                     f"by countries {countries} as " \
                                                     "available in the DI interface."
    else:
        try:
            country_info = pycountry.countries.get(alpha_3=countries[0])
            country_name = country_info.name
        except:
            country_name = countries[0]
        pm2if_specifications["meta_data"]["title"] = "Data submitted to the UNFCCC " \
                                                     f"by country {country_name} as " \
                                                     "available in the DI interface " \
                                                     f"on {date_str}."
    pm2if_specifications["meta_data"]["comment"] = \
        pm2if_specifications["meta_data"]["comment"] + f" Data read on {date_str}."

    # remove baseyear
    idx_base_year = data_temp["year"] == "Base year"
    data_temp = data_temp.drop(data_temp.index[idx_base_year])

    # add GWP to entities where necessary
    data_temp["unit"] = data_temp["unit"].replace(to_replace=r"(.*) CO2 equivalent",
                                                value=r"\1CO2eq", regex=True)
    row_idx_co2eq = data_temp["unit"].str.endswith("CO2eq")
    if default_gwp is not None:
        # convert all with GWPs given in input
        data_temp.loc[row_idx_co2eq, "gas"] = data_temp.loc[row_idx_co2eq, "gas"] + \
                                              " (SARGWP100)"
    elif ai_dataset:
        # convert with AR4
        data_temp.loc[row_idx_co2eq, "gas"] = data_temp.loc[row_idx_co2eq, "gas"] + \
                                              " (AR4GWP100)"
    else:
        # convert with SAR
        data_temp.loc[row_idx_co2eq, "gas"] = data_temp.loc[row_idx_co2eq, "gas"] + \
                                              " (SARGWP100)"

    # combine numeric and string values
    nan_idx = data_temp["numberValue"].isna()
    data_temp.loc[nan_idx, "numberValue"] = data_temp.loc[nan_idx, "stringValue"]
    data_temp = data_temp.drop(columns=["stringValue"])

    # Currently in primap2 a data reading a column can only be used once.
    # We want to use the category column both for the primap2 "category"
    # column (which contains the code only) and an additional column which stores
    # the full name as available from the DI API. As a workaround we create a
    # copy of the category column
    if not ai_dataset:
        data_temp["category_copy"] = data_temp["category"]

    # replace category name and code by just the code
    repl = lambda m: m.group('code')
    data_temp["category"] = data_temp["category"].str.replace(cat_code_regexp, repl,
                                                              regex=True)

    # convert to pm2 interchange format
    data_pm2if = pm2.pm2io.convert_long_dataframe_if(
        data_temp,
        **pm2if_specifications,
    )

    if filename is not None:
        print(f"Save data to {filename.name + '.csv/.yaml'}")
        pm2.pm2io.write_interchange_format(filename, data_pm2if)

    return data_pm2if


def convert_DI_IF_data_to_pm2(
        data_di_if: pd.DataFrame,
        filename: Optional[Path]=None,
)-> xr.Dataset:
    if_index_cols = set(itertools.chain(*data_di_if.attrs["dimensions"].values()))
    time_cols = set(data_di_if.columns.values) - if_index_cols
    data_di_if.dropna(subset=time_cols, inplace=True, how="all")

    #try:
        # try to convert all in one go
        # use a copy as from_interchange_format modifies the input DF
    data_pm2 = pm2.pm2io.from_interchange_format(data_di_if.copy(deep=True),
                                                 attrs=copy.deepcopy(data_di_if.attrs))
    #except ValueError: # better more specific error in primap2
    #    print()

    if filename is not None:
        compression = dict(zlib=True, complevel=9)

        if not filename.parent.exists():
            filename.parent.mkdir()

         # write data in native PRIMAP2 format
        encoding = {var: compression for var in data_pm2.data_vars}
        data_pm2.pr.to_netcdf(filename.parent / (filename.name + ".nc"),
                            encoding=encoding)

    return data_pm2

## datalad and pydoit interface functions
def read_DI_for_country_datalad(
        country: str,
) -> None:
    """
    Wrapper around read_DI_for_country which takes care of selecting input
    and output files and using datalad run to trigger the data reading

    Parameters
    __________

    country_codes: str
        ISO 3-letter country code

    """

    # get all the info for the country
    country_info = get_input_and_output_files_for_country(
        country, submission_year=submission_year, verbose=True)

    print(f"Attempting to read DI data for {country}.")
    print("#"*80)
    print("")
    print(f"Using the UNFCCC_DI_reader")
    print("")
    print(f"Run the script using datalad run via the python api")
    script = code_path / "UNFCCC_DI_reader" / "read_UNFCCC_DI_country.py"

    cmd = f"./venv/bin/python3 {script.as_posix()} --country={country} ""
    datalad.api.run(
        cmd=cmd,
        dataset=root_path,
        message=f"Read DI data for {country}.",
        inputs=country_info["input"],
        outputs=country_info["output"],
        dry_run=None,
        explicit=True,
    )

## helper functions

def determine_filename(
        country_code: str,
        date_str: str,
        raw: bool=False,
)->Path:
    """
    Determine the filename for a dataset from given country code and date string.


    Parameters
    ----------
    country_code: str
        ISO 3 letter code of the country
    date_str:
        formatted date string
    raw:
        bool specifying if filename fow raw or processed data should be returned

    Returns
    _______
        pathlib Path object for the file name (without suffix)

    """

    # get the country folder
    with open(extracted_data_path / "folder_mapping.json", "r") as mapping_file:
        folder_mapping = json.load(mapping_file)

    if country_code in folder_mapping:
        file_filter = {}
        file_filter["party"] = country_code
        country_folders = folder_mapping[country_code]
        if isinstance(country_folders, str):
            # only one folder
            filename = Path(country_folders) / f"{country_code}_DI_{date_str}"

        else:
            raise ValueError("More than one output folder for country "
                             f"{country_code}. This should not happen.")
    else:
        # folder not in mapping. It will be created if not present yet
        country_name = get_country_name(country_code)
        country_folder = extracted_data_path / country_name.replace(" ", "_")
        if country_folder.exists():
           print(f"Output folder {country_name.replace(' ', '_')} for country "
                 f"{country_code} exists but is not in folder mapping. Update "
                 "folder mapping")
        else:
            country_folder.mkdir()

        if raw:
            filename = Path(country_folder) / f"{country_code}_DI_{date_str}_raw"
        else:
            filename = Path(country_folder) / f"{country_code}_DI_{date_str}"

    return filename


def convert_categories(
        ds_input: xr.Dataset,
        conversion: Dict[str, Dict[str, str]],
        #terminology_from: str,
        terminology_to: str,
        debug: bool=False,
        tolerance: float=0.01,
)->xr.Dataset:
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

def get_input_and_output_files_for_country(
        country: str,
        submission_year: int,
        submission_date: Optional[str]=None,
        verbose: Optional[bool]=True,
) -> Dict[str, Union[List, str]]:
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

    # determine latest data
    print(f"Determining input and output files for {country}")
    if submission_date is None:
        if verbose:
            print(f"No submission date given, find latest date.")
        submission_date = get_latest_date_for_country(country_code, submission_year)
    else:
        if verbose:
            print(f"Using given submissions date {submission_date}")

    if submission_date is None:
        # there is no data. Raise an exception
        raise NoCRFFilesError(f"No submissions found for {country_code}, "
                              f"submission_year={submission_year}, "
                              f"date={date}")
    else:
        if verbose:
            print(f"Latest submission date for CRF{submission_year} is {submission_date}")
    country_info["date"] = submission_date

    # get possible input files
    input_files = get_crf_files(country_codes=country_code,
                                submission_year=submission_year,
                                date=submission_date)
    if not input_files:
        raise NoCRFFilesError(f"No possible input files found for {country}, CRF{submission_year}, "
                              f"v{submission_date}. Are they already submitted and included in the "
                              f"repository?")
    elif verbose:
        print(f"Found the following input_files:")
        for file in input_files:
            print(file.name)
        print("")


    # convert file's path to str
    input_files = [file.as_posix() for file in input_files]
    country_info["input"] = input_files

    # get output file
    output_folder = extracted_data_path / country_name.replace(" ", "_")
    output_files = [output_folder / f"{country_code}_CRF{submission_year}"
                                    f"_{submission_date}.{suffix}" for suffix
                    in ['yaml', 'csv', 'nc']]
    if verbose:
        print(f"The following files are considered as output_files:")
        for file in output_files:
            print(file)
        print("")

    # check if output data present

    # convert file paths to str
    output_files = [file.as_posix() for file in output_files]
    country_info["output"] = output_files

    return country_info

# TODO

# functions

# def compare_with_existing
# def