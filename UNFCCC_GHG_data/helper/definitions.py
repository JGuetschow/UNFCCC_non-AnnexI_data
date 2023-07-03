import os
from pathlib import Path


def get_root_path() -> Path:
    """ get the root_path from an environment variable """
    root_path_env = os.getenv('UNFCCC_GHG_ROOT_PATH', None)
    if root_path_env is None:
        raise ValueError('UNFCCC_GHG_ROOT_PATH environment variable needs to be set')
    else:
        root_path = Path(root_path_env).resolve()
    return root_path

root_path = get_root_path()
code_path = root_path / "UNFCCC_GHG_data"
log_path = root_path / "log"
extracted_data_path = root_path / "extracted_data"
extracted_data_path_UNFCCC = extracted_data_path / "UNFCCC"
downloaded_data_path = root_path / "downloaded_data"
downloaded_data_path_UNFCCC = downloaded_data_path / "UNFCCC"
legacy_data_path = root_path / "legacy_data"
dataset_path = root_path / "datasets"
dataset_path_UNFCCC = dataset_path / "UNFCCC"


custom_country_mapping = {
    "EUA": "European Union",
    "EUC": "European Union",
    "FRK": "France",
    "DKE": "Denmark",
    "DNM": "Denmark",
    "GBK": "United Kingdom of Great Britain and Northern Ireland",
}

custom_folders = {
    'Venezeula_(Bolivarian_Republic_of)': 'VEN',
    'Venezuela_(Bolivarian_Republic_of)': 'VEN',
    'Micronesia_(Federated_State_of)': 'FSM',
    'Micronesia_(Federated_States_of)': 'FSM',
    'The_Republic_of_North_Macedonia': 'MKD',
    'Republic_of_Korea': 'KOR',
    'Bolivia_(Plurinational_State_of)': 'BOL',
    'Türkiye': 'TUR',
    'Iran_(Islamic_Republic_of)': 'IRN',
    'Côte_d’Ivoire': 'CIV',
    'Democratic_Republic_of_the_Congo': "COD",
    'European_Union': 'EUA',
    'Taiwan': 'TWN',
}

GWP_factors = {
    'SARGWP100_to_AR4GWP100': {
        'HFCS': 1.1,
        'PFCS': 1.1,
    },
    'SARGWP100_to_AR5GWP100': {
        'HFCS': 1.2,
        'PFCS': 1.2,
    },
    'SARGWP100_to_AR6GWP100': {
        'HFCS': 1.4,
        'PFCS': 1.3,
    },
}