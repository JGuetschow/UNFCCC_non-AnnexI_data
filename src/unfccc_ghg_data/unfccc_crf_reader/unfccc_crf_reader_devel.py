"""
Functions for CRF reading development

This file holds functions that are used in CRF reading development like
adding new tables or new submission years (and according country specific
categories). The functions are tailored towards debug output and reading
of single years in contrast to the production functions which are tailored
towards the creation of full datasets including storage in the
"""

from datetime import date
from pathlib import Path

import pandas as pd
import primap2 as pm2
import xarray as xr

from unfccc_ghg_data.helper import all_countries, get_country_name, log_path

from . import crf_specifications as crf
from .unfccc_crf_reader_core import (
    convert_crf_table_to_pm2if,
    get_latest_date_for_country,
    get_latest_version_for_country,
    read_crf_table,
)
from .util import all_crf_countries


def read_year_to_test_specs(  # noqa: PLR0912, PLR0915
    submission_year: int,
    data_year: int | None = None,
    submission_type: str = "CRF",
    totest: bool | None = False,
    country_code: str | None = None,
) -> xr.Dataset:
    """
    Read on file per country

    Read one xlsx file (so one data year) for each country for a submission year to
    create log files and extend the specifications

    Parameters
    ----------
    submission_year
        submission year to read
    data_year
        year to read
    submission_type: str = CRF
        read CRF or CRT data
    totest
        if true only read tables with "totest" status
    country_code
        country to read. If not given all countries will be read

    Returns
    -------
    xr.Dataset with data for given parameters
    """
    # long name for type
    if submission_type == "CRF":
        type_name = "common reporting format"
    elif submission_type in ["CRT", "CRTAI"]:
        type_name = "common reporting tables"
    else:
        raise ValueError("Type must be CRF, CRT, or CRTAI")  # noqa: TRY003

    if data_year is None:
        data_year = 2000

    if country_code == "None":
        country_code = None

    exceptions = []
    unknown_categories = []
    last_row_info = []
    empty_tables = []
    missing_worksheets = []
    ds_all = None
    print(
        f"{submission_type} test reading for {submission_type}{submission_year}. "
        f"Using data year {data_year}"
    )
    if totest:
        print("Reading only tables to test.")
    print("#" * 80)

    if country_code is not None:
        countries_to_read = [country_code]
    else:  # noqa: PLR5501
        if submission_type in ["CRF", "CRTAI"]:
            countries_to_read = all_crf_countries
        elif submission_type == "CRT":
            countries_to_read = all_countries
        else:
            raise ValueError("Type must be CRF, CRT, or CRTAI")  # noqa: TRY003
    for current_country_code in countries_to_read:
        # get country name
        country_name = get_country_name(current_country_code)
        print(f"reading for country: {current_country_code}")
        # get specification and available tables
        # if we only have a single country check if we might have a country specific
        # specification (currently only Australia, 2023)
        if current_country_code is not None:
            try:
                crf_spec = getattr(
                    crf, f"{submission_type}{submission_year}_{current_country_code}"
                )
                print(
                    f"Using country specific specification: "
                    f"{submission_type}{submission_year}_{current_country_code}"
                )
            except Exception:
                # no country specific specification, check for general specification
                try:
                    crf_spec = getattr(crf, f"{submission_type}{submission_year}")
                except Exception as ex:
                    raise ValueError(  # noqa: TRY003
                        f"No terminology exists for submission year {submission_year}"
                    ) from ex
        else:
            try:
                crf_spec = getattr(crf, f"{submission_type}{submission_year}")
            except Exception as ex:
                raise ValueError(  # noqa: TRY003
                    f"No terminology exists for {submission_type}{submission_year}"
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
            f"{submission_type}{submission_year} specification: {tables}"
        )
        print("#" * 80)

        try:
            if submission_type == "CRF":
                date_or_version = get_latest_date_for_country(
                    current_country_code,
                    submission_year,
                    submission_type=submission_type,
                )
            else:
                date_or_version = get_latest_version_for_country(
                    current_country_code,
                    submission_round=submission_year,
                    submission_type=submission_type,
                )
        except Exception:
            message = (
                f"No submissions for country {country_name} ({current_country_code}), "
                f"{submission_type}{submission_year}"
            )
            print(message)
            exceptions.append(
                f"No_sub: {country_name} ({current_country_code}): {message}"
            )
            date_or_version = None
            pass

        if date_or_version is not None:
            for table in tables:
                try:
                    # read table for given years
                    (
                        ds_table,
                        new_unknown_categories,
                        new_last_row_info,
                        not_present,
                    ) = read_crf_table(
                        current_country_code,
                        table,
                        submission_year,
                        date_or_version=date_or_version,
                        data_year=[data_year],
                        debug=True,
                        submission_type=submission_type,
                    )

                    # collect messages on unknown rows etc
                    unknown_categories = unknown_categories + new_unknown_categories
                    last_row_info = last_row_info + new_last_row_info

                except Exception as e:
                    message = (
                        f"Error occurred when converting table {table} for"
                        f" {country_name} to PRIMAP2 IF. Exception: {e}"
                    )
                    print(message)
                    exceptions.append(f"Error: {country_name}: {message}")
                    ds_table = None
                    not_present = None
                    pass

                try:
                    if ds_table is not None:
                        # convert to PRIMAP2 IF
                        # first drop the orig_cat_name col as it can have multiple
                        # values for one category
                        ds_table = ds_table.drop(columns=["orig_cat_name"])

                        # TODO: catch entity conversion errors and make list of error
                        #  entities
                        # if we need to map entities pass this info to the conversion
                        # function
                        if "entity_mapping" in crf_spec[table]:
                            entity_mapping = crf_spec[table]["entity_mapping"]
                        else:
                            entity_mapping = None

                        if "decimal_sep" in crf_spec[table]["table"]:
                            decimal_sep = crf_spec[table]["table"]["decimal_sep"]
                        else:
                            decimal_sep = "."
                        if "thousands_sep" in crf_spec[table]["table"]:
                            thousands_sep = crf_spec[table]["table"]["thousands_sep"]
                        else:
                            thousands_sep = ","

                        ds_table_if = convert_crf_table_to_pm2if(
                            ds_table,
                            submission_year,
                            meta_data_input={
                                "title": f"Data submitted in {submission_year} to the "
                                f"UNFCCC in the {type_name} ({submission_type}) "
                                f"by {country_name}. "
                                f"Submission date / version: {date_or_version}"
                            },
                            entity_mapping=entity_mapping,
                            submission_type=submission_type,
                            decimal_sep=decimal_sep,
                            thousands_sep=thousands_sep,
                        )

                        # skip empty tables
                        if (
                            not ds_table_if.set_index(
                                ds_table_if.attrs["dimensions"]["*"]
                            )
                            .isna()
                            .all(axis=None)
                        ):
                            # now convert to native PRIMAP2 format
                            ds_table_pm2 = pm2.pm2io.from_interchange_format(
                                ds_table_if
                            )

                            # if individual data for emissions and removals /
                            # recovery exist combine them
                            if (
                                ("CO2 removals" in ds_table_pm2.data_vars)
                                and ("CO2 emissions" in ds_table_pm2.data_vars)
                                and "CO2" not in ds_table_pm2.data_vars
                            ):
                                # we can just sum to CO2 as we made sure that it doesn't
                                # exist.
                                # If we have CO2 and removals but not emissions,
                                # CO2 already
                                # has removals subtracted and we do nothing here
                                ds_table_pm2["CO2"] = ds_table_pm2[
                                    ["CO2 emissions", "CO2 removals"]
                                ].pr.sum(dim="entity", skipna=True, min_count=1)
                                ds_table_pm2["CO2"].attrs["entity"] = "CO2"

                            if (
                                ("CH4 removals" in ds_table_pm2.data_vars)
                                and ("CH4 emissions" in ds_table_pm2.data_vars)
                                and "CH4" not in ds_table_pm2.data_vars
                            ):
                                # we can just sum to CH4 as we made sure that it doesn't
                                # exist.
                                # If we have CH4 and removals but not emissions, CH4
                                # already has removals subtracted and we do nothing here
                                ds_table_pm2["CH4"] = ds_table_pm2[
                                    ["CH4 emissions", "CH4 removals"]
                                ].pr.sum(dim="entity", skipna=True, min_count=1)
                                ds_table_pm2["CH4"].attrs["entity"] = "CH4"

                            # combine per table DS
                            if ds_all is None:
                                ds_all = ds_table_pm2
                            else:
                                ds_all = ds_all.combine_first(ds_table_pm2)
                        else:
                            empty_tables.append(
                                [table, current_country_code, data_year]
                            )
                    elif not_present:
                        # log that table is not present
                        missing_worksheets.append(
                            [table, current_country_code, data_year]
                        )
                    else:
                        print(
                            f"Empty DataFrame returned for table {table}, "
                            f"country {country_code}. Check log for errors."
                        )
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
    output_folder = log_path / f"test_read_{submission_type}{submission_year}"
    if not output_folder.exists():
        output_folder.mkdir()
    if len(unknown_categories) > 0:
        if country_code is not None:
            log_location = (
                output_folder / f"{data_year}_unknown_categories_{country_code}"
                f"_{today.strftime('%Y-%m-%d')}.csv"
            )
        else:
            log_location = (
                output_folder / f"{data_year}_unknown_categories_"
                f"{today.strftime('%Y-%m-%d')}.csv"
            )
        print(f"Unknown rows found. Savin log to {log_location}")
        save_unknown_categories_info(unknown_categories, log_location)

    if len(last_row_info) > 0:
        if country_code is not None:
            log_location = (
                output_folder / f"{data_year}_last_row_info_{country_code}_"
                f"{today.strftime('%Y-%m-%d')}.csv"
            )
        else:
            log_location = (
                output_folder / f"{data_year}_last_row_info_"
                f"{today.strftime('%Y-%m-%d')}.csv"
            )
        print(f"Data found in the last row. Saving log to {log_location}")
        save_last_row_info(last_row_info, log_location)

    if len(empty_tables) > 0:
        today = date.today()
        if country_code is not None:
            log_location = (
                output_folder / f"{data_year}_empty_tables_{country_code}_"
                f"{today.strftime('%Y-%m-%d')}.csv"
            )
        else:
            log_location = (
                output_folder / f"{data_year}_empty_tables_"
                f"{today.strftime('%Y-%m-%d')}.csv"
            )
        print(f"Empty tables found:. Save log to {log_location}")
        save_empty_tables_info(empty_tables, log_location)

    if len(missing_worksheets) > 0:
        today = date.today()
        if country_code is not None:
            log_location = (
                output_folder / f"{data_year}_missing_tables_{country_code}_"
                f"{today.strftime('%Y-%m-%d')}.csv"
            )
        else:
            log_location = (
                output_folder / f"{data_year}_missing_tables_"
                f"{today.strftime('%Y-%m-%d')}.csv"
            )
        print(f"Missing worksheets. Save log to {log_location}")
        save_empty_tables_info(missing_worksheets, log_location)

    # write exceptions
    f_ex = open(
        output_folder / f"{data_year}_exceptions_{today.strftime('%Y-%m-%d')}.txt", "w"
    )
    for ex in exceptions:
        f_ex.write(f"{ex}\n")
    f_ex.close()

    # save the data:
    print(f"Save dataset to log folder: {log_path}")
    compression = dict(zlib=True, complevel=9)

    if country_code is not None:
        output_filename = (
            f"{submission_type}{submission_year}_{country_code}_"
            f"{today.strftime('%Y-%m-%d')}"
        )
    else:
        output_filename = (
            f"{submission_type}{submission_year}_{today.strftime('%Y-%m-%d')}"
        )
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


