#import requests
import time
import pandas as pd
import re

from pathlib import Path
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from random import randrange

root = Path(__file__).absolute().parents[2]

"""
Download UNFCCC Biennial Update Report submissions
from Non-Annex I Parties and create list of submissions as CSV file
Based on `process_bur` from national-inventory-submissions 
(https://github.com/openclimatedata/national-inventory-submisions)
"""

print("Fetching NC submissions ...")

url = "https://unfccc.int/non-annex-I-NCs"

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


pattern = re.compile(r"NC ?\d")

#skip = True
# Go through sub-pages.
for target in targets:
    #if target["url"] == "https://unfccc.int/documents/199234":
    #    skip = False
    #if skip:
    #    print(f"Skipping { target['title']}")
    #    continue
    time.sleep(randrange(5, 15))
    url = target["url"]
    #subpage = requests.get(url, timeout=15.5)
    driver.get(url)
    html = BeautifulSoup(driver.page_source, "html.parser")
    title = html.find("h1").contents[0]
    match = pattern.search(title)
    if match:
        kind = match.group(0).replace(" ", "")
    else:
        kind = None


    h2 = html.find("h2", text="Versions")
    if h2:
        div = h2.findNext("div")
        links = div.findAll("a")
        try:
            country = (
                html.find("h2", text="Countries").findNext("div").findNext("div").text
            )
        except AttributeError:
            country = (
                html.find("h2", text="Corporate Author")
                .findNext("div")
                .findNext("div")
                .text
            )
        doctype = (
            html.find("h2", text="Document Type").findNext("div").findNext("div").text
        )
        for link in links:
            url = link.attrs["href"]
            if not kind:
                match = pattern.search(url.upper())
                if match:
                    kind = match.group(0)
                else:
                    if ("NIR" in doctype) or ("NIR" in title):
                        kind = "NIR"
                    elif ("INV" in title) or ("Inventory" in title):
                        kind = "INV"
                    else:
                        print("found unknown record" + url)
            downloads.append(
                {
                    "Kind": kind,
                    "Country": country,
                    "Title": title,
                    "URL": url,
                }
            )
        print("\t".join([kind, country, title, url]))
    else:
        no_downloads.append((title, url))

if len(no_downloads) > 0:
    print("No downloads for ", no_downloads)

driver.close()
df = pd.DataFrame(downloads)
df = df[["Kind", "Country", "Title", "URL"]]
df.to_csv(root / "downloaded_data" / "UNFCCC" / "submissions-nc.csv", index=False)
