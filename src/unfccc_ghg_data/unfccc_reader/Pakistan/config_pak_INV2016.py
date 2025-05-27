"""Config for Mexico's BTR1

Full configuration including PRIMAP2 conversion config and metadata

"""


# page_defs_old_inv = {
#     '20': { # overview old inventories
#         "table_areas": ['50,316,531,101'],
#         "split_text": False,
#         "flavor": "stream",
#         # fix rows by hand (header)
#         # table also needs transposing
#     },
# }  # not read because we read old inventories from a different report

page_defs = {
    "23": {  # main sectors
        "camelot": {
            "table_areas": ["62,740,532,131"],
            "columns": ["200,251,300,338,369,406,445,496"],
            "split_text": False,
            "flavor": "stream",
        },
        "rows_to_fix": {
            -5: ["Greenhouse gas source and sink"],
            2: [
                "Total national emissions and",
                "A. Fuel combustion (sectoral",
                "2. Manufacturing industries",
                "B. Fugitive emissions from",
                "F. Consumption of halocarbons",
                "E. Prescribed burning of",
                "F. Field burning of agricultural",
                "5. Land-use change and forestry",
                "A. Changes in forest and other",
                "B. Forest and grassland",
                "C. Abandonment of managed",
                "D. CO2 emissions and",
            ],
            3: ["E. Production of halocarbons"],
        },
        "year": 1994,
    },
    "25": {  # main sectors
        "camelot": {
            "table_areas": ["55,740,538,140"],
            "columns": ["210,261,313,347,381,416,453,504"],
            "split_text": False,
            "flavor": "stream",
        },
        "rows_to_fix": {
            -5: ["Greenhouse gas source and sink"],
            2: [
                "Total national emissions and",
                "A. Fuel combustion (sectoral",
                "2. Manufacturing industries and",
                "E. Production of halocarbons and",
                "F. Consumption of halocarbons and",
                "F. Field burning of agricultural",
                "A. Changes in forest and other",
                "D. CO2 emissions and removals",
            ],
        },
        "year": 2008,
    },
    "27": {  # main sectors
        "camelot": {
            "table_areas": ["68,741,526,105"],
            "columns": ["214,264,312,344,377,411,444,495"],
            "split_text": False,
            "flavor": "stream",
        },
        "rows_to_fix": {
            -5: ["Greenhouse gas source and sink"],
            2: [
                "Total national emissions and",
                "A. Fuel combustion (sectoral",
                "2. Manufacturing industries",
                "E. Production of halocarbons and",
                "F. Consumption of halocarbons",
                "E. Prescribed burning of",
                "F. Field burning of agricultural",
                "A. Changes in forest and other",
                "B. Forest and grassland",
                "C. Abandonment of managed",
                "D. CO2 emissions and removals",
            ],
        },
        "year": 2012,
    },
}

gwp_to_use = "SARGWP100"

fix_cat_names = {
    "G. Other (please specify)": {
        "F. Consumption of halocarbons and sulphur hexafluoride": "2.",
        "F. Field burning of agricultural residues": "4.",
    },
}

# special header as category code and name in one column
header_long = ["orig_cat_name", "entity", "unit", "time", "data"]

