"""
This file holds functions that are used in CRF reading development like
adding new tables or new submission years (and according country specific
categories). Thue functions are tailored towards debug output and reading
of single years in contrast to the production functions which are tailored
towards the creation of full datasets including storage in the
"""

import pandas as pd
from typing import List
from pathlib import Path


def save_unknown_categories_info(
        unknown_categories: List[List],
        file: Path,
) -> None:
    """
    Save information on unknown categories to a csv file.

    Parameters
    __________

    unknown_categories: List[List]
        List of lists with information on the unknown categories.
        (which table, country and year, and which categories)

    file: pathlib.Path
        File including path where the data should be stored

    """
    # process unknown categories
    df_unknown_cats = pd.DataFrame(unknown_categories, columns=["Table", "Country", "Category", "Year"])

    processed_cats = []
    all_tables = df_unknown_cats["Table"].unique()
    all_years = set(df_unknown_cats["Year"].unique())
    all_years = set([year for year in all_years if isinstance(year, int)])
    all_years = set([year for year in all_years if int(year) > 1989])
    for table in all_tables:
        df_cats_current_table = df_unknown_cats[df_unknown_cats["Table"] == table]
        cats_current_table = list(df_cats_current_table["Category"].unique())
        for cat in cats_current_table:
            df_current_cat_table = df_cats_current_table[df_cats_current_table["Category"] == cat]
            all_countries = df_current_cat_table["Country"].unique()
            countries_cat = ""
            for country in all_countries:
                years_country = df_current_cat_table[df_current_cat_table["Country"] == country]["Year"].unique()
                if set(years_country) == all_years:
                    countries_cat = f"{countries_cat}; {country}"
                else:
                    countries_cat = f"{countries_cat}; {country} ({years_country})"
            processed_cats.append([table, cat, countries_cat])

    folder = file.parents[0]
    if not folder.exists:
        folder.mkdir()
    df_processed_cats = pd.DataFrame(processed_cats, columns=["Table", "Category", "Countries"])
    df_processed_cats.to_csv(file, index=False)


def save_last_row_info(
        last_row_info: List[List],
        file: Path,
    ) -> None:
    """
    Save information on data found in the last row read for a table.
    The last row read should not contain data. If it does contain data
    it is a hint that table size is larger for some countries than
    given in the specification and thus we might not read the full table.

    Parameters
    __________

    last_row_info: List[List]
        List of lists with information on the unknown categories.
        (which table, country and year, and which categories)

    file: pathlib.Path
        File including path where the data should be stored

    """
    # process last row with information messages
    df_last_row_info = pd.DataFrame(last_row_info, columns=["Table", "Country", "Category", "Year"])

    processed_last_row_info = []
    all_tables = df_last_row_info["Table"].unique()
    all_years = set(df_last_row_info["Year"].unique())
    all_years = set([year for year in all_years if isinstance(year, int)])
    all_years = set([year for year in all_years if year > 1989])
    for table in all_tables:
        df_last_row_current_table = df_last_row_info[df_last_row_info["Table"] == table]
        all_countries = df_last_row_current_table["Country"].unique()
        for country in all_countries:
            df_current_country_table = df_last_row_current_table[df_last_row_current_table["Country"] == country]
            all_categories = df_current_country_table["Category"].unique()
            cats_country = ""
            for cat in all_categories:
                years_category = df_current_country_table[df_current_country_table["Category"] == cat]["Year"].unique()
                if set(years_category) == all_years:
                    cats_country = f"{cats_country}; {cat}"
                else:
                    cats_country = f"{cats_country}; {cat} ({years_category})"
            processed_last_row_info.append([table, country, cats_country])

    folder = file.parents[0]
    if not folder.exists:
        folder.mkdir()
    df_processed_lost_row_info = pd.DataFrame(processed_last_row_info, columns=["Table", "Country", "Categories"])
    df_processed_lost_row_info.to_csv("test_last_row_info.csv", index=False)