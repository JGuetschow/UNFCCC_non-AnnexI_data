"""
Downlaod annexI submissions

Download and unzip data from UNFCCC National Inventory Submissions.
Based on download.py from national-inventory-submissions
(https://github.com/openclimatedata/national-inventory-submisions)
"""

import argparse
import os
import shutil
import time
import zipfile
from datetime import date
from pathlib import Path
from random import randrange

import pandas as pd
import requests
from requests import ConnectionError
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from unfccc_ghg_data.helper import downloaded_data_path_UNFCCC, root_path

###############
#
# TODO
# download directly via selenium see link below
# https://sqa.stackexchange.com/questions/2197/
# how-to-download-a-file-using-seleniums-webdriver
# for automatic downloading see https://stackoverflow.com/questions/70740163/
# python-selenium-firefox-driver-dismiss-open-save-file-popup
###############
if __name__ == "__main__":
    descr = (
        "Download and unzip data from UNFCCC National Inventory Submissions. "
        "Based on download.py from national-inventory-submissions "
        "(https://github.com/openclimatedata/national-inventory-submisions)"
    )
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument("--category", help="Category to download, CRF, NIR, SEF")
    parser.add_argument("--year", help="Year to download")

    args = parser.parse_args()
    year = args.year
    category = args.category.upper()
    dataset = category + year
    print(f"Downloading data for {dataset}")

    # generate the correct url
    url = (
        "https://unfccc.int/process/transparency-and-reporting/"
        "reporting-and-review-under-the-convention/"
        "greenhouse-gas-inventories-annex-i-parties/"
        f"submissions/national-inventory-submissions-{year}"
    )

    # TODO: move to utils as used in two places
    if int(year) == 2019:  # noqa: PLR2004
        url = (
            "https://unfccc.int/process-and-meetings/transparency-and-reporting/"
            "reporting-and-review-under-the-convention/"
            "greenhouse-gas-inventories-annex-i-parties/"
            f"national-inventory-submissions-{year}"
        )
    elif int(year) in range(2020, 2025):
        url = f"https://unfccc.int/ghg-inventories-annex-i-parties/{year}"
    elif int(year) >= 2025:  # noqa: PLR2004
        url = f"https://unfccc.int/ghg-inventories-annex-i-parties/{year}"
    else:
        url = (
            "https://unfccc.int/process/transparency-and-reporting/"
            "reporting-and-review-under-the-convention/"
            "greenhouse-gas-inventories-annex-i-parties/"
            f"submissions/national-inventory-submissions-{year}"
        )

    error_file_sizes = [212, 210]

    # Read submissions list
    submissions = pd.read_csv(
        downloaded_data_path_UNFCCC / f"submissions-annexI_{year}.csv"
    )

    # filter submissions list or category
    items = submissions[submissions.Kind == category.upper()]

    # set options for headless mode
    profile_path = ".firefox"
    options = Options()
    # options.add_argument('-headless')

    # create profile for headless mode and automatic downloading
    options.set_preference("profile", profile_path)
    options.set_preference("browser.download.folderList", 2)

    # set up selenium driver
    driver = Firefox(options=options)
    # visit the main data page once to create cookies
    driver.get(url)

    # wait a bit for the website to load before we get the cokkies
    time.sleep(20)

    # get the session id cookie
    cookies_selenium = driver.get_cookies()
    cookies = {}
    for cookie in cookies_selenium:
        cookies[cookie["name"]] = cookie["value"]

    new_downloaded = []

    for idx, submission in items.iterrows():
        print("=" * 60)
        title = submission.Title
        url = submission.URL
        country = submission.Country
        country = country.replace(" ", "_")
        print(f"Downloading {title} from {url}")

        country_folder = downloaded_data_path_UNFCCC / country
        if not country_folder.exists():
            country_folder.mkdir()
        local_filename = (
            country_folder
            / dataset
            / url.split("/")[-1].replace("%20", "_").replace(" ", "_")
        )
        if not local_filename.parent.exists():
            local_filename.parent.mkdir()

        try:
            if local_filename.exists():
                # check file size. if 210 or 212 bytes it's the error page
                if Path(local_filename).stat().st_size in error_file_sizes:
                    # found the error page. delete file
                    os.remove(local_filename)
        except OSError as ex:
            if ex.errno == 36:  # noqa: PLR2004
                print(
                    f"Filename is too long: "
                    f"{local_filename.relative_to(root_path)}. "
                    f" Message: {ex}"
                )
                continue
            else:
                raise

        # now we have removed error pages, so a present file should not be overwritten
        if (not local_filename.exists()) and (not local_filename.is_symlink()):
            i = 0  # reset counter
            while not local_filename.exists() and i < 10:  # noqa: PLR2004
                # for i = 0 and i = 5 try to get a new session ID
                if i in (1, 5):
                    driver = Firefox(options=options)

                    # visit the main data page once to create cookies
                    driver.get(url)
                    time.sleep(20)

                    # get the session id cookie
                    cookies_selenium = driver.get_cookies()
                    cookies = {}
                    for cookie in cookies_selenium:
                        cookies[cookie["name"]] = cookie["value"]

                try:
                    r = requests.get(url, stream=True, cookies=cookies, timeout=120)
                    with open(str(local_filename), "wb") as f:
                        shutil.copyfileobj(r.raw, f)

                    # check file size. if 210 or 212 bytes it's the error page
                    if Path(local_filename).stat().st_size in error_file_sizes:
                        # found the error page. delete file
                        os.remove(local_filename)
                except ConnectionError as ex:
                    print(f"ConnectionError occurred: {ex}")

                # sleep a bit to avoid running into captchas
                time.sleep(randrange(5, 15))  # noqa: S311

            if local_filename.exists():
                new_downloaded.append(submission)
                print(f"Download => {local_filename.relative_to(root_path)}")
                # unzip data (only for new downloads)
                if local_filename.suffix == ".zip":
                    try:
                        zipped_file = zipfile.ZipFile(str(local_filename), "r")
                        zipped_file.extractall(str(local_filename.parent))
                        print(f"Extracted {len(zipped_file.namelist())} files.")
                        zipped_file.close()
                    # TODO Better error logging/visibilty
                    except zipfile.BadZipFile:
                        print(
                            f"Error while trying to extract "
                            f"{local_filename.relative_to(root_path)}"
                        )
                    except NotImplementedError:
                        print(
                            "Zip format not supported, "
                            "please unzip on the command line."
                        )
                    except OSError as ex:
                        if ex.errno == 36:  # noqa: PLR2004
                            print(
                                f"A filename is too long in file: "
                                f"{local_filename.relative_to(root_path)}. "
                                "Unzip manually if any other files needed."
                                f" Message: {ex}"
                            )
                        else:
                            raise
                else:
                    print(
                        f"Not attempting to extract "
                        f"{local_filename.relative_to(root_path)}."
                    )
            else:
                print(f"Failed to download {local_filename.relative_to(root_path)}")

        else:
            print(f"=> Already downloaded {local_filename.relative_to(root_path)}")

    driver.close()

    df_new_downloaded = pd.DataFrame(new_downloaded)
    df_new_downloaded.to_csv(
        downloaded_data_path_UNFCCC
        / f"00_new_downloads_{category}{year}-{date.today()}.csv",
        index=False,
    )
