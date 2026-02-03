"""definitions like folders, mappings etc."""

import os
from pathlib import Path

import numpy as np
import pandas as pd


def get_root_path(root_indicator: str = ".datalad") -> Path:
    """
    Traverse up from the current script location to find the repository root.

    The root is defined by the presence of a root_indicator file or
    directory (e.g., '.git').

    Parameters
    ----------
        root_indicator
            A filename or directory name that indicates the root of the repository.

    Returns
    -------
    Path
        The path to the root directory of the repository.

    Raises
    ------
        RuntimeError: If the repository root cannot be found.
    """
    root_path_env = os.getenv("UNFCCC_GHG_ROOT_PATH", None)
    if root_path_env is None:
        current_dir = Path(__file__).resolve().parent
        while current_dir != Path(current_dir.root):
            if (current_dir / root_indicator).exists():
                return current_dir
            current_dir = current_dir.parent
        msg = f"Repository root with indicator '{root_indicator}' not found."
        raise RuntimeError(msg)
    else:
        return Path(root_path_env).resolve()


# def get_root_path() -> Path:
#     """Get the root_path from an environment variable"""
#     root_path_env = os.getenv("UNFCCC_GHG_ROOT_PATH", None)
#     if root_path_env is None:
#         raise ValueError(
#             "UNFCCC_GHG_ROOT_PATH environment variable needs to be set"
#         )
#     else:
#         root_path = Path(root_path_env).resolve()
#     return root_path


root_path = get_root_path()
code_path = root_path / "src" / "unfccc_ghg_data"
log_path = root_path / "log"
extracted_data_path = root_path / "extracted_data"
extracted_data_path_UNFCCC = extracted_data_path / "UNFCCC"
downloaded_data_path = root_path / "downloaded_data"
downloaded_data_path_UNFCCC = downloaded_data_path / "UNFCCC"
legacy_data_path = root_path / "legacy_data"
dataset_path = root_path / "datasets"
dataset_path_UNFCCC = dataset_path / "UNFCCC"

nAI_countries = list(pd.read_csv(code_path / "helper" / "DI_NAI_parties.conf")["code"])
# AI_countries = list(reader.annex_one_reader.parties["code"])
AI_countries = list(pd.read_csv(code_path / "helper" / "DI_AI_parties.conf")["code"])
additional_territories = ["HKG", "MAC", "VAT"]
# TODO: check if CRTAI countries are the same as CRF countries. It seems that Kazakhstan
#  has been eremoved

all_countries = nAI_countries + AI_countries + additional_territories

custom_country_mapping = {
    "EUA": "European Union",
    "EUC": "European Union",
    "FRK": "France",
    "DKE": "Denmark",
    "DNM": "Denmark",
    "GBK": "United Kingdom of Great Britain and Northern Ireland",
}

custom_folders = {
    "Venezeula_(Bolivarian_Republic_of)": "VEN",
    "Venezuela_(Bolivarian_Republic_of)": "VEN",
    "Micronesia_(Federated_State_of)": "FSM",
    "Micronesia_(Federated_States_of)": "FSM",
    "The_Republic_of_North_Macedonia": "MKD",
    "Republic_of_Korea": "KOR",
    "Bolivia_(Plurinational_State_of)": "BOL",
    "Türkiye": "TUR",
    "Iran_(Islamic_Republic_of)": "IRN",
    "Côte_d`Ivoire": "CIV",
    "Côte_d’Ivoire": "CIV",  # noqa: RUF001
    "Democratic_Republic_of_the_Congo": "COD",
    "European_Union": "EUA",
    "Taiwan": "TWN",
}

