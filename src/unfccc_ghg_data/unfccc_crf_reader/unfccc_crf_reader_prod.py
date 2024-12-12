"""
Functions for CRF/CRT reading - productions functions for full reading
"""

from datetime import date
from typing import Optional, Union

import datalad.api
import primap2 as pm2
import xarray as xr

from unfccc_ghg_data.helper import (
    all_countries,
    code_path,
    custom_country_mapping,
    extracted_data_path_UNFCCC,
    get_country_code,
    get_country_name,
    log_path,
    root_path,
)

from . import crf_specifications as crf
from .unfccc_crf_reader_core import (
    convert_crf_table_to_pm2if,
    get_crf_files,
    get_latest_date_for_country,
    read_crf_table,
)
from .unfccc_crf_reader_devel import save_last_row_info, save_unknown_categories_info
from .util import NoCRFFilesError, all_crf_countries

# functions:
# * testing fucntions
# ** read one or more table(s) for all countries
#    (and a if desired only a single year) and write
#    output files with missing sectors etc
# **

# general approach:
# main code in a function that reads on table from one file.
# return raw pandas DF for use in different functions
# wrappers around this function to read for a whole country or for test reading
# where we also write files with missing sectors etc.
# merging functions use native pm2 format


def read_crf_for_country(  # noqa: PLR0912, PLR0915
    country_code: str,
    submission_year: int,
    submission_date: Optional[str] = None,
    re_read: Optional[bool] = True,
    type: str = "CRF",
) -> xr.Dataset:
    """
    Read for given submission year and country.

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
    ----------
    country_codes: str
        ISO 3-letter country code
    submission_year: int
        Year of the submission of the data
    submission_data: Optional(str)
        Read for a specific submission date (given as string as in the file names)
        If not specified latest data will be read
    re_read: Optional(bool) default: True
        Read the data also if it's already present
    type: str default "CRF"
        Read CRF or CRT

    Returns
    -------
        return value is a Pandas DataFrame with the read data in PRIMAP2 format
    """
    # long name for type
    if type == "CRF":
        type_name = "common reporting format"
    elif type == "CRT":
        type_name = "common reporting tables"
    else:
        raise ValueError("Type must be CRF or CRT")  # noqa: TRY003
    # get country name
    country_name = get_country_name(country_code)

    # get specification
    # if we only have a single country check if we might have a country specific
    # specification (currently only Australia, 2023)
    try:
        crf_spec = getattr(crf, f"{type}{submission_year}_{country_code}")
        print(
            f"Using country specific specification: "
            f"{type}{submission_year}_{country_code}"
        )
    except Exception:
        # no country specific specification, check for general specification
        try:
            crf_spec = getattr(crf, f"{type}{submission_year}")
        except Exception as ex:
            raise ValueError(  # noqa: TRY003
                f"No terminology exists for submission year/round " f"{submission_year}"
            ) from ex

    tables = [
        table for table in crf_spec.keys() if crf_spec[table]["status"] == "tested"
    ]
    print(
        f"The following tables are available in the "
        f"{type}{submission_year} specification: {tables}"
    )

    if submission_date is None:
        submission_date = get_latest_date_for_country(
            country_code, submission_year, type
        )

    # check if data has been read already
    read_data = not submission_has_been_read(
        country_code,
        country_name,
        submission_year=submission_year,
        submission_date=submission_date,
        submission_type=type,
        verbose=True,
    )

    ds_all = None
    if read_data or re_read:
        unknown_categories = []
        last_row_info = []
        for table in tables:
            # read table for all years
            ds_table, new_unknown_categories, new_last_row_info = read_crf_table(
                country_code,
                table,
                submission_year,
                date=submission_date,
                submission_type=type,
            )  # , data_year=[1990])

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
                meta_data_input={
                    "title": f"Data submitted in {submission_year} to the UNFCCC "
                    f"in the {type_name} ({type}) by {country_name}. "
                    f"Submission date: {submission_date}"
                },
                entity_mapping=entity_mapping,
                submission_type=type,
            )

            # now convert to native PRIMAP2 format
            ds_table_pm2 = pm2.pm2io.from_interchange_format(ds_table_if)

            # if individual data for emissions and removals / recovery exist combine
            # them
            if (
                ("CO2 removals" in ds_table_pm2.data_vars)
                and ("CO2 emissions" in ds_table_pm2.data_vars)
                and "CO2" not in ds_table_pm2.data_vars
            ):
                # we can just sum to CO2 as we made sure that it doesn't exist.
                # If we have CO2 and removals but not emissions, CO2 already has
                # removals subtracted and we do nothing here
                ds_table_pm2["CO2"] = ds_table_pm2[
                    ["CO2 emissions", "CO2 removals"]
                ].pr.sum(dim="entity", skipna=True, min_count=1)
                ds_table_pm2["CO2"].attrs["entity"] = "CO2"

            if (
                ("CH4 removals" in ds_table_pm2.data_vars)
                and ("CH4 emissions" in ds_table_pm2.data_vars)
                and "CH4" not in ds_table_pm2.data_vars
            ):
                # we can just sum to CH4 as we made sure that it doesn't exist.
                # If we have CH4 and removals but not emissions, CH4 already has
                # removals subtracted and we do nothing here
                ds_table_pm2["CH4"] = ds_table_pm2[
                    ["CH4 emissions", "CH4 removals"]
                ].pr.sum(dim="entity", skipna=True, min_count=1)
                ds_table_pm2["CH4"].attrs["entity"] = "CH4"

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
            log_location = (
                log_path
                / f"{type}{submission_year}"
                / f"{country_code}_unknown_categories_{today.strftime('%Y-%m-%d')}.csv"
            )
            print(
                f"Unknown rows found for {country_code}. Not saving data. "
                f"Saving log to {log_location}"
            )
            save_unknown_categories_info(unknown_categories, log_location)

        if len(last_row_info) > 0:
            save_data = False
            today = date.today()
            log_location = (
                log_path
                / f"{type}{submission_year}"
                / f"{country_code}_last_row_info_{today.strftime('%Y-%m-%d')}.csv"
            )
            print(
                f"Data found in the last row found for {country_code}. "
                f"Not saving data. Saving log to {log_location}"
            )
            save_last_row_info(last_row_info, log_location)

        if save_data:
            compression = dict(zlib=True, complevel=9)
            output_folder = extracted_data_path_UNFCCC / country_name.replace(" ", "_")
            output_filename = (
                f"{country_code}_{type}{submission_year}_" f"{submission_date}"
            )

            if not output_folder.exists():
                output_folder.mkdir()

            # write data in interchange format
            pm2.pm2io.write_interchange_format(
                output_folder / output_filename, ds_all.pr.to_interchange_format()
            )

            # write data in native PRIMAP2 format
            encoding = {var: compression for var in ds_all.data_vars}
            ds_all.pr.to_netcdf(
                output_folder / (output_filename + ".nc"), encoding=encoding
            )

    return ds_all


