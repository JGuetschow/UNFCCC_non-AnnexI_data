""" create mapping of folder to countries

this script takes a folder as input (from doit) and
runs creates the mapping of subfolders to country codes
for that folder
"""

import argparse

from unfccc_ghg_data.helper import create_folder_mapping

if __name__ == "__main__":
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
