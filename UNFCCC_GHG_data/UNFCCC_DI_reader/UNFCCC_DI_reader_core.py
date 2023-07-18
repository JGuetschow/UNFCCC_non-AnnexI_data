import primap2 as pm2
import unfccc_di_api
import pandas as pd
import pycountry
import itertools
import copy
import xarray as xr

from datetime import date
from typing import Optional, Dict
from copy import deepcopy

from .UNFCCC_DI_reader_config import di_to_pm2if_template_nai
from .UNFCCC_DI_reader_config import di_to_pm2if_template_ai
from .UNFCCC_DI_reader_config import di_query_filters

from .UNFCCC_DI_reader_config import cat_code_regexp
from .util import NoDIDataError, nAI_countries, AI_countries
from .util import DI_date_format

from .UNFCCC_DI_reader_io import save_DI_dataset, save_DI_country_data


def read_UNFCCC_DI_for_country(
        country_code: str,
        category_groups: Optional[Dict]=None,
        read_subsectors: bool=False,
        save_data: Optional[bool]=True,
        date_str: Optional[str]=None,
        pm2if_specifications: Optional[dict]=None,
        default_gwp: Optional[str]=None,
        debug: Optional[bool]=False,
        use_zenodo: Optional[bool]=True,
):
    """
    reads data for a country from the UNFCCC DI interface and saves to native and
    interchange format
    """

    # read the data
    if use_zenodo:
        data_df = read_UNFCCC_DI_for_country_df_zenodo(
            country_code=country_code,
            category_groups=category_groups,
            read_subsectors=read_subsectors,
            debug=debug,
        )
    else:
        data_df = read_UNFCCC_DI_for_country_df(
            country_code=country_code,
            category_groups=category_groups,
            read_subsectors=read_subsectors,
            debug=debug,
        )

    # set date_str if not given
    if date_str is None:
        today = date.today()
        date_str = today.strftime(DI_date_format)

    # convert raw data to pm2 interchange format and save
    data_if = convert_DI_data_to_pm2_if(
        data=data_df,
        pm2if_specifications=deepcopy(pm2if_specifications),
        default_gwp=default_gwp,
        date_str=date_str,
        debug=debug,
    )

    # convert raw data to native pm2 format and save that
    data_pm2 = convert_DI_IF_data_to_pm2(
        data_di_if=data_if,
    )

    # save
    if save_data:
        save_DI_country_data(data_pm2, raw=True)

    return data_pm2


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
    if country_code in nAI_countries:
        ai_country = False
    elif country_code in AI_countries:
        ai_country = True
        #di_data = reader.annex_one_reader.query(**query)
    else:
        raise ValueError(f"Country code {country_code} found neither in AnnexI nor "
                         f"non-AnnexI country lists.")

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