def read_crf_for_country_datalad(
    country: str,
    submission_year: int,
    submission_date: Optional[str] = None,
    re_read: Optional[bool] = True,
    type: str = "CRF",
) -> None:
    """
    Prepare input for read_crf_for_country

    Wrapper around read_crf_for_country which takes care of selecting input
    and output files and using datalad run to trigger the data reading

    Parameters
    ----------
    country_codes: str
        ISO 3-letter country code
    submission_year: int
        Year of the submission of the data
    submission_date: Optional(str)
        Read for a specific submission date (given as string as in the file names)
        If not specified latest data will be read
    type: str default "CRF"
        Read CRF or CRT

    """
    # check type
    if type not in ["CRF", "CRT"]:
        raise ValueError("Type must be CRF or CRT")  # noqa: TRY003
    # get all the info for the country
    country_info = get_input_and_output_files_for_country(
        country,
        submission_year=submission_year,
        verbose=True,
        type=type,
    )

    print(f"Attempting to read data for {type}{submission_year} from {country}.")
    print("#" * 80)
    print("")
    print("Using the unfccc_crf_reader")
    print("")
    print("Run the script using datalad run via the python api")
    script = code_path / "unfccc_crf_reader" / "read_unfccc_crf_submission.py"

    cmd = (
        f"python3 {script.as_posix()} "
        f"--country={country} "
        f"--submission_year={submission_year} "
        f"--submission_date={submission_date} "
        f"--type={type}"
    )
    if re_read:
        cmd = cmd + " --re_read"
    datalad.api.run(
        cmd=cmd,
        dataset=root_path,
        message=f"Read data for {country}, {type}{submission_year}, {submission_date}.",
        inputs=country_info["input"],
        outputs=country_info["output"],
        dry_run=None,
        explicit=True,
    )


