import pandas as pd
import requests
import shutil
import time
import os
from datetime import date
from selenium import webdriver
from random import randrange

from pathlib import Path
root = Path(__file__).parents[2]
"""
based on download_bur from national-inventory-submissions
# (https://github.com/openclimatedata/national-inventory-submisions)
"""

###############
#
# TODO
# download directly via selenium see link below
# https://sqa.stackexchange.com/questions/2197/
# how-to-download-a-file-using-seleniums-webdriver
###############

submissions = pd.read_csv(root / "downloaded_data" / "UNFCCC" /
                          "submissions-nc.csv")

url = "https://unfccc.int/non-annex-I-NCs"

# if we get files of this size they are error pages and we need to
# try the download again
error_file_sizes = [212, 210]

# find which BUR submission rounds exist
present_BURs = submissions.Kind.unique()

# Ensure download path and subfolders exist
download_path = root / "downloaded_data" / "UNFCCC"
if not download_path.exists():
    download_path.mkdir(parents=True)

# set options for headless mode
options = webdriver.firefox.options.Options()
# options.add_argument('-headless')

# create profile for headless mode 
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)

# set up selenium driver
driver = webdriver.Firefox(options=options, firefox_profile=profile)

# visit the main data page once to create cookies
driver.get(url)
time.sleep(20)

# get the session id cookie
cookies_selenium = driver.get_cookies()
cookies = {}
for cookie in cookies_selenium:
    cookies[cookie['name']] = cookie['value']

print(cookies)

new_downloaded = []

for idx, submission in submissions.iterrows():
    print("=" * 60)
    bur = submission.Kind
    title = submission.Title
    url = submission.URL
    country = submission.Country
    country = country.replace(' ', '_')
    print(title)

    country_folder = download_path / country
    if not country_folder.exists():
        country_folder.mkdir()
    local_filename = country_folder / bur / url.split('/')[-1]
    local_filename_underscore = \
        download_path / country / bur / \
        url.split('/')[-1].replace("%20", "_").replace(" ", "_")
    if not local_filename.parent.exists():
        local_filename.parent.mkdir()

    ### remove, not needed as no legacy data present
    #if local_filename.exists():
    #    # rename
    #    local_filename.rename(local_filename_underscore)
    #    print("Renamed " + bur + "/" + country + "/" + local_filename.name)

    # this should never be needed but in case anything goes wrong and
    # an error page is present it should be overwritten
    if local_filename_underscore.exists():
        # check file size. if 210 or 212 bytes it's the error page
        if Path(local_filename_underscore).stat().st_size in error_file_sizes:
            # found the error page. delete file
            os.remove(local_filename_underscore)
    
    # now we have remove error pages, so a present file should not be overwritten
    if not local_filename_underscore.exists():
        i = 0  # reset counter
        while not local_filename_underscore.exists() and i < 10:
            # for i = 0 and i = 5 try to get a new session ID
            if i == 1 or i == 5:
                driver = webdriver.Firefox(options=options,
                                           firefox_profile=profile)
    
                # visit the main data page once to create cookies
                driver.get(url)
                time.sleep(20)
                
                # get the session id cookie
                cookies_selenium = driver.get_cookies()
                cookies = {}
                for cookie in cookies_selenium:
                    cookies[cookie['name']] = cookie['value']
                    
            r = requests.get(url, stream=True, cookies=cookies)
            with open(str(local_filename_underscore), 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            
            # check file size. if 210 or 212 bytes it's the error page
            if Path(local_filename_underscore).stat().st_size in error_file_sizes:
                # found the error page. delete file
                os.remove(local_filename_underscore)
            
            # sleep a bit to avoid running into captchas
            time.sleep(randrange(5, 15))
            
        if local_filename_underscore.exists():
            new_downloaded.append(submission)
            print("Download => downloaded_data/UNFCCC/" + country + "/" + bur +
                  "/" + local_filename_underscore.name)
        else:
            print("Failed downloading downloaded_data/UNFCCC/" + country + "/"
                  + bur + "/" + local_filename_underscore.name)

    else:
        print("=> Already downloaded " + local_filename_underscore.name)

driver.close()

df = pd.DataFrame(new_downloaded)
df.to_csv(download_path / "00_new_downloads_nc-{}.csv".format(date.today()), index=False)
