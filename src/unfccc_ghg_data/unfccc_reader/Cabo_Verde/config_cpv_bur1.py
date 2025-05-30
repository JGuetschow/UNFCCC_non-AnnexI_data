"""
Configuration for Cabo Verde BUR1 (read from pdf)
"""

# reading tables on pages:
# 33/1, GHG emissions and removals by type of gas, by sector and by year
# 39, Total GHG Emissions, in CO2eq, for international bunkers, in 1995, 2000, 2005, 2010, 2015 and 2019
# 86-89, GHG emissions in 2019
# Not reading tables on pages:
# 37/38, has additional columns on PFCs, Unspecified mixture of HFCs and PFCs,
# and SF6, but they are all empty
# 32, same information as in table 33/1
# 33/2, aggregation of table 33/1
# 43, no new information here

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

# primap2 format conversion
coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

coords_defaults = {
    "source": "CPV-GHG-Inventory",
    "provenance": "measured",
    "area": "CPV",
    "scenario": "BUR1",
}

gwp_to_use = "SARGWP100"

coords_value_mapping_main = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        "HFCs": f"HFCS ({gwp_to_use})",
        "HFC": f"HFCS ({gwp_to_use})",
    },
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        "CO²": "CO2",
        "CH⁴": "CH4",
        "N²O": "N2O",
        "F-gases": f"FGASES ({gwp_to_use})",
    },
}

filter_remove = {
    "f_memo": {"category": "MEMO"},
    # They are all NaN and don't match a pre-defined entity
    "f_fluor": {"entity": "Other fluorinated products"},
}

meta_data = {
    "references": "unfccc.int/documents/638907",
    "rights": "",  # unknown
    "contact": "daniel-busch@climate-resource.de",
    "title": "Cabo Verde. Biennial update report (BUR). BUR1",
    "comment": "Read fom pdf by Daniel Busch",
    "institution": "UNFCCC",
}

trend_years = ["1995", "2000", "2005", "2010", "2015", "2019"]

inv_conf_per_sector = {
    "main": {
        "page": "33",
        "skip_rows_start": 2,
        "cat_codes_manual": {
            "Energy": "1",
            "IPPU": "2",
            "Agriculture": "M.AG",
            "LULUCF": "M.LULUCF",
            "Waste": "4",
        },
        "header": ["category", "entity", *trend_years],
        "unit": ["Gg"] * 4 + ["GgCO2eq"] + ["Gg"] * 9,
        "unit_conversion": {
            "index": 6,
            "conversion_factor": 2240.625,
        },
        # "unit": ["Gg"] * 4 + ["Gg CO2eq"] + ["Gg"] * 9,
    },
    "int_bunkers": {
        "page": "39",
        "skip_rows_start": 2,
        "cat_codes_manual": {
            "Total International Bunkers": "M.BK",
            "International aviation": "M.BK.A",
            "International shipping": "M.BK.M",
        },
        "header": ["category", *trend_years],
        "unit": "Gg CO2eq",
        "drop_cols": 7,
        "entity": "KYOTOGHG (SARGWP100)",
    },
}

inv_conf = {
    "cat_code_regexp": r"^(?P<code>[a-zA-Z0-9\.]{1,11})[\s\.].*",
    "year": "2019",
    # TODO check again!
    # "CO2 emissions from Biomass" and "CO2 emissions from using manure as energy" are the same category
    "merge_cats": "MBIO",
}

