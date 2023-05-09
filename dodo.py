# define tasks for UNFCCC data repository
from doit import get_var

# TODO: task for folder mapping

# create virtual environment
def task_setup_venv():
    """Create virtual environment"""
    return {
        'file_dep': ['requirements_dev.txt', 'setup.cfg', 'pyproject.toml'],
        'actions': ['python3 -m venv venv',
                    './venv/bin/pip install --upgrade pip wheel',
                    #'./venv/bin/pip install -Ur UNFCCC_GHG_data/requirements.txt',
                    './venv/bin/pip install --upgrade --upgrade-strategy '
                    'eager -e .[dev]',
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
        'actions': [f"./venv/bin/python UNFCCC_GHG_data/UNFCCC_reader/folder_mapping.py "
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
                    './venv/bin/python UNFCCC_GHG_data/UNFCCC_downloader/fetch_submissions_bur.py'],
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
                    './venv/bin/python UNFCCC_GHG_data/UNFCCC_downloader/download_non-annexI.py --category=BUR',
                    f"./venv/bin/python UNFCCC_GHG_data/UNFCCC_reader/folder_mapping.py "
                    f"--folder=downloaded_data/UNFCCC"
                    ],
        'verbosity': 2,
        'setup': ['setup_venv'],
    }


def task_update_nc():
    """ Update list of NC submissions """
    return {
        'targets': ['downloaded_data/UNFCCC/submissions-nc.csv'],
        'actions': ['datalad run -m "Fetch NC submissions" '
                    '-o downloaded_data/UNFCCC/submissions-nc.csv '
                    './venv/bin/python UNFCCC_GHG_data/UNFCCC_downloader/fetch_submissions_nc.py'],
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
                    './venv/bin/python UNFCCC_GHG_data/UNFCCC_downloader/download_non-annexI.py --category=NC',
                    f"./venv/bin/python UNFCCC_GHG_data/UNFCCC_reader/folder_mapping.py "
                    f"--folder=downloaded_data/UNFCCC"
                    ],
        'verbosity': 2,
        'setup': ['setup_venv'],
    }

# annexI data: one update call for all data types (as they are on one page)
# but for each year separately.
# downloading is per year and
update_aI_config = {
    "year": get_var('year', None),
    "category": get_var('category', None),
}


def task_update_annexi():
    """ Update list of AnnexI submissions """
    return {
        'targets': [f"downloaded_data/UNFCCC/submissions-annexI_{update_aI_config['year']}.csv"],
        'actions': [f"datalad run -m 'Fetch AnnexI submissions for {update_aI_config['year']}' "
                    "--explicit "
                    f"-o downloaded_data/UNFCCC/submissions-annexI_{update_aI_config['year']}.csv "
                    f"./venv/bin/python UNFCCC_GHG_data/UNFCCC_downloader/fetch_submissions_annexI.py "
                    f"--year={update_aI_config['year']}"],
        'verbosity': 2,
        'setup': ['setup_venv'],
    }


def task_download_annexi():
    """ Download AnnexI submissions """
    return {
        #'file_dep': ['downloaded_data/UNFCCC/submissions-nc.csv'],
        # deactivate file_dep fow now as it will always run fetch submissions
        # before download
        'actions': [f"datalad run -m 'Download AnnexI submissions for "
                    f"{update_aI_config['category']}{update_aI_config['year']}' "
                    f"-i downloaded_data/UNFCCC/submissions-annexI_{update_aI_config['year']}.csv "
                    f"./venv/bin/python UNFCCC_GHG_data/UNFCCC_downloader/download_annexI.py "
                    f"--category={update_aI_config['category']} --year={update_aI_config['year']}",
                    f"./venv/bin/python UNFCCC_GHG_data/UNFCCC_reader/folder_mapping.py "
                    f"--folder=downloaded_data/UNFCCC"
                    ],
        'verbosity': 2,
        'setup': ['setup_venv'],
    }


