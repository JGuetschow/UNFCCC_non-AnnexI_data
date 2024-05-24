"""
Define the tasks for UNFCCC data repository

The setup with the function that calls datalad.api.run is necessary because doit doesn't
like the return values of datalad.api.run

TODO: could add try-except blocks and return proper values so doit knows if the task
 was run successfully
"""
import os
import sys

import datalad.api
from doit import get_var

root_path = "."
os.environ["UNFCCC_GHG_ROOT_PATH"] = root_path

from unfccc_ghg_data.helper.functions import (  # noqa: E402
    get_country_datasets,
    get_country_submissions,
)
from unfccc_ghg_data.unfccc_crf_reader.unfccc_crf_reader_devel import (  # noqa: E402
    read_year_to_test_specs,
)
from unfccc_ghg_data.unfccc_crf_reader.unfccc_crf_reader_prod import (  # noqa: E402
    read_crf_for_country_datalad,
    read_new_crf_for_year_datalad,
)
from unfccc_ghg_data.unfccc_di_reader import (  # noqa: E402
    process_DI_for_country_datalad,
    process_DI_for_country_group_datalad,
    read_DI_for_country_datalad,
    read_DI_for_country_group_datalad,
)


def set_root_path():
    """Set the root folder for the repository"""
    os.environ["UNFCCC_GHG_ROOT_PATH"] = root_path


def map_folders(parent_folder):
    """
    Create or update the folder mapping in the given folder

    Internal function
    """
    datalad.api.run(
        cmd="python3 src/unfccc_ghg_data/helper/folder_mapping.py "
        f"--folder={parent_folder}",
        dataset=root_path,
        message=f"Update folder mapping for {parent_folder}",
        outputs=f"{parent_folder}/folder_mapping.json",
        dry_run=None,
        explicit=True,
    )


def task_in_venv():
    """
    Check if code run from virtual environment and throw an error is not.

    Returns
    -------
    Nothing

    """

    def in_venv():
        if sys.prefix == sys.base_prefix:
            raise ValueError(  # noqa: TRY003
                "You need to run the code from the virtual environment."
            )

    return {
        "actions": [in_venv],
    }


# Task to create the mapping files which map folder names to ISO 3-letter country codes
read_config_folder = {
    "folder": get_var("folder", None),
}


