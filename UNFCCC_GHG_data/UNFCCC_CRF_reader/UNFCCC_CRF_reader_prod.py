import xarray as xr
import primap2 as pm2
import datalad.api
from datetime import date
from typing import Optional, List, Dict, Union

from . import crf_specifications as crf

from .UNFCCC_CRF_reader_core import read_crf_table
from .UNFCCC_CRF_reader_core import convert_crf_table_to_pm2if
from .UNFCCC_CRF_reader_core import get_latest_date_for_country
from .UNFCCC_CRF_reader_core import get_crf_files
from .UNFCCC_CRF_reader_devel import save_unknown_categories_info
from .UNFCCC_CRF_reader_devel import save_last_row_info

from UNFCCC_GHG_data.helper import code_path, log_path, root_path
from UNFCCC_GHG_data.helper import custom_country_mapping, extracted_data_path_UNFCCC
from UNFCCC_GHG_data.helper import get_country_code, get_country_name
from .util import all_crf_countries, NoCRFFilesError

#import sys
#sys.path.append(code_path.name)

# functions:
# * testing fucntions
# ** read one or more table(s) for all countries
#    (and a if desired only a single year) and write
#    output files with missing sectors etc
# **

# TODO: add function to read several / all countries

# general approach:
# main UNFCCC_GHG_data in a function that reads on table from one file.
# return raw pandas DF for use in different functions
# wrappers around this function to read for a whole country or for test reading where we also
# write files with missing sectors etc.
# merging functions use native pm2 format


def read_crf_for_country(
        country_code: str,
        submission_year: int,
        submission_date: Optional[str]=None,
        re_read: Optional[bool]=True,
) -> xr.Dataset:
    """
    Read CRF data for given submission year and country. All tables
    available in the specification will be read for all years. Result
    will be written to appropriate country folder.

    Folders are determined from the submission_year and country_code variables.
    The output is a primap2 dataset (xarray based).

    If you want to read data for more countries or from a different folder
    use the read_latest_crf_submissions_for_year or test_read_crf_data function.

    IMPORTANT NOTE:
    Currently there is no consistency check between data for the same category
    read from different tables

    We only save the data in the country folder if there were no messages like
    unknown rows to make sure that data that goes into the repository is complete.
    The result dataframe is returned in any case. In case log messages appeared
    they are saved in the folder 'log' under the file name
    'country_reading_<country_code>_<date>_X.csv'.


    Parameters
    __________

    country_codes: str
        ISO 3-letter country UNFCCC_GHG_data

    submission_year: int
        Year of the submission of the data

    submission_data: Optional(str)
        Read for a specific submission date (given as string as in the file names)
        If not specified latest data will be read

    re_read: Optional(bool) default: True
        Read the data also if it's already present

    Returns
    _______
        return value is a Pandas DataFrame with the read data in PRIMAP2 format
    """

    # get country name
    country_name = get_country_name(country_code)


    # get specification
    # if we only have a single country check if we might have a country specific
    # specification (currently only Australia, 2023)
    try:
        crf_spec = getattr(crf, f"CRF{submission_year}_{country_code}")
        print(f"Using country specific specification: "
              f"CRF{submission_year}_{country_code}")
    except:
        # no country specific specification, check for general specification
        try:
            crf_spec = getattr(crf, f"CRF{submission_year}")
        except:
            raise ValueError(
                f"No terminology exists for submission year " f"{submission_year}"
            )


    tables = [table for table in crf_spec.keys()
              if crf_spec[table]["status"] == "tested"]
    print(f"The following tables are available in the " \
          f"CRF{submission_year} specification: {tables}")

    if submission_date is None:
        submission_date = get_latest_date_for_country(country_code, submission_year)

    # check if data has been read already
    read_data = not submission_has_been_read(
        country_code, country_name, submission_year=submission_year,
        submission_date=submission_date, verbose=True,
    )

    ds_all = None
    if read_data or re_read:
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
                submission_year,
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
            output_folder = extracted_data_path_UNFCCC / country_name.replace(" ", "_")
            output_filename = f"{country_code}_CRF{submission_year}_{submission_date}"

            if not output_folder.exists():
                output_folder.mkdir()

            # write data in interchange format
            pm2.pm2io.write_interchange_format(output_folder / output_filename,
                                               ds_all.pr.to_interchange_format())

            # write data in native PRIMAP2 format
            encoding = {var: compression for var in ds_all.data_vars}
            ds_all.pr.to_netcdf(output_folder / (output_filename + ".nc"),
                                  encoding=encoding)

    return ds_all


