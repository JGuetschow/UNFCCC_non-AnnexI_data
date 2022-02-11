# define tasks for UNFCCC data repository
from doit import get_var

# TODO: task for folder mapping

# create virtual environment
def task_setup_venv():
    """Create virtual environment"""
    return {
        'file_dep': ['code/requirements.txt'],
        'actions': ['python3 -m venv venv',
                    './venv/bin/pip install --upgrade pip',
                    './venv/bin/pip install -Ur code/requirements.txt',
                    'touch venv',],
        'targets': ['venv'],
        'verbosity': 2,
    }


# Task to create the mapping files which map folder names to ISO 3-letter country codes
read_config_folder = {
    "folder": get_var('folder', None),
}

def task_map_folders():
    """
    Create or update the folder mapping in the given folder
    """
    return {
        'actions': [f"./venv/bin/python code/UNFCCC_reader/folder_mapping.py "
                    f"--folder={read_config_folder['folder']}"],
        'verbosity': 2,
        'setup': ['setup_venv'],
    }

# Tasks for getting submissions and downloading them
def task_update_bur():
    """ Update list of BUR submissions """
    return {
        'targets': ['downloaded_data/UNFCCC/submissions-bur.csv'],
        'actions': ['datalad run -m "Fetch BUR submissions" '
                    '-o downloaded_data/UNFCCC/submissions-bur.csv '
                    './venv/bin/python code/UNFCCC_downloader/fetch_submissions_bur.py'],
        'verbosity': 2,
        'setup': ['setup_venv'],
    }


def task_download_bur():
    """ Download BUR submissions """
    return {
        #'file_dep': ['downloaded_data/UNFCCC/submissions-bur.csv'],
        # deactivate file_dep fow now as it will always run fetch submissions
        # before download
        'actions': ['datalad run -m "Download BUR submissions" '
                    '-i downloaded_data/UNFCCC/submissions-bur.csv '
                    './venv/bin/python code/UNFCCC_downloader/download_bur.py'],
        'verbosity': 2,
        'setup': ['setup_venv'],
    }


def task_update_nc():
    """ Update list of NC submissions """
    return {
        'targets': ['downloaded_data/UNFCCC/submissions-nc.csv'],
        'actions': ['datalad run -m "Fetch NC submissions" '
                    '-o downloaded_data/UNFCCC/submissions-nc.csv '
                    './venv/bin/python code/UNFCCC_downloader/fetch_submissions_nc.py'],
        'verbosity': 2,
        'setup': ['setup_venv'],
    }


def task_download_nc():
    """ Download NC submissions """
    return {
        #'file_dep': ['downloaded_data/UNFCCC/submissions-nc.csv'],
        # deactivate file_dep fow now as it will always run fetch submissions
        # before download
        'actions': ['datalad run -m "Download NC submissions" '
                    '-i downloaded_data/UNFCCC/submissions-nc.csv '
                    './venv/bin/python code/UNFCCC_downloader/download_nc.py'],
        'verbosity': 2,
        'setup': ['setup_venv'],
    }


def task_download_ndc():
    """ Download NDC submissions """
    return {
        'actions': ['datalad run -m "Download NDC submissions" '
                    './venv/bin/python code/UNFCCC_downloader/download_ndc.py'],
        'verbosity': 2,
        'setup': ['setup_venv'],
    }


# read UNFCCC submissions.
# datalad run is called from within the read_UNFCCC_submission.py script
read_config = {
    "country": get_var('country', None),
    "submission": get_var('submission', None),
}

def task_read_unfccc_submission():
    """ Read submission for a country (if code exists) """
    return {
        'actions': [f"./venv/bin/python code/UNFCCC_reader/read_UNFCCC_submission.py "
                    f"--country={read_config['country']} --submission={read_config['submission']}"],
        'verbosity': 2,
        'setup': ['setup_venv'],
    }


def task_country_info():
    """ Print information on submissions and datasets
    available for given country"""
    return {
        'actions': [f"./venv/bin/python code/UNFCCC_reader/country_info.py "
                    f"--country={read_config['country']}"],
        'verbosity': 2,
        'setup': ['setup_venv'],
    }

