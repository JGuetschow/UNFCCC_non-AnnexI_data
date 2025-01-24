"""
Functions for CTF reading - all functions
"""

from collections import Counter
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Optional

import datalad as dl
import numpy as np
import pandas as pd
import primap2 as pm2
import xarray as xr

from unfccc_ghg_data.helper import (
    all_countries,
    extracted_data_path_UNFCCC,
    get_country_name,
    log_path,
    root_path,
)

from . import crf_specifications as crf
from .unfccc_crf_reader_core import (
    create_category_tree,
    get_crf_files,
    get_info_from_crf_filename,
    get_latest_version_for_country,
    prep_specification,
)
from .unfccc_crf_reader_devel import (
    save_last_row_info,
    save_unknown_categories_info,
)
from .util import BTR_urls, NoCRFFilesError


def read_ctf_for_country(  # noqa: PLR0912, PLR0915
    country_code: str,
    submission_round: int,
    version: Optional[str] = None,
    re_read: Optional[bool] = True,
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
    country_code: str
        ISO 3-letter country code
    submission_round: int
        Year of the submission of the data
    date_or_version: Optional(str)
        Read for a specific submission date (CRF) or version (CRT/BTR)
        (given as string as in the file names)
        If not specified latest data will be read
    re_read: Optional(bool) default: True
        Read the data also if it's already present
    submission_type: str default "CRF"
        Read CRF or CRT

    Returns
    -------
        return value is a Pandas DataFrame with the read data in PRIMAP2 format
    """
    # get country name
    country_name = get_country_name(country_code)

    # get specification
    # if we only have a single country check if we might have a country specific
    # specification (currently only Australia, 2023)
    try:
        crf_spec = getattr(crf, f"CTF{submission_round}_{country_code}")
        print(
            f"Using country specific specification: "
            f"CTF{submission_round}_{country_code}"
        )
    except Exception:
        # no country specific specification, check for general specification
        try:
            crf_spec = getattr(crf, f"CTF{submission_round}")
        except Exception as ex:
            raise ValueError(  # noqa: TRY003
                f"No terminology exists for submission year/round "
                f"{submission_round}"
            ) from ex

    tables = [
        table for table in crf_spec.keys() if crf_spec[table]["status"] == "tested"
    ]
    print(
        f"The following tables are available in the "
        f"CTF{submission_round} specification: {tables}"
    )

    if version is None:
        version = get_latest_version_for_country(
            country_code,
            submission_round=submission_round,
            submission_type="CTF",
        )

    # check if data has been read already
    # TODO: enable submissions_has_been_read for CTF files
    # read_data = not submission_has_been_read(
    #     country_code,
    #     country_name,
    #     submission_year=submission_year,
    #     date_or_version=date_or_version,
    #     submission_type=submission_type,
    #     verbose=True,
    # )
    read_data = True

    ds_all = None
    if read_data or re_read:
        unknown_categories = []
        last_row_info = []
        for table in tables:
            # read table for all years
            (
                ds_table,
                new_unknown_categories,
                new_last_row_info,
                not_present,
            ) = read_ctf_table(
                country_code,
                table,
                submission_round,
                version=version,
            )

            # collect messages on unknown rows etc
            unknown_categories = unknown_categories + new_unknown_categories
            last_row_info = last_row_info + new_last_row_info

            if ds_table is not None:
                # convert to PRIMAP2 IF
                # first drop the category_entity col as it can have multiple values for
                # one category
                ds_table = ds_table.drop(columns=["category_entity"])

                # if we need to map entities pass this info to the conversion function
                if "entity_mapping" in crf_spec[table]:
                    entity_mapping = crf_spec[table]["entity_mapping"]
                else:
                    entity_mapping = None
                meta_data_input = {
                    "title": f"CTF data submitted for round {submission_round} "
                    f"to the UNFCCC in the Biannial Transparency Report (BTR) "
                    f"by {country_name}. Submission version: {version}"
                }
                ds_table_if = convert_ctf_table_to_pm2if(
                    ds_table,
                    submission_round,
                    meta_data_input=meta_data_input,
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
        # TODO temp. for now don't save for individual countries
        save_data = False
        if len(unknown_categories) > 0:
            save_data = False
            today = date.today()
            log_location = (
                log_path
                / f"CTF{submission_round}"
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
                / f"CTF{submission_round}"
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
            # TODO: function that creates the filename so if we modify something it's
            #  modified everywhere (but will break old data, so better keep file name)
            output_filename = f"{country_code}_CTF{submission_round}_" f"{version}"

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


def read_to_test_specs_CTF(  # noqa: PLR0912, PLR0915
    submission_round: int,
    totest: bool | None = False,
    country_code: str | None = None,
) -> xr.Dataset:
    """
    Read on file per country

    TODO: rename submission_year to submission_round
     rename version to version
    Read one xlsx file (so one data year) for each country for a submission year to
    create log files and extend the specifications

    Parameters
    ----------
    submission_round
        submission year to read
    totest
        if true only read tables with "totest" status
    country_code
        country to read. If not given all countries will be read

    Returns
    -------
    xr.Dataset with data for given parameters
    """
    # long name for type
    type_name = "common tabular format"

    if country_code == "None":
        country_code = None

    exceptions = []
    unknown_categories = []
    last_row_info = []
    ds_all = None
    print(f"CTF test reading for CTF{submission_round}. ")
    if totest:
        print("Reading only tables to test.")
    print("#" * 80)

    if country_code is not None:
        countries_to_read = [country_code]
    else:
        countries_to_read = all_countries

    for current_country_code in countries_to_read:
        # get country name
        country_name = get_country_name(current_country_code)
        print(f"reading for country: {current_country_code}")
        # get specification and available tables
        # if we only have a single country check if we might have a country specific
        # specification (currently only Australia, 2023)
        if current_country_code is not None:
            try:
                crf_spec = getattr(crf, f"CTF{submission_round}_{current_country_code}")
                print(
                    f"Using country specific specification: "
                    f"CTF{submission_round}_{current_country_code}"
                )
            except Exception:
                # no country specific specification, check for general specification
                try:
                    crf_spec = getattr(crf, f"CTF{submission_round}")
                except Exception as ex:
                    raise ValueError(  # noqa: TRY003
                        f"No terminology exists for submission year "
                        f"{submission_round}"
                    ) from ex
        else:
            try:
                crf_spec = getattr(crf, f"CTF{submission_round}")
            except Exception as ex:
                raise ValueError(  # noqa: TRY003
                    f"No terminology exists for CTF{submission_round}"
                ) from ex

        if totest:
            tables = [
                table
                for table in crf_spec.keys()
                if crf_spec[table]["status"] == "totest"
            ]
        else:
            tables = [
                table
                for table in crf_spec.keys()
                if crf_spec[table]["status"] == "tested"
            ]
        print(
            f"The following tables are available in the "
            f"CTF{submission_round} specification: {tables}"
        )
        print("#" * 80)

        try:
            version = get_latest_version_for_country(
                current_country_code,
                submission_round=submission_round,
                submission_type="CTF",
            )
        except Exception:
            message = (
                f"No submissions for country {country_name}, " f"CTF{submission_round}"
            )
            print(message)
            exceptions.append(f"No_sub: {country_name}: {message}")
            version = None
            pass

        if version is not None:
            for table in tables:
                try:
                    # read table for given years
                    (
                        ds_table,
                        new_unknown_categories,
                        new_last_row_info,
                        not_present,
                    ) = read_ctf_table(
                        current_country_code,
                        table,
                        submission_round,
                        version=version,
                        debug=True,
                    )

                    # collect messages on unknown rows etc
                    unknown_categories = unknown_categories + new_unknown_categories
                    last_row_info = last_row_info + new_last_row_info

                    if ds_table is None:
                        if not_present:
                            exceptions.append(
                                f"Note: Table {table} not present for" f"{country_name}"
                            )

                    else:
                        # convert to PRIMAP2 IF
                        # first drop the category_entity col as it can have multiple
                        # values for one category
                        ds_table = ds_table.drop(columns=["category_entity"])

                        # TODO: catch entity conversion errors and make list of error
                        #  entities
                        # if we need to map entities pass this info to the conversion
                        # function
                        if "entity_mapping" in crf_spec[table]:
                            entity_mapping = crf_spec[table]["entity_mapping"]
                        else:
                            entity_mapping = None

                        ds_table_if = convert_ctf_table_to_pm2if(
                            ds_table,
                            submission_round,
                            meta_data_input={
                                "title": f"Data submitted in {submission_round} to the "
                                f"UNFCCC in the {type_name} (CTF) "
                                f"by {country_name}. "
                                f"Submission date / version: {version}"
                            },
                            entity_mapping=entity_mapping,
                        )

                        # now convert to native PRIMAP2 format
                        ds_table_pm2 = pm2.pm2io.from_interchange_format(ds_table_if)

                        # combine per table DS
                        if ds_all is None:
                            ds_all = ds_table_pm2
                        else:
                            ds_all = ds_all.combine_first(ds_table_pm2)
                except Exception as e:
                    message = (
                        f"Error occurred when converting table {table} for"
                        f" {country_name} to PRIMAP2 IF. Exception: {e}"
                    )
                    print(message)
                    exceptions.append(f"Error: {country_name}: {message}")
                    pass

    # process log messages.
    today = date.today()
    output_folder = log_path / f"test_read_CTF{submission_round}"
    if not output_folder.exists():
        output_folder.mkdir()
    if len(unknown_categories) > 0:
        if country_code is not None:
            log_location = (
                output_folder / f"CTF_unknown_categories_{country_code}"
                f"_{today.strftime('%Y-%m-%d')}.csv"
            )
        else:
            log_location = (
                output_folder / f"CTF_unknown_categories_"
                f"{today.strftime('%Y-%m-%d')}.csv"
            )
        print(f"Unknown rows found. Savin log to {log_location}")
        save_unknown_categories_info(unknown_categories, log_location)

    if len(last_row_info) > 0:
        if country_code is not None:
            log_location = (
                output_folder / f"CTF_last_row_info_{country_code}_"
                f"{today.strftime('%Y-%m-%d')}.csv"
            )
        else:
            log_location = (
                output_folder / f"CTF_last_row_info_"
                f"{today.strftime('%Y-%m-%d')}.csv"
            )
        print(f"Data found in the last row. Saving log to " f"{log_location}")
        save_last_row_info(last_row_info, log_location)

    # write exceptions
    f_ex = open(output_folder / f"CTF_exceptions_{today.strftime('%Y-%m-%d')}.txt", "w")
    for ex in exceptions:
        f_ex.write(f"{ex}\n")
    f_ex.close()

    # save the data:
    print(f"Save dataset to log folder: {log_path}")
    compression = dict(zlib=True, complevel=9)

    if country_code is not None:
        output_filename = (
            f"CTF{submission_round}_{country_code}_" f"{today.strftime('%Y-%m-%d')}"
        )
    else:
        output_filename = f"CTF{submission_round}_{today.strftime('%Y-%m-%d')}"
    if totest:
        output_filename = output_filename + "_totest"

    # write data in interchange format
    pm2.pm2io.write_interchange_format(
        output_folder / output_filename, ds_all.pr.to_interchange_format()
    )

    # write data in native PRIMAP2 format
    encoding = {var: compression for var in ds_all.data_vars}
    ds_all.pr.to_netcdf(output_folder / (output_filename + ".nc"), encoding=encoding)

    return ds_all


def convert_ctf_table_to_pm2if(  # noqa: PLR0912, PLR0913
    df_table: pd.DataFrame,
    submission_round: int,
    entity_mapping: dict[str, str] | None = None,
    coords_defaults_input: dict[str, str] | None = None,
    filter_remove_input: dict[str, dict[str, str | list]] | None = None,
    filter_keep_input: dict[str, dict[str, str | list]] | None = None,
    meta_data_input: dict[str, str] | None = None,
) -> pd.DataFrame:
    """
    Convert a given pandas long format crf table to PRIMAP2 interchange format

    Parameters
    ----------
    df_table: pd.DataFrame
        Data to convert
    submission_round: int
        Year of submission
    entity_mapping: Optional[Dict[str,str]]
        Mapping of entities to PRIMAP2 format. Not necessary for all tables
    coords_defaults_input: Optional[Dict[str,str]],
        Additional default values for coordinates. (e.g. "Total" for `type`)
    filter_remove_input: Optional[Dict[str,Dict[str,Union[str,List]]]]
        Filter to remove data during conversion. The format is as in
        PRIMAP2
    filter_keep_input: Optional[Dict[str,Dict[str,Union[str,List]]]]
        Filter to keep only specified data during conversion.
        The format is as in PRIMAP2
    meta_data_input: Optional[Dict[str,str]]
        Meta data information. If values filled by this function automatically
        are given as input the automatic values are overwritten.

    Returns
    -------
    pd.DataFrame:
        Pandas DataFrame containing the data in PRIMAP2 interchange format
        Metadata is stored as attrs in the DataFrame
    """
    coords_cols = {
        "category": "category",
        "entity": "entity",
        "unit": "unit",
        "area": "country",
        "scenario": "scenario",
    }

    # set scenario and terminologies
    category_terminology = f"CTF{submission_round}"
    title = (
        f"Data submitted with BTR {submission_round} to the UNFCCC using the "
        f"Common Tabular Format (CTF)"
    )

    add_coords_cols = {
        #    "orig_cat_name": ["orig_cat_name", "category"],
    }

    coords_terminologies = {
        "area": "ISO3",
        "category": category_terminology,
        "scenario": "CTF-NDC",
    }

    coords_defaults = {
        "source": "UNFCCC",
        "provenance": "measured",
    }
    if coords_defaults_input is not None:
        for key in coords_defaults_input.keys():
            coords_defaults[key] = coords_defaults_input[key]

    coords_value_mapping = {
        "unit": "PRIMAP1",
    }
    if entity_mapping is not None:
        coords_value_mapping["entity"] = entity_mapping

    # coords_value_filling_template = {
    # }

    filter_remove = {
        "f1": {
            "category": ["\\IGNORE"],
        }
    }
    if filter_remove_input is not None:
        for key in filter_remove_input.keys():
            filter_remove[key] = filter_remove_input[key]

    filter_keep = {}
    if filter_keep_input is not None:
        for key in filter_keep_input.keys():
            filter_keep[key] = filter_keep_input[key]

    meta_data = {
        "rights": "",
        "contact": "mail@johannes-guetschow.de",
        "title": title,
        "comment": "Read fom xlsx file by Johannes Gütschow",
        "institution": "United Nations Framework Convention on Climate Change "
        "(www.unfccc.int)",
    }
    if submission_round in BTR_urls.keys():
        meta_data["references"] = BTR_urls[submission_round]
    elif meta_data_input is not None:
        if "references" not in meta_data_input.keys():
            raise ValueError(  # noqa: TRY003
                f"Submission round {submission_round} unknown, please add metadata."
            )
    else:
        raise ValueError(  # noqa: TRY003
            f"Submission round {submission_round} unknown, please add metadata."
        )

    if meta_data_input is not None:
        for key in meta_data_input.keys():
            meta_data[key] = meta_data_input[key]

    # make sure column names are str
    df_table.columns = df_table.columns.astype(str)

    df_table_if = pm2.pm2io.convert_wide_dataframe_if(
        df_table,
        coords_cols=coords_cols,
        add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        # coords_value_filling=coords_value_filling,
        filter_remove=filter_remove,
        filter_keep=filter_keep,
        meta_data=meta_data,
        time_format="%Y",
    )
    return df_table_if


def read_ctf_table(  # noqa: PLR0913, PLR0912
    country_codes: str | list[str],
    table: str,
    submission_round: int,
    version: str | None = None,
    folder: str | None = None,
    debug: bool = False,
) -> tuple[pd.DataFrame, list[list], list[list], bool]:
    """
    Read CTF table for given year and country/countries

    TODO: change
    Read CRF table for given submission year and country / or countries
    This function can read for multiple years and countries but only a single
    table. The reason is that combining data from different tables needs
    consistency checks while combining for different years and countries does not.

    The folder can either be given explicitly or if not given folders are determined
    from the submission_year and country_code variables

    Parameters
    ----------
    country_codes: str or list[str]
        ISO 3-letter country code or list of country codes
    table: str
        name of the table sheet in the CRF xlsx file
    submission_round: int
        Year of the submission of the data
    data_year: int or List of int (optional)
        if int a single data year will be read. if a list of ints is given these
        years will be read. If no nothing is given all data years will be read
    version: str (optional, default is None)
        readonly submission from the given date (CRF) or version (CRT/BTR)
        use "latest" to read the latest submissions
    folder: str (optional)
        Folder that contains the xls files. If not given folders are determined by the
        submissions_year and country_code variables
    submission_type: str default = "CRF"
        read CRF or CRT/BTR data
    debug: bool (optional)
        if true print some debug information like column headers

    Returns
    -------
    Tuple of parameters
        * First return parameter is the data as a pandas DataFrame in long format.
        * Second return parameter is a list of unknown categories / row headers.
        * Third return parameter holds information on data found in the last read row.
          This is used as a hint to check if table specifications might have to
          be adapted as country submitted tables are longer than expected.

    """
    if isinstance(country_codes, str):
        country_codes = [country_codes]

    # get file names and locations
    input_files = get_crf_files(
        country_codes=country_codes,
        submission_year=submission_round,
        date_or_version=version,
        folder=folder,
        submission_type="CTF",
    )

    if not input_files:
        raise NoCRFFilesError(  # noqa: TRY003
            f"No files found for {country_codes}, "
            f"submission_year={submission_round}, "
            f"date/version={version}, "
            f"folder={folder}."
        )

    # get specification
    # if we only have a single country check if we might have a country specific
    # specification (currently only Australia, 2023)
    if len(country_codes) == 1:
        try:
            crf_spec = getattr(crf, f"CTF{submission_round}_{country_codes[0]}")
            print(
                f"Using country specific specification: "
                f"CTF{submission_round}_{country_codes[0]}"
            )
        except:  # noqa: E722
            # no country specific specification, check for general specification
            try:
                crf_spec = getattr(crf, f"CTF{submission_round}")
            except Exception as ex:
                raise ValueError(  # noqa: TRY003
                    f"No terminology exists for submission year " f"{submission_round}"
                ) from ex
    else:
        try:
            crf_spec = getattr(crf, f"CTF{submission_round}")
        except Exception as ex:
            raise ValueError(  # noqa: TRY003
                f"No terminology exists for submission year " f"{submission_round}"
            ) from ex

    # now loop over files and read them
    # TODO: this loop is not necessary for CTF-NDC files as they have only one file per
    #  submission
    df_all = None
    unknown_rows = []
    last_row_info = []
    not_present = False
    for file in input_files:
        file_info = get_info_from_crf_filename(file.name)
        try:
            int(file_info["data_year"])
            (
                df_this_file,
                unknown_rows_this_file,
                last_row_info_this_file,
            ) = read_ctf_table_from_file(file, table, crf_spec[table], debug=debug)
            if df_all is None:
                df_all = df_this_file.copy(deep=True)
                unknown_rows = unknown_rows_this_file
                last_row_info = last_row_info_this_file
            else:
                df_all = pd.concat([df_this_file, df_all])
                unknown_rows = unknown_rows + unknown_rows_this_file
                last_row_info = last_row_info + last_row_info_this_file
        except ValueError as e:
            if e.args[0] == f"Worksheet named '{table}' not found":
                print(f"Table {table} not present")
                not_present = True
                pass
            else:
                print(f"Error when reading file {file}. Skipping file. Exception: {e}")
        except Exception as e:
            print(f"Error when reading file {file}. Skipping file. Exception: {e}")

    return df_all, unknown_rows, last_row_info, not_present


def read_ctf_table_from_file(  # noqa: PLR0912, PLR0915
    file: Path,
    table: str,
    table_spec: dict[str, dict],
    debug: bool = False,
) -> tuple[pd.DataFrame, list[list], list[list]]:
    """
    Read single crf table from file

    Read a single CRF table from a given file. This is the core function of the CRF
    reading process as it reads the data from xls and performs the category mapping.

    Parameters
    ----------
    file: Path
        file to read from
    table: str
        table to read (name of the sheet in the xlsx file)
    table_spec: Dict[str, Dict]
        Specification for the given table, e.g. CRF2021["Table4"]
    debug: bool (optional)
        if true print some debug information like column headers

    Returns
    -------
    Tuple of parameters
        * First return parameter is the data as a pandas DataFrame in long format
        * Second return parameter is a list of unknown categories / row headers
        * Third return parameter holds information on data found in the last read row.
          This is used as a hint to check if table specifications might have to
          be adapted as country submitted tables are longer than expected.

    """
    # check if file exists and if not download
    # TODO: fix such that it also follows links (if the target of the link is a link
    #  check if that exists and if not download)
    if file.is_symlink():
        if not file.exists():
            dlds = dl.api.Dataset(root_path)
            dlds.get(file.relative_to(root_path))

    table_properties = table_spec["table"]
    file_info = get_info_from_crf_filename(file.name)

    # find non-unique categories in mapping
    all_cats_mapping = deepcopy(table_spec["sector_mapping"])
    # prep specification
    all_cats_mapping = prep_specification(
        specification=all_cats_mapping, country=file_info["party"]
    )
    all_cats = [cat[0][0] for cat in all_cats_mapping]

    unique_cats = [cat for (cat, count) in Counter(all_cats).items() if count == 1]
    unique_cat_tuples = [
        mapping for mapping in all_cats_mapping if mapping[0][0] in unique_cats
    ]
    unique_mapping = dict(
        zip(
            [tup[0][0] for tup in unique_cat_tuples],
            [tup[1] for tup in unique_cat_tuples],
        )
    )
    non_unique_cats = [cat for (cat, count) in Counter(all_cats).items() if count > 1]

    # prepare the sector hierarchy
    if non_unique_cats:
        # if we have non-unique categories present we need the information on
        # levels within the category hierarchy
        category_tree = create_category_tree(
            all_cats_mapping, table, file_info["party"]
        )

    # prepare index colum information
    cat_col = table_properties["col_for_categories"]
    cols_for_space_stripping = [table_properties["col_for_categories"]]

    # read the data
    print(f"Reading table {table} for year {file_info['data_year']} from {file.name}.")
    skiprows = table_properties["firstrow"] - 1
    nrows = (
        table_properties["lastrow"] - skiprows + 1
    )  # read one row more to check if we reached the end
    # we read with user specific NaN treatment as the NaN treatment is part of
    # the conversion to PRIMAP2 format.
    df_raw = pd.read_excel(
        file,
        sheet_name=table,
        skiprows=skiprows,
        nrows=nrows,
        engine="openpyxl",
        na_values=[
            "-1.#IND",
            "-1.#QNAN",
            "-NaN",
            "-nan",
            "1.#IND",
            "1.#QNAN",
            "NULL",
            "NaN",
            "",
            " ",
        ],
        keep_default_na=False,
    )

    cols_to_drop = []
    # remove empty first column (because CRTables start with an empty column)
    # df_raw = df_raw.dropna(how="all", axis=1)
    if df_raw.iloc[:, 0].isna().all():
        cols_to_drop.append(df_raw.columns.to_numpy()[0])
    # select only first table by cutting everything after a all-nan column (unless
    # it's the first column)
    if debug:
        print(f"Header before table end detection: {df_raw.columns.to_numpy()}")
    for colIdx in range(1, len(df_raw.columns.values)):
        if (df_raw.iloc[:, colIdx].isna().all()) & (
            df_raw.columns[colIdx].startswith("Unnamed")
        ):
            cols_to_drop = cols_to_drop + list(df_raw.columns.to_numpy()[colIdx:])
            if debug:
                print(f"cols_to_drop: {cols_to_drop}")
            break

    if cols_to_drop is not None:
        df_raw = df_raw.drop(columns=cols_to_drop)

    #### prepare the header (2 row header, first entity, then unit)
    # We do this before removing columns and any other processing to
    # have consistent column names in the configuration and to avoid
    # "Unnamed: X" column names which appear after reading of merged
    # cells
    # the filling leads to long and a bit confusing headers, but as long
    # as pandas can not fill values of merged cells in all individual cells
    # we have to use some filling algorithm.
    df_header = df_raw.iloc[0 : len(table_properties["header"]) - 1].copy(deep=True)
    df_header.loc[-1] = df_header.columns.to_numpy()
    df_header.index = df_header.index + 1
    # replace "Unnamed: X" colum names by nan to fill from left in next step
    df_header = df_header.sort_index()
    df_header = df_header.replace(r"Unnamed: [0-9]{1,2}", np.nan, regex=True)
    header = []
    # fill nans with the last value from the left
    if "header_fill" in table_properties:
        for row in range(0, len(df_header)):
            if table_properties["header_fill"][row]:
                header.append(list(df_header.iloc[row].ffill()))
            else:
                header.append(list(df_header.iloc[row]))
    else:
        for row in range(0, len(df_header)):
            header.append(list(df_header.iloc[row].ffill()))

    # use hard coded rows (years: row 1, units: row 0)
    # map units
    header[0] = [
        table_properties["unit_replacement"][unit]
        if unit in table_properties["unit_replacement"].keys()
        else unit
        for unit in header[0]
    ]

    if len(set(header[0][1:])) > 1:
        raise (
            ValueError(  # noqa: TRY003
                f"Header should not have more than one unit.: {header[0][1:]}"
            )
        )
    # store the unit and frop from header
    unit = header[0][1]
    header[1][0] = cat_col
    cols = [f"{int(col)}" if isinstance(col, float) else col for col in header[1]]

    # replace the old header
    df_current = df_raw.drop(index=df_raw.iloc[0:1].index)

    df_current.columns = cols
    if debug:
        print(f"Columns present: {cols}")
    # remove all columns to ignore
    df_current = df_current.drop(columns=table_properties["cols_to_ignore"])

    # remove double spaces
    for col in cols_for_space_stripping:
        df_current[col] = df_current[col].str.strip()
        df_current[col] = df_current[col].replace("\\s+", " ", regex=True)

    # prepare for sector mapping by initializing result lists and
    # variables
    new_cats = [[""] * len(table_properties["categories"])] * len(df_current)

    # copy the header rows which are not part of the index (unit)
    new_cats[0] = [df_current.iloc[0][cat_col]] * len(table_properties["categories"])

    # do the sector mapping here as we need to keep track of unmapped categories
    # and also need to consider the order of elements for the mapping
    unknown_categories = []
    info_last_row = []
    if non_unique_cats:
        # need to initialize the tree parsing.
        last_parent = category_tree.get_node("root")
        all_nodes = set(
            [category_tree.get_node(node).tag for node in category_tree.nodes]
        )

        for idx in range(0, len(df_current)):
            current_cat = str(df_current.iloc[idx][cat_col])
            if current_cat in table_properties["stop_cats"]:
                # we've reached the end of the table, so stop processing
                # and remove all further rows
                df_current = df_current.drop(df_current.index[idx:])
                new_cats = new_cats[0:idx]
                break

            # check if current category is a child of the last node
            children = dict(
                [
                    [child.tag, child.identifier]
                    for child in category_tree.children(last_parent.identifier)
                ]
            )
            if current_cat in children.keys():
                # the current category is a child of the current parent
                # do the mapping
                node = category_tree.get_node(children[current_cat])
                new_cats[idx] = node.data[1]
                # check if the node has children
                new_children = category_tree.children(node.identifier)
                if new_children:
                    last_parent = node

            # two other possibilities
            # 1. The category is at a higher point in the hierarchy
            # 2. It's missing in the hierarchy
            # we have to first move up the hierarchy
            # first check if category is present at all
            elif current_cat in all_nodes:
                old_parent = last_parent

                while (current_cat not in children.keys()) and (
                    last_parent.identifier != "root"
                ):
                    last_parent = category_tree.get_node(
                        last_parent.predecessor(category_tree.identifier)
                    )
                    children = dict(
                        [
                            [child.tag, child.identifier]
                            for child in category_tree.children(last_parent.identifier)
                        ]
                    )

                if (last_parent.identifier == "root") and (
                    current_cat not in children.keys()
                ):
                    # we have not found the category as direct child of any of the
                    # predecessors. Thus it is missing in the specification in
                    # that place
                    print(
                        f"Unknown category '{current_cat}' found in {table} for "
                        f"{file_info['party']}, {file_info['data_year']} "
                        f"(last parent: {old_parent.tag})."
                    )
                    unknown_categories.append(
                        [
                            table,
                            file_info["party"],
                            current_cat,
                            file_info["data_year"],
                            idx,
                        ]
                    )
                    # copy back the parent info to continue with next category
                    last_parent = old_parent
                else:
                    # do the mapping
                    node = category_tree.get_node(children[current_cat])
                    new_cats[idx] = node.data[1]
                    # check if the node has children
                    new_children = category_tree.children(node.identifier)
                    if new_children:
                        last_parent = node
            else:
                print(
                    f"Unknown category '{current_cat}' found in {table} for "
                    f"{file_info['party']}, {file_info['data_year']}, {idx}."
                )
                unknown_categories.append(
                    [
                        table,
                        file_info["party"],
                        current_cat,
                        file_info["data_year"],
                        idx,
                    ]
                )
    else:
        for idx in range(1, len(df_current)):
            current_cat = str(df_current.iloc[idx][cat_col])
            if current_cat in table_properties["stop_cats"]:
                # we've reached the end of the table, so stop processing
                # and remove all further rows
                df_current = df_current.drop(df_current.index[idx:])
                new_cats = new_cats[0:idx]
                break
            else:
                if idx == len(df_current) - 1:
                    print(
                        f"found information in last row: category {current_cat}, "
                        f"row {idx}"
                    )
                    info_last_row.append(
                        [table, file_info["party"], current_cat, file_info["data_year"]]
                    )
                if current_cat in all_cats:
                    new_cats[idx] = unique_mapping[current_cat]

                else:
                    print(
                        f"Unknown category '{current_cat}' found in {table} for "
                        f"{file_info['party']}, {file_info['data_year']}."
                    )
                    unknown_categories.append(
                        [
                            table,
                            file_info["party"],
                            current_cat,
                            file_info["data_year"],
                            idx,
                        ]
                    )

    for idx, col in enumerate(table_properties["categories"]):
        df_current.insert(loc=idx, column=col, value=[cat[idx] for cat in new_cats])

    # add country information
    df_current.insert(0, column="country", value=file_info["party"])
    df_current.insert(0, column="unit", value=unit)
    # df_long.insert(1, column="submission", value=f"CRF{file_info['submission_year']}")
    if "coords_defaults" in table_spec.keys():
        for col in table_spec["coords_defaults"]:
            df_current.insert(2, column=col, value=table_spec["coords_defaults"][col])

    return df_current, unknown_categories, info_last_row
