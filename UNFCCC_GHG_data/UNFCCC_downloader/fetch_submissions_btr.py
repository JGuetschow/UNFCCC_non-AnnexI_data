import argparse
import time
import pandas as pd

from pathlib import Path
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from random import randrange
from unfccc_submission_info import (get_unfccc_submission_info,
                                    get_BTR_name_and_URL)
from UNFCCC_GHG_data.helper import downloaded_data_path_UNFCCC

max_tries = 10

descr = ("Download UNFCCC Biannial Transparency Reports Submissions lists "
         "and create list of submissions as CSV file. Based on "
         "process.py from national-inventory-submissions "
         "(https://github.com/openclimatedata/national-inventory-submisions)")
parser = argparse.ArgumentParser(description=descr)
parser.add_argument(
    '--round',
    help='1 for first BTRs, 2 for second BTRs etc.'
)

args = parser.parse_args()
submission_round = int(args.round)

round_name, url = get_BTR_name_and_URL(submission_round)

print(f"Fetching submissions for {round_name} BTRs")
print(f"Using {url} to get submissions list")

# set options for headless mode
profile_path = ".firefox"
options = Options()
options.add_argument('-headless')

# create profile for headless mode and automatic downloading
options.set_preference('profile', profile_path)

# set up selenium driver
driver = Firefox(options=options)
driver.get(url)

html = BeautifulSoup(driver.page_source, "html.parser")

table = html.find("table")

# check if table found. if not the get command didn't work, likely because of a captcha on the site
### TODO replace by error message
if not table:
    raise RuntimeError('No table found on URL. Possibly due to a captcha.')

links = table.findAll('a')

targets = []  # sub-pages
downloads = []
no_downloads = []

# Check links for Zipfiles or subpages
for link in links:
    if "href" not in link.attrs:
        continue
    href = link.attrs["href"]
    if "/documents/" in href:
        if "title" in link.attrs.keys():
            title = link.attrs["title"]
        else:
            title = link.contents[0]
        if href.startswith("/documents"):
            href = "https://unfccc.int" + href
        # Only add pages in the format https://unfccc.int/documents/65587
        # to further downloads
        if str(Path(href).parent).endswith("documents"):
            targets.append({"title": title, "url": href})
    else:
        print(f"Ignored link: {href}: not in the right format.")

# Go through sub-pages.
for target in targets:
    time.sleep(randrange(5, 15))
    url = target["url"]

    submission_info = get_unfccc_submission_info(url, driver, 10)

    if submission_info:
        downloads = downloads + submission_info
    else:
        no_downloads.append({target["title"], url})

if len(no_downloads) > 0:
    print("No downloads for ", no_downloads)

driver.close()
df = pd.DataFrame(downloads)
df.to_csv(downloaded_data_path_UNFCCC / f"submissions-BTR{submission_round}.csv", index=False)