inv_conf_main = {
    "pages": {
        "86": {
            "skip_rows_start": 2,
            "entities": ["CO2", "CH4", "N2O"],
            "column_names": ["category", "CO2", "CH4", "N2O"],
            "cat_codes_manual": {
                "Memo items": "MEMO",
                "International bunkers": "M.BK",
                "CO² emissions from Biomass": "M.BIO",
                "CO² emissions from using manure as energy": "M.BIO",
            },
            "unit_for_entity": {
                "CO2": "Gg",
                "CH4": "Gg",
                "N2O": "Gg",
            },
            # "units" : ["no unit", "Gg", "Gg", "Gg"]
        },
        "87": {
            "skip_rows_start": 2,
            "entities": ["CO2", "CH4", "N2O", "HFCs", "Other fluorinated products"],
            "column_names": [
                "category",
                "CO2",
                "CH4",
                "N2O",
                "HFCs",
                "Other fluorinated products",
            ],
            "cat_codes_manual": {
                "2F. Use of products as substitutes for \nsubstances that degrade the ozone layer": "2.F",
                "2B4. Production of caprolactam, \nglyoxal and glyoxylic acid": "2.B.4",
            },
            "unit_for_entity": {
                "CO2": "Gg",
                "CH4": "Gg",
                "N2O": "Gg",
                "HFCs": "Gg CO2eq",
            },
        },
        "88": {
            "skip_rows_start": 2,
            "entities": ["CO2", "CH4", "N2O"],
            "column_names": ["category", "CO2", "CH4", "N2O"],
            "cat_codes_manual": {
                "3C6. Indirect emissions of N²O from manure \nmanagement": "3.C.6",
                "3C. Aggregate Sources and Sources of Non-CO²\nEmissions in the soil": "3.C",
            },
            "unit_for_entity": {
                "CO2": "Gg",
                "CH4": "Gg",
                "N2O": "Gg",
            },
        },
        "89": {
            "skip_rows_start": 2,
            "entities": ["CO2", "CH4", "N2O"],
            "column_names": ["category", "CO2", "CH4", "N2O"],
            "cat_codes_manual": {
                "3C6. Indirect emissions of N²O from manure \nmanagement": "3.C.6",
                "3C. Aggregate Sources and Sources of Non-CO²\nEmissions in the soil": "3.C",
            },
            "unit_for_entity": {
                "CO2": "Gg",
                "CH4": "Gg",
                "N2O": "Gg",
            },
        },
    },
}

country_processing_step1 = {
    # rounding error 0.038 for yr2019/entN2O/cat4: 0.011 + 0.015 != 0.027
    "tolerance": 0.04,
    "aggregate_cats": {
        # First generate additional categories
        "0": {"sources": ["1", "2", "3", "4", "5"]},
        "2.A": {"sources": ["2.A.1", "2.A.2", "2.A.3", "2.A.4", "2.A.5"]},
        "2.C": {
            "sources": [
                "2.C.1",
                "2.C.2",
                "2.C.3",
                "2.C.4",
                "2.C.5",
                "2.C.6",
                "2.C.7",
            ]
        },
        "2.E": {"sources": ["2.E.1", "2.E.2", "2.E.3", "2.E.4", "2.E.5"]},
        "3.C": {
            "sources": [
                "3.C.1",
                "3.C.2",
                "3.C.3",
                "3.C.4",
                "3.C.5",
                "3.C.6",
                "3.C.7",
                "3.C.8",
            ]
        },
        "3.D": {"sources": ["3.D.2"]},
        # 3.D would go into M.LULUCF as well but we don't have it
        "M.LULUCF": {"sources": ["3.B"]},
        # Only 3.C.7 in table, but values are all zero or empty
        "M.3.C.AG": {
            "sources": [
                "3.C.1",
                "3.C.2",
                "3.C.3",
                "3.C.4",
                "3.C.5",
                "3.C.6",
                "3.C.7",
                "3.C.8",
            ]
        },
        # 3.D.2 is all zeros
        "M.3.D.AG": {"sources": ["3.D.2"]},
        "M.AG.ELV": {
            "sources": ["M.3.C.AG", "M.3.D.AG"],
        },
        "M.AG": {"sources": ["3.A", "M.AG.ELV"]},
        "M.0.EL": {
            "sources": ["1", "2", "M.AG", "4"],
        },
        "4.D": {"sources": ["4.D.1", "4.D.2"]},  # consistency check
        "1": {"sources": ["1.A"]},  # consistency check
        "1.A": {
            "sources": ["1.A.1", "1.A.2", "1.A.3", "1.A.4", "1.A.5"]
        },  # consistency check
        "2": {
            "sources": ["2.A", "2.B", "2.C", "2.D", "2.E", "2.F", "2.G", "2.H"]
        },  # consistency check
        "3": {"sources": ["M.AG", "M.LULUCF"]},  # consistency check
        # "3.A": {"sources": ["3.A.1", "3.A.2"]}, # consistency check
        "4": {"sources": ["4.A", "4.B", "4.C", "4.D", "4.E"]},  # consistency check
    },
}

