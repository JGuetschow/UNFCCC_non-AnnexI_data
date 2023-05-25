import argparse
import pandas as pd
import requests
import shutil
import time
import os
import zipfile
from datetime import date
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from random import randrange
from pathlib import Path

from UNFCCC_GHG_data.helper import root_path, downloaded_data_path_UNFCCC

###############
#
# TODO
# download directly via selenium see link below
# https://sqa.stackexchange.com/questions/2197/
# how-to-download-a-file-using-seleniums-webdriver
# for automatic downloading see https://stackoverflow.com/questions/70740163/
# python-selenium-firefox-driver-dismiss-open-save-file-popup
###############

descr = 'Download and unzip data from UNFCCC National Inventory Submissions. ' \
        'Based on download.py from national-inventory-submissions ' \
        '(https://github.com/openclimatedata/national-inventory-submisions)'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument(
    '--category',
    help='Category to download, CRF, NIR, SEF'
)
parser.add_argument(
    '--year',
    help='Year to download'
)

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
    "submissions/national-inventory-submissions-{}".format(year)
)

# TODO: move to utils as used in two places
if int(year) == 2019:
    url = (
        "https://unfccc.int/process-and-meetings/transparency-and-reporting/"
        "reporting-and-review-under-the-convention/"
        "greenhouse-gas-inventories-annex-i-parties/"
        "national-inventory-submissions-{}".format(year)
    )
elif int(year) in range(2020,2023):
    url = (
        "https://unfccc.int/ghg-inventories-annex-i-parties/{}".format(year)
    )
elif int(year) >= 2023:
    url = (
        "https://unfccc.int/process-and-meetings/transparency-and-reporting/"
        "reporting-and-review-under-the-convention/"
        "greenhouse-gas-inventories-annex-i-parties/"
        "national-inventory-submissions-{}".format(year)
    )
else:
    url = (
        "https://unfccc.int/process/transparency-and-reporting/"
        "reporting-and-review-under-the-convention/"
        "greenhouse-gas-inventories-annex-i-parties/"
        "submissions/national-inventory-submissions-{}".format(year)
    )

error_file_sizes = [212, 210]

# Read submissions list
submissions = pd.read_csv(downloaded_data_path_UNFCCC / f"submissions-annexI_{year}.csv")

# filter submissions list or category
items = submissions[submissions.Kind  == category.upper()]

# set options for headless mode
profile_path = ".firefox"
options = Options()
#options.add_argument('-headless')

# create profile for headless mode and automatic downloading
options.set_preference('profile', profile_path)
options.set_preference('browser.download.folderList', 2)

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
    cookies[cookie['name']] = cookie['value']

new_downloaded = []

for idx, submission in items.iterrows():
    print("=" * 60)
    title = submission.Title
    url = submission.URL
    country = submission.Country
    country = country.replace(' ', '_')
    print(f"Downloading {title} from {url}")

    country_folder = downloaded_data_path_UNFCCC / country
    if not country_folder.exists():
        country_folder.mkdir()
    local_filename = \
        country_folder / dataset / \
        url.split('/')[-1].replace("%20", "_").replace(" ", "_")
    if not local_filename.parent.exists():
        local_filename.parent.mkdir()

    if local_filename.exists():
        # check file size. if 210 or 212 bytes it's the error page
        if Path(local_filename).stat().st_size in error_file_sizes:
            # found the error page. delete file
            os.remove(local_filename)
    
    # now we have removed error pages, so a present file should not be overwritten
    if (not local_filename.exists()) and (not local_filename.is_symlink()):
        i = 0  # reset counter
        while not local_filename.exists() and i < 10:
            # for i = 0 and i = 5 try to get a new session ID
            if i == 1 or i == 5:
                driver = Firefox(options=options)
    
                # visit the main data page once to create cookies
                driver.get(url)
                time.sleep(20)

                # get the session id cookie
                cookies_selenium = driver.get_cookies()
                cookies = {}
                for cookie in cookies_selenium:
                    cookies[cookie['name']] = cookie['value']

            r = requests.get(url, stream=True, cookies=cookies)
            with open(str(local_filename), 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            
            # check file size. if 210 or 212 bytes it's the error page
            if Path(local_filename).stat().st_size in error_file_sizes:
                # found the error page. delete file
                os.remove(local_filename)
            
            # sleep a bit to avoid running into captchas
            time.sleep(randrange(5, 15))
            
        if local_filename.exists():
            new_downloaded.append(submission)
            print(f"Download => {local_filename.relative_to(root_path)}")
            # unzip data (only for new downloads)
            if local_filename.suffix == ".zip":
                try:
                    zipped_file = zipfile.ZipFile(str(local_filename), 'r')
                    zipped_file.extractall(str(local_filename.parent))
                    print(f"Extracted {len(zipped_file.namelist())} files.")
                    zipped_file.close()
                # TODO Better error logging/visibilty
                except zipfile.BadZipFile:
                    print(f"Error while trying to extract "
                          f"{local_filename.relative_to(root_path)}")
                except NotImplementedError:
                    print("Zip format not supported, please unzip on the command line.")
            else:
                print(f"Not attempting to extract "
                      f"{local_filename.relative_to(root_path)}.")
        else:
            print(f"Failed to download {local_filename.relative_to(root_path)}")

    else:
        print(f"=> Already downloaded {local_filename.relative_to(root_path)}")

driver.close()

df = pd.DataFrame(new_downloaded)
df.to_csv(downloaded_data_path_UNFCCC
          / f"00_new_downloads_{category}{year}-{date.today()}.csv", index=False)