# manual category codes
### TODO: need sector mapping that also uses preceeding cat at G. Other () is present twice
cat_codes_manual = {
    "Total national emissions and removals": "0",
    "1. Energy": "1",
    "A. Fuel combustion (sectoral approach)": "1.A",
    "1. Energy Industries": "1.A.1",
    "2. Manufacturing industries and construction": "1.A.2",
    "3. Transport": "1.A.3",
    "4. Other sectors": "1.A.4",
    "5. Other (please specify)": "1.A.5",
    "B. Fugitive emissions from fuels": "1.B",
    "1. Solid fuels": "1.B.1",
    "2. Oil and natural gas": "1.B.2",
    "3. Ozone precursors & SO2": "1.B.3",
    "2. Industrial processes": "2",
    "A. Mineral products": "2.A",
    "B. Chemical industry": "2.B",
    "C. Metal production": "2.C",
    "D. Other production": "2.D",
    "E. Production of halocarbons and sulphur hexafluoride": "2.E",
    "F. Consumption of halocarbons and sulphur hexafluoride": "2.F",
    "2.G. Other (please specify)": "2.G",
    "3. Solvent and other product use": "3",
    "4. Agriculture": "4",
    "A. Enteric fermentation": "4.A",
    "B. Manure management": "4.B",
    "C. Rice cultivation": "4.C",
    "D. Agricultural soils": "4.D",
    "E. Prescribed burning of savannahs": "4.E",
    "F. Field burning of agricultural residues": "4.F",
    "4.G. Other (please specify)": "4.G",
    "5. Land-use change and forestry 1": "5",
    "A. Changes in forest and other woody biomass stocks": "5.A",
    "B. Forest and grassland conversion": "5.B",
    "C. Abandonment of managed lands": "5.C",
    "D. CO2 emissions and removals from soil": "5.D",
    "E. Other (please specify)": "5.E",
    "6. Waste": "6",
    "A. Solid waste disposal on land": "6.A",
    "B. Waste-water handling": "6.B",
    "C. Waste incineration": "6.C",
    "D. Other (please specify)": "6.D",
    "D. Other (human sewage)": "6.D",
    "7. Other (please specify)": "7",
    "Memo items": r"\IGNORE",
    "International bunkers": "M.BK",
    "Aviation": "M.BK.A",
    "Marine": "M.BK.M",
    "CO2 emissions from biomass": "M.BIO",
}

# cat_code_regexp = r"^(?P<code>[a-zA-Z0-9\.]{1,6})\s-\s.*"

coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC1996",
    "scenario": "PRIMAP",
}
terminology_proc = "IPCC2006_PRIMAP"

coords_defaults = {
    "source": "PAK-GHG-Inventory",
    "provenance": "measured",
    "area": "PAK",
    "scenario": "INV2016",
}


coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        "NMVOCs": "NMVOC",
    },
}

filter_remove = {
    "f1": {
        "category": "\\IGNORE",
    },
}

filter_keep = {}

meta_data = {
    "references": "https://gcisc.org.pk/GHGINVENTORY2011-2012_FINAL_GCISCRR19.pdf",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Greenhouse Gas Emission Inventory of Pakistan for the Year 2011-2012",
    "comment": "Read fom pdf by Johannes Gütschow",
    "institution": "Global Change Impact Studies Centre, "
    "Ministry of Climate Change, Islamabad, Pakistan",
}