def save_unknown_categories_info(
    unknown_categories: list[list],
    file: Path,
) -> None:
    """
    Save information on unknown categories to a csv file.

    Parameters
    ----------
    unknown_categories: List[List]
        List of lists with information on the unknown categories.
        (which table, country and year, and which categories)

    file: pathlib.Path
        File including path where the data should be stored

    """
    # process unknown categories
    df_unknown_cats = pd.DataFrame(
        unknown_categories, columns=["Table", "Country", "Category", "Year", "index"]
    )

    processed_cats = []
    all_tables = df_unknown_cats["Table"].unique()
    all_years = set(df_unknown_cats["Year"].unique())
    all_years = set([year for year in all_years if isinstance(year, int)])
    all_years = set([year for year in all_years if int(year) > 1989])  # noqa: PLR2004
    for table in all_tables:
        df_cats_current_table = df_unknown_cats[df_unknown_cats["Table"] == table]
        cats_current_table = list(df_cats_current_table["Category"].unique())
        for cat in cats_current_table:
            df_current_cat_table = df_cats_current_table[
                df_cats_current_table["Category"] == cat
            ]
            all_countries = df_current_cat_table["Country"].unique()
            countries_cat = ""
            for country in all_countries:
                years_country = df_current_cat_table[
                    df_current_cat_table["Country"] == country
                ]["Year"].unique()
                idx_country = df_current_cat_table[
                    df_current_cat_table["Country"] == country
                ]["index"].unique()
                if set(years_country) == all_years:
                    countries_cat = f"{countries_cat}; {country} ({idx_country})"
                else:
                    countries_cat = (
                        f"{countries_cat}; {country} ({years_country}) ({idx_country})"
                    )
            processed_cats.append([table, cat, countries_cat])

    if not file.parents[1].exists():
        file.parents[1].mkdir()
    if not file.parents[0].exists():
        file.parents[0].mkdir()
    df_processed_cats = pd.DataFrame(
        processed_cats, columns=["Table", "Category", "Countries"]
    )
    df_processed_cats.to_csv(file, index=False)


