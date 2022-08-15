"""
This script is a wrapper around the read_crf_for_country
function such that it can be called from datalad
"""

import argparse
import sys
from datetime import date
from util import code_path
#from UNFCCC_CRF_reader import custom_country_mapping
sys.path.append(code_path.name)
from UNFCCC_DI_reader_core import read_UNFCCC_DI_for_party
from UNFCCC_DI_reader_core import determine_filename
from util import custom_country_mapping
from util import get_country_name
from util import get_country_code

#from pathlib import Path

suffixes = ["nc", "yaml", "csv"]

parser = argparse.ArgumentParser()
parser.add_argument('--country', help='Country name or code')
args = parser.parse_args()

country = args.country

#country_info = {}
if country in custom_country_mapping:
    country_code = country
else:
    country_code = get_country_code(country)
# now get the country name
country_name = get_country_name(country_code)
#country_info["code"] = country_code
#country_info["name"] = country_name

# get current date to pass on to other functions in case reading is done over night
# and the date changes
date_str = str(date.today())


# TODO: this function: get output files and run datalad.
# problem: the data. should be the same in file name and scenario but is determined
# at two different places and might differ when running over night.  so it should be
# a parameter determined in this function and passed on to the datalad function / script

print(f"Attempting to read DI data for {country}.")
print("#"*80)
print("")
print(f"Using the UNFCCC_CRF_reader")
print("")

# determine output files
filename_base = determine_filename(country_code, date_str)

# we have no input files as data is read from DI API

read_UNFCCC_DI_for_party(
    party_code=country_code,
    category_groups=None, # read all categories
    read_subsectors=False, # not applicable as we read all categories
    date_str=date_str,
    pm2if_specifications=None, # automatically use the right specs for AI and NAI
    default_gwp=None, # automatically uses right default GWP for AI and NAI
    debug=False,
)



#    print(f"Run the script using datalad run via the python api")
#    script = code_path / "UNFCCC_CRF_reader" / "read_UNFCCC_CRF_submission.py"
#
#     cmd = f"./venv/bin/python3 {script.as_posix()} --country={country} "\
#           f"--submission_year={submission_year} --submission_date={submission_date}"
#     if re_read:
#         cmd = cmd + f" --re_read"
#     datalad.api.run(
#         cmd=cmd,
#         dataset=root_path,
#         message=f"Read data for {country}, CRF{submission_year}, {submission_date}.",
#         inputs=country_info["input"],
#         outputs=country_info["output"],
#         dry_run=None,
#         explicit=True,
#     )




################################3






# country = args.country
# submission = args.submission
#
# codepath = Path(__file__).parent
# rootpath = codepath / ".." / ".."
# rootpath = rootpath.resolve()
#
# if script_name is not None:
#     print(f"Found code file {script_name}")
#     print("")
#
#     # get possible input files
#     input_files = get_possible_inputs(country, submission)
#     if not input_files:
#         print(f"No possible input files found for {country}, {submission}. "
#               f"Something might be wrong here.")
#     else:
#         print(f"Found the following input_files:")
#         for file in input_files:
#             print(file)
#         print("")
#     # make input files absolute to avoid datalad confusions when
#     # root directory is via symlink
#     input_files = [rootpath / file for file in input_files]
#     # convert file's path to str
#     input_files = [file.as_posix() for file in input_files]
#
#     # get possible output files
#     output_files = get_possible_outputs(country, submission)
#     if not output_files:
#         print(f"No possible output files found for {country}, {submission}. "
#               f"This is either the first run or something is wrong.")
#     else:
#         print(f"Found the following output_files:")
#         for file in output_files:
#             print(file)
#         print("")
#     # convert file path's to str
#     output_files = [file.as_posix() for file in output_files]
#
#     print(f"Run the script using datalad run via the python api")
#     datalad.api.run(
#         cmd=f"./venv/bin/python3 {script_name.as_posix()}",
#         dataset=rootpath,
#         message=f"Read data for {country}, {submission}.",
#         inputs=input_files,
#         outputs=output_files,
#         dry_run=None,
#         explicit=True,
#     )
# else:
#     # no code found.
#     print(f"No code found to read {submission} from {country}")
#     print(f"Use 'doit country_info --country={country} to get "
#           f"a list of available submissions and datasets.")