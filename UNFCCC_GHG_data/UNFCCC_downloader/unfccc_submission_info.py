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
    pattern_NC = re.compile(r"NC ?\d")
    i = 0
    last_excep = None
    while i < max_tries:
        try:
            driver.get(url)
            html = BeautifulSoup(driver.page_source, "html.parser")
            subtree = html.find(class_="document-title")
            title = subtree.find("span").contents[0]
            break
        except (AttributeError, WebDriverException) as excep:
            last_excep = excep
            print(f"Error fetching {url}")
            print("Retrying ...")
            time.sleep(randrange(5, 15))
            i += 1
            continue

    if i == max_tries:
        print(f"Aborting after {max_tries} tries.")
        print(last_excep)
    else:
        match = pattern.search(title)
        if match:
            kind = match.group(0).replace(" ", "")
        else:
            match = pattern_NC.search(title)
            if match:
                kind = match.group(0).replace(" ", "")
            else:
                kind = None

        # TODO: might improve speed by first searching for class="document-line" and then operating on thie resulting subtree for the info
        try:
            subtree = html.find_all(
                class_="field field--name-field-document-country field--type-termstore-entity-reference field--label-inline")
            country = subtree[0].find(class_="field--item").contents[0]
        except (AttributeError, IndexError) as e:
            # author as backup for country
            subtree = html.find_all(class_="field--name-field-document-ca")
            country = subtree[0].find(class_="field--item").contents[0]
        # document type
        subtree = html.find_all(
            class_="field field--name-field-document-type field--type-termstore-entity-reference field--label-hidden field--items")
        doctype = subtree[0].find(class_="field--item").contents[0]

        # get files
        sub_files = html.find(
            class_=["form-select form-control", "form-select form-control download"])
        if sub_files:
            files = sub_files.find_all("option", value=True)
            files = [file.attrs['value'] for file in files]
        else:
            files = []

        if len(files) > 0:
            for file in files:
                if not kind:
                    match = pattern.search(file.upper())
                    if match:
                        kind = match.group(0)
                    else:
                        match = pattern_NC.search(file.upper())
                        if match:
                            kind = match.group(0).replace(" ", "")
                        else:
                            if ("CRT" in doctype) or ("CRT" in title):
                                kind = "CRT"
                            elif ("NID" in doctype) or ("NID" in title):
                                kind = "NID"
                            elif ("NIR" in doctype) or ("NIR" in title):
                                kind = "NIR"
                            elif ("BRT" in doctype) or ("BTR" in title):
                                kind = "BTR"
                            else:
                                kind = "other"
                info.append({
                    "Kind": kind,
                    "Country": country,
                    "Title": title,
                    "URL": file,
                })

                print("\t".join([kind, country, title, file]))
        else:
            print(f"No files found for {url}")

    return info


def get_BTR_name_and_URL(submission_round: int) -> (str, str):
    """
        Get the name and URL of a BTR for a given number

    Parameters
    ----------
    submission_round (int)
        submission_round of the BTRs e.g. 1

    Returns
    -------
    name (str): name of the BTR submission round, e.g. 'first'
    URL (str): URL of the submission page on the UNFCCC website

    """

    if submission_round == 1:
        name = "first"
        URL = "https://unfccc.int/first-biennial-transparency-reports"
    else:
        raise ValueError(f"Submission round {submission_round} is not defined")

    return name, URL
