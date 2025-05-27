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

page_defs_2021 = {
    "22": {  # 2021 inventory pages 22 and 23
        "table_areas": ["51,305,538,73", "686,705,1177,73"],
        "split_text": False,
        "flavor": "stream",
        # fix rows by hand (header)
    },
    "24": {  # 2021 inventory
        "table_areas": ["50,708,538,382"],
        "split_text": False,
        "flavor": "stream",
        # fix rows by hand (header)
    },
}

gwp_to_use = "AR5GWP100"


# special header as category code and name in one column
header_long = ["orig_cat_name", "entity", "unit", "time", "data"]

# manual category codes
cat_codes_manual = {
    "3.C – Managed Soils": "3.C",
    "CO2 emissions from biomass": "M.BIO",
    "International Bunkers": "M.BK",
    "Memo Items": r"\IGNORE",
    "Multilateral operations": "M.MULTIOP",
    "Mt CO e2": "0",
    "Energy": "1",
    "Agricluture": "M.AG",
    "Industrial Processes": "2",
    "LUCF": "M.LULUCF",
    "Waste": "4",
}

cat_code_regexp = r"^(?P<code>[a-zA-Z0-9\.]{1,6})\s-\s.*"

coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}


add_coords_cols = {
    "orig_cat_name": ["orig_cat_name", "category"],
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PAK_INV",
    "scenario": "PRIMAP",
}
terminology_proc = "IPCC2006_PRIMAP"

coords_defaults = {
    "source": "PAK-GHG-Inventory",
    "provenance": "measured",
    "area": "PAK",
    "scenario": "BTR1",
}


coords_value_mapping = {
    # "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        "Net CO2 emissions / removals": "CO2",
        "CH4": f"CH4 ({gwp_to_use})",
        "N2O": f"N2O ({gwp_to_use})",
        "Total": f"KYOTOGHG ({gwp_to_use})",
    },
}

filter_remove = {
    "f1": {
        "category": "\\IGNORE",
    },
}

filter_keep = {}

meta_data = {
    "references": "https://unfccc.int/documents/645241",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Pakistan. 2024 Biennial Transparency Report (BTR). BTR1",
    "comment": "Read fom pdf by Johannes Gütschow",
    "institution": "UNFCCC",
}

category_conversion = {
    "mapping": {
        "0": "0",
        "1": "1",
        "1.A": "1.A",
        "1.A.1": "1.A.1",
        "1.A.2": "1.A.2",
        "1.A.3": "1.A.3",
        "1.A.3.a.i": "M.BK.A",
        "1.A.3.d.i": "M.BK.M",
        "1.A.4": "1.A.4",
        "1.A.5": "1.A.5",
        "1.B": "1.B",
        "1.B.1": "1.B.1",
        "1.B.2": "1.B.2",
        "1.B.3": "1.B.3",
        "1.C": "1.C",
        "1.C.1": "1.C.1",
        "1.C.2": "1.C.2",
        "1.C.3": "1.C.3",
        "2": "2",
        "2.A": "2.A",
        "2.A.1": "2.A.1",
        "2.A.2": "2.A.2",
        "2.A.3": "2.A.3",
        "2.A.4": "2.A.4",
        "2.B": "2.B",
        "2.B.1": "2.B.1",
        "2.C": "2.C",
        "2.D": "2.D",
        "2.D.1": "2.D.1",
        "2.E": "2.E",
        "2.F": "2.F",
        "2.G": "2.G",
        "2.H": "2.H",
        "2.H.1": "2.H.1",
        "2.H.2": "2.H.2",
        "3": "3",
        "3.A": "3.A",
        "3.A.1": "3.A.1",
        "3.A.2": "3.A.2",
        "3.B": "3.B",
        "3.B.1": "3.B.1",
        "3.B.2": "3.B.2",
        "3.B.3": "3.B.3",
        "3.B.4": "3.B.4",
        # "3.C": "",
        "3.C.2": "3.C.3",
        "3.C.3": "3.C.4",
        "3.C.4": "3.C.5",
        "3.C.5": "3.C.6",
        "3.D": "3.C.7",
        "4": "4",
        "4.A": "4.A",
        "4.C": "4.C",
        "4.C.1": "4.C.1",
        "4.C.2": "4.C.2",
        "4.D": "4.D",
        "4.D.1": "4.D.1",
        "4.D.2": "4.D.2",
        "M.BIO": "M.BIO",
        "M.BK": "M.BK",
        "M.MULTIOP": "M.MULTIOP",
    },
    "aggregate": {
        "3.C": {
            "sources": ["3.C.3", "3.C.4", "3.C.5", "3.C.6", "3.C.7"],
            "orig_cat_name": "3.C Aggregate Sources and Non-CO2 Emissions Sources on Land",
        },
        "M.3.C.AG": {
            "sources": [
                "3.C.2",
                "3.C.3",
                "3.C.4",
                "3.C.5",
                "3.C.6",
                "3.C.7",
            ],
            "orig_cat_name": "Aggregate sources and non-CO2 emissions sources on land ("
            "Agriculture)",
        },
        "M.AG.ELV": {
            "sources": ["M.3.C.AG"],
            "orig_cat_name": "Agriculture excluding livestock",
        },
        "M.LULUCF": {
            "sources": ["3.B"],
            "orig_cat_name": "Land Use, Land Use Change, and Forestry",
        },
        "M.AG": {"sources": ["3.A", "M.AG.ELV"], "orig_cat_name": "Agriculture"},
        "M.0.EL": {
            "sources": ["1", "2", "M.AG", "4"],
            "orig_cat_name": "National Total Excluding LULUCF",
        },
        # consistency check: AFOLU and national total
        "3": {
            "sources": ["3.A", "3.B", "3.C", "3.D"],
            "orig_cat_name": "3 - Agriculture, Forestry, and Other Land Use",
        },
        "0": {
            "sources": ["1", "2", "3", "4"],
            "orig_cat_name": "National Total Excluding LULUCF",
        },
    },
}

processing_info_country = {
    "tolerance": 0.021,  # for 3.B.4 (rounding error)
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
