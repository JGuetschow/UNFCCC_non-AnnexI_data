"""Config for Mexico's BUR3

Full configuration including PRIMAP2 conversion config and metadata

"""

import pandas as pd


def fix_rows(
    data: pd.DataFrame, rows_to_fix: list, col_to_use: str, n_rows: int
) -> pd.DataFrame:
    """
    Combine split rows

    This function combines rows which have been split into several rows during data
    reading from pdf because they contained line breaks.

    Parameters
    ----------
    data: pd.DataFrame
        The data to work with
    rows_to_fix: list
        List of values for which to fix rows
    col_to_use: str
        column to use to find the rows to merge
    n_rows: int
        How many rows to combine for each row found. e.g. 3 means combine the found
        row with the following two rows. Negative values are used for more
        complicated situations where the rows to merge are also before the position
        of the value that indicates the merge. See code for details

    Returns
    -------
        pandas DataFrame with combined rows. The individual rows are removed

    TODO: move function to helper module (make sure to have one function that works
     for all cases)
    """
    for row in rows_to_fix:
        # print(row)
        # find the row number and collect the row and the next two rows
        index = data.loc[data[col_to_use] == row].index
        if not list(index):
            print(f"Can't merge split row {row}")
            print(data[col_to_use])
        print(f"Merging split row {row}")
        indices_to_drop = []
        ####print(index)
        for item in index:
            loc = data.index.get_loc(item)
            ####print(data[col_to_use].loc[loc + 1])
            if n_rows == -2:  # noqa: PLR2004
                locs_to_merge = list(range(loc - 1, loc + 1))
                loc_to_check = loc - 1
            elif n_rows == -6:  # noqa: PLR2004
                locs_to_merge = list(range(loc - 3, loc + 3))
                loc_to_check = loc - 3
            elif n_rows == -3:  # noqa: PLR2004
                locs_to_merge = list(range(loc - 1, loc + 2))
                loc_to_check = loc - 1
            else:
                locs_to_merge = list(range(loc, loc + n_rows))
                loc_to_check = loc + 1

            if (not data[col_to_use].loc[loc_to_check]) or n_rows == 2:  # noqa: PLR2004
                rows_to_merge = data.iloc[locs_to_merge]
                indices_to_merge = rows_to_merge.index
                # replace numerical NaN values
                ####print(rows_to_merge)
                rows_to_merge = rows_to_merge.fillna("")
                ####print("fillna")
                ####print(rows_to_merge)
                # join the three rows
                new_row = rows_to_merge.agg(" ".join)
                # replace the double spaces that are created
                # must be done here and not at the end as splits are not always
                # the same and join would produce different col values
                new_row = new_row.str.replace("  ", " ")
                new_row = new_row.str.strip()
                # new_row = new_row.str.replace("N O", "NO")
                # new_row = new_row.str.replace(", N", ",N")
                # new_row = new_row.str.replace("- ", "-")
                data.loc[indices_to_merge[0]] = new_row
                indices_to_drop = indices_to_drop + list(indices_to_merge[1:])

        data = data.drop(indices_to_drop)
        data = data.reset_index(drop=True)
    return data


page_defs = {
    "118": {
        "camelot": {
            "table_areas": ["49,602,551,73"],
            "columns": ["223,277,314,348,392,422,446,483"],
            "split_text": False,
            "flavor": "stream",
        },
        "rows_to_fix": {
            -6: ["Categorías de fuentes y"],
            3: [
                "Todas las emisiones y las absorciones",
                "Todas las emisiones (sin [3B] Tierra ni",
                "[1A] Actividades de quema del",
                "[1A2] Industrias manufactura y de la",
                "[1B] Emisiones fugitivas provenientes de",
                "[2] Procesos industriales y uso de",
            ],
        },
    },
    "119": {
        "camelot": {
            "table_areas": ["49,650,551,77"],
            "columns": ["228,275,317,352,394,421,446,483"],
            "split_text": True,
            "flavor": "stream",
        },
        "rows_to_fix": {
            -6: ["Categorías de fuentes y"],
            3: [
                "[2B4] Producción de caprolactama,",
                "[2B8] Producción petroquímica y negro",
                "[2D] Uso de productos no energéticos de",
                "[2E1] Circuitos integrados o",
            ],
        },
    },
    "120": {
        "camelot": {
            "table_areas": ["49,650,551,77"],
            "columns": ["223,277,314,348,392,422,446,483"],
            "split_text": False,
            "flavor": "stream",
        },
        "rows_to_fix": {
            -6: ["Categorías de fuentes y"],
            -3: ["[3B] Tierra"],
            3: [
                "[2F] Uso de productos sustitutos de las",
                "[2G] Manufactura y utilización de otros",
                "[3] Agricultura, silvicultura y otros usos",
            ],
            2: [
                "[2H2] Industria de la alimentación y las",
                "[2G2] SF₆ y PFC de otros usos de",
            ],
        },
    },
    "121": {
        "camelot": {
            "table_areas": ["49,650,551,70"],
            "columns": ["223,277,314,348,392,422,446,483"],
            "split_text": False,
            "flavor": "stream",
        },
        "rows_to_fix": {
            -6: ["Categorías de fuentes y"],
            -3: ["[3B1] Tierra forestales"],
            3: [
                "[3C] Fuentes agregadas y fuentes de",
                "[3C1] Emisiones de GEI por quemado de",
                "[3C4] Emisiones directas de los N₂O de",
                "[3C5] Emisiones indirectas de los N₂O de",
                "[3C6] Emisiones indirectas de los N₂O de",
                "[4A1] Sitios gestionados de eliminación",
                "[4A2] Sitios no controlados de",
                "[4A3] Tiraderos a cielo abierto para",
                "[4B] Tratamiento biológico de los",
            ],
        },
    },
    "122": {
        "camelot": {
            "table_areas": ["49,650,551,404"],
            "columns": ["223,277,314,348,392,422,446,483"],
            "split_text": False,
            "flavor": "stream",
        },
        "rows_to_fix": {
            -6: ["Categorías de fuentes y"],
            3: [
                "[4C] Incineración y quema a cielo abierto",
                "[4C1] Incineración de residuos peligrosos",
                "[4C2] Quema a cielo abierto de residuos",
                "[4D] Tratamiento y eliminación de aguas",
                "[4D1] Tratamiento y eliminación de",
                "[4D2] Tratamiento y eliminación de",
            ],
        },
    },
}