def read_new_crf_for_year(
    submission_year: int,
    countries: list[str] | None = None,
    re_read: bool | None = False,
    type: str = "CRF",
) -> dict:
    """
    Read CRF for given countries

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
    ----------
    submission_year: int
        Year of the submission of the data
    countries: List[int] (optional)
        List of countries to read. If not given reading is tried for all
        CRF countries
    re_read: bool (optional, default=False)
        If true data will be read even if already read before.
    type: str default "CRF"
        Read CRF or CRT

    TODO: write log with failed countries and what has been read

    Returns
    -------
        list[str]: list with country codes for which the data has been read

    """
    if type == "CRF":
        if countries is None:
            countries = all_crf_countries
    elif type == "CRT":
        if countries is None:
            countries = all_countries
    else:
        raise ValueError("Type must be CRF or CRT")  # noqa: TRY003

    read_countries = {}
    for country in countries:
        try:
            country_df = read_crf_for_country(
                country, submission_year, re_read=re_read, type=type
            )
            if country_df is None:
                read_countries[country] = "skipped"
            else:
                read_countries[country] = "read"
        except NoCRFFilesError:
            print(f"No {type} data for country {country}, {submission_year}")
            read_countries[country] = "no data"
        except Exception as ex:
            print(
                f"{type} data for country {country}, "
                f"{submission_year} could not be read"
            )
            print(f"The following error occurred: {ex}")
            read_countries[country] = "failed"

    # print overview
    successful_countries = [
        country for country in read_countries if read_countries[country] == "read"
    ]
    skipped_countries = [
        country for country in read_countries if read_countries[country] == "skipped"
    ]
    failed_countries = [
        country for country in read_countries if read_countries[country] == "failed"
    ]
    no_data_countries = [
        country for country in read_countries if read_countries[country] == "no data"
    ]

    print(f"Read data for countries {successful_countries}")
    print(f"Skipped countries {skipped_countries}")
    print(f"No data for countries {no_data_countries}")
    print(f"!!!!! Reading failed for {failed_countries}. Check why")
    return read_countries


def read_new_crf_for_year_datalad(  # noqa: PLR0912
    submission_year: int,
    countries: Optional[list[str]] = None,
    re_read: Optional[bool] = False,
    type: str = "CRF",
) -> None:
    """
    Prepare input for read_crf_for_year

    Wrapper around read_crf_for_year_datalad which takes care of selecting input
    and output files and using datalad run to trigger the data reading

    Parameters
    ----------
    submission_year: int
        Year of the submission of the data
    countries: List[int] (optional)
        List of countries to read. If not given reading is tried for all
        CRF countries
    re_read: bool (optional, default=False)
        If true data will be read even if already read before.
    type: str default "CRF"
        Read CRF or CRT

    """
    if countries is not None:
        print(
            f"Reading {type}{submission_year} for countries {countries} "
            f"using unfccc_crf_reader."
        )
    else:
        print(
            f"Reading {type}{submission_year} for all countries "
            f"using unfccc_crf_reader."
        )
        if type == "CRF":
            if countries is None:
                countries = all_crf_countries
        elif type == "CRT":
            if countries is None:
                countries = all_countries
        else:
            raise ValueError("Type must be CRF or CRT")  # noqa: TRY003

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
                country, submission_year=submission_year, verbose=False
            )
            # check if the submission has been read already
            if re_read:
                input_files = input_files + country_info["input"]
                output_files = output_files + country_info["output"]
            else:
                data_read = submission_has_been_read(
                    country_info["code"],
                    country_info["name"],
                    submission_year=submission_year,
                    submission_date=country_info["date"],
                    submission_type=type,
                    verbose=False,
                )
                if not data_read:
                    input_files = input_files + country_info["input"]
                    output_files = output_files + country_info["output"]
        except Exception:  # noqa: S110
            # no error handling here as that is done in the function that does
            # the actual reading
            pass

    print("Run the script using datalad run via the python api")
    script = code_path / "unfccc_crf_reader" / "read_new_unfccc_crf_for_year.py"

    # cmd = f"python3 {script.as_posix()} --countries={countries} "\
    #      f"--submission_year={submission_year}"
    cmd = (
        f"python3 {script.as_posix()} "
        f"--submission_year={submission_year} "
        f"--type={type}"
    )

    if re_read:
        cmd = cmd + " --re_read"
    datalad.api.run(
        cmd=cmd,
        dataset=root_path,
        message=f"Read data for {countries}, {type}{submission_year}. "
        f"Re-reading: {re_read}",
        inputs=input_files,
        outputs=output_files,
        dry_run=None,
        # explicit=True,
    )


