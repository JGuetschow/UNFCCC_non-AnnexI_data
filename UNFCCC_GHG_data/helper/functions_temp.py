import pandas as pd
import warnings
import numpy as np


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
