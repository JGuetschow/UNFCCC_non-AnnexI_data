#import re
#
#from treelib import Tree


#import pandas as pd
import xarray as xr
import primap2 as pm2
import numpy as np
import pycountry
import datalad.api
from datetime import date
from pathlib import Path
from typing import Optional

from . import crf_specifications as crf

from .UNFCCC_CRF_reader_core import read_crf_table
from .UNFCCC_CRF_reader_core import convert_crf_table_to_pm2if
from .UNFCCC_CRF_reader_core import get_latest_date_for_country
from .UNFCCC_CRF_reader_core import get_crf_files
from .UNFCCC_CRF_reader_devel import save_unknown_categories_info
from .UNFCCC_CRF_reader_devel import save_last_row_info

from .utils import code_path, log_path, \
    custom_country_mapping, extracted_data_path, root_path

import sys
sys.path.append('../UNFCCC_reader')
from UNFCCC_reader.get_submissions_info import get_country_code


# functions:
# * testing fucntions
# ** read one or more table(s) for all countries
#    (and a if desired only a single year) and write
#    output files with missing sectors etc
# **

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
        submission_date: Optional[str]=None,
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

    submission_data: Optional(str)
        Read for a specific submission date (given as string as in the file names)
        If not specified latest data will be read

    Returns
    _______
        return value is a Pandas DataFrame with the read data in PRIMAP2 format
    """

    # get country name
    country_name = get_country_name(country_code)

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

    if submission_date is None:
        submission_date = get_latest_date_for_country(country_code, submission_year)

    ds_all = None
    unknown_categories = []
    last_row_info = []
    for table in tables:
        # read table for all years
        ds_table, new_unknown_categories, new_last_row_info = read_crf_table(
            country_code, table, submission_year, date=submission_date)#, data_year=[1990])

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
            meta_data_input={"title": f"Data submitted in {submission_year} to the UNFCCC "
                                      f"in the common reporting format (CRF) by {country_name}. "
                                      f"Submission date: {submission_date}"},
            entity_mapping=entity_mapping,
        )

        # now convert to native PRIMAP2 format
        ds_table_pm2 = pm2.pm2io.from_interchange_format(ds_table_if)

        # combine per table DS
        if ds_all is None:
            ds_all = ds_table_pm2
        else:
            ds_all = ds_all.combine_first(ds_table_pm2)

    # check if there were log messages.
    save_data = True
    if len(unknown_categories) > 0:
        save_data = False
        today = date.today()
        log_location = log_path / f"CRF{submission_year}" \
                       / f"{country_code}_unknown_categories_{today.strftime('%Y-%m-%d')}.csv"
        print(f"Unknown rows found for {country_code}. Not saving data. Savin log to "
              f"{log_location}" )
        save_unknown_categories_info(unknown_categories, log_location)

    if len(last_row_info) > 0:
        save_data = False
        today = date.today()
        log_location = log_path / f"CRF{submission_year}" \
                       / f"{country_code}_last_row_info_{today.strftime('%Y-%m-%d')}.csv"
        print(f"Data found in the last row found for {country_code}. Not saving data. Savin log to "
              f"{log_location}")
        save_last_row_info(last_row_info, log_location)

    if save_data:
        compression = dict(zlib=True, complevel=9)
        output_folder = extracted_data_path / country_name.replace(" ", "_")
        output_filename = f"{country_code}_CRF{submission_year}_{submission_date}"

        if not output_folder.exists():
            output_folder.mkdir()
            # folder mapping has to be updated !!!
            # if we do it here we will do it a lot of times when reading several countries at once

        # write data in interchange format
        pm2.pm2io.write_interchange_format(output_folder / output_filename,
                                           ds_all.pr.to_interchange_format())

        # write data in native PRIAMP2 formart
        encoding = {var: compression for var in ds_all.data_vars}
        ds_all.pr.to_netcdf(output_folder / (output_filename + ".nc"),
                              encoding=encoding)

    return ds_all


def read_crf_for_country_datalad(
        country: str,
        submission_year: int,
        submission_date: Optional[str]=None,
) -> None:
    """
    Wrapper around read_crf_for_country which takes care of selecting input
    and output files and using datalad run to trigger the data reading

    Parameters
    __________

    country_codes: str
        ISO 3-letter country code

    submission_year: int
        Year of the submission of the data

    submission_date: Optional(str)
        Read for a specific submission date (given as string as in the file names)
        If not specified latest data will be read

    """

    # get the country code and name
    # both could be given as input, so we need this two step process
    if country in custom_country_mapping:
        country_code = country
    else:
        country_code = get_country_code(country)
    # now get the country name
    country_name = get_country_name(country_code)

    print(f"Attempting to read data for CRF{submission_year} from {country}.")
    print("#"*80)
    print("")

    print(f"Using the UNFCCC_CRF_reader")
    print("")

    # get possible input files
    input_files = get_crf_files(country_codes=country_code,
                                submission_year=submission_year,
                                date=submission_date)
    if not input_files:
        if submission_date is not None:
            print(f"No possible input files found for {country}, CRF{submission_year}, "
                  f"v{submission_date}. Are they already submitted and included in the "
                  f"repository?")
        else:
            print(f"No possible input files found for {country}, CRF{submission_year}. "
                  f"Are they already submitted and included in the repository?")
    else:
        print(f"Found the following input_files:")
        for file in input_files:
            print(file.name)
        print("")

    # convert file's path to str
    input_files = [file.as_posix() for file in input_files]

    # get output file
    if submission_date is None:
        submission_date = get_latest_date_for_country(country_code, submission_year)

    output_folder = extracted_data_path / country_name.replace(" ", "_")
    output_files = [output_folder / f"{country_code}_CRF{submission_year}"
                    f"_{submission_date}.{suffix}" for suffix
                    in ['yaml', 'csv', 'nc']]
    print(f"The following files are considered as output_files:")
    for file in output_files:
        print(file)
    print("")

    # convert file paths to str
    output_files = [file.as_posix() for file in output_files]

    print(f"Run the script using datalad run via the python api")
    script = code_path / "UNFCCC_CRF_reader" / "read_UNFCCC_CRF_submission.py"
    datalad.api.run(
        cmd=f"./venv/bin/python3 {script.name} --country={country} "
            f"--submission_year={submission_year} --submission_date=={submission_date}",
        dataset=root_path,
        message=f"Read data for {country}, CRF{submission_year}, {submission_date}.",
        inputs=input_files,
        outputs=output_files,
        dry_run=None,
        explicit=True,
    )



def get_country_name(
        country_code: str,
) -> str:
    """get country name from code """
    if country_code in custom_country_mapping:
        country_name = custom_country_mapping(country_code)
    else:
        try:
            country = pycountry.countries.get(alpha_3=country_code)
            country_name = country.name
        except:
            raise ValueError(f"Country code {country_code} can not be mapped to "
                             f"any country")

    return country_name