def save_last_row_info(
    last_row_info: list[list],
    file: Path,
) -> None:
    """
    Save information on data found in the last row read for a table.

    The last row read should not contain data. If it does contain data
    it is a hint that table size is larger for some countries than
    given in the specification and thus we might not read the full table.

    Parameters
    ----------
    last_row_info: List[List]
        List of lists with information on the unknown categories.
        (which table, country and year, and which categories)

    file: pathlib.Path
        File including path where the data should be stored

    """
    # process last row with information messages
    df_last_row_info = pd.DataFrame(
        last_row_info, columns=["Table", "Country", "Category", "Year"]
    )

    processed_last_row_info = []
    all_tables = df_last_row_info["Table"].unique()
    all_years = set(df_last_row_info["Year"].unique())
    all_years = set([year for year in all_years if isinstance(year, int)])
    all_years = set([year for year in all_years if year > 1989])  # noqa: PLR2004
    for table in all_tables:
        df_last_row_current_table = df_last_row_info[df_last_row_info["Table"] == table]
        all_countries = df_last_row_current_table["Country"].unique()
        for country in all_countries:
            df_current_country_table = df_last_row_current_table[
                df_last_row_current_table["Country"] == country
            ]
            all_categories = df_current_country_table["Category"].unique()
            cats_country = ""
            for cat in all_categories:
                years_category = df_current_country_table[
                    df_current_country_table["Category"] == cat
                ]["Year"].unique()
                if set(years_category) == all_years:
                    cats_country = f"{cats_country}; {cat}"
                else:
                    cats_country = f"{cats_country}; {cat} ({years_category})"
            processed_last_row_info.append([table, country, cats_country])

    if not file.parents[1].exists():
        file.parents[1].mkdir()
    if not file.parents[0].exists():
        file.parents[0].mkdir()
    df_processed_lost_row_info = pd.DataFrame(
        processed_last_row_info, columns=["Table", "Country", "Categories"]
    )
    df_processed_lost_row_info.to_csv(file, index=False)


