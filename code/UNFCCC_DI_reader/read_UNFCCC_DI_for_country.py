"""
This script is a wrapper around the read_crf_for_country
function such that it can be called from datalad
"""

from UNFCCC_DI_reader import read_UNFCCC_DI_for_party
from UNFCCC_DI_reader import determine_filename
import argparse
#from pathlib import Path

suffixes = ["nc", "yaml", "csv"]

parser = argparse.ArgumentParser()
parser.add_argument('--country', help='Country name or code')
args = parser.parse_args()

country = args.country

#TODO: get country name and code

# TODO: this function: get output files and run datalad.
# problem: the data. should be the same in file name and scenario but is determined
# at two different places and might differ when running over night.  so it should be
# a parameter determined in this function and passed on to the datalad function / script


print(f"Attempting to read DI data for {country}.")
print("#"*80)
print("")

# determine output files
filename_base = determine_filename(country)

# we have no input files as data is read from DI API




read_crf_for_country(
    country,
    submission_year=submission_year,
    submission_date=submission_date,
    re_read=re_read
)

#######################




country = args.country
submission = args.submission

codepath = Path(__file__).parent
rootpath = codepath / ".." / ".."
rootpath = rootpath.resolve()

if script_name is not None:
    print(f"Found code file {script_name}")
    print("")

    # get possible input files
    input_files = get_possible_inputs(country, submission)
    if not input_files:
        print(f"No possible input files found for {country}, {submission}. "
              f"Something might be wrong here.")
    else:
        print(f"Found the following input_files:")
        for file in input_files:
            print(file)
        print("")
    # make input files absolute to avoid datalad confusions when
    # root directory is via symlink
    input_files = [rootpath / file for file in input_files]
    # convert file's path to str
    input_files = [file.as_posix() for file in input_files]

    # get possible output files
    output_files = get_possible_outputs(country, submission)
    if not output_files:
        print(f"No possible output files found for {country}, {submission}. "
              f"This is either the first run or something is wrong.")
    else:
        print(f"Found the following output_files:")
        for file in output_files:
            print(file)
        print("")
    # convert file path's to str
    output_files = [file.as_posix() for file in output_files]

    print(f"Run the script using datalad run via the python api")
    datalad.api.run(
        cmd=f"./venv/bin/python3 {script_name.as_posix()}",
        dataset=rootpath,
        message=f"Read data for {country}, {submission}.",
        inputs=input_files,
        outputs=output_files,
        dry_run=None,
        explicit=True,
    )
else:
    # no code found.
    print(f"No code found to read {submission} from {country}")
    print(f"Use 'doit country_info --country={country} to get "
          f"a list of available submissions and datasets.")