#import requests
import time
import pandas as pd
import re

from pathlib import Path
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from random import randrange
from unfccc_submission_info import get_unfccc_submission_info

root = Path(__file__).absolute().parents[2]

"""
Download UNFCCC Biennial Update Report submissions
from Non-Annex I Parties and create list of submissions as CSV file
Based on `process_bur` from national-inventory-submissions 
(https://github.com/openclimatedata/national-inventory-submisions)
"""

print("Fetching BUR submissions ...")

url = "https://unfccc.int/BURs"

#print(url)

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
table = html.find_all("table")[1]
links = table.findAll("a")

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


pattern = re.compile(r"BUR ?\d")

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
df = df[["Kind", "Country", "Title", "URL"]]
df.to_csv(root / "downloaded_data" / "UNFCCC" / "submissions-bur.csv", index=False)