def get_input_and_output_files_for_country(
    country: str,
    submission_year: int,
    submission_date: Optional[str] = None,
    type: str = "CRF",
    verbose: Optional[bool] = True,
) -> dict[str, Union[list, str]]:
    """
    Get input and output files for a given country

    Parameters
    ----------
    country: str
        3 letter country code
    submission_year: int
        year of submissions for CRF or submission round for CRT
    submission_date
        date of submission (as in the filename)
    type: str: default "CRF"
        CRF or CRT
    verbose: bool (optional, default True)
        if True print additional output

    Returns
    -------
    dict with keays "input" and "output". Values are a list of files
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
            print("No submission date given, find latest date.")
        submission_date = get_latest_date_for_country(
            country_code, submission_year, type=type
        )
    elif verbose:
        print(f"Using given submissions date {submission_date}")

    if submission_date is None:
        # there is no data. Raise an exception
        raise NoCRFFilesError(  # noqa: TRY003
            f"No submissions found for {country_code}, "
            f"type={type}, "
            f"submission_year={submission_year}, "
            f"date={date}"
        )
    elif verbose:
        print(
            f"Latest submission date for {type}{submission_year} is {submission_date}"
        )
    country_info["date"] = submission_date

    # get possible input files
    input_files = get_crf_files(
        country_codes=country_code,
        submission_year=submission_year,
        date=submission_date,
        submission_type=type,
    )
    if not input_files:
        raise NoCRFFilesError(  # noqa: TRY003
            f"No possible input files found for {country}, {type}{submission_year}, "
            f"v{submission_date}. Are they already submitted and included in the "
            f"repository?"
        )
    elif verbose:
        print("Found the following input_files:")
        for file in input_files:
            print(file.name)
        print("")

    # convert file's path to str
    input_files = [file.as_posix() for file in input_files]
    country_info["input"] = input_files

    # get output file
    output_folder = extracted_data_path_UNFCCC / country_name.replace(" ", "_")
    output_files = [
        output_folder / f"{country_code}_{type}{submission_year}"
        f"_{submission_date}.{suffix}"
        for suffix in ["yaml", "csv", "nc"]
    ]
    if verbose:
        print("The following files are considered as output_files:")
        for file in output_files:
            print(file)
        print("")

    # check if output data present

    # convert file paths to str
    output_files = [file.as_posix() for file in output_files]
    country_info["output"] = output_files

    return country_info


def submission_has_been_read(  # noqa: PLR0913
    country_code: str,
    country_name: str,
    submission_year: int,
    submission_date: str,
    submission_type: str = "CRF",
    verbose: Optional[bool] = True,
) -> bool:
    """
    Check if a CRF/CRT submission has already been read

    Parameters
    ----------
    country_code: str
        3 letter country code
    country_name: str
        Name of the country
    submission_year: int
        year of submissions for CRF or submission round for CRT
    submission_date
        date of submission (as in the filename)
    submission_type: str: default "CRF"
        CRF or CRT
    verbose: bool (optional, default True)
        if True print additional output

    Returns
    -------
    True if data has been read, False otherwise
    """
    output_folder = extracted_data_path_UNFCCC / country_name.replace(" ", "_")
    output_filename = (
        f"{country_code}_{submission_type}{submission_year}_{submission_date}"
    )

    #    check if the submission_year is correctly used for CRT
    if output_folder.exists():
        existing_files = output_folder.glob(f"{output_filename}.*")
        existing_suffixes = [file.suffix for file in existing_files]
        if all(suffix in existing_suffixes for suffix in [".nc", ".yaml", ".csv"]):
            has_been_read = True
            if verbose:
                print(
                    f"Data already available for {country_code}, "
                    f"{submission_type}{submission_year}, version {submission_date}."
                )
        elif existing_suffixes:
            has_been_read = False
            if verbose:
                print(
                    f"Partial data available for {country_code}, "
                    f"{submission_type}{submission_year}, version {submission_date}. "
                    "Please check if all files have been written after "
                    f"reading. Existing suffixes: {existing_suffixes}"
                )
        else:
            has_been_read = False
            if verbose:
                print(
                    f"No read data available for {country_code}, "
                    f"{submission_type}{submission_year}, version {submission_date}. "
                )
    else:
        has_been_read = False
        if verbose:
            print(f"No read data available for {country_code}. ")

    return has_been_read
