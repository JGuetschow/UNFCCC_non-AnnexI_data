"""
Fetch list of BTR submissions from UNFCCC website
"""

import argparse
import time
from pathlib import Path
from random import randrange

import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from unfccc_ghg_data.helper import downloaded_data_path_UNFCCC
from unfccc_ghg_data.unfccc_downloader import (
    get_BTR_name_and_URL,
    get_unfccc_submission_info,
)

# TODO: use categories like in AnnexI downloading (for round 2)

if __name__ == "__main__":
    max_tries = 10

    descr = (
        "Download UNFCCC Biannial Transparency Reports Submissions lists "
        "and create list of submissions as CSV file. Based on "
        "process.py from national-inventory-submissions "
        "(https://github.com/openclimatedata/national-inventory-submisions)"
    )
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument("--round", help="1 for first BTRs, 2 for second BTRs etc.")

    args = parser.parse_args()
    submission_round = int(args.round)

    round_name, url = get_BTR_name_and_URL(submission_round)

    print(f"Fetching submissions for {round_name} BTRs")
    print(f"Using {url} to get submissions list")

    # set options for headless mode
    profile_path = ".firefox"
    options = Options()
    # options.add_argument("-headless")

    # create profile for headless mode and automatic downloading
    options.set_preference("profile", profile_path)

    # set up selenium driver
    driver = Firefox(options=options)
    driver.get(url)

    html = BeautifulSoup(driver.page_source, "html.parser")

    table = html.find("table")

    # check if table found. if not the get command didn't work, likely because of a
    # captcha on the site
    ### TODO replace by error message
    if not table:
        raise RuntimeError(  # noqa: TRY003
            "No table found on URL. Possibly due to a captcha."
        )

    links = table.findAll("a")

    targets = []  # sub-pages
    downloads = []
    no_downloads = []

    # Check links for Zipfiles or subpages
    for link in links:
        if "href" not in link.attrs:
            continue
        href = link.attrs["href"]
        if (
            ("documents/" in href)
            or ("node/" in href)
            or ("NODE/" in href)
            or ("files/" in href)
        ):
            if "title" in link.attrs.keys():
                title = link.attrs["title"]
            else:
                title = link.contents[0]
            if href.startswith("/documents"):
                href = "https://unfccc.int" + href
            elif href.startswith("documents"):
                href = "https://unfccc.int/" + href
            if href.startswith("/node"):
                href = "https://unfccc.int" + href
            if href.startswith("/NODE"):
                href = "https://unfccc.int" + href
            # Only add pages in the format https://unfccc.int/documents/65587
            # or https://unfccc.int/[node/NODE]/65587
            # to further downloads
            if str(Path(href).parent).endswith("documents"):
                targets.append({"title": title, "url": href})
        else:
            print(f"Ignored link: {href}: not in the right format.")

    # Go through sub-pages.
    for target in targets:
        time.sleep(randrange(5, 15))  # noqa: S311
        url = target["url"]

        submission_info = get_unfccc_submission_info(url, driver, max_tries=max_tries)

        if submission_info:
            downloads = downloads + submission_info
        else:
            no_downloads.append({target["title"], url})

    if len(no_downloads) > 0:
        print("No downloads for ", no_downloads)

    driver.close()
    df_downloads = pd.DataFrame(downloads)
    df_downloads.to_csv(
        downloaded_data_path_UNFCCC / f"submissions-BTR{submission_round}.csv",
        index=False,
    )
