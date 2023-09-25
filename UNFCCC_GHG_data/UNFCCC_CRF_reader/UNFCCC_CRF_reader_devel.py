"""
This file holds functions that are used in CRF reading development like
adding new tables or new submission years (and according country specific
categories). Thue functions are tailored towards debug output and reading
of single years in contrast to the production functions which are tailored
towards the creation of full datasets including storage in the
"""

import pandas as pd
import xarray as xr
import primap2 as pm2
from typing import List, Optional
from pathlib import Path
from datetime import date

from .util import all_crf_countries
from UNFCCC_GHG_data.helper import log_path, get_country_name
from . import crf_specifications as crf
from .UNFCCC_CRF_reader_core import get_latest_date_for_country, read_crf_table
from .UNFCCC_CRF_reader_core import convert_crf_table_to_pm2if

def read_year_to_test_specs(
        submission_year: int,
        data_year: Optional[int]=None,
        totest: Optional[bool]=False,
        country_code: Optional=None,
) -> xr.Dataset:
    """
    Read one xlsx file (so one data year) for each country for a submission year to
    create log files and extend the specifications

    totest: if true only read tables with "totest" status

    """
    if data_year is None:
        data_year=2000

    unknown_categories = []
    last_row_info = []
    ds_all = None
    print(f"CRF test reading for CRF{submission_year}. Using data year {data_year}")
    if totest:
        print("Reading only tables to test.")
    print("#"*80)


    # get specification
    # if we only have a single country check if we might have a country specific
    # specification (currently only Australia, 2023)
    if country_code is not None:
        try:
            crf_spec = getattr(crf, f"CRF{submission_year}_{country_code}")
            print(
                f"Using country specific specification: "
                f"CRF{submission_year}_{country_code}"
            )
        except:
            # no country specific specification, check for general specification
            try:
                crf_spec = getattr(crf, f"CRF{submission_year}")
            except:
                raise ValueError(
                    f"No terminology exists for submission year " f"{submission_year}"
                )
    else:
        try:
            crf_spec = getattr(crf, f"CRF{submission_year}")
        except:
            raise ValueError(
                f"No terminology exists for submission year " f"{submission_year}"
            )

    if totest:
        tables = [table for table in crf_spec.keys()
                  if crf_spec[table]["status"] == "totest"]
    else:
        tables = [table for table in crf_spec.keys()
                  if crf_spec[table]["status"] == "tested"]
    print(f"The following tables are available in the " \
          f"CRF{submission_year} specification: {tables}")
    print("#" * 80)

    if country_code is not None:
        countries_to_read = [country_code]
    else:
        countries_to_read = all_crf_countries
    for country_code in countries_to_read:
        # get country name
        country_name = get_country_name(country_code)
        print(f"Reading for {country_name}")
        # get specification and available tables

        try:
            submission_date = get_latest_date_for_country(country_code, submission_year)
        except:
            print(f"No submissions for country {country_name}, CRF{submission_year}")
            submission_date = None

        if submission_date is not None:
            for table in tables:
                # read table for all years
                ds_table, new_unknown_categories, new_last_row_info = read_crf_table(
                    country_code, table, submission_year, date=submission_date,
                    data_year=[data_year], debug=True)

                # collect messages on unknown rows etc
                unknown_categories = unknown_categories + new_unknown_categories
                last_row_info = last_row_info + new_last_row_info

                # convert to PRIMAP2 IF
                # first drop the orig_cat_name col as it can have multiple values for
                # one category
                ds_table = ds_table.drop(columns=["orig_cat_name"])

                # TODO: catch entity conversion errors and make list of error entities
                # if we need to map entities pass this info to the conversion function
                if "entity_mapping" in crf_spec[table]:
                    entity_mapping = crf_spec[table]["entity_mapping"]
                else:
                    entity_mapping = None
                try:
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

                    # if individual data for emissions and removals / recovery exist combine
                    # them
                    if (('CO2 removals' in ds_table_pm2.data_vars) and
                            ('CO2 emissions' in ds_table_pm2.data_vars) and not
                            ('CO2' in ds_table_pm2.data_vars)):
                        # we can just sum to CO2 as we made sure that it doesn't exist.
                        # If we have CO2 and removals but not emissions, CO2 already has
                        # removals subtracted and we do nothing here
                        ds_table_pm2["CO2"] = ds_table_pm2[["CO2 emissions",
                                                            "CO2 removals"]].pr.sum(
                            dim="entity", skipna=True, min_count=1
                        )
                        ds_table_pm2["CO2"].attrs["entity"] = "CO2"

                    if (('CH4 removals' in ds_table_pm2.data_vars) and
                            ('CH4 emissions' in ds_table_pm2.data_vars) and not
                            ('CH4' in ds_table_pm2.data_vars)):
                        # we can just sum to CH4 as we made sure that it doesn't exist.
                        # If we have CH4 and removals but not emissions, CH4 already has
                        # removals subtracted and we do nothing here
                        ds_table_pm2["CH4"] = ds_table_pm2[["CH4 emissions",
                                                            "CH4 removals"]].pr.sum(
                            dim="entity", skipna=True, min_count=1
                        )
                        ds_table_pm2["CH4"].attrs["entity"] = "CH4"

                    # combine per table DS
                    if ds_all is None:
                        ds_all = ds_table_pm2
                    else:
                        ds_all = ds_all.combine_first(ds_table_pm2)
                except Exception as e:
                    print(f"Error occured when converting table {table} for"
                          f" {country_name} to PRIMAP2 IF. Exception: {e}")
                    # TODO: error handling and logging

    # process log messages.
    today = date.today()
    if len(unknown_categories) > 0:
        if country_code is not None:
            log_location = (
                log_path
                / f"CRF{submission_year}"
                / f"{data_year}_unknown_categories_{country_code}"
                  f"_{today.strftime('%Y-%m-%d')}.csv"
            )
        else:
            log_location = (log_path / f"CRF{submission_year}"
                            / f"{data_year}_unknown_categories_"
                              f"{today.strftime('%Y-%m-%d')}.csv")
        print(f"Unknown rows found. Savin log to {log_location}")
        save_unknown_categories_info(unknown_categories, log_location)

    if len(last_row_info) > 0:
        if country_code is not None:
            log_location = (
               log_path
               / f"CRF{submission_year}"
               / f"{data_year}_last_row_info_{country_code}_"
                 f"{today.strftime('%Y-%m-%d')}.csv"
           )
        else:
            log_location = (log_path / f"CRF{submission_year}"
                            / f"{data_year}_last_row_info_"
                              f"{today.strftime('%Y-%m-%d')}.csv")
        print(f"Data found in the last row. Saving log to "
              f"{log_location}")
        save_last_row_info(last_row_info, log_location)

    # save the data:
    compression = dict(zlib=True, complevel=9)
    output_folder = log_path / f"test_read_CRF{submission_year}"
    if country_code is not None:
        output_filename = (f"CRF{submission_year}_{country_code}_"
                           f"{today.strftime('%Y-%m-%d')}")
    else:
        output_filename = f"CRF{submission_year}_{today.strftime('%Y-%m-%d')}"
    if totest:
        output_filename = output_filename + "_totest"

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


