# this script takes a folder as input (from doit) and
# runs creates the mapping of subfolders to country codes
# oir that folder

import argparse
from get_submissions_info import create_folder_mapping

# Find the right function and possible input and output files and
# read the data using datalad run.
parser = argparse.ArgumentParser()
parser.add_argument('--folder', help='folder name, relative to '
                                     'repository root folder')
args = parser.parse_args()
folder = args.folder

if 'extracted_data' in folder:
    extracted = True
else:
    extracted = False

# print available submissions
print("="*10 + f" Creating folder mapping for  {folder} " + "="*10)
create_folder_mapping(folder, extracted)