def task_download_ndc():
    """ Download NDC submissions """
    return {
        'actions': ['datalad run -m "Download NDC submissions" '
                    './venv/bin/python UNFCCC_GHG_data/UNFCCC_downloader/download_ndc.py',
                    f"./venv/bin/python UNFCCC_GHG_data/UNFCCC_reader/folder_mapping.py "
                    f"--folder=downloaded_data/UNFCCC"
                    ],
        'verbosity': 2,
        'setup': ['setup_venv'],
    }


# read UNFCCC submissions.
# datalad run is called from within the read_UNFCCC_submission.py script
read_config = {
    "country": get_var('country', None),
    "submission": get_var('submission', None),
}


# TODO: make individual task for non-UNFCCC submissions
def task_read_unfccc_submission():
    """ Read submission for a country (if UNFCCC_GHG_data exists) (not for CRF)"""
    return {
        'actions': [f"./venv/bin/python UNFCCC_GHG_data/UNFCCC_reader/read_UNFCCC_submission.py "
                    f"--country={read_config['country']} --submission={read_config['submission']}",
                    f"./venv/bin/python UNFCCC_GHG_data/UNFCCC_reader/folder_mapping.py "
                    f"--folder=extracted_data/UNFCCC"
                    ],
        'verbosity': 2,
        'setup': ['setup_venv'],
    }


# read UNFCCC submissions.
# datalad run is called from within the read_UNFCCC_submission.py script
read_config_crf = {
    "country": get_var('country', None),
    "submission_year": get_var('submission_year', None),
    "submission_date": get_var('submission_date', None),
    "re_read": get_var('re_read', False),
    "countries": get_var('countries', None),
}

def task_read_unfccc_crf_submission():
    """ Read CRF submission for a country """
    actions = [
        f"./venv/bin/python UNFCCC_GHG_data/UNFCCC_CRF_reader/read_UNFCCC_CRF_submission_datalad.py "
        f"--country={read_config_crf['country']} "
        f"--submission_year={read_config_crf['submission_year']} "
        f"--submission_date={read_config_crf['submission_date']} ",
        f"./venv/bin/python UNFCCC_GHG_data/UNFCCC_reader/folder_mapping.py "
        f"--folder=extracted_data/UNFCCC"
        ]
    if read_config_crf["re_read"] == "True":
        actions[0] = actions[0] + " --re_read"
    return {
        'actions': actions,
        'verbosity': 2,
        'setup': ['setup_venv'],
    }


def task_read_new_unfccc_crf_for_year():
    """ Read CRF submission for all countries for given submission year. by default only reads
    data not present yet. Only reads the latest updated submission for each country."""
    actions = [f"./venv/bin/python UNFCCC_GHG_data/UNFCCC_CRF_reader/read_new_UNFCCC_CRF_for_year_datalad.py "
               f"--submission_year={read_config_crf['submission_year']} ",
               f"./venv/bin/python UNFCCC_GHG_data/UNFCCC_reader/folder_mapping.py "
               f"--folder=extracted_data/UNFCCC"
               ]
    # specifying countries is currently disabled duo to problems with command line
    # list arguments
    #if read_config_crf["countries"] is not None:
    #        actions[0] = actions[0] + f"--countries={read_config_crf['countries']} "
    if read_config_crf["re_read"] == "True":
        actions[0] = actions[0] + " --re_read"
    return {
        #'basename': "Read_CRF_year",
        'actions': actions,
        'verbosity': 2,
        'setup': ['setup_venv'],
    }


def task_country_info():
    """ Print information on submissions and datasets
    available for given country"""
    return {
        'actions': [f"./venv/bin/python UNFCCC_GHG_data/UNFCCC_reader/country_info.py "
                    f"--country={read_config['country']}"],
        'verbosity': 2,
        'setup': ['setup_venv'],
    }