def save_empty_tables_info(
    empty_tables: list[list],
    file: Path,
) -> None:
    """
    Save information on empty tables to a csv file.

    Parameters
    ----------
    empty_tables: List[List]
        List of lists with information on the empty tables.
        (which table, country and year)

    file: pathlib.Path
        File including path where the data should be stored

    """
    # process unknown categories
    df_empty_tables = pd.DataFrame(empty_tables, columns=["Table", "Country", "Year"])

    processed_tables = []
    all_tables = df_empty_tables["Table"].unique()
    all_years = set(df_empty_tables["Year"].unique())
    all_years = set([year for year in all_years if isinstance(year, int)])
    all_years = set([year for year in all_years if int(year) > 1989])  # noqa: PLR2004
    for table in all_tables:
        df_current_table = df_empty_tables[df_empty_tables["Table"] == table]
        all_countries = df_current_table["Country"].unique()
        countries_table = ""
        for country in all_countries:
            years_country = df_current_table[df_current_table["Country"] == country][
                "Year"
            ].unique()
            if set(years_country) == all_years:
                countries_table = f"{countries_table}; {country}"
            else:
                countries_table = f"{countries_table}; {country} ({years_country})"
        processed_tables.append([table, countries_table])

    if not file.parents[1].exists():
        file.parents[1].mkdir()
    if not file.parents[0].exists():
        file.parents[0].mkdir()
    df_processed_tables = pd.DataFrame(processed_tables, columns=["Table", "Countries"])
    df_processed_tables.to_csv(file, index=False)
