import primap2 as pm2
import unfccc_di_api
import numpy as np
import xarray as xr
import re
from datetime import date
from typing import Optional, Dict, List, Union

from .UNFCCC_DI_reader_config import di_processing_info
from .UNFCCC_DI_reader_config import cat_conversion
from .UNFCCC_DI_reader_config import gas_baskets
from .util import NoDIDataError, nAI_countries
from .util import DI_date_format

from UNFCCC_GHG_data.helper import process_data_for_country
from .UNFCCC_DI_reader_helper import find_latest_DI_data
from .UNFCCC_DI_reader_helper import determine_filename

from .UNFCCC_DI_reader_io import save_DI_dataset, save_DI_country_data


def process_and_save_UNFCCC_DI_for_country(
        country_code: str,
        date_str: Union[str, None] = None,
) -> xr.Dataset:
    """
    process data and save them to disk using default parameters
    """

    # get latest dataset if no date given
    if date_str is None:
        # get the latest date
        raw_data_file = find_latest_DI_data(country_code, raw=True)
        if raw_data_file is None:
            raise ValueError(f"No raw data available for {country_code}.")
    else:
        raw_data_file = determine_filename(country_code, date_str, raw=True,
                                           hash=False)

        raw_data_file = raw_data_file.parent / (raw_data_file.name + '.nc')

        if not raw_data_file.exists():
            raise ValueError(f"File {raw_data_file.name} does not exist. Check if it "
                             "has been read.")

    print(f"process {raw_data_file.name}")

    # load the data
    data_to_process = pm2.open_dataset(raw_data_file)

    # get parameters
    countries = list(data_to_process.coords[data_to_process.attrs['area']].values)
    if len(countries) > 1:
        raise ValueError(
            f"Found {len(countries)} countries. Only single country data "
            f"can be processed by this function. countries: {countries}")
    else:
        country_code = countries[0]
    if country_code in di_processing_info.keys():
        processing_info_country = di_processing_info[country_code]
    else:
        processing_info_country = None
    entities_to_ignore = []  # TODO: check and make default list

    # process
    data_processed = process_UNFCCC_DI_for_country(
        data_country=data_to_process,
        entities_to_ignore=entities_to_ignore,
        gas_baskets=gas_baskets,
        #category_conversion=cat_conversion,
        sectors_out=None,
        processing_info_country=processing_info_country,
    )

    # save
    save_DI_country_data(data_processed, raw=False)

    return data_processed


def process_UNFCCC_DI_for_country(
        data_country: xr.Dataset,
        entities_to_ignore: List[str],
        gas_baskets: Dict[str, List[str]],
        filter_dims: Optional[Dict[str, List[str]]] = None,
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
    # get country
    countries = list(data_country.coords[data_country.attrs['area']].values)
    if len(countries) > 1:
        raise ValueError(
            f"Found {len(countries)} countries. Only single country data "
            f"can be processed by this function. countries: {countries}")
    else:
        country_code = countries[0]

    # get scenario
    scenarios = list(data_country.coords[data_country.attrs['scen']].values)
    if len(scenarios) > 1:
        raise ValueError(
            f"Found {len(scenarios)} scenarios. Only single scenario data "
            f"can be processed by this function. Scenarios: {scenarios}")
    scenario = scenarios[0]

    # get category terminology
    cat_col = data_country.attrs['cat']
    temp = re.findall(r'\((.*)\)', cat_col)
    cat_terminology_in = temp[0]

    # get processing specification
    if processing_info_country is not None:
        if scenario in processing_info_country.keys():
            processing_info_country_scen = processing_info_country[scenario]
        else:
            processing_info_country_scen = processing_info_country['default']
    else:
        processing_info_country_scen = None

    # 3: map categories
    if country_code in nAI_countries:
        # conversion from BURDI to IPCC2006_PRIMAP needed
        cat_terminology_out = 'IPCC2006_PRIMAP'
        if category_conversion is None:
            category_conversion = cat_conversion[f"{cat_terminology_in}_to_{cat_terminology_out}"]

    else:
        cat_terminology_out = cat_terminology_in

    data_country = process_data_for_country(
        data_country,
        entities_to_ignore=entities_to_ignore,
        gas_baskets=gas_baskets,
        filter_dims=filter_dims,
        cat_terminology_out=cat_terminology_out,
        category_conversion=category_conversion,
        sectors_out=sectors_out,
        processing_info_country=processing_info_country_scen,
    )

    return data_country


def process_UNFCCC_DI_for_country_group(
        annexI: bool = False,
        date_str: Optional[str] = None,
) -> xr.Dataset:
    """
    This function processes DI data for all countries in a group (annexI or non-AnnexI)

    Parameters
    __________

    annexI: bool (default False)
        If True process all annexI countries (not implemented yet), else all non-AnnexI
        countries.
    date_str: str (default None)
        Date of the data to be processed in the format %Y-%m-%d (e.g. 2023-01-30). If
        no date is given the last data read will be processed.

    """
    today = date.today()
    date_str_today = today.strftime(DI_date_format)

    if annexI:
        raise ValueError("Bulk processing for AnnexI countries not implemented yet")
        countries = AI_countries
        #data_all_if = None
        country_group = "AnnexI"
    else:
        countries = nAI_countries
        data_all = None
        country_group = "non-AnnexI"

    # read the data
    exception_countries = []
    for country in countries:
        print(f"processing DI data for country {country}")

        try:
            data_country = process_and_save_UNFCCC_DI_for_country(
                country_code=country,
                date_str=date_str,
            )

            # change the scenario to today's date
            data_country = data_country.assign_coords({"scenario (Access_Date)": [
                f"DI{date_str_today}"]})
            scen_dim = data_country.attrs["scen"]
            data_country.attrs["scen"] = f"scenario (Process_Date)"
            data_country = data_country.rename({scen_dim: data_country.attrs["scen"]})

            if data_all is None:
                data_all = data_country
            else:
                data_all = data_all.pr.merge(data_country)
        except Exception as err:
            exception_countries.append(country)
            print(f"Error occurred when processing data for {country}.")
            print(err)

    # update metadata
    countries_present = list(data_all.coords[data_all.attrs['area']].values)
    data_all.attrs["title"] = f"Data submitted by the following {country_group} " \
                              f"countries and available in the DI interface, " \
                              f"converted to IPCC2006 categories and downscaled " \
                              f"where applicable. For download date see scenario. " \
                              f"Countries: {', '.join(countries_present)}"


    # save the data
    save_DI_dataset(data_all, raw=False, annexI=annexI)
    print(data_all.coords["scenario (Process_Date)"].values)
    print(f"Errors occured for countries: {exception_countries}")
    return data_all

