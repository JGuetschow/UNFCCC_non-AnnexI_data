"""
Configuration file to read Saint Kitts and Nevis' BUR 1.

Tables to read:
- The sector tables in the Annex from page 149 - done
- trend tables page 111-113 - done
- page 116 - done
- page 118 - done
- page 119 - done
- page 121 - done
- page 123 - wip

Not reading:
- page 97 - trend table with data for 2008, because it's in the trend tables from page 111
- page 113 - slice of trend table on page 111
"""

gwp_to_use = "AR5GWP100"

# primap2 format conversion
coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

coords_defaults = {
    "source": "KNA-GHG-Inventory",
    "provenance": "measured",
    "area": "KNA",
    "scenario": "BUR1",
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        "NMVOCs": "NMVOC",
        "HFCS": f"HFCS ({gwp_to_use})",
        "PFCS": f"PFCS ({gwp_to_use})",
        "SF6": f"SF6 ({gwp_to_use})",
        "Other halogenated gases with CO2 equivalent conversion factors (1)": f"UnspMixOfHFCs ({gwp_to_use})",
    },
}

meta_data = {
    "references": "https://unfccc.int/documents/633382",
    "rights": "",  # unknown
    "contact": "daniel-busch@climate-resource.de",
    "title": "Saint Kitts and Nevis. Biennial update report (BUR). BUR1",
    "comment": "Read fom pdf by Daniel Busch",
    "institution": "UNFCCC",
}

filter_remove = {
    "f_memo": {"category": "MEMO"},
    "f1": {
        "entity": "Other halogenated gases without CO2 equivalent conversion factors (2)"
    },
    "f2": {"entity": "3.D.X"},
}

conf_general = {
    "cat_code_regexp": r"^(?P<code>[a-zA-Z0-9\.]{1,11})[\s\.].*",
}

