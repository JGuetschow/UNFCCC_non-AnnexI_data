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
        'UnspMixOfHFCs': 1.1,
        'UnspMixOfPFCs': 1.1,
        'FGASES': 1.1,
    },
    'SARGWP100_to_AR5GWP100': {
        'HFCS': 1.2,
        'PFCS': 1.2,
        'UnspMixOfHFCs': 1.2,
        'UnspMixOfPFCs': 1.2,
        'FGASES': 1.2,
    },
    'SARGWP100_to_AR6GWP100': {
        'HFCS': 1.4,
        'PFCS': 1.3,
        'UnspMixOfHFCs': 1.4,
        'UnspMixOfPFCs': 1.3,
        'FGASES': 1.35,
    },
    'AR4GWP100_to_SARGWP100': {
        'HFCS': 0.91,
        'PFCS': 0.91,
        'UnspMixOfHFCs': 0.91,
        'UnspMixOfPFCs': 0.91,
        'FGASES': 0.91,
    },
    'AR4GWP100_to_AR5GWP100': {
        'HFCS': 1.1,
        'PFCS': 1.1,
        'UnspMixOfHFCs': 1.1,
        'UnspMixOfPFCs': 1.1,
        'FGASES': 1.1,
    },
    'AR4GWP100_to_AR6GWP100': {
        'HFCS': 1.27,
        'PFCS': 1.18,
        'UnspMixOfHFCs': 1.27,
        'UnspMixOfPFCs': 1.18,
        'FGASES': 1.23,
    },
    'AR5GWP100_to_SARGWP100': {
        'HFCS': 0.83,
        'PFCS': 0.83,
        'UnspMixOfHFCs': 0.83,
        'UnspMixOfPFCs': 0.83,
        'FGASES': 0.83,
    },
    'AR5GWP100_to_AR4GWP100': {
        'HFCS': 0.91,
        'PFCS': 0.91,
        'UnspMixOfHFCs': 0.91,
        'UnspMixOfPFCs': 0.91,
        'FGASES': 0.91,
    },
    'AR5GWP100_to_AR6GWP100': {
        'HFCS': 1.17,
        'PFCS': 1.08,
        'UnspMixOfHFCs': 1.17,
        'UnspMixOfPFCs': 1.08,
        'FGASES': 1.125,
    },
}

gas_baskets = {
    'HFCS (SARGWP100)': ['HFC23', 'HFC32', 'HFC41', 'HFC125', 'HFC134',
                         'HFC134a', 'HFC143',  'HFC143a', 'HFC152', 'HFC152a',
                         'HFC227ea', 'HFC161', 'HFC227EA', 'HFC236cb', 'HFC236ea',
                         'HFC236fa', 'HFC245ca', 'HFC245fa', 'HFC365mfc', 'HFC404a',
                         'HFC407c', 'HFC410a', 'HFC4310mee',
                         'UnspMixOfHFCs (SARGWP100)'],
    'HFCS (AR4GWP100)': ['HFC23', 'HFC32', 'HFC41', 'HFC125', 'HFC134',
                         'HFC134a', 'HFC143',  'HFC143a', 'HFC152', 'HFC152a',
                         'HFC227ea', 'HFC161', 'HFC227EA', 'HFC236cb', 'HFC236ea',
                         'HFC236fa', 'HFC245ca', 'HFC245fa', 'HFC365mfc', 'HFC404a',
                         'HFC407c', 'HFC410a', 'HFC4310mee',
                         'UnspMixOfHFCs (AR4GWP100)'],
    'HFCS (AR5GWP100)': ['HFC23', 'HFC32', 'HFC41', 'HFC125', 'HFC134',
                         'HFC134a', 'HFC143',  'HFC143a', 'HFC152', 'HFC152a',
                         'HFC227ea', 'HFC161', 'HFC227EA', 'HFC236cb', 'HFC236ea',
                         'HFC236fa', 'HFC245ca', 'HFC245fa', 'HFC365mfc', 'HFC404a',
                         'HFC407c', 'HFC410a', 'HFC4310mee',
                         'UnspMixOfHFCs (AR5GWP100)'],
    'HFCS (AR6GWP100)': ['HFC23', 'HFC32', 'HFC41', 'HFC125', 'HFC134',
                         'HFC134a', 'HFC143',  'HFC143a', 'HFC152', 'HFC152a',
                         'HFC227ea', 'HFC161', 'HFC227EA', 'HFC236cb', 'HFC236ea',
                         'HFC236fa', 'HFC245ca', 'HFC245fa', 'HFC365mfc', 'HFC404a',
                         'HFC407c', 'HFC410a', 'HFC4310mee',
                         'UnspMixOfHFCs (AR6GWP100)'],
    'PFCS (SARGWP100)': ['CF4', 'C2F6', 'C3F8', 'C4F10', 'C5F12', 'C6F14',
                         'C10F18', 'cC3F6', 'cC4F8', 'UnspMixOfPFCs (SARGWP100)'],
    'PFCS (AR4GWP100)': ['CF4', 'C2F6', 'C3F8', 'C4F10', 'C5F12', 'C6F14',
                         'C10F18', 'cC3F6', 'cC4F8', 'UnspMixOfPFCs (AR4GWP100)'],
    'PFCS (AR5GWP100)': ['CF4', 'C2F6', 'C3F8', 'C4F10', 'C5F12', 'C6F14',
                         'C10F18', 'cC3F6', 'cC4F8', 'UnspMixOfPFCs (AR5GWP100)'],
    'PFCS (AR6GWP100)': ['CF4', 'C2F6', 'C3F8', 'C4F10', 'C5F12', 'C6F14',
                         'C10F18', 'cC3F6', 'cC4F8', 'UnspMixOfPFCs (AR6GWP100)'],
    'FGASES (SARGWP100)': ['HFCS (SARGWP100)', 'PFCS (SARGWP100)', 'SF6', 'NF3'],
    'FGASES (AR4GWP100)': ['HFCS (AR4GWP100)', 'PFCS (AR4GWP100)', 'SF6', 'NF3'],
    'FGASES (AR5GWP100)':['HFCS (AR5GWP100)', 'PFCS (AR5GWP100)', 'SF6', 'NF3'],
    'FGASES (AR6GWP100)':['HFCS (AR6GWP100)', 'PFCS (AR6GWP100)', 'SF6', 'NF3'],
    'KYOTOGHG (SARGWP100)': ['CO2', 'CH4', 'N2O', 'SF6', 'NF3', 'HFCS (SARGWP100)',
                          'PFCS (SARGWP100)'],
    'KYOTOGHG (AR4GWP100)': ['CO2', 'CH4', 'N2O', 'SF6', 'NF3', 'HFCS (AR4GWP100)',
                          'PFCS (AR4GWP100)'],
    'KYOTOGHG (AR5GWP100)': ['CO2', 'CH4', 'N2O', 'SF6', 'NF3', 'HFCS (AR5GWP100)',
                            'PFCS (AR5GWP100)'],
    'KYOTOGHG (AR6GWP100)': ['CO2', 'CH4', 'N2O', 'SF6', 'NF3', 'HFCS (AR6GWP100)',
                            'PFCS (AR6GWP100)'],
}

compression = dict(zlib=True, complevel=9)