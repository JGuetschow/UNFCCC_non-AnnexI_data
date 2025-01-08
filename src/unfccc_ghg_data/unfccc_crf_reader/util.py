"""Definitions and errors for the CRF reader"""

all_crf_countries = [
    "AUS",
    "AUT",
    "BEL",
    "BGR",
    "BLR",
    "CAN",
    "CHE",
    "CYP",
    "CZE",
    "DEU",  # 10
    "DKE",
    "DNK",
    "DNM",
    "ESP",
    "EST",
    "EUA",
    "EUC",
    "FIN",
    "FRA",
    "FRK",  # 20
    "GBK",
    "GBR",
    "GRC",
    "HRV",
    "HUN",
    "IRL",
    "ISL",
    "ITA",
    "JPN",
    "KAZ",  # 30
    "LIE",
    "LTU",
    "LUX",
    "LVA",
    "MCO",
    "MLT",
    "NLD",
    "NOR",
    "NZL",
    "POL",  # 40
    "PRT",
    "ROU",
    "RUS",
    "SVK",
    "SVN",
    "SWE",
    "TUR",
    "UKR",
    "USA",  # 49
]

BTR_urls = {
    1: "https://unfccc.int/first-biennial-transparency-reports",
}


class NoCRFFilesError(Exception):
    """Error raised when no CRF files are found"""

    pass