conf_trend = {
    "fugitive": {
        "rows_to_fix": {2: ["1.B.3 - Other emissions from"]},
        "page_defs": {
            "125": {
                "read_params": dict(flavor="lattice"),
                "skip_rows_start": 2,
            },
            "126": {
                "read_params": dict(
                    flavor="stream",
                    table_areas=["72,681,564,638"],
                    columns=["203,238,272,305,340,370,402,439,469,504,536"],
                ),
                "skip_rows_start": 1,
            },
        },
        "entity": f"KYOTOGHG ({gwp_to_use})",
        "unit": "GgCO2eq",
        "header": ["orig_category"],
        "years": [
            "2008",
            "2009",
            "2010",
            "2011",
            "2012",
            "2013",
            "2014",
            "2015",
            "2016",
            "2017",
            "2018",
        ],
        "extra_columns": [],
    },
    "other_sectors": {
        "page_defs": {
            "123": {
                "read_params": dict(flavor="lattice"),
                "skip_rows_start": 2,
            },
        },
        "entity": f"KYOTOGHG ({gwp_to_use})",
        "unit": "GgCO2eq",
        "header": ["orig_category"],
        "years": [
            "2008",
            "2009",
            "2010",
            "2011",
            "2012",
            "2013",
            "2014",
            "2015",
            "2016",
            "2017",
            "2018",
        ],
        "extra_columns": [],
    },
    "transport_sub": {
        "page_defs": {
            "121": {
                "read_params": dict(flavor="lattice"),
                "skip_rows_start": 2,
            },
            "122": {
                "read_params": dict(flavor="lattice"),
                "skip_rows_start": 0,
            },
        },
        "entity": f"KYOTOGHG ({gwp_to_use})",
        "unit": "GgCO2eq",
        "header": ["orig_category"],
        "years": [
            "2008",
            "2009",
            "2010",
            "2011",
            "2012",
            "2013",
            "2014",
            "2015",
            "2016",
            "2017",
            "2018",
        ],
        "extra_columns": [],
    },
    "transport": {
        "page_defs": {
            "119": {
                "read_params": dict(flavor="lattice"),
                "skip_rows_start": 2,
            }
        },
        "entity": f"KYOTOGHG ({gwp_to_use})",
        "unit": "GgCO2eq",
        "header": ["orig_category"],
        "years": [
            "2008",
            "2009",
            "2010",
            "2011",
            "2012",
            "2013",
            "2014",
            "2015",
            "2016",
            "2017",
            "2018",
        ],
        "extra_columns": [],
    },
    "manufacturing_and_construction": {
        "page_defs": {
            "118": {
                "read_params": dict(flavor="lattice"),
                "skip_rows_start": 2,
            }
        },
        "entity": f"KYOTOGHG ({gwp_to_use})",
        "unit": "GgCO2eq",
        "header": ["orig_category"],
        "years": [
            "2008",
            "2009",
            "2010",
            "2011",
            "2012",
            "2013",
            "2014",
            "2015",
            "2016",
            "2017",
            "2018",
        ],
        "extra_columns": [],
    },
    "energy_industries": {
        "entity": f"KYOTOGHG ({gwp_to_use})",
        "unit": "GgCO2eq",
        "replace_data_entries": {"NO,NE": "NO"},
        "cat_codes_manual": {
            "a. Public electricity and heat production": "1.A.1.a",
            "b. Petroleum refining": "1.A.1.b",
            "c. Manufacture of solid fuels": "1.A.1.c",
        },
        "header": ["orig_category"],
        "years": [
            "2008",
            "2009",
            "2010",
            "2011",
            "2012",
            "2013",
            "2014",
            "2015",
            "2016",
            "2017",
            "2018",
        ],
        "extra_columns": [],
        "rows_to_fix": {3: ["a. Public electricity and heat"]},
        "page_defs": {
            "116": {
                "read_params": dict(
                    flavor="stream",
                    table_areas=["72,426,543,333"],
                    columns=["199,229,261,293,324,356,386,416,448,480,511"],
                ),
                "skip_rows_start": 2,
            },
        },
    },
    "overview": {
        # Inconsistencies for table page 11 and page 125 for categories 1.B, 1.B.1 and 1.B.2
        "rows_to_drop": ["1B", "1B1", "1B2"],
        "fix_single_value": {
            "cat": "MBIO",
            "year": "2018",
            "new_value": "0.17",
        },
        "entity": f"KYOTOGHG ({gwp_to_use})",
        "unit": "GgCO2eq",
        "replace_data_entries": {"NO,NE": "NO"},
        "cat_codes_manual": {
            "Total CO2 Eq. Emissions without  LULUCF": "M.0.EL",
            "Total CO2 Eq. Emissions with  LULUCF": "0",
            # "1. Energy": "1. Energy",
            "A. Fuel Combustion": "1.A",
            "1.  Energy Industries": "1.A.1",
            "2.  Man. Ind. & Constr.": "1.A.2",
            "3.  Transport": "1.A.3",
            "4.  Other Sectors": "1.A.4",
            "5.  Other": "1.A.5",
            "B. Fugitive Emissions from Fuels": "1.B",
            "1.  Solid Fuels": "1.B.1",
            "2.  Oil and Natural Gas and other…": "1.B.2",
            # "2.  Industrial Processes": "2.  Industrial Processes",
            "A.  Mineral Industry": "2.A",
            "B.  Chemical Industry": "2.B",
            "C.  Metal Industry": "2.C",
            "D.  Non-energy products": "2.D",
            "E.  Electronics industry": "2.E",
            "F.  Product uses as ODS substitutes": "2.F",
            "G.  Other product manufacture and": "2.G",
            "use  H.  Other": "2.H",
            "3.  Agriculture": "M.AG",
            "A.  Enteric Fermentation": "3.A.1",
            "B.  Manure Management": "3.A.2",
            "C.  Rice Cultivation": "3.C.7",
            "D.  Agricultural Soils": "3.C.4",  # TODO confirm!
            "E.  Prescribed Burning of Savannahs": "3.C.1.d",  # TODO confirm!
            "F.  Field Burning of Agricultural": "3.C.1.b",  # TODO confirm!
            "Residues  G.  Liming": "3.C.2",
            "H.  Urea applications": "3.C.3",
            "I.  Other carbon-containing": "3.D.2",  # TODO confirm!
            "fertilisers  4. Land Use, Land-Use Change and  Forestry": "M.LULUCF",
            "A. Forest Land": "3.B.1",
            "B. Cropland": "3.B.2",
            "C. Grassland": "3.B.3",
            "D. Wetlands": "3.B.4",
            "E. Settlements": "3.B.5",
            "F. Other Land": "3.B.6",
            "G. Harvested wood products": "3.D.1",
            "H. Other": "3.D.X",
            "5. Waste": "4",
            "A.  Solid Waste Disposal": "4.A",
            "B.  Biological treatment of solid": "4.B",
            "waste  C. Incineration and open burning of": "4.C",
            "D. Waste water treatment and": "4.D",
            "discharge  E.  Other": "4.E",
            "6.  Other": "5",
            "CO2 Emissions from Biomass": "M.BIO",
        },
        "drop_cols": [
            "change to BY",
            "change to PY",
        ],
        "header": ["orig_category"],
        "years": [
            "2008",
            "2009",
            "2010",
            "2011",
            "2012",
            "2013",
            "2014",
            "2015",
            "2016",
            "2017",
            "2018",
        ],
        "extra_columns": [
            "change to BY",
            "change to PY",
        ],
        "split_values": {
            "cat": "3B2",
            "keep_value_no": 1,
        },
        "page_defs": {
            "111": {"read_params": dict(flavor="lattice"), "skip_rows_start": 1},
            "112": {"read_params": dict(flavor="lattice"), "skip_rows_start": 1},
            "113": {"read_params": dict(flavor="lattice"), "skip_rows_start": 1},
        },
    },
}