country_processing_step2 = {
    "downscale": {
        "sectors": {
            "1_all": {
                "basket": "1",
                "basket_contents": ["1.A"],
                "entities": ["CO2", "CH4", "N2O"],
                "dim": f"category ({coords_terminologies['category']})",
            },
            # Values for 1995/2000/2005/2010/2015/2019 are only available for CO2 and F-gases (table 6)
            "2_CO2": {
                "basket": "2",
                "basket_contents": ["2.A", "2.B", "2.C", "2.D", "2.H"],
                "entities": ["CO2"],
                "dim": f"category ({coords_terminologies['category']})",
            },
            # "2_KYOTO": {  # commented as KYOTOGHG only present for bunkers, so aggregate later
            #     # error of 3.5% for KYOTOGHG (AR6GWP100)
            #     "check_consistency": False,
            #     "basket": "2",
            #     "basket_contents": [
            #         "2.A",
            #         "2.B",
            #         "2.C",
            #         "2.D",
            #         "2.E",
            #         "2.F",
            #         "2.G",
            #         "2.H",
            #     ],
            #     "entities": [
            #         "KYOTOGHG (SARGWP100)",
            #         "KYOTOGHG (AR4GWP100)",
            #         "KYOTOGHG (AR5GWP100)",
            #         "KYOTOGHG (AR6GWP100)",
            #     ],
            #     "dim": f'category ({coords_terminologies["category"]})',
            # },
            # "2_FGASES": {  # f-gases have no sectoral detail and HFCs only 2019,
            #     # no downscaling of original data possible
            #     # error of 3.5% for KYOTOGHG (AR6GWP100)
            #     "check_consistency": False,
            #     "basket": "2",
            #     "basket_contents": [
            #         "2.B",
            #         "2.C",
            #         "2.E",
            #         "2.F",
            #         "2.G",
            #     ],
            #     "entities": [
            #         "FGASES (SARGWP100)",
            #         "FGASES (AR4GWP100)",
            #         "FGASES (AR5GWP100)",
            #         "FGASES (AR6GWP100)",
            #         "HFCS (SARGWP100)",
            #         "HFCS (AR4GWP100)",
            #         "HFCS (AR5GWP100)",
            #         "HFCS (AR6GWP100)",
            #     ],
            #     "dim": f'category ({coords_terminologies["category"]})',
            # },
            "3_CH4": {
                "basket": "3",
                "basket_contents": ["3.A", "3.B", "3.C", "3.D"],
                "entities": ["CH4"],
                "dim": f"category ({coords_terminologies['category']})",
            },
            "3_CO2": {
                "basket": "3",
                "basket_contents": ["3.B", "3.C", "3.D"],
                "entities": ["CO2"],
                "dim": f"category ({coords_terminologies['category']})",
            },
            "3_N2O": {
                "basket": "3",
                "basket_contents": ["3.A", "3.B", "3.C", "3.D"],
                "entities": ["N2O"],
                "dim": f"category ({coords_terminologies['category']})",
            },
            # "3_KYOTO": {  # no original data here. aggregate basket later
            #     "basket": "3",
            #     "basket_contents": ["3.A", "3.B", "3.C", "3.D"],
            #     "entities": [
            #         "KYOTOGHG (SARGWP100)",
            #         "KYOTOGHG (AR4GWP100)",
            #         "KYOTOGHG (AR5GWP100)",
            #         "KYOTOGHG (AR6GWP100)",
            #     ],
            #     "dim": f'category ({coords_terminologies["category"]})',
            # },
        },
        "entities": {
            "FGASES": {
                "basket": "FGASES (SARGWP100)",
                "basket_contents": ["HFCS (SARGWP100)"],
            },
        },
    },
    "basket_copy": {
        "GWPs_to_add": ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
        "entities": ["HFCS"],
        "source_GWP": gwp_to_use,
    },
}

gas_baskets = {
    "FGASES (SARGWP100)": ["HFCS (SARGWP100)"],
    "FGASES (AR4GWP100)": ["HFCS (AR4GWP100)"],
    "FGASES (AR5GWP100)": ["HFCS (AR5GWP100)"],
    "FGASES (AR6GWP100)": ["HFCS (AR6GWP100)"],
    "KYOTOGHG (SARGWP100)": ["CO2", "CH4", "N2O", "FGASES (SARGWP100)"],
    "KYOTOGHG (AR4GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR4GWP100)"],
    "KYOTOGHG (AR5GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR5GWP100)"],
    "KYOTOGHG (AR6GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR6GWP100)"],
}