category_conversion = {
    # almost BURDI to IPCC2006, but not exactly as e.g. 1.B.3 exists here and
    # M.0.EL not
    "mapping": {
        "0": "0",
        "1": "1",
        "1.A": "1.A",
        "1.A.1": "1.A.1",
        "1.A.2": "1.A.2",
        "1.A.3": "1.A.3",
        "1.A.4": "1.A.4",
        "1.A.5": "1.A.5",
        "1.B": "1.B",
        "1.B.1": "1.B.1",
        "1.B.2": "1.B.2",
        "1.B.3": "1.B.3",
        "2.A": "2.A",
        "2.B": "M.2.B_2.B",
        "2.C": "2.C",
        "2.D": "M.2.H.1_2",
        "2.E": "M.2.B_2.E",  # actually empty
        "2.F": "2.F",  # actually empty
        "2.G": "2.H.3",
        "3": "2.D",
        "4": "M.AG",
        "4.A": "3.A.1",
        "4.B": "3.A.2",
        "4.C": "3.C.7",
        "4.D": "M.3.C.45.AG",
        "4.E": "3.C.1.c",
        "4.F": "3.C.1.b",
        "4.G": "3.C.8",
        "5": "M.LULUCF",
        "6": "4",
        "6.A": "4.A",
        "6.B": "4.D",
        "6.C": "4.C",
        "6.D": "4.E",
        "M.BK": "M.BK",
        "M.BK.A": "M.BK.A",
        "M.BK.M": "M.BK.M",
        "M.BIO": "M.BIO",
        "7": "5",
    },  # 5.A-D ignored as not fitting 2006 cats
    "aggregate": {
        "2.B": {
            "sources": ["M.2.B_2.B", "M.2.B_2.E"],
            # "orig_cat_name": "Chemical Industry",
        },
        "2.H": {
            "sources": ["M.2.H.1_2", "2.H.3"],
            # "orig_cat_name": "Other"
        },
        "2": {
            "sources": ["2.A", "2.B", "2.C", "2.D", "2.F", "2.H"],
            # "orig_cat_name": "Industrial Processes and Product Use",
        },
        "3.A": {
            "sources": ["3.A.1", "3.A.2"],
            # "orig_cat_name": "Livestock"
        },
        "3.C.1": {
            "sources": ["3.C.1.b", "3.C.1.c"],
            # "orig_cat_name": "Emissions from biomass burning",
        },
        "M.3.C.1.AG": {
            "sources": ["3.C.1.b", "3.C.1.c"],
            # "orig_cat_name": "Emissions from biomass burning (Agriculture)",
        },
        "3.C": {
            "sources": ["3.C.1", "M.3.C.45.AG", "3.C.7", "3.C.8"],
            # "orig_cat_name": "Aggregate sources and non-CO2 emissions sources on land",
        },
        "M.3.C.AG": {
            "sources": ["M.3.C.1.AG", "M.3.C.45.AG", "3.C.7", "3.C.8"],
            # "orig_cat_name": "Aggregate sources and non-CO2 emissions sources on land ("
            #                 "Agriculture)",
        },
        "M.AG.ELV": {
            "sources": ["M.3.C.AG"],
            # "orig_cat_name": "Agriculture excluding livestock",
        },
        "3": {
            "sources": ["M.AG", "M.LULUCF"],
            # "orig_cat_name": "AFOLU"
        },
        "M.0.EL": {
            "sources": ["1", "2", "M.AG", "4", "5"],
        },
        # consistency checks
        "0": {
            "sources": ["1", "2", "3", "4", "5"],
        },
        "M.AG": {
            "sources": ["3.A", "M.AG.ELV"],
            # "orig_cat_name": "Agriculture",
        },
    },
}


processing_info_country = {
    # "tolerance": 0.021,  # for 3.B.4 (rounding error)
    # "aggregate_coords": {
    #     "category": {
    #         "M.3.C.AG": {
    #             "sources": [
    #                 "3.C.2",
    #                 "3.C.3",
    #                 "3.C.4",
    #                 "3.C.5",
    #             ],
    #             "orig_cat_name": "Aggregate Sources and Non-CO2 Emissions Sources on Land "
    #             "- Agriculture",
    #         },
    #         "M.AG.ELV": {
    #             "sources": ["M.3.C.AG"],
    #             "orig_cat_name": "Agriculture excluding livestock",
    #         },
    #         "M.AG": {
    #             "sources": ["3.A", "M.AG.ELV"],
    #             "orig_cat_name": "Agriculture",
    #         },
    #         "M.LULUCF": {
    #             "sources": ["M.3.C.LU", "3.B", "3.D"],
    #             "orig_cat_name": "Land Use, Land Use Change, and Forestry",
    #         },
    #         "1.B": {
    #             "sources": ["1.B.1", "1.B.2"],
    #             "orig_cat_name": "Fugitive emissions from fuels",
    #         },
    #         # for consistency checks
    #         "3": {
    #             "sources": ["M.AG", "M.LULUCF"],
    #             "orig_cat_name": "[3] Agricultura, silvicultura y otros usos de la tierra",
    #         },
    #         "0": {
    #             "sources": ["M.LULUCF", "M.0.EL"],
    #             "orig_cat_name": "Todas las emisiones y las absorciones nacionales",
    #         },
    #     }
    # },
}