conf = {
    "energy": {
        # TODO: List of entities are always keys of unit mapping dict
        "entities": ["CO2", "CH4", "N2O", "NOX", "CO", "NMVOCs", "SO2"],
        "header": ["orig_category"],
        "cat_codes_manual": {
            "Information Items": "MEMO",
            "CO2 from Biomass Combustion for Energy Production": "MBIO",
        },
        "page_defs": {
            "149": {"skip_rows_start": 2},
            "150": {"skip_rows_start": 2},
            "151": {"skip_rows_start": 2},
            "152": {"skip_rows_start": 2},
        },
        "replace_data_entries": {
            "NO,NE": "NO",
            "NE,NO": "NO",
            "NO,IE": "NO",
        },
        "unit_mapping": {
            "CO2": "Gg",
            "CH4": "Gg",
            "N2O": "Gg",
            "NOX": "Gg",
            "CO": "Gg",
            "NMVOCs": "Gg",
            "SO2": "Gg",
        },
    },
    "ipuu": {
        "entities": [
            "CO2",
            "CH4",
            "N2O",
            "HFCS",
            "PFCS",
            "SF6",
            "Other halogenated gases with CO2 equivalent conversion factors (1)",
            "Other halogenated gases without CO2 equivalent conversion factors (2)",
            "NOX",
            "CO",
            "NMVOC",
            "SO2",
        ],
        "header": ["orig_category"],
        "cat_codes_manual": {
            "Information Items": "MEMO",
            "CO2 from Biomass Combustion for Energy Production": "MBIO",
        },
        "page_defs": {
            "153": {"skip_rows_start": 2},
            "154": {"skip_rows_start": 2},
            "155": {"skip_rows_start": 2},
        },
        "replace_data_entries": {
            "NO,NE": "NO",
            "NE,NO": "NO",
            "NO,IE": "NO",
        },
        "unit_mapping": {
            "CO2": "Gg",
            "CH4": "Gg",
            "N2O": "Gg",
            "HFCS": "GgCO2eq",
            "PFCS": "GgCO2eq",
            "SF6": "GgCO2eq",
            "Other halogenated gases with CO2 equivalent conversion factors (1)": "GgCO2eq",
            "Other halogenated gases without CO2 equivalent conversion factors (2)": "Gg",
            "NOX": "Gg",
            "CO": "Gg",
            "NMVOC": "Gg",
            "SO2": "Gg",
        },
    },
    "AFOLU": {
        "entities": [
            "CO2",
            "CH4",
            "N2O",
            "NOX",
            "CO",
            "NMVOC",
        ],
        "header": ["orig_category"],
        "cat_codes_manual": {
            "Information Items": "MEMO",
            "CO2 from Biomass Combustion for Energy Production": "MBIO",
        },
        "page_defs": {
            "156": {"skip_rows_start": 3},
            "157": {"skip_rows_start": 3},
            "158": {"skip_rows_start": 3},
        },
        "replace_data_entries": {
            "NO,NA": "NO",
            "NO,NE": "NO",
            "NE,NO": "NO",
            "NO,IE": "NO",
        },
        "unit_mapping": {
            "CO2": "Gg",
            "CH4": "Gg",
            "N2O": "Gg",
            "NOX": "Gg",
            "CO": "Gg",
            "NMVOC": "Gg",
        },
    },
    "waste": {
        "entities": [
            "CO2",
            "CH4",
            "N2O",
            "NOX",
            "CO",
            "NMVOC",
            "SO2",
        ],
        "header": ["orig_category"],
        "cat_codes_manual": {
            "Information Items": "MEMO",
            "CO2 from Biomass Combustion for Energy Production": "MBIO",
        },
        "page_defs": {
            "159": {"skip_rows_start": 2},
        },
        "replace_data_entries": {
            "NO,NA": "NO",
            "NO,NE": "NO",
            "NE,NO": "NO",
            "NO,IE": "NO",
        },
        "unit_mapping": {
            "CO2": "Gg",
            "CH4": "Gg",
            "N2O": "Gg",
            "NOX": "Gg",
            "CO": "Gg",
            "NMVOC": "Gg",
            "SO2": "Gg",
        },
    },
}

