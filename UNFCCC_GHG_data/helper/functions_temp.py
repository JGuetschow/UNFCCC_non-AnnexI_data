"""Temporary file for new functions to avoid merging issues due to different automatic formatting. Delete after merge."""

import numpy as np
import pandas as pd


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
