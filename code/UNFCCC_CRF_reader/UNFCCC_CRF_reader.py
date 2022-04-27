import re
from pathlib import Path
from treelib import Tree

import pandas as pd
import xarray as xr
import primap2 as pm2
import pycountry
import crf_specifications as crf
from typing import Dict, List, Optional, Tuple, Union
from datetime import date

from .UNFCCC_CRF_reader_core import read_crf_table
from .UNFCCC_CRF_reader_core import convert_crf_table_to_pm2if
from .UNFCCC_CRF_reader_devel import save_unknown_categories_info
from .UNFCCC_CRF_reader_devel import save_last_row_info

from . import log_path, custom_country_mapping, extracted_data_path

# functions:
# * production functions
# ** read one table for a country
# ** read alist of tables for one country
# ** convert to IF and NC and save
# * testing fucntions
# ** read one or more table(s) for all countries
#    (and a if desired only a single year) and write
#    output files with missing sectors etc
# **

# TODO: add saving to read_crf_for_country
# TODO: add function to read several / all countries



# general approach:
# main code in a function that reads on table from one file.
# return raw pandas DF for use in different functions
# wrappers around this function to read for a whole country or for test reading where we also
# write files with missing sectors etc.
# merging functions use native pm2 format


def read_crf_for_country(
        country_code: str,
        submission_year: int,
) -> xr.Dataset:
    """
    Read CRF data for given submission year and country. All tables
    available in the specification will be read for all years. Result
    will be written to appropriate country folder.

    If you want to read data for more countries of from a different folder
    use the test_read_crf_data function.

    IMPORTANT NOTE:
    Currently there is no consistency check between data for the same category
    read from different tables

    The folder can either be given explicitly or if not given folders are determined
    from the submission_year and country_code variables.
    The output is a primap2 dataset (xarray based).

    We only save the data in the country folder if there were no messages like
    unknown rows to make sure that data that goes into the repository is complete.
    The result dataframe is returned in any case. In case log messages appeared
    they are saved in the folder 'log' under the file name
    'country_reading_<country_code>_<date>_X.csv'.


    Parameters
    __________

    country_codes: str
        ISO 3-letter country code

    submission_year: int
        Year of the submission of the data

    Returns
    _______
        first return value is a Pandas DataFrame with the read data in long format
        second return value
        third return value TODO

    """
    # get country name
    if country_code in custom_country_mapping:
        country_name = custom_country_mapping(country_code)
    else:
        try:
            country = pycountry.countries.get(alpha_3=country_code)
            country_name = country.name
        except:
            raise ValueError(f"Country code {country_code} can not be mapped to "
                             f"any country")

    # get specification and available tables
    try:
        crf_spec = getattr(crf, f"CRF{submission_year}")
        #print(table_spec)
    except:
        raise ValueError(f"No terminology exists for submission year {submission_year}")

    tables = [table for table in crf_spec.keys()
              if crf_spec[table]["status"] == "tested"]
    print(f"The following tables are available in the " \
          f"CRF{submission_year} specification: {tables}")

    # TODO: get available dates (first get folders for country, then dates, select latest date and passt on)
    # dates need to be determined here.

    ds_all = None
    unknown_categories = []
    last_row_info = []
    for table in tables:
        # read table for all years
        ds_table, new_unknown_categories, new_last_row_info = read_crf_table(
            country_code, table, submission_year, folder="CRF2021")#, data_year=[1990])

        # collect messages on unknown rows etc
        unknown_categories = unknown_categories + new_unknown_categories
        last_row_info = last_row_info + new_last_row_info

        # convert to PRIMAP2 IF
        # first drop the orig_cat_name col as it can have multiple values for
        # one category
        ds_table = ds_table.drop(columns=["orig_cat_name"])

        # if we need to map entities pass this info to the conversion function
        if "entity_mapping" in crf_spec[table]:
            entity_mapping = crf_spec[table]["entity_mapping"]
        else:
            entity_mapping = None
        ds_table_if = convert_crf_table_to_pm2if(
            ds_table,
            2021,
            meta_data_input={"title": "DEU"},
            entity_mapping=entity_mapping,
        )

        # now convert to native PRIMAP2 format
        ds_table_pm2 = pm2.pm2io.from_interchange_format(ds_table_if)

        # combine per table DS
        if ds_all is None:
            ds_all = ds_table_pm2
        else:
            ds_all = xr.combine_by_coords(data_objects=[ds_all, ds_table_pm2],
                                          compat='override',
                                          data_vars='all',
                                          coords='all',
                                          fill_value=np.nan,
                                          #join='outer',
                                          combine_attrs='drop_conflicts'
                                          )

    # check if there were log messages.
    save_data = True
    if len(unknown_categories) > 0:
        save_data = False
        today = date.today()
        log_location = log_path / f"CRF{submission_year}" \
                       / f"{country_code}_unknown_categories_{today.strftime('%d/%m/%Y')}.csv"
        print(f"Unknown rows found for {country_code}. Not saving data. Savin log to "
              f"{log_location}" )
        save_unknown_categories_info(unknown_categories, log_location)

    if len(last_row_info) > 0:
        save_data = False
        today = date.today()
        log_location = log_path / f"CRF{submission_year}" \
                       / f"{country_code}_last_row_info_{today.strftime('%d/%m/%Y')}.csv"
        print(f"Data found in the last row found for {country_code}. Not saving data. Savin log to "
              f"{log_location}")
        save_last_row_info(last_row_info, log_location)

    if save_data:
        output_folder = extracted_data_path / country_name.replace(" ", "_")
        output_filename = f"{country_code}_CRF{submission_year}_

# TODO: need to consider the date when reading, there might be multiple submissions...

        if not output_folder.exists():
            output_folder.mkdir()

        # write data in interchnange formart
        pm2.pm2io.write_interchange_format(output_folder / (output_filename + coords_terminologies["category"]), data_if)

        # write data in native PRIAMP2 formart
        data_pm2 = pm2.pm2io.from_interchange_format(data_if)
        encoding = {var: compression for var in data_pm2.data_vars}
        data_pm2.pr.to_netcdf(output_folder / (output_filename + coords_terminologies["category"] + ".nc"),
                              encoding=encoding)

    return ds_all


