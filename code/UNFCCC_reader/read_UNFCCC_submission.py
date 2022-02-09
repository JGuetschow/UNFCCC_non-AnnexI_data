# this script takes submission and country as input (from make) and
# runs the appropriate script to extract the submission data

import sys
import datalad.api
from pathlib import Path
from get_submissions_info import get_code_file
from get_submissions_info import get_possible_inputs
from get_submissions_info import get_possible_outputs


if len(sys.argv) > 3:
    raise TypeError('Too many arguments given. '
                    'Need exactly two arguments (country, submission)')
elif len(sys.argv) < 3:
    raise TypeError('Too few arguments given. '
                    'Need exactly two arguments (country, submission)')

country = sys.argv[1]
submission = sys.argv[2]

codepath = Path(__file__).parent
rootpath = codepath / ".." / ".."
rootpath = rootpath.resolve()

print(f"Attempting to extract data for {submission} from {country}.")
print("#"*80)
print("")

# get the correct script
script_name = get_code_file(country, submission)
if script_name:
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
    # convert file path's to str
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
        dry_run='basic'
    )
else:
    # no code found.
    print(f"No code found to read {submission} from {country}")
    # TODO write info on available submissions and data

