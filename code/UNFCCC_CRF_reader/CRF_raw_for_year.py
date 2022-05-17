"""
This script collects all latest CRF submissions for a given year

Currently it only checks the extracted_data folder and not if new
submission are available in the downloaded data folder.
"""

# TODO: sort importing and move to datasets folder
# TODO: integrate into doit

import argparse
import sys
import primap2 as pm2
from pathlib import Path
from datetime import date

root_path = Path(__file__).parents[2].absolute()
root_path = root_path.resolve()
#log_path = root_path / "log"
code_path = root_path / "code"
downloaded_data_path = root_path / "downloaded_data" / "UNFCCC"
extracted_data_path = root_path / "extracted_data" / "UNFCCC"
dataset_path = root_path / "datasets" / "UNFCCC"

#sys.path.append(code_path.name)

from util import all_crf_countries
from UNFCCC_CRF_reader_prod import get_input_and_output_files_for_country
from UNFCCC_CRF_reader_prod import submission_has_been_read

parser = argparse.ArgumentParser()
parser.add_argument('--submission_year', help='Submission round to read', type=int)
args = parser.parse_args()
submission_year = args.submission_year

ds_all_CRF = None
outdated_countries = []
included_countries = []

for country in all_crf_countries:
    # determine folder
    try:
        country_info = get_input_and_output_files_for_country(
            country, submission_year=submission_year, verbose=False)

        # check if the latest submission has been read already

        data_read = submission_has_been_read(
            country_info["code"], country_info["name"],
            submission_year=submission_year,
            submission_date=country_info["date"],
            verbose=False,
        )
        if not data_read:
            print(f"Latest submission for {country} has not been read yet.")
            # TODO: make sure an older submission is read if present. currently none is included at all
            outdated_countries.append(country)

        # read the native format file
        #print(country_info["output"])
        input_files = [file for file in country_info["output"] if Path(file).suffix == ".nc"]

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
output_folder = dataset_path / f"CRF{submission_year}"
output_filename = f"CRF{submission_year}_raw_{today.strftime('%Y-%m-%d')}"

if not output_folder.exists():
    output_folder.mkdir()

# write data in interchange format
pm2.pm2io.write_interchange_format(output_folder / output_filename,
                                   ds_all_CRF.pr.to_interchange_format())

# write data in native PRIMAP2 format
encoding = {var: compression for var in ds_all_CRF.data_vars}
ds_all_CRF.pr.to_netcdf(output_folder / (output_filename + ".nc"),
                      encoding=encoding)

# show info
print(f"The following countries are included in the dataset: {included_countries}")
print(f"The following countries have updated submission not yet read "
      f"and not included in the dataset: {outdated_countries}")