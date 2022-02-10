# define tasks for UNFCCC data repository

# Tasks for getting submissions and downloading them
def task_update_bur():
    """ Update list of BUR submissions """
    return {
        'targets': ['downloaded_data/UNFCCC/submissions-bur.csv'],
        'actions': ['datalad run -m "Fetch BUR submissions" '
                    '-o downloaded_data/UNFCCC/submissions-bur.csv '
                    './venv/bin/python code/UNFCCC_downloader/fetch_submissions_bur.py'],
        'verbosity': 2,
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
    }


def task_update_nc():
    """ Update list of NC submissions """
    return {
        'targets': ['downloaded_data/UNFCCC/submissions-nc.csv'],
        'actions': ['datalad run -m "Fetch NC submissions" '
                    '-o downloaded_data/UNFCCC/submissions-nc.csv '
                    './venv/bin/python code/UNFCCC_downloader/fetch_submissions_nc.py'],
        'verbosity': 2,
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
    }


def task_download_ndc():
    """ Download NDC submissions """
    return {
        'actions': ['datalad run -m "Download NDC submissions" '
                    './venv/bin/python code/UNFCCC_downloader/download_ndc.py'],
        'verbosity': 2,
    }


# read UNFCCC submissions.
# datalad run is called from within the read_UNFCCC_submission.py script
# add parameters and pass them to script
def task_read_unfccc_submission():
    """ Read submission for a country (if code exists) """
    return {
        'actions': ['./venv/bin/python code/UNFCCC_downloader/read_UNFCCC_submission.py'],
        'verbosity': 2,
        'params': [{'name': 'country',
                    'short': 'c',
                    'long': 'country',
                    'default': None,
                    'help': 'name or ISO 3-letter code of the country to read data for (e.g. China)',
                    'type': str,
                    },
                   {'name': 'submission',
                    'short': 's',
                    'long': 'submission',
                    'default': None,
                    'help': 'submission to read (e.g. BUR4)',
                    'type': str,
                    },
                   ],
    }