def save_unknown_categories_info(
        unknown_categories: List[List],
        file: Path,
) -> None:
    """
    Save information on unknown categories to a csv file.

    Parameters
    __________

    unknown_categories: List[List]
        List of lists with information on the unknown categories.
        (which table, country and year, and which categories)

    file: pathlib.Path
        File including path where the data should be stored

    """
    # process unknown categories
    df_unknown_cats = pd.DataFrame(unknown_categories, columns=["Table", "Country", "Category", "Year"])

    processed_cats = []
    all_tables = df_unknown_cats["Table"].unique()
    all_years = set(df_unknown_cats["Year"].unique())
    all_years = set([year for year in all_years if isinstance(year, int)])
    all_years = set([year for year in all_years if int(year) > 1989])
    for table in all_tables:
        df_cats_current_table = df_unknown_cats[df_unknown_cats["Table"] == table]
        cats_current_table = list(df_cats_current_table["Category"].unique())
        for cat in cats_current_table:
            df_current_cat_table = df_cats_current_table[df_cats_current_table["Category"] == cat]
            all_countries = df_current_cat_table["Country"].unique()
            countries_cat = ""
            for country in all_countries:
                years_country = df_current_cat_table[df_current_cat_table["Country"] == country]["Year"].unique()
                if set(years_country) == all_years:
                    countries_cat = f"{countries_cat}; {country}"
                else:
                    countries_cat = f"{countries_cat}; {country} ({years_country})"
            processed_cats.append([table, cat, countries_cat])


    if not file.parents[1].exists():
        file.parents[1].mkdir()
    if not file.parents[0].exists():
        file.parents[0].mkdir()
    df_processed_cats = pd.DataFrame(processed_cats, columns=["Table", "Category", "Countries"])
    df_processed_cats.to_csv(file, index=False)


def save_last_row_info(
        last_row_info: List[List],
        file: Path,
    ) -> None:
    """
    Save information on data found in the last row read for a table.
    The last row read should not contain data. If it does contain data
    it is a hint that table size is larger for some countries than
    given in the specification and thus we might not read the full table.

    Parameters
    __________

    last_row_info: List[List]
        List of lists with information on the unknown categories.
        (which table, country and year, and which categories)

    file: pathlib.Path
        File including path where the data should be stored

    """
    # process last row with information messages
    df_last_row_info = pd.DataFrame(last_row_info, columns=["Table", "Country", "Category", "Year"])

    processed_last_row_info = []
    all_tables = df_last_row_info["Table"].unique()
    all_years = set(df_last_row_info["Year"].unique())
    all_years = set([year for year in all_years if isinstance(year, int)])
    all_years = set([year for year in all_years if year > 1989])
    for table in all_tables:
        df_last_row_current_table = df_last_row_info[df_last_row_info["Table"] == table]
        all_countries = df_last_row_current_table["Country"].unique()
        for country in all_countries:
            df_current_country_table = df_last_row_current_table[df_last_row_current_table["Country"] == country]
            all_categories = df_current_country_table["Category"].unique()
            cats_country = ""
            for cat in all_categories:
                years_category = df_current_country_table[df_current_country_table["Category"] == cat]["Year"].unique()
                if set(years_category) == all_years:
                    cats_country = f"{cats_country}; {cat}"
                else:
                    cats_country = f"{cats_country}; {cat} ({years_category})"
            processed_last_row_info.append([table, country, cats_country])

    if not file.parents[1].exists():
        file.parents[1].mkdir()
    if not file.parents[0].exists():
        file.parents[0].mkdir()
    df_processed_lost_row_info = pd.DataFrame(processed_last_row_info, columns=["Table", "Country", "Categories"])
    df_processed_lost_row_info.to_csv("test_last_row_info.csv", index=False)