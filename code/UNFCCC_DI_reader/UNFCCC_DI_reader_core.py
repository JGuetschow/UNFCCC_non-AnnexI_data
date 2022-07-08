import primap2 as pm2
import unfccc_di_api
import pandas as pd
import pycountry
import itertools
import json
import copy
from datetime import date
from typing import Optional, Dict
from pathlib import Path

from .UNFCCC_DI_reader_config import di_to_pm2if_template_nai
from .UNFCCC_DI_reader_config import di_to_pm2if_template_ai
from .UNFCCC_DI_reader_config import di_query_filters
from util import NoDIDataError, extracted_data_path



def read_UNFCCC_DI_for_party_df(
        party: str,
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
    party: str
        ISO3 code of the party (country names don't work, use the wrapper function)

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
        "party_codes": [party],
        "normalize_gas_names": True
    }


    # find country group
    if party in list(reader.non_annex_one_reader.parties["code"]):
        ai_country = False
    elif party in list(reader.annex_one_reader.parties["code"]):
        ai_country = True
        #di_data = reader.annex_one_reader.query(**query)
    else:
        raise ValueError(f"Party code {party} found neither in AnnexI nor non-AnnexI "
                         f"party lists.")

    if category_groups is None:
        # no category defs given, so use default which is all categories,
        # all gases, but no other data
        if debug:
            print(f"Using default config to read for party {party}")
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
        raise ValueError(f"No data collected for party {party} and category groups "
                         f"{category_groups}")
    elif debug:
        # print some information on collected data
        print(f"Collected data for party {party}")
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
        filename: str = "",
        default_gwp: Optional[str]=None,
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

    # set the scenario to today's date
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

    # Currently in primap2 data reading a column can only be used once.
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

    if filename != "":
        print(f"Save data to {filename + '.csv/.yaml'}")
        pm2.pm2io.write_interchange_format(filename, data_pm2if)

    return data_pm2if


def convert_DI_IF_data_to_pm2(data_di_if: pd.DataFrame)-> xr.Dataset:
    if_index_cols = set(itertools.chain(*data_di_if.attrs["dimensions"].values()))
    time_cols = set(data_di_if.columns.values) - if_index_cols
    data_di_if.dropna(subset=time_cols, inplace=True)

    #try:
        # try to convert all in one go
        # use a copy as from_interchange_format modifies the input DF
    data_pm2 = pm2.pm2io.from_interchange_format(data_di_if.copy(deep=True),
                                                 attrs=copy.deepcopy(data_di_if.attrs))
    #except ValueError: # better more specific error in primap2
    #    print()

    return data_pm2


def determine_filename(country_code, date_str)->Path:
    """
    Determine the filename for a dataset from given country code and data string.


    Parameters
    ----------
    country_code: str
        ISO 3 letter code of the country
    date_str:
        formatted date string

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
        raise ValueError(f"No output data folder found for country {country_code}. "
                         f"Check if folder mapping is up to date.")

    return filename

# TODO

# functions

# def compare_with_existing
# def