def task_map_folders():
    """
    Create or update the folder mapping in the given folder
    """
    return {
        "actions": [(map_folders, [read_config_folder["folder"]])],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


# Tasks for getting submissions and downloading them
def task_update_bur():
    """Update list of BUR submissions"""

    def fetch_bur():
        datalad.api.run(
            cmd="python3 src/unfccc_ghg_data/unfccc_downloader/"
            "fetch_submissions_bur.py",
            dataset=root_path,
            message="Fetch BUR submissions",
            outputs="downloaded_data/UNFCCC/submissions-bur.csv",
            dry_run=None,
            explicit=True,
        )

    return {
        "targets": ["downloaded_data/UNFCCC/submissions-bur.csv"],
        "actions": [
            (fetch_bur,),
        ],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


def task_download_bur():
    """Download BUR submissions"""

    def download_bur():
        (
            datalad.api.run(
                cmd="python3 src/unfccc_ghg_data/unfccc_downloader/"
                "download_nonannexI.py --category=BUR",
                dataset=root_path,
                message="Download BUR submissions",
                inputs="downloaded_data/UNFCCC/submissions-bur.csv",
                dry_run=None,
                explicit=False,
            ),
        )

    return {
        #'file_dep': ['downloaded_data/UNFCCC/submissions-bur.csv'],
        # deactivate file_dep fow now as it will always run fetch submissions
        # before download
        "actions": [
            (download_bur,),
            (map_folders, ["downloaded_data/UNFCCC"]),
        ],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


def task_update_nc():
    """Update list of NC submissions"""

    def fetch_nc():
        datalad.api.run(
            cmd="python3 src/unfccc_ghg_data/unfccc_downloader/"
            "fetch_submissions_nc.py",
            dataset=root_path,
            message="Fetch NC submissions",
            outputs="downloaded_data/UNFCCC/submissions-nc.csv",
            dry_run=None,
            explicit=True,
        )

    return {
        "targets": ["downloaded_data/UNFCCC/submissions-nc.csv"],
        "actions": [
            (fetch_nc,),
        ],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


def task_download_nc():
    """Download BUR submissions"""

    def download_nc():
        (
            datalad.api.run(
                cmd="python3 src/unfccc_ghg_data/unfccc_downloader/"
                "download_nonannexI.py --category=NC",
                dataset=root_path,
                message="Download NC submissions",
                inputs="downloaded_data/UNFCCC/submissions-nc.csv",
                dry_run=None,
                explicit=False,
            ),
        )

    return {
        #'file_dep': ['downloaded_data/UNFCCC/submissions-bur.csv'],
        # deactivate file_dep fow now as it will always run fetch submissions
        # before download
        "actions": [
            (download_nc,),
            (map_folders, ["downloaded_data/UNFCCC"]),
        ],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


# annexI data: one update call for all data types (as they are on one page)
# but for each year separately.
# downloading is per year and
update_aI_config = {
    "year": get_var("year", None),
    "category": get_var("category", None),
}


def task_update_annexi():
    """Update list of AnnexI submissions"""

    def fetch_annexi():
        (
            datalad.api.run(
                cmd="python src/unfccc_ghg_data/unfccc_downloader/"
                "fetch_submissions_annexI.py "
                f"--year={update_aI_config['year']}",
                dataset=root_path,
                message=f"Fetch AnnexI submissions for {update_aI_config['year']}",
                outputs=f"downloaded_data/UNFCCC/submissions-annexI_"
                f"{update_aI_config['year']}.csv",
                dry_run=None,
                explicit=True,
            ),
        )

    return {
        "targets": [
            f"downloaded_data/UNFCCC/submissions-annexI_{update_aI_config['year']}.csv"
        ],
        "actions": [
            (fetch_annexi,),
        ],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


def task_download_annexi():
    """Download AnnexI submissions"""

    def download_annexi():
        (
            datalad.api.run(
                cmd="python src/unfccc_ghg_data/unfccc_downloader/download_annexI.py "
                f"--category={update_aI_config['category']} "
                f"--year={update_aI_config['year']}",
                dataset=root_path,
                message=f"Download AnnexI submissions for "
                f"{update_aI_config['category']}"
                f"{update_aI_config['year']}",
                inputs=f"downloaded_data/UNFCCC/submissions-annexI_"
                f"{update_aI_config['year']}.csv",
                dry_run=None,
                explicit=False,
            ),
        )

    return {
        # 'file_dep': [f"downloaded_data/UNFCCC/submissions-annex1_"
        #              f"{update_aI_config['year']}.csv"],
        # deactivate file_dep fow now as it will always run fetch submissions
        # before download
        "actions": [
            (download_annexi,),
            (map_folders, ["downloaded_data/UNFCCC"]),
        ],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


# BTR data: one update call for all data types (as they are on one page)
# but for each submission round separately.
# downloading is per submission round
update_btr_config = {
    "round": get_var("round", None),
}


def task_update_btr():
    """Update list of BTR submissions"""

    def fetch_btr():
        (
            datalad.api.run(
                cmd="python src/unfccc_ghg_data/unfccc_downloader/"
                "fetch_submissions_btr.py "
                f"--round={update_btr_config['round']}",
                dataset=root_path,
                message=f"Fetch Biannial Transparency Report submissions for "
                f"BTR{update_btr_config['round']}",
                outputs=f"downloaded_data/UNFCCC/submissions-BTR"
                f"{update_btr_config['round']}.csv",
                dry_run=None,
                explicit=True,
            ),
        )

    return {
        "targets": [
            f"downloaded_data/UNFCCC/submissions-BTR{update_btr_config['round']}.csv"
        ],
        "actions": [
            (fetch_btr,),
        ],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


def task_download_btr():
    """Download BTR submissions"""

    def download_btr():
        (
            datalad.api.run(
                cmd="python src/unfccc_ghg_data/unfccc_downloader/download_btr.py "
                f"--round={update_btr_config['round']}",
                dataset=root_path,
                message="Download BTR submissions for "
                f"BTR{update_btr_config['round']}",
                inputs=f"downloaded_data/UNFCCC/submissions-BTR"
                f"{update_btr_config['round']}.csv",
                dry_run=None,
                explicit=False,
            ),
        )

    return {
        # 'file_dep': [f"downloaded_data/UNFCCC/submissions-btr.csv "
        #              f"{update_btr_config['round']}.csv"],
        # deactivate file_dep fow now as it will always run fetch submissions
        # before download
        "actions": [
            (download_btr,),
            (map_folders, ["downloaded_data/UNFCCC"]),
        ],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


def task_download_ndc():
    """Download NDC submissions"""

    def download_ndc():
        (
            datalad.api.run(
                cmd="src/unfccc_ghg_data/unfccc_downloader/download_ndc.py",
                dataset=root_path,
                message="Download NDC submissions",
                inputs=None,
                dry_run=None,
                explicit=False,
            ),
        )

    return {
        "actions": [
            (download_ndc,),
            (map_folders, ["downloaded_data/UNFCCC"]),
        ],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


# read UNFCCC submissions.
# datalad run is called from within the read_UNFCCC_submission.py script
read_config = {
    "country": get_var("country", None),
    "submission": get_var("submission", None),
}


# TODO: make individual task for non-UNFCCC submissions
def task_read_unfccc_submission():
    """Read submission for a country (if code exists) (not for CRF)

    Datalad is called from `read_UNFCCC_submission`, so we can just call this script
    here.

    TODO: check if it makes sense to convert script to function
    """
    return {
        "actions": [
            f"python src/unfccc_ghg_data/unfccc_reader/read_UNFCCC_submission.py "
            f"--country={read_config['country']} "
            f"--submission={read_config['submission']}",
            (map_folders, ["extracted_data/UNFCCC"]),
        ],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


# read UNFCCC CRF submissions.
# datalad run is called from within the read_UNFCCC_submission.py script
read_config_crf = {
    "country": get_var("country", None),
    "submission_year": get_var("submission_year", None),
    "submission_date": get_var("submission_date", None),
    "re_read": get_var("re_read", False),
    "countries": get_var("countries", None),
    "data_year": get_var("data_year", None),
    "totest": get_var("totest", None),
    "type": get_var("type", "CRF"),
}


def task_read_unfccc_crf_submission():
    """Read CRF submission for a country"""

    def read_CRF():
        if read_config_crf["re_read"] == "True":
            re_read = True
        else:
            re_read = False
        read_crf_for_country_datalad(
            read_config_crf["country"],
            submission_year=int(read_config_crf["submission_year"]),
            submission_date=read_config_crf["submission_date"],
            re_read=re_read,
            type=read_config_crf["type"],
        )

    return {
        "actions": [
            (read_CRF,),
            (map_folders, ["extracted_data/UNFCCC"]),
        ],
        "task_dep": ["set_env"],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


def task_read_new_unfccc_crf_for_year():
    """
    Read CRF/CRT submission for all countries for given submission year.

    By default only reads data not present yet. Only reads the latest updated
    submission for each country.
    """

    def read_new_CRF():
        if read_config_crf["re_read"] == "True":
            re_read = True
        else:
            re_read = False
        read_new_crf_for_year_datalad(
            submission_year=int(read_config_crf["submission_year"]),
            # countries=read_config_crf["countries"],
            re_read=re_read,
            type=read_config_crf["type"],
        )

    return {
        "actions": [
            (read_new_CRF,),
            (map_folders, ["extracted_data/UNFCCC"]),
        ],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


def task_test_read_unfccc_crf_for_year():
    """
    Test CRF/CRT reading.

    Test CRF/CRT with a single year only for speed and logging to extend specifications
    if necessary.
    """

    def read_CRF():
        if read_config_crf["totest"] == "True":
            totest = True
        else:
            totest = False
        if read_config_crf["data_year"] is not None:
            data_year = int(read_config_crf["data_year"])
        else:
            data_year = None
        read_year_to_test_specs(
            submission_year=int(read_config_crf["submission_year"]),
            data_year=data_year,
            totest=totest,
            country_code=read_config_crf["country"],
            type=read_config_crf["type"],
        )

    return {
        "actions": [
            (read_CRF,),
            (map_folders, ["extracted_data/UNFCCC"]),
        ],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


def task_compile_raw_unfccc_crf_for_year():
    """
    Collect all latest CRF/CRT submissions for a given year / submission round

    Reads the latest data from the extracted data folder for each country.
    Notifies the user if new data are available in the downloaded_data folder
    which have not yet been read.

    Data are saved in the datasets/UNFCCC/[CRFYYYY|CRTX] folder.
    TODO: could make a function from the script
    """
    actions = [
        f"python "
        f"src/unfccc_ghg_data/unfccc_crf_reader/crf_raw_for_year.py "
        f"--submission_year={read_config_crf['submission_year']} "
        f"--type={read_config_crf['type']} "
    ]
    return {
        "actions": actions,
        "task_dep": ["set_env"],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


# tasks for DI reader
# TODO DI tasks need testing
# datalad run is called from within the read_unfccc_di_for_country.py script
read_config_di = {
    "country": get_var("country", None),
    "date": get_var("date", None),
    "annexI": get_var("annexI", False),
    # "countries": get_var('countries', None),
}


def task_read_unfccc_di_for_country():
    """Read DI data for a country"""
    return {
        "actions": [
            (read_DI_for_country_datalad, [read_config_di["country"]]),
            (map_folders, ["extracted_data/UNFCCC"]),
        ],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


def task_process_unfccc_di_for_country():
    """Process DI data for a country"""
    return {
        "actions": [
            (
                process_DI_for_country_datalad,
                [],
                {
                    "country": read_config_di["country"],
                    "date_str": read_config_di["date"],
                },
            ),
            (map_folders, ["extracted_data/UNFCCC"]),
        ],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


def task_read_unfccc_di_for_country_group():
    """Read DI data for a country group"""

    def read_DI():
        if read_config_di["annexI"] == "True":
            annexI = True
        else:
            annexI = False
        read_DI_for_country_group_datalad(annexI=annexI)

    return {
        "actions": [(read_DI,), (map_folders, ["extracted_data/UNFCCC"])],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


def task_process_unfccc_di_for_country_group():
    """Process DI data for a country group"""

    def proc_DI():
        if read_config_di["annexI"] == "True":
            annexI = True
        else:
            annexI = False
        process_DI_for_country_group_datalad(
            annexI=annexI,
            date_str=read_config_di["date"],
        )

    return {
        "actions": [(proc_DI,), (map_folders, ["extracted_data/UNFCCC"])],
        "verbosity": 2,
        "setup": ["in_venv"],
    }


# general tasks
def task_country_info():
    """
    Print information on submissions and datasets available for given country
    """

    def country_info(country):
        # print available submissions
        print("=" * 15 + " Available submissions " + "=" * 15)
        get_country_submissions(country, True)
        print("")

        # print available datasets
        print("=" * 15 + " Available datasets " + "=" * 15)
        get_country_datasets(country, True)

    return {
        "actions": [(country_info, [read_config["country"]])],
        "verbosity": 2,
        "setup": ["in_venv"],
    }
