# this script takes submission and country as input (from doit) and
# runs the appropriate script to extract the submission data

import argparse

import datalad.api
from get_submissions_info import get_possible_inputs, get_possible_outputs

from unfccc_ghg_data.helper import get_code_file, root_path

# Find the right function and possible input and output files and
# read the data using datalad run.
parser = argparse.ArgumentParser()
parser.add_argument('--country', help='Country name or code')
parser.add_argument('--submission', help='Submission to read')

args = parser.parse_args()

country = args.country
submission = args.submission


print(f"Attempting to extract data for {submission} from {country}.")
print("#"*80)
print("")

# get the correct script
script_name = get_code_file(country, submission)

if script_name is not None:
    print(f"Found code file {script_name}")
    print("")

    # get possible input files
    input_files = get_possible_inputs(country, submission)
    if not input_files:
        print(f"No possible input files found for {country}, {submission}. "
              f"Something might be wrong here.")
    else:
        print("Found the following input_files:")
        for file in input_files:
            print(file)
        print("")
    # make input files absolute to avoid datalad confusions when
    # root directory is via symlink
    input_files = [root_path / file for file in input_files]
    # convert file's path to str
    input_files = [file.as_posix() for file in input_files]

    # get possible output files
    output_files = get_possible_outputs(country, submission)
    if not output_files:
        print(f"No possible output files found for {country}, {submission}. "
              f"This is either the first run or something is wrong.")
    else:
        print("Found the following output_files:")
        for file in output_files:
            print(file)
        print("")
    # convert file path's to str
    output_files = [file.as_posix() for file in output_files]

    print("Run the script using datalad run via the python api")
    datalad.api.run(
        cmd=f"./venv/bin/python3 {script_name.as_posix()}",
        dataset=root_path,
        message=f"Read data for {country}, {submission}.",
        inputs=input_files,
        outputs=output_files,
        dry_run=None,
        explicit=True,
    )
else:
    # no code found.
    print(f"No code found to read {submission} from {country}")
    print(f"Use 'doit country_info country={country} to get "
          f"a list of available submissions and datasets.")

