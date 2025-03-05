"""
Script to test a new approach for handling sparse data.

A copy of the script to collect all latest CRF submissions for a given year

Reads the latest data from the extracted data folder for each country.
Notifies the user if new data are available in the downloaded_data folder
which have not yet been read.

Data are saved in the datasets/UNFCCC/CRFYYYY/CRTX folder.

"""


from datetime import date
from pathlib import Path

import datalad.api
import numpy as np
import pandas as pd
import primap2 as pm2
import sparse

from unfccc_ghg_data.helper import all_countries
from unfccc_ghg_data.unfccc_crf_reader.unfccc_crf_reader_prod import (
    get_input_and_output_files_for_country,
    submission_has_been_read,
)
from unfccc_ghg_data.unfccc_crf_reader.util import all_crf_countries


def crf_raw_for_year_original_version(
    submission_year: int,
    output_folder: Path,
    type: str = "CRF",
    n_countries: int = 5,
):
    """
    Collect all latest CRF submissions for a given year
    """
    if type == "CRF":
        countries = all_crf_countries
    elif type == "CRT":
        countries = all_countries
    else:
        raise ValueError("Type must be CRF or CRT")  # noqa: TRY003

    countries = countries[:n_countries]
    ds_all_CRF = None
    outdated_countries = []
    included_countries = []

    for country in countries:
        # determine folder
        try:
            country_info = get_input_and_output_files_for_country(
                country, submission_year=submission_year, type=type, verbose=False
            )

            # check if the latest submission has been read already

            data_read = submission_has_been_read(
                country_info["code"],
                country_info["name"],
                submission_year=submission_year,
                submission_date=country_info["date"],
                type=type,
                verbose=False,
            )
            if not data_read:
                print(f"Latest submission for {country} has not been read yet.")
                # TODO: make sure an older submission is read if present.
                #  currently none is included at all
                outdated_countries.append(country)

            # read the native format file
            # print(country_info["output"])
            input_files = [
                file for file in country_info["output"] if Path(file).suffix == ".nc"
            ]

            datalad.api.get(input_files)

            ds_country = pm2.open_dataset(input_files[0])

            # combine per table DS
            if ds_all_CRF is None:
                ds_all_CRF = ds_country
            else:
                ds_all_CRF = ds_all_CRF.combine_first(ds_country)

            included_countries.append(country)

        except Exception as ex:
            print(f"Exception {ex} occurred for {country}")

    # Update metadata
    # not necessary

    # write to disc
    today = date.today()

    compression = dict(zlib=True, complevel=9)

    # instead of saving to the output folder, we save to a temporary directory
    output_filename = f"{type}{submission_year}_raw_{today.strftime('%Y-%m-%d')}"

    # write data in interchange format
    pm2.pm2io.write_interchange_format(
        output_folder / output_filename, ds_all_CRF.pr.to_interchange_format()
    )

    # write data in native PRIMAP2 format
    encoding = {var: compression for var in ds_all_CRF.data_vars}
    ds_all_CRF.pr.to_netcdf(
        output_folder / (output_filename + ".nc"), encoding=encoding
    )

    # show info
    print(f"The following countries are included in the dataset: {included_countries}")
    print(
        f"The following countries have updated submission not yet read "
        f"and not included in the dataset: {outdated_countries}"
    )


