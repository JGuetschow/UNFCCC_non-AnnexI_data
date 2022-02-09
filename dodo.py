# define tasks for UNFCCC data repository

# Tasks for getting submissions and downloading them
def task_update_bur():
    """ Update list of BUR submissions """
    return {
        'targets': ['downloaded_data/UNFCCC/submissions-bur.csv'],
        'actions': ['datalad run -m "Fetch BUR submissions" '
                    '-o downloaded_data/UNFCCC/submissions-bur.csv '
                    './venv/bin/python code/UNFCCC_downloader/fetch_submissions_bur.py'],
    }


def task_download_bur():
    """ Download BUR submissions """
    return {
        'file_dep': ['downloaded_data/UNFCCC/submissions-bur.csv'],
        'actions': ['datalad run -m "Download BUR submissions" '
                    '-i downloaded_data/UNFCCC/submissions-bur.csv '
                    './venv/bin/python code/UNFCCC_downloader/download_bur.py'],
    }


def task_update_nc():
    """ Update list of NC submissions """
    return {
        'targets': ['downloaded_data/UNFCCC/submissions-nc.csv'],
        'actions': ['datalad run -m "Fetch NC submissions" '
                    '-o downloaded_data/UNFCCC/submissions-nc.csv '
                    './venv/bin/python code/UNFCCC_downloader/fetch_submissions_nc.py'],
    }


def task_download_nc():
    """ Download NC submissions """
    return {
        'file_dep': ['downloaded_data/UNFCCC/submissions-nc.csv'],
        'actions': ['datalad run -m "Download NC submissions" '
                    '-i downloaded_data/UNFCCC/submissions-nc.csv '
                    './venv/bin/python code/UNFCCC_downloader/download_nc.py'],
    }


def task_download_ndc():
    """ Download NDC submissions """
    return {
        'actions': ['datalad run -m "Download NDC submissions" '
                    './venv/bin/python code/UNFCCC_downloader/download_ndc.py'],
    }