fix_values_main = [
    # ("3A", "CH4", "0.203"),
    ("3A2", "CH4", "0.03"),
    # ("3A", "N2O", "0.01"),
    ("3A2", "N2O", "0"),
]
# (category, year, new_value)
# There are missing numbers in "Fores Land" on page 112
# I found them as invisible numbers in the row below
# but deleted them because I didn't know where they belong.
# Leaving it as it is now, but numbers could be added upstream TODO
fix_values_trend = [
    ("3B1", "2008", "-130.02"),
    ("3B", "2009", "-130.02"),
    ("3B", "2010", "-130.02"),
    ("3B", "2011", "-151.6"),
    ("3B", "2012", "-151.6"),
    ("3B", "2013", "-151.6"),
    ("3B", "2014", "-140.34"),
    ("3B", "2015", "-140.34"),
    ("3B", "2016", "-140.34"),
    ("3B", "2017", "-140.34"),
    ("3B", "2018", "-140.34"),
]

gas_baskets = {
    "FGASES (SARGWP100)": ["HFCS (SARGWP100)", "PFCS (SARGWP100)", "SF6", "NF3"],
    "FGASES (AR4GWP100)": ["HFCS (AR4GWP100)", "PFCS (AR4GWP100)", "SF6", "NF3"],
    "FGASES (AR5GWP100)": ["HFCS (AR5GWP100)", "PFCS (AR5GWP100)", "SF6", "NF3"],
    "FGASES (AR6GWP100)": ["HFCS (AR6GWP100)", "PFCS (AR6GWP100)", "SF6", "NF3"],
    "KYOTOGHG (SARGWP100)": ["CO2", "CH4", "N2O", "FGASES (SARGWP100)"],
    "KYOTOGHG (AR4GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR4GWP100)"],
    "KYOTOGHG (AR5GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR5GWP100)"],
    "KYOTOGHG (AR6GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR6GWP100)"],
}

country_processing_step1 = {
    "tolerance": 0.01,
    "aggregate_cats": {
        "M.3.D.AG": {"sources": ["3.D.2"]},
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
            ],
        },
        "M.AG.ELV": {
            "sources": ["M.3.C.AG", "M.3.D.AG"],
        },
        "3.A": {"sources": ["3.A.1", "3.A.2"]},
        "3.B": {"sources": ["3.B.1", "3.B.2", "3.B.3", "3.B.4", "3.B.5", "3.B.6"]},
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
        "3.D": {"sources": ["3.D.1", "3.D.2"]},
        "M.AG": {"sources": ["3.A", "M.AG.ELV"]},
        "M.3.D.LU": {"sources": ["3.D.1"]},
        "M.LULUCF": {"sources": ["3.B", "M.3.D.LU"]},
        "M.0.EL": {
            "sources": ["1", "2", "M.AG", "4"],
        },
        "3": {"sources": ["M.AG", "M.LULUCF"]},  # consistency check
        "0": {"sources": ["1", "2", "3", "4"]},  # consistency check
    },
    "basket_copy": {
        "GWPs_to_add": ["AR4GWP100", "SARGWP100", "AR6GWP100"],
        "entities": ["HFCS", "PFCS", "UnspMixOfHFCs"],
        "source_GWP": gwp_to_use,
    },
    # "downscale": {
    #     "sectors": {
    #         "1.B_CH4": {
    #             "basket": "1.B",
    #             "basket_contents": ["1.B.1", "1.B.2"],
    #             "entities": ["CH4"],
    #             "dim": f"category ({coords_terminologies['category']})",
    #             # "tolerance": 0.05,  # some inconsistencies (rounding?)
    #         },
    #         "1.B_CO2": {
    #             "basket": "1.B",
    #             "basket_contents": ["1.B.1", "1.B.2"],
    #             "entities": ["CO2"],
    #             "dim": f"category ({coords_terminologies['category']})",
    #             "sel": {
    #                 "time": [
    #                     "2000",
    #                     "2005",
    #                     "2010",
    #                     "2015",
    #                     "2020",
    #                 ]
    #             },
    #         },
    #     }
    # },
}