def crf_raw_for_year_sparse_arrays(
    submission_year: int,
    output_folder: Path,
    type: str = "CRF",
    n_countries: int = 5,
):
    """
    Collect all latest CRF submissions for a given year using sparse arrays
    """
    if type == "CRF":
        countries = all_crf_countries
    elif type == "CRT":
        countries = all_countries
    else:
        raise ValueError("Type must be CRF or CRT")  # noqa: TRY003

    countries = countries[:n_countries]
    ds_all_CRF = None
    outdated_countries = []
    included_countries = []

    for country in countries:
        # determine folder
        try:
            country_info = get_input_and_output_files_for_country(
                country, submission_year=submission_year, type=type, verbose=False
            )

            # check if the latest submission has been read already

            data_read = submission_has_been_read(
                country_info["code"],
                country_info["name"],
                submission_year=submission_year,
                submission_date=country_info["date"],
                type=type,
                verbose=False,
            )
            if not data_read:
                print(f"Latest submission for {country} has not been read yet.")
                # TODO: make sure an older submission is read if present.
                #  currently none is included at all
                outdated_countries.append(country)

            # read the native format file
            # print(country_info["output"])
            input_files = [
                file for file in country_info["output"] if Path(file).suffix == ".nc"
            ]

            datalad.api.get(input_files)

            ds_country = pm2.open_dataset(input_files[0])

            ds_country_sparse = ds_country.copy()

            # I suspect this loop takes a lot of time
            for var in ds_country.data_vars:
                ds_country_sparse[var].data = sparse.COO.from_numpy(
                    ds_country_sparse[var].data, fill_value=np.nan
                )

            # combine per table DS
            if ds_all_CRF is None:
                ds_all_CRF = ds_country_sparse
            else:
                # TODO: This will fail for the latest xarray / sparse versions
                # There is a github issue for this: todo: add link
                ds_all_CRF = ds_all_CRF.merge(ds_country_sparse)
                # ds_all_CRF = ds_all_CRF.combine_first(ds_country_sparse)

            included_countries.append(country)

        except Exception as ex:
            print(f"Exception {ex} occurred for {country}")

    # convert back to dense arrays
    # TODO: some sources suggest we should use .to_numpy(), or .values instead of .data
    for var in ds_all_CRF.data_vars:
        ds_all_CRF[var].data = sparse.COO.todense(ds_all_CRF[var].data)

    # Update metadata
    # not necessary

    # write to disc
    today = date.today()

    compression = dict(zlib=True, complevel=9)

    # instead of saving to the output folder, we save to a temporary directory
    output_filename = f"{type}{submission_year}_raw_{today.strftime('%Y-%m-%d')}"

    # write data in interchange format
    pm2.pm2io.write_interchange_format(
        output_folder / output_filename, ds_all_CRF.pr.to_interchange_format()
    )

    # write data in native PRIMAP2 format
    encoding = {var: compression for var in ds_all_CRF.data_vars}
    ds_all_CRF.pr.to_netcdf(
        output_folder / (output_filename + ".nc"), encoding=encoding
    )

    # show info
    print(f"The following countries are included in the dataset: {included_countries}")
    print(
        f"The following countries have updated submission not yet read "
        f"and not included in the dataset: {outdated_countries}"
    )


def crf_raw_for_year_pandas(
    submission_year: int,
    output_folder: Path,
    type: str = "CRF",
    n_countries: int = 5,
):
    """
    Collect all latest CRF submissions for a given year using pandas
    """
    if type == "CRF":
        countries = all_crf_countries
    elif type == "CRT":
        countries = all_countries
    else:
        raise ValueError("Type must be CRF or CRT")  # noqa: TRY003

    countries = countries[:n_countries]
    ds_all_CRF_if = None
    outdated_countries = []
    included_countries = []

    for country in countries:
        # determine folder
        try:
            country_info = get_input_and_output_files_for_country(
                country, submission_year=submission_year, type=type, verbose=False
            )

            # check if the latest submission has been read already

            data_read = submission_has_been_read(
                country_info["code"],
                country_info["name"],
                submission_year=submission_year,
                submission_date=country_info["date"],
                type=type,
                verbose=False,
            )
            if not data_read:
                print(f"Latest submission for {country} has not been read yet.")
                # TODO: make sure an older submission is read if present.
                #  currently none is included at all
                outdated_countries.append(country)

            # read the native format file
            # print(country_info["output"])
            input_files = [
                file for file in country_info["output"] if Path(file).suffix == ".nc"
            ]

            datalad.api.get(input_files)

            ds_country = pm2.open_dataset(input_files[0])

            ds_country_if = ds_country.pr.to_interchange_format()

            # combine per table DS
            if ds_all_CRF_if is None:
                ds_all_CRF_if = ds_country_if
            else:
                ds_all_CRF_if = pd.concat(
                    [
                        ds_all_CRF_if,
                        ds_country_if,
                    ],
                    axis=0,
                    join="outer",
                ).reset_index(drop=True)

            included_countries.append(country)

        except Exception as ex:
            print(f"Exception {ex} occurred for {country}")

    # The attrs get lost when concatenating interchange format data sets

    all_dimensions = [str(dim) for dim in ds_country.dims] + ["entity", "unit"]
    ds_all_CRF_if.attrs = {
        "attrs": ds_country.attrs,
        "time_format": "%Y",
        "dimensions": {"*": all_dimensions},
    }

    # write to disc
    today = date.today()

    compression = dict(zlib=True, complevel=9)

    # instead of saving to the output folder, we save to a temporary directory
    output_filename = f"{type}{submission_year}_raw_{today.strftime('%Y-%m-%d')}"

    # write data in interchange format
    pm2.pm2io.write_interchange_format(output_folder / output_filename, ds_all_CRF_if)

    # write data in native PRIMAP2 format
    ds_all_CRF = pm2.pm2io.from_interchange_format(ds_all_CRF_if)
    encoding = {var: compression for var in ds_all_CRF.data_vars}
    ds_all_CRF.pr.to_netcdf(
        output_folder / (output_filename + ".nc"), encoding=encoding
    )

    # show info
    print(f"The following countries are included in the dataset: {included_countries}")
    print(
        f"The following countries have updated submission not yet read "
        f"and not included in the dataset: {outdated_countries}"
    )
