"""
configuration for South Korea's 2023 inventory

Contains category name translations and information on category mapping and aggregation
"""

terminology_proc = "IPCC2006_PRIMAP"
gwp_to_use = "AR5GWP100"

# definitions for conversion to interchange format
time_format = "%Y"

coords_cols = {
    "category": "Sector",
    "entity": "Gas",
    "unit": "Unit",
}

add_coords_cols = {
    "orig_cat_name": ["orig_cat_name", "category"],
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC1996_PRIMAP",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "PHL-GHG-Inventory",
    "provenance": "measured",
    "area": "PHL",
    "scenario": "NICCDIES2025",
}

coords_value_mapping = {
    "category": {
        "Energy and Transport": "1",
        "Industry": "2",
        "Agriculture": "3",
        "Waste": "5",
        "LULUCF": "4",
        "Total excl. LULUCF": "M.0.EL",
        "Total incl. LULUCF": "0",
    },
}

filter_remove = {}

filter_keep = {}

meta_data = {
    "references": "https://niccdies.climate.gov.ph/ghg-inventory/national",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Philippines: National Greenhouse Gas Inventory",
    "comment": "Read by Johannes Gütschow",
    "institution": "Philippines National Integrated Climate Change Database "
    "and Information Exchange System",
}

category_conversion = {
    "mapping": {
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "M.AG",
        "4": "M.LULUCF",
        "5": "4",
        "M.0.EL": "M.0.EL",
    },
    "aggregate": {
        "3": {
            "sources": ["M.AG", "M.LULUCF"],
            # "name": "AFOLU"
        },
        "M.0.EL": {
            "sources": ["1", "2", "M.AG", "4"],
        },
        "0": {
            "sources": ["M.LULUCF", "M.0.EL"],
        },
    },
}

processing_info_country = {
    "basket_copy": {
        "GWPs_to_add": ["SARGWP100", "AR4GWP100", "AR6GWP100"],
        "entities": ["HFCS"],
        "source_GWP": gwp_to_use,
    },
    # "remove_ts": {
    #     "3B2_GHG": {  # rounding errors
    #         "entities": ["KYOTOGHG (AR5GWP100)"],
    #         "category (IPCC2006_KOR_INV)": ["3.B.2"],
    #         "time": [
    #             "1994",
    #             "1996",
    #             "1997",
    #             "1998",
    #             "2001",
    #             "2003",
    #             "2004",
    #             "2007",
    #             "2017",
    #             "2019",
    #             "2020",
    #         ],
    #     },
    # },
}
