"""Temporary file for new functions to avoid merging issues due to different automatic formatting. Delete after merge."""

import pandas as pd
import warnings
import numpy as np



def find_and_replace_values(
    df: pd.DataFrame,
    replace_info: list[tuple[str | float]],
    category_column: str,
    entity_column: str = "entity",
) -> pd.DataFrame:
    """
    Find values and replace single values in a dataframe.

    Input
    -----
    df
        Input data frame
    replace_info
        Category, entity, year, and new value. Don't put a new value if you would like to replace with nan.
        For example [("3.C", "CO", "2019", 3.423)] or [("3.C", "CO", "2019")]
    category_column
        The name of the column that contains the categories.
    entity_column
        The name of the column that contains the categories.

    Output
    ------
        Data frame with updated values.

    """
    for replace_info_value in replace_info:
        category = replace_info_value[0]
        entity = replace_info_value[1]
        year = replace_info_value[2]

        if len(replace_info_value) == 4:
            new_value = replace_info_value[3]
        elif len(replace_info_value) == 3:
            new_value = np.nan
        else:
            raise AssertionError(
                f"Expected tuple of length 3 or 4. Got {replace_info_value}"
            )

        index = df.loc[
            (df[category_column] == category) & (df[entity_column] == entity),
        ].index[0]

        # pandas recommends using .at[] for changing single values
        df.at[index, year] = new_value
        print(f"Set value for {category}, {entity}, {year} to {new_value}.")

    return df


def assert_values(
        df: pd.DataFrame,
        test_case: tuple[str | float | int],
        category_column: str = "category (IPCC1996_2006_GIN_Inv)",
        entity_column: str = "entity",
) -> None:
    """
    Check if a value in a dataframe matches the expected value.
    Input
    -----
    df
        The data frame to check.
    test_case
        The combination of parameters and the expected value.
        Use the format (<category>, <entity>, <year>, <expected_value>).
    category_column
        The columns where to look for the category.
    entity_column
        The column where to look for the entity.
    """
    category = test_case[0]
    entity = test_case[1]
    year = test_case[2]
    expected_value = test_case[3]

    assert isinstance(expected_value, (float, int)), "This function only works for numbers. Use assert_nan_values to check for NaNs and empty values."

    arr = df.loc[
        (df[category_column] == category) & (df[entity_column] == entity), year
    ].values

    # Assert the category exists in the data frame
    assert (
            category in df[category_column].unique()
    ), f"{category} is not a valid category. Choose from {df[category_column].unique()}"

    # Assert the entity exists in the data frame
    assert (
            entity in df[entity_column].unique()
    ), f"{entity} is not a valid entity. Choose from {df[entity_column].unique()}"

    assert (
            arr.size > 0
    ), f"No value found for category {category}, entity {entity}, year {year}!"

    assert (
            arr.size <= 1
    ), f"More than one value found for category {category}, entity {entity}, year {year}!"

    assert (
            arr[0] == test_case[3]
    ), f"Expected value {expected_value}, actual value is {arr[0]}"

    print(
        f"Value for category {category}, entity {entity}, year {year} is as expected."
    )

def assert_nan_values(
        df: pd.DataFrame,
        test_case: tuple[str, ...],
        category_column: str = "category (IPCC1996_2006_GIN_Inv)",
        entity_column: str = "entity",
) -> None:
    """
    Check if values that are empty or NE or NE1 in the PDF tables
    are not present in the dataset.

    Input
    -----
    df
        The data frame to check.
    test_case
        The combination of input parameters.
        Use the format (<category>, <entity>, <year>).
    category_column
        The columns where to look for the category.
    entity_column
        The column where to look for the entity.

    """
    category = test_case[0]
    entity = test_case[1]
    year = test_case[2]

    if category not in df[category_column].unique():
        warning_string = f"{category} is not in the data set. Either all values for this category are NaN or the category never existed in the data set."
        warnings.warn(warning_string)
        return

    if entity not in df[entity_column].unique():
        warning_string = f"{entity} is not in the data set. Either all values for this entity are NaN or the category never existed in the data set."
        warnings.warn(warning_string)
        return

    arr = df.loc[
        (df[category_column] == category) & (df[entity_column] == entity), year
    ].values

    assert np.isnan(arr[0]), f"Value is {arr[0]} and not NaN."

    print(f"Value for category {category}, entity {entity}, year {year} is NaN.")
