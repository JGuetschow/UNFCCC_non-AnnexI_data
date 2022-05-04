from pathlib import Path

# 4 for use from nbs, fix
root_path = Path(__file__).parents[2].absolute()
root_path = root_path.resolve()
log_path = root_path / "log"
code_path = root_path / "code"
downloaded_data_path = root_path / "downloaded_data" / "UNFCCC"
extracted_data_path = root_path / "extracted_data" / "UNFCCC"

custom_country_mapping = {
    "EUA": "European Union",
    "EUC": "European Union",
    "FRK": "France",
    "DKE": "Denmark",
    "DNM": "Denmark",
    "GBK": "United Kingdom",
}

all_crf_countries = [
    'AUS', 'AUT', 'BEL', 'BGR', 'BLR',
    'CAN', 'CHE', 'CYP', 'CZE', 'DEU', # 10
    'DKE', 'DNK', 'DNM', 'ESP', 'EST',
    'EUA', 'EUC', 'FIN', 'FRA', 'FRK', # 20
    'GBK', 'GBR', 'GRC', 'HRV', 'HUN',
    'IRL', 'ISL', 'ITA', 'JPN', 'KAZ', # 30
    'LIE', 'LTU', 'LUX', 'LVA', 'MCO',
    'MLT', 'NLD', 'NOR', 'NZL', 'POL', # 40
    'PRT', 'ROU', 'RUS', 'SVK', 'SVN',
    'SWE', 'TUR', 'UKR', 'USA', # 49
]

class NoCRFFilesError(Exception):
    pass