GWP_factors = {
    "SARGWP100_to_AR4GWP100": {
        "HFCS": 1.1,
        "PFCS": 1.1,
        "UnspMixOfHFCs": 1.1,
        "UnspMixOfPFCs": 1.1,
        "FGASES": 1.1,
        "other halogenated gases": 1.1,
        "UnspMixOfHFCsPFCs": 1.1,
    },
    "SARGWP100_to_AR5GWP100": {
        "HFCS": 1.2,
        "PFCS": 1.2,
        "UnspMixOfHFCs": 1.2,
        "UnspMixOfPFCs": 1.2,
        "FGASES": 1.2,
        "other halogenated gases": 1.2,
        "UnspMixOfHFCsPFCs": 1.2,
    },
    "SARGWP100_to_AR6GWP100": {
        "HFCS": 1.4,
        "PFCS": 1.3,
        "UnspMixOfHFCs": 1.4,
        "UnspMixOfPFCs": 1.3,
        "FGASES": 1.35,
        "other halogenated gases": 1.35,
        "UnspMixOfHFCsPFCs": 1.35,
    },
    "AR4GWP100_to_SARGWP100": {
        "HFCS": 0.91,
        "PFCS": 0.91,
        "UnspMixOfHFCs": 0.91,
        "UnspMixOfPFCs": 0.91,
        "FGASES": 0.91,
        "other halogenated gases": 0.91,
        "UnspMixOfHFCsPFCs": 0.91,
    },
    "AR4GWP100_to_AR5GWP100": {
        "HFCS": 1.1,
        "PFCS": 1.1,
        "UnspMixOfHFCs": 1.1,
        "UnspMixOfPFCs": 1.1,
        "FGASES": 1.1,
        "other halogenated gases": 1.1,
        "UnspMixOfHFCsPFCs": 1.1,
    },
    "AR4GWP100_to_AR6GWP100": {
        "HFCS": 1.27,
        "PFCS": 1.18,
        "UnspMixOfHFCs": 1.27,
        "UnspMixOfPFCs": 1.18,
        "FGASES": 1.23,
        "other halogenated gases": 1.23,
        "UnspMixOfHFCsPFCs": 1.23,
    },
    "AR5GWP100_to_SARGWP100": {
        "HFCS": 0.83,
        "PFCS": 0.83,
        "UnspMixOfHFCs": 0.83,
        "UnspMixOfPFCs": 0.83,
        "FGASES": 0.83,
        "other halogenated gases": 0.83,
        "UnspMixOfHFCsPFCs": 0.83,
    },
    "AR5GWP100_to_AR4GWP100": {
        "HFCS": 0.91,
        "PFCS": 0.91,
        "UnspMixOfHFCs": 0.91,
        "UnspMixOfPFCs": 0.91,
        "FGASES": 0.91,
        "other halogenated gases": 0.91,
        "UnspMixOfHFCsPFCs": 0.91,
    },
    "AR5GWP100_to_AR6GWP100": {
        "HFCS": 1.17,
        "PFCS": 1.08,
        "UnspMixOfHFCs": 1.17,
        "UnspMixOfPFCs": 1.08,
        "FGASES": 1.125,
        "other halogenated gases": 1.125,
        "UnspMixOfHFCsPFCs": 1.125,
    },
    ### All TAR factors just averages between SAR and AR4
    "TARGWP100_to_SARGWP100": {
        "HFCS": 0.953,
        "PFCS": 0.953,
        "UnspMixOfHFCs": 0.953,
        "UnspMixOfPFCs": 0.953,
        "FGASES": 0.953,
        "other halogenated gases": 0.953,
        "UnspMixOfHFCsPFCs": 0.953,
    },
    "SARGWP100_to_TARGWP100": {
        "HFCS": 1.0488,
        "PFCS": 1.0488,
        "UnspMixOfHFCs": 1.0488,
        "UnspMixOfPFCs": 1.0488,
        "FGASES": 1.0488,
        "other halogenated gases": 1.0488,
        "UnspMixOfHFCsPFCs": 1.0488,
    },
    "TARGWP100_to_AR4GWP100": {
        "HFCS": 1.0488,
        "PFCS": 1.0488,
        "UnspMixOfHFCs": 1.0488,
        "UnspMixOfPFCs": 1.0488,
        "FGASES": 1.0488,
        "other halogenated gases": 1.0488,
        "UnspMixOfHFCsPFCs": 1.0488,
    },
    "AR4GWP100_to_TARGWP100": {
        "HFCS": 0.953,
        "PFCS": 0.953,
        "UnspMixOfHFCs": 0.953,
        "UnspMixOfPFCs": 0.953,
        "FGASES": 0.953,
        "other halogenated gases": 0.953,
        "UnspMixOfHFCsPFCs": 0.953,
    },
    "TARGWP100_to_AR5GWP100": {
        "HFCS": 1.15,
        "PFCS": 1.15,
        "UnspMixOfHFCs": 1.15,
        "UnspMixOfPFCs": 1.15,
        "FGASES": 1.15,
        "other halogenated gases": 1.15,
        "UnspMixOfHFCsPFCs": 1.15,
    },
    "AR5GWP100_to_TARGWP100": {
        "HFCS": 0.87,
        "PFCS": 0.87,
        "UnspMixOfHFCs": 0.87,
        "UnspMixOfPFCs": 0.87,
        "FGASES": 0.87,
        "other halogenated gases": 0.87,
        "UnspMixOfHFCsPFCs": 0.87,
    },
    "TARGWP100_to_AR6GWP100": {
        "HFCS": 1.335,
        "PFCS": 1.24,
        "UnspMixOfHFCs": 1.335,
        "UnspMixOfPFCs": 1.24,
        "FGASES": 1.29,
        "other halogenated gases": 1.35,
        "UnspMixOfHFCsPFCs": 1.35,
    },
    "AR6GWP100_to_TARGWP100": {
        "HFCS": 0.75,
        "PFCS": 0.806,
        "UnspMixOfHFCs": 0.75,
        "UnspMixOfPFCs": 0.806,
        "FGASES": 0.776,
        "other halogenated gases": 0.741,
        "UnspMixOfHFCsPFCs": 0.741,
    },
}

