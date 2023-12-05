import argparse
import time
import pandas as pd

from pathlib import Path
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from random import randrange
from unfccc_submission_info import get_unfccc_submission_info
from unfccc_ghg_data.helper import downloaded_data_path_UNFCCC

max_tries = 10

descr = ("Download UNFCCC National Inventory Submissions lists "
         "and create list of submissions as CSV file. Based on "
         "process.py from national-inventory-submissions "
         "(https://github.com/openclimatedata/national-inventory-submisions)")
parser = argparse.ArgumentParser(description=descr)
parser.add_argument(
    '--year',
    help='Year to download'
)

args = parser.parse_args()
year = args.year

print("Fetching submissions for {}".format(year))
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
    # try to load html file from disk
    print('Download failed, trying to load manually downloaded file')
    file = open("manual_page_downloads/National-Inventory-Submissions-{}.html".format(year))
    content = file.read()
    html = BeautifulSoup(content, "html.parser")
    table = html.find("table")
    if not table:
        print(
            "Manually downloaded file " + "manual_page_downloads/National-Inventory-Submissions-{}.html".format(year) +
            " not found")
        exit()

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
    elif href.endswith(".zip"):
        if href.startswith("/files"):
            href = "https://unfccc.int" + href
        country = Path(href).name.split("-")[0].upper()
        title = f"{country} {link.contents[0]}"
        filename = Path(href).name
        file_parts = filename.split('-')
        if len(file_parts) >= 2:
            kind = file_parts[2].upper()
        elif filename.startswith('asr'):
            kind = 'CRF'
        else:
            kind = None

        print("\t".join([kind, country, title, href]))
        downloads.append({"Kind": kind, "Country": country, "Title": title, "URL": href})

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
df.to_csv(downloaded_data_path_UNFCCC / f"submissions-annexI_{year}.csv", index=False)
