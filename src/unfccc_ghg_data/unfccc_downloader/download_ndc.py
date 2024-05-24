"""
Download NDC submissions

TODO: needs updating
"""
import os
import re
import shutil
import time
from datetime import date
from pathlib import Path
from random import randrange

import pandas as pd
import requests

from unfccc_ghg_data.helper import downloaded_data_path_UNFCCC

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

if __name__ == "__main__":
    # we use the ndc package provided by openclimatedata which is updated on
    # a daily basis
    submissions_url = "https://github.com/openclimatedata/ndcs/raw/main/data/ndcs.csv"
    submissions = pd.read_csv(submissions_url)

    url = "https://www4.unfccc.int/sites/NDCStaging/Pages/All.aspx"

    # if we get files of this size they are error pages and we need to
    # try the download again
    # TODO error page sizes are from BUR and NC and might differ for NDCs
    # if an error page is found instead of a pdf adjust sizes here
    error_file_sizes = [212, 210]
    ndc_regex = r".*\s([A-Za-z]*)\sNDC"

    # Ensure download path and subfolders exist
    if not downloaded_data_path_UNFCCC.exists():
        downloaded_data_path_UNFCCC.mkdir(parents=True)

    new_downloaded = []

    for idx, submission in submissions.iterrows():
        print("=" * 60)
        # ndc = submission.Number
        title = submission.Title
        temp = re.findall(ndc_regex, title)
        ndc = temp[0]
        url = submission.EncodedAbsUrl
        submission_date = submission.SubmissionDate
        country = submission.Party
        country = country.replace(" ", "_")
        print(title)

        ndc_folder = "NDC_" + ndc + "_" + submission_date

        country_folder = downloaded_data_path_UNFCCC / country
        if not country_folder.exists():
            country_folder.mkdir()
        local_filename = country_folder / ndc_folder / url.split("/")[-1]
        local_filename_underscore = (
            downloaded_data_path_UNFCCC
            / country
            / ndc_folder
            / url.split("/")[-1].replace("%20", "_").replace(" ", "_")
        )
        if not local_filename.parent.exists():
            local_filename.parent.mkdir()

        # this should never be needed but in case anything goes wrong and
        # an error page is present it should be overwritten
        if local_filename_underscore.exists():
            # check file size. if 210 or 212 bytes it's the error page
            if Path(local_filename_underscore).stat().st_size in error_file_sizes:
                # found the error page. delete file
                os.remove(local_filename_underscore)

        # now we have to remove error pages, so a present file should not be overwritten
        if (not local_filename_underscore.exists()) and (
            not local_filename_underscore.is_symlink()
        ):
            i = 0  # reset counter
            while not local_filename_underscore.exists() and i < 10:  # noqa: PLR2004
                r = requests.get(url, stream=True, timeout=120)
                with open(str(local_filename_underscore), "wb") as f:
                    shutil.copyfileobj(r.raw, f)

                # check file size. if 210 or 212 bytes it's the error page
                if Path(local_filename_underscore).stat().st_size in error_file_sizes:
                    # found the error page. delete file
                    os.remove(local_filename_underscore)

                # sleep a bit to avoid running into captchas
                time.sleep(randrange(5, 15))  # noqa :S311

            if local_filename_underscore.exists():
                new_downloaded.append(submission)
                print(
                    "Download => downloaded_data/UNFCCC/"
                    + country
                    + "/"
                    + ndc_folder
                    + "/"
                    + local_filename_underscore.name
                )
            else:
                print(
                    "Failed downloading downloaded_data/UNFCCC/"
                    + country
                    + "/"
                    + ndc_folder
                    + "/"
                    + local_filename_underscore.name
                )

        else:
            print("=> Already downloaded " + local_filename_underscore.name)

    df_new_downloaded = pd.DataFrame(new_downloaded)
    df_new_downloaded.to_csv(
        downloaded_data_path_UNFCCC / f"00_new_downloads_ndc-{date.today()}.csv",
        index=False,
    )
