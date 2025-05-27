"""
configuration for South Korea's 2023 inventory

Contains category name translations and information on category mapping and aggregation
"""

import numpy as np
import pandas as pd

from unfccc_ghg_data.helper import code_path

terminology_proc = "IPCC2006_PRIMAP"
gwp_to_use = "AR5GWP100"

filename_sectors = (
    code_path / "unfccc_reader" / "Republic_of_Korea" / "sector_mapping_INV2024.csv"
)

sector_mapping = pd.read_csv(filename_sectors)
# read from csv
cat_name_translations = dict(
    zip(sector_mapping["Original"], sector_mapping["Translation"])
)
cat_codes = dict(zip(sector_mapping["Original"], sector_mapping["Sector"]))
mapping_to_IPCC2006 = dict(
    zip(sector_mapping["Sector"], sector_mapping["Sector IPCC2006"])
)
mapping_to_IPCC2006 = {
    source: target
    for source, target in mapping_to_IPCC2006.items()
    if target is not np.nan
}


fix_rows = {
    "1. 소": {"A.  장내발효": "A.", "B.  가축분뇨처리": "B."},
    "2. 양(면양)": {"A.  장내발효": "A.", "B.  가축분뇨처리": "B."},
    "3. 돼지": {"A.  장내발효": "A.", "B.  가축분뇨처리": "B."},
    "4. 기타 가축": {"A.  장내발효": "A.", "B.  가축분뇨처리": "B."},
    "H. 기타": {"G. 수확된 목재제품": "4.", "3.  제품사용의 아산화질소": "2."},
    "    내륙습지": {"1. 습지로 유지된 습지": "1.", "2. 타토지에서 전용된 습지": "2."},
    "3.  기타": {"2. 파라핀 왁스 사용": "D.", "2.  식품 및 음료": "H."},
    # "7. 기타": {
    #     "  6. 섬유 및 가죽": "2.",
    #     "2.  식품 및 음료": "H."
    # },
}

coords_terminologies_2006 = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

processing_info_country = {
    "basket_copy": {
        "GWPs_to_add": ["SARGWP100", "AR4GWP100", "AR6GWP100"],
        "entities": ["HFCS", "PFCS"],
        "source_GWP": gwp_to_use,
    },
    "remove_ts": {
        "3B2_GHG": {  # rounding errors
            "entities": ["KYOTOGHG (AR5GWP100)"],
            "category (IPCC2006_KOR_INV)": ["3.B.2"],
            "time": [
                "1994",
                "1996",
                "1997",
                "1998",
                "2001",
                "2003",
                "2004",
                "2007",
                "2017",
                "2019",
                "2020",
            ],
        },
    },
}

category_conversion = {
    "mapping": mapping_to_IPCC2006,
    "aggregate": {
        "1.A.3.a": {
            "sources": ["1.A.3.a.2"],
            # "name": "Civil Aviation"
        },  # aviation
        "1.A.3.d": {
            "sources": ["1.A.3.d.2"],
            # "name": "Water-borne Navigation"
        },  # shipping
        "3.A.2": {
            "sources": ["3.A.2.a", "3.A.2.c", "3.A.2.h", "3.A.2.j"],
            # "name": "Livestock"
        },
        "3.A": {
            "sources": ["3.A.1", "3.A.2"],
            # "name": "Livestock"
        },
        "3.B": {
            "sources": ["3.B.1", "3.B.2", "3.B.3", "3.B.4", "3.B.5", "3.B.6"],
            # "name": "Land"
        },
        "3.C.1": {
            "sources": ["3.C.1.b", "3.C.1.c"],
            # "name": "Emissions from Biomass Burning"
        },
        "M.3.C.1.AG": {
            "sources": ["3.C.1.b", "3.C.1.c"],
            # "name": "Emissions from Biomass Burning (Agriculture)"
        },
        "3.C": {
            "sources": ["3.C.1", "3.C.2", "3.C.3", "3.C.4", "3.C.5", "3.C.6", "3.C.7"],
            # "name": "Aggregate sources and non-CO2 emissions sources on land",
        },
        "M.3.C.AG": {
            "sources": [
                "M.3.C.1.AG",
                "3.C.2",
                "3.C.3",
                "3.C.4",
                "3.C.5",
                "3.C.6",
                "3.C.7",
            ],
            # "name": "Aggregate sources and non-CO2 emissions sources on land ("
            #        "Agriculture)",
        },
        "M.AG.ELV": {
            "sources": ["M.3.C.AG"],
            # "name": "Agriculture excluding livestock"
        },
        "3.D.2": {
            "sources": ["M.3.D.2.LU"],
            # "name": "Other (please specify)"
        },
        "3.D": {
            "sources": ["3.D.1", "3.D.2"],
            # "name": "Other"
        },
        "M.3.D.LU": {
            "sources": ["3.D.1", "M.3.D.2.LU"],
            # "name": "Other"
        },
        # consistency check: reaggregate M.AG and M.LULUCF
        "M.LULUCF": {
            "sources": ["3.B", "M.3.D.LU"],
            # "name": "Land Use, Land Use Change, and Forestry"
        },
        "M.AG": {
            "sources": ["3.A", "M.AG.ELV"],
            # "name": "Agriculture"
        },
        # AFOLU
        "3": {
            "sources": ["3.A", "3.B", "3.C", "3.D"],
            # "name": "AFOLU"
        },
    },
}