def read_crf_for_country_datalad(
        country: str,
        submission_year: int,
        submission_date: Optional[str]=None,
        re_read: Optional[bool]=True
) -> None:
    """
    Wrapper around read_crf_for_country which takes care of selecting input
    and output files and using datalad run to trigger the data reading

    Parameters
    __________

    country_codes: str
        ISO 3-letter country UNFCCC_GHG_data

    submission_year: int
        Year of the submission of the data

    submission_date: Optional(str)
        Read for a specific submission date (given as string as in the file names)
        If not specified latest data will be read

    """

    # get all the info for the country
    country_info = get_input_and_output_files_for_country(
        country, submission_year=submission_year, verbose=True)

    print(f"Attempting to read data for CRF{submission_year} from {country}.")
    print("#"*80)
    print("")
    print(f"Using the UNFCCC_CRF_reader")
    print("")
    print(f"Run the script using datalad run via the python api")
    script = code_path / "UNFCCC_CRF_reader" / "read_UNFCCC_CRF_submission.py"

    cmd = f"./venv/bin/python3 {script.as_posix()} --country={country} "\
          f"--submission_year={submission_year} --submission_date={submission_date}"
    if re_read:
        cmd = cmd + f" --re_read"
    datalad.api.run(
        cmd=cmd,
        dataset=root_path,
        message=f"Read data for {country}, CRF{submission_year}, {submission_date}.",
        inputs=country_info["input"],
        outputs=country_info["output"],
        dry_run=None,
        explicit=True,
    )


def read_new_crf_for_year(
        submission_year: int,
        countries: Optional[List[str]]=None,
        re_read: Optional[bool]=False,
) -> dict:
    """
    Read CRF data for given submission year for all countries in
    `countries` that have submitted data. If no `countries` list is
    given, all countries are used.
    When updated submission exist the latest will be read.
    All tables available in the specification will be read for all years.
    Results will be written to appropriate country folders.

    If you want to read data from a different folder use the
    test_read_crf_data function.

    IMPORTANT NOTE:
    Currently there is no consistency check between data for the same category
    read from different tables

    Parameters
    __________

    submission_year: int
        Year of the submission of the data

    countries: List[int] (optional)
        List of countries to read. If not given reading is tried for all
        CRF countries

    re_read: bool (optional, default=False)
        If true data will be read even if already read before.

    TODO: write log with failed countries and what has been read

    Returns
    _______
        list[str]: list with country codes for which the data has been read

    """

    if countries is None:
        countries = all_crf_countries

    read_countries = {}
    for country in countries:
        try:
            country_df = read_crf_for_country(country, submission_year, re_read=re_read)
            if country_df is None:
                read_countries[country] = "skipped"
            else:
                read_countries[country] = "read"
        except NoCRFFilesError:
            print(f"No data for country {country}, {submission_year}")
            read_countries[country] = "no data"
        except Exception as ex:
            print(f"Data for country {country}, {submission_year} could not be read")
            print(f"The following error occurred: {ex}")
            read_countries[country]= "failed"

    # print overview
    successful_countries = [country for country in read_countries if read_countries[country] == "read"]
    skipped_countries = [country for country in read_countries if read_countries[country] == "skipped"]
    failed_countries = [country for country in read_countries if read_countries[country] == "failed"]
    no_data_countries = [country for country in read_countries if read_countries[country] == "no data"]

    print(f"Read data for countries {successful_countries}")
    print(f"Skipped countries {skipped_countries}")
    print(f"No data for countries {no_data_countries}")
    print(f"!!!!! Reading failed for {failed_countries}. Check why")
    return(read_countries)