def read_UNFCCC_DI_for_country_df_zenodo(
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
    if read_subsectors:
        raise ValueError("Subsector reading is not possible with the Zenodo reader "
                         "yet")

    reader = unfccc_di_api.ZenodoReader()

    di_data = reader.query(party_code=country_code)

    # remove the "no_gas" data
    di_data = di_data[di_data["gas"] != "No gas"]

    if category_groups is not None:
        di_data = di_data[di_data["category"].isin(category_groups)]

    # if data has been collected print some information and save the data
    if di_data is None or len(di_data) == 0:
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

    # create a copy of the data to avoid data altering the original data
    # this will be done inside the *convert_to_long_dataframe* function
    # in the future. Thus it can be removed here once the category column
    # copy workaround is no longer necessary
    data_temp = data.copy(deep=True)

    # check which country group we have
    parties_present_ai = [party for party in data_temp["party"].unique() if party
                          in AI_countries]
    parties_present_nai = [party for party in data_temp["party"].unique() if party
                          in nAI_countries]
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
            pm2if_specifications = deepcopy(di_to_pm2if_template_ai)
        else:
            pm2if_specifications = deepcopy(di_to_pm2if_template_nai)

    # modify specifications
    #pm2if_specifications["filter_remove"].update(filter_activity_factors)

    # set the scenario to today's date if not given explicitly
    if date_str == "country":
        pm2if_specifications["coords_defaults"]["scenario"] = f"DIrolling"
    elif date_str is None:
        today = date.today()
        date_str = today.strftime(DI_date_format)
    pm2if_specifications["coords_defaults"]["scenario"] = f"DI{date_str}"

    # set metadata
    countries = data["party"].unique()
    if len(countries) > 1:
        pm2if_specifications["meta_data"]["title"] = \
            f"Data submitted to the UNFCCC by countries {countries} as " \
            f"available in the DI interface on {date_str}."
    else:
        try:
            country_info = pycountry.countries.get(alpha_3=countries[0])
            country_name = country_info.name
        except:
            country_name = countries[0]

        pm2if_specifications["meta_data"]["title"] = \
            f"Data submitted to the UNFCCC by country {country_name} as " \
            f"available in the DI interface on {date_str}."

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

    return data_pm2if


def convert_DI_IF_data_to_pm2(
        data_di_if: pd.DataFrame,
)-> xr.Dataset:
    if_index_cols = set(itertools.chain(*data_di_if.attrs["dimensions"].values()))
    time_cols = set(data_di_if.columns.values) - if_index_cols
    data_di_if.dropna(subset=time_cols, inplace=True, how="all")

    try:
        # use a copy as from_interchange_format modifies the input DF
        data_pm2 = pm2.pm2io.from_interchange_format(
            data_di_if.copy(deep=True), attrs=copy.deepcopy(data_di_if.attrs))
    except Exception as ex: # better more specific error in primap2
        print(f'Error on conversion to PRIMAP2 native format: {ex}')

    return data_pm2


## functions for multiple country reading
def read_UNFCCC_DI_for_country_group(
        annexI: bool=False,
) -> xr.Dataset:
    '''
    This function reads DI data for all countries in a group (annexI or non-AnnexI)
    The function reads all data in one go using datalad run. as the output data file
    names are unknown beforehand datalad run uses explicit=false
    '''

    today = date.today()
    date_str = today.strftime(DI_date_format)

    if annexI:
        countries = AI_countries
        data_all_if = None
        country_group = "AnnexI"
    else:
        countries = nAI_countries
        data_all = None
        country_group = "non-AnnexI"

    # read the data
    for country in countries:
        print(f"reading DI data for country {country}")

        try:
            data_country = read_UNFCCC_DI_for_country(
                country_code=country,
                category_groups=None,  # read all categories
                read_subsectors=False,  # not applicable as we read all categories
                date_str=date_str,
                pm2if_specifications=None,
                # automatically use the right specs for AI and NAI
                default_gwp=None,  # automatically uses right default GWP for AI and NAI
                debug=False)

            if annexI:
            # annexI data has additional dimensions and unfortunately the xarray
            # merge function needs some extra memory which is not needed when
            # converting from IF to pm2
                if data_all_if is None:
                    data_all_if = data_country.pr.to_interchange_format()
                    attrs = data_all_if.attrs
                else:
                    data_all_if = pd.concat([data_all_if,
                                          data_country.pr.to_interchange_format()])
            else:
                if data_all is None:
                    data_all = data_country
                else:
                    data_all = data_all.pr.merge(data_country)

        except unfccc_di_api.NoDataError as err:
            print(f"No data for {country}.")
            print(err)
        except ValueError as err:
            print(f"ValueError for {country}.")
            print(err)

    if annexI:
        data_all = pm2.pm2io.from_interchange_format(data_all_if, attrs=attrs,
                                                     max_array_size=500000000000)

    countries_present = list(data_all.coords[data_all.attrs['area']].values)
    data_all.attrs["title"] = f"Data submitted by the following {country_group} " \
                              f"countries and available in the DI interface on " \
                              f"{date_str}: {', '.join(countries_present)}"

    # save the data
    save_DI_dataset(data_all, raw=True, annexI=annexI)

    return data_all


