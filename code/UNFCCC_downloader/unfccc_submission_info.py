# helper functions to gather submission info from UNFCCC website
import time
import re
from random import randrange
from typing import Dict, List
from selenium.webdriver import Firefox
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup


def get_unfccc_submission_info(
        url: str,
        driver: Firefox,
        max_tries: int=10,

) -> List[Dict[str,str]]:
    info = []
    pattern = re.compile(r"BUR ?\d")
    i = 0
    while i < max_tries:
        try:
            driver.get(url)
            html = BeautifulSoup(driver.page_source, "html.parser")
            title = html.find("h1").contents[0]
            break
        except (AttributeError, WebDriverException):
            print(f"Error fetching {url}")
            print("Retrying ...")
            time.sleep(randrange(5, 15))
            i += 1
            continue

    if i == max_tries:
        print(f"Aborting after {max_tries} tries")
    else:
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
                        if ("CRF" in doctype) or ("CRF" in title):
                            kind = "CRF"
                        elif ("SEF" in doctype) or ("SEF" in title):
                            kind = "SEF"
                        elif ("NIR" in doctype) or ("NIR" in title):
                            kind = "NIR"
                        elif "NC" in title:
                            kind = "NC"
                        elif "Status report" in title:
                            kind = "CRF"
                        else:
                            kind = "other"
                info.append({
                    "Kind": kind,
                    "Country": country,
                    "Title": title,
                    "URL": url,
                })

            print("\t".join([kind, country, title, url]))
        else:
            print(f"No files found for {url}")

    return info
