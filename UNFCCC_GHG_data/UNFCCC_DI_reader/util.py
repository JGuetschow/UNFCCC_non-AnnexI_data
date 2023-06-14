import unfccc_di_api
import pandas as pd
from UNFCCC_GHG_data.helper import code_path

#reader = unfccc_di_api.UNFCCCApiReader()
#nAI_countries = list(reader.non_annex_one_reader.parties["code"])
nAI_countries = list(pd.read_csv(code_path / 'UNFCCC_DI_reader' /
                                 'DI_NAI_parties.conf')["code"])
#AI_countries = list(reader.annex_one_reader.parties["code"])
AI_countries = list(pd.read_csv(code_path / 'UNFCCC_DI_reader' /
                                'DI_AI_parties.conf')["code"])

DI_date_format = '%Y-%m-%d'
regex_date = r"([0-9]{4}-[0-9]{2}-[0-9]{2})"

class NoDIDataError(Exception):
    pass


