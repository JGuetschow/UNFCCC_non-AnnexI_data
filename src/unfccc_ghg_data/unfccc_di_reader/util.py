"""
Country group and error definitions for DI reader
"""


# reader = unfccc_di_api.UNFCCCApiReader()
# nAI_countries = list(reader.non_annex_one_reader.parties["code"])


DI_date_format = "%Y-%m-%d"
regex_date = r"([0-9]{4}-[0-9]{2}-[0-9]{2})"


class NoDIDataError(Exception):
    """
    Error raised when no DI data is available
    """

    pass
