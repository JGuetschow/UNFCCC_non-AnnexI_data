"""
A script to collect all latest CRF submissions for a given year

Reads the latest data from the extracted data folder for each country.
Notifies the user if new data are available in the downloaded_data folder
which have not yet been read.

Data are saved in the datasets/UNFCCC/CRFYYYY/CRTX folder.

TODO: sort importing and move to datasets folder
TODO: add datalad get to obtain the input files
"""

import argparse
from datetime import date
from pathlib import Path

import datalad.api
import primap2 as pm2

from unfccc_ghg_data.helper import all_countries, dataset_path_UNFCCC
from unfccc_ghg_data.unfccc_crf_reader.unfccc_crf_reader_prod import (
    get_input_and_output_files_for_country,
    submission_has_been_read,
)
from unfccc_ghg_data.unfccc_crf_reader.util import all_crf_countries

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--submission_year", help="Submission round to read", type=int)
    parser.add_argument("--type", help="CRF or CRT tables", default="CRF")
    args = parser.parse_args()
    submission_year = args.submission_year
    submission_type = args.type

    if submission_type == "CRF":
        countries = all_crf_countries
    elif submission_type == "CRT":
        countries = all_countries
    else:
        raise ValueError("Type must be CRF or CRT")  # noqa: TRY003

    ds_all_CRF = None
    outdated_countries = []
    included_countries = []

    for country in countries:
        # determine folder
        try:
            country_info = get_input_and_output_files_for_country(
                country,
                submission_year=submission_year,
                submission_type=submission_type,
                verbose=False,
            )

            if submission_type == "CRF":
                date_or_version = country_info["date"]
            else:
                date_or_version = country_info["version"]
            # check if the latest submission has been read already
            data_read = submission_has_been_read(
                country_info["code"],
                country_info["name"],
                submission_year=submission_year,
                date_or_version=date_or_version,
                submission_type=submission_type,
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
    output_folder = dataset_path_UNFCCC / f"{submission_type}{submission_year}"
    output_filename = (
        f"{submission_type}{submission_year}_raw_{today.strftime('%Y-%m-%d')}"
    )

    if not output_folder.exists():
        output_folder.mkdir()

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
