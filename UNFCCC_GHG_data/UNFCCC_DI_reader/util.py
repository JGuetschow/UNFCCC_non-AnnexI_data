from pathlib import Path
import unfccc_di_api
# imports for copied functions
import pycountry

root_path = Path(__file__).parents[2].absolute()
root_path = root_path.resolve()
log_path = root_path / "log"
code_path = root_path / "UNFCCC_GHG_data"
downloaded_data_path = root_path / "downloaded_data" / "UNFCCC"
extracted_data_path = root_path / "extracted_data" / "UNFCCC"

reader = unfccc_di_api.UNFCCCApiReader()

nAI_countries = list(reader.non_annex_one_reader.parties["code"])
AI_countries = list(reader.annex_one_reader.parties["code"])

DI_date_format = '%Y-%m-%d'
regex_date = r"([0-9]{4}-[0-9]{2}-[0-9]{2})"

class NoDIDataError(Exception):
    pass


# the following is copied from other sub-packages
# TODO: move these functions to common location to allow easy importing into all modules
custom_country_mapping = {
    "EUA": "European Union",
    "EUC": "European Union",
    "FRK": "France",
    "DKE": "Denmark",
    "DNM": "Denmark",
    "GBK": "United Kingdom of Great Britain and Northern Ireland",
}


def get_country_name(
        country_code: str,
) -> str:
    """get country name from code """
    if country_code in custom_country_mapping:
        country_name = custom_country_mapping[country_code]
    else:
        try:
            country = pycountry.countries.get(alpha_3=country_code)
            country_name = country.name
        except:
            raise ValueError(f"Country code {country_code} can not be mapped to "
                             f"any country")

    return country_name


def get_country_code(
        country_name: str,
)->str:
    """
    obtain country code. If the input is a code it will be returned, if the input
    is not a three letter code a search will be performed

    Parameters
    __________
    country_name: str
        Country code or name to get the three-letter code for.

    """
    try:
        # check if it's a 3 letter code
        country = pycountry.countries.get(alpha_3=country_name)
        country_code = country.alpha_3
    except:
        try:
            country = pycountry.countries.search_fuzzy(country_name)
        except:
            raise ValueError(f"Country name {country_name} can not be mapped to "
                             f"any country code")
        if len(country) > 1:
            country_code = None
            for current_country in country:
                if current_country.name == country_name:
                    country_code = current_country.alpha_3
            if country_code is None:
                raise ValueError(f"Country name {country_name} has {len(country)} "
                                 f"possible results for country codes.")

        country_code = country[0].alpha_3

    return country_code