def read_new_crf_for_year_datalad(
        submission_year: int,
        countries: Optional[List[str]] = None,
        re_read: Optional[bool] = False,
) -> None:
    """
    Wrapper around read_crf_for_year_datalad which takes care of selecting input
    and output files and using datalad run to trigger the data reading

    Parameters
    __________

    submission_year: int
        Year of the submission of the data

    countries: List[int] (optional)
        List of countries to read. If not given reading is tried for all
        CRF countries

    re_read: bool (optional, default=False)
        If true data will be read even if already read before.

    """

    if countries is not None:
        print(f"Reading CRF{submission_year} for countries {countries} using UNFCCC_CRF_reader.")
    else:
        print(f"Reading CRF{submission_year} for all countries using UNFCCC_CRF_reader.")
        countries = all_crf_countries
    print("#" * 80)
    print("")
    if re_read:
        print("Re-reading all latest submissions.")
    else:
        print("Only reading new submissions not read yet.")


    input_files = []
    output_files = []
    # loop over countries to collect input and output files
    print("Collect input and output files to pass to datalad")
    for country in countries:
        try:
            country_info = get_input_and_output_files_for_country(
                country, submission_year=submission_year, verbose=False)
            # check if the submission has been read already
            if re_read:
                input_files = input_files + country_info["input"]
                output_files = output_files + country_info["output"]
            else:
                data_read = submission_has_been_read(
                    country_info["code"], country_info["name"],
                    submission_year=submission_year,
                    submission_date=country_info["date"],
                    verbose=False,
                )
                if not data_read:
                    input_files = input_files + country_info["input"]
                    output_files = output_files + country_info["output"]
        except:
            # no error handling here as that is done in the function that does the actual reading
            pass

    print(f"Run the script using datalad run via the python api")
    script = code_path / "UNFCCC_CRF_reader" / "read_new_UNFCCC_CRF_for_year.py"

    #cmd = f"./venv/bin/python3 {script.as_posix()} --countries={countries} "\
    #      f"--submission_year={submission_year}"
    cmd = f"./venv/bin/python3 {script.as_posix()} " \
          f"--submission_year={submission_year}"

    if re_read:
        cmd = cmd + " --re_read"
    datalad.api.run(
        cmd=cmd,
        dataset=root_path,
        message=f"Read data for {countries}, CRF{submission_year}. Re-reading: {re_read}",
        inputs=input_files,
        outputs=output_files,
        dry_run=None,
        #explicit=True,
    )


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
    output_folder = extracted_data_path_UNFCCC / country_name.replace(" ", "_")
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


def submission_has_been_read(
        country_code: str,
        country_name: str,
        submission_year: int,
        submission_date: str,
        verbose: Optional[bool]=True,
) -> bool:
    """
    Check if a CRF submission has already been read
    """
    output_folder = extracted_data_path_UNFCCC / country_name.replace(" ", "_")
    output_filename = f"{country_code}_CRF{submission_year}_{submission_date}"
    if output_folder.exists():
        existing_files = output_folder.glob(f"{output_filename}.*")
        existing_suffixes = [file.suffix for file in existing_files]
        if all(suffix in existing_suffixes for suffix in [".nc", ".yaml", ".csv"]):
            has_been_read = True
            if verbose:
                print(f"Data already available for {country_code}, "
                      f"CRF{submission_year}, version {submission_date}.")
        else:
            has_been_read = False
            if verbose:
                print(f"Partial data available for {country_code}, "
                      f"CRF{submission_year}, version {submission_date}. "
                      "Please check if all files have been written after "
                      "reading.")
    else:
        has_been_read = False
        if verbose:
            print(f"No read data available for {country_code}, "
                  f"CRF{submission_year}, version {submission_date}. ")

    return has_been_read