gwps_for_basket_aggregation = [
    "SARGWP100",
    "AR4GWP100",
    "AR5GWP100",
    "AR6GWP100",
]  # 'TARGWP100'

gas_baskets = {}
for gwp in gwps_for_basket_aggregation:
    gas_baskets.update(
        {
            f"HFCS ({gwp})": [
                "HFC23",
                "HFC32",
                "HFC41",
                "HFC125",
                "HFC134",
                "HFC134a",
                "HFC143",
                "HFC143a",
                "HFC152",
                "HFC152a",
                "HFC161",
                "HFC227ea",
                "HFC236cb",
                "HFC236ea",
                "HFC236fa",
                "HFC245ca",
                "HFC245fa",
                "HFC365mfc",
                "HFC404a",
                "HFC407c",
                "HFC410a",
                "HFC507a",
                "HFC4310mee",
                f"UnspMixOfHFCs ({gwp})",
            ],
            f"PFCS ({gwp})": [
                "CF4",
                "C2F6",
                "C3F8",
                "C4F10",
                "C5F12",
                "C6F14",
                "C10F18",
                "cC3F6",
                "cC4F8",
                "cC4F8",
                f"UnspMixOfPFCs ({gwp})",
            ],
            f"FGASES ({gwp})": [
                f"HFCS ({gwp})",
                f"PFCS ({gwp})",
                "SF6",
                "NF3",
                f"UnspMixOfHFCsPFCs ({gwp})",
            ],
            f"KYOTOGHG ({gwp})": [
                "CO2",
                "CH4",
                "N2O",
                f"FGASES ({gwp})",
            ],
        }
    )


compression = dict(zlib=True, complevel=9)

str_value_mapping = {
    "MO": np.nan,
    "IE/NE": 0,
    "NO;NE": 0,
    "NA;NO": 0,
    "NO; NE": 0,
    'NO"': np.nan,
    "CH4": np.nan,
    "N/A": np.nan,
}

nan_values_crf_crt = [
    "-1.#IND",
    "-1.#QNAN",
    "-NaN",
    "-nan",
    "1.#IND",
    "1.#QNAN",
    "NULL",
    "NaN",
    "",
    " ",
]
