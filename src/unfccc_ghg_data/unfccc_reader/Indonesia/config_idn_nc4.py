"""Config for Indonesia's NC4

Full configuration including PRIMAP2 conversion config and metadata

"""

# ###
# for reading
# ###

# general
gwp_to_use = "AR5GWP100"
tolerance = 0.01

page_defs = {
    "90": {
        "table_areas": ["52,384,570,180"],
    },
    "93": {  # CO2
        "table_areas": ["61,318,559,111"],
    },
    "95": {  # CH4  // N2O part 1
        "table_areas": ["54,657,566,369", "54,180,566,72"],
    },
    "96": {  # N2O lower part
        "table_areas": ["53,718,575,556"],
    },
    "99": {  # energy detail 2024
        "table_areas": ["73,285,549,69"],
    },
    "100": {  # energy detail 2024 2
        "table_areas": ["72,720,549,292"],
        "columns": ["314,390,439,484"],
    },
    "106": {  # IPPU detail 2024
        "table_areas": ["92,410,534,104"],
    },
    "110": {  # Agriculture detail 2024 1
        "table_areas": ["73,701,580,75"],
    },
    "111": {  # Agriculture detail 2024 2
        "table_areas": ["75,720,580,538"],
    },
    "116": {  # LULUCF detail 2024
        "table_areas": ["53,697,565,124"],
    },
    "121": {  # waste detail 2024
        "table_areas": ["75,451,547,141"],
    },
    # TODO: waste detail timeseries
}

table_defs_timeseries = {
    "Table_3-5": {  # Trends, only read PFCs
        "tables": [0],
        "cols_to_drop": [8, 9],
        "rows_to_fix": {
            3: [
                "CO2 excluding",
                "CH4 excluding",
                "N2O excluding",
                "Total GHG emissions",
            ]
        },
        "unit": "ktCO2eq",
        "entity": f"PFCS ({gwp_to_use})",
        "cat_col": "GHGs",
        "rows_to_merge": [0, 1],
        # "rows_to_drop": [2, 3],
        "rows_to_drop": [
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            18,
            19,
            20,
            21,
        ],
    },
    "Table_3-7": {  # CO2 trends
        "tables": [1],
        "cols_to_drop": [8, 9],
        "rows_to_fix": {
            2: [
                "1.A.2.  Manufacturing",
                "1.B. Fugitive emissions",
                "2.D. Non-Energy Products",
            ]
        },
        "unit": "kt",
        "entity": "CO2",
        "cat_col": "GHGs",
        "rows_to_merge": [2, 3],
        "rows_to_drop": [0, 1],
    },
    "Table_3-8": {  # CH4
        "tables": [2],
        "cols_to_drop": [8, 9],
        "rows_to_fix": {
            2: [
                "1.B. Fugitive emissions",
                "3.B.  Manure",
                "3.E.  Prescribed burning",
                "3.F.  Field burning of",
                "5.B.  Biological treatment",
                "5.C.  Incineration and",
                "5.D.  Wastewater",
            ],
            3: [
                "1.A.2.  Manufacturing",
            ],
        },
        "unit": "ktCO2eq",
        "entity": f"CH4 ({gwp_to_use})",
        "cat_col": "GHGs",
        "rows_to_merge": [2, 3],
        "rows_to_drop": [0, 1],
    },
    "Table_3-9": {  # N2O part 1
        "tables": [3, 4],
        "cols_to_drop": [8, 9],
        "rows_to_fix": {
            2: [
                "1.A.2.  Manufacturing",
                "1.B. Fugitive emissions",
                "3.E.  Prescribed burning of",
                "3.F.  Field burning of",
                "5.B.  Biological treatment",
                "5.C.  Incineration and open",
                "5.D.  Wastewater treatment",
            ],
        },
        "unit": "ktCO2eq",
        "entity": f"N2O ({gwp_to_use})",
        "cat_col": "GHGs",
        "rows_to_merge": [2, 3],
        "rows_to_drop": [0, 1],
    },
    # "Table_3-9_2": {  # N2O part 2
    #     "tables": [4],
    #     "cols_to_drop": [8, 9],
    #     "rows_to_fix": {
    #         2: ["3.E.  Prescribed burning of", "3.F.  Field burning of",
    #             "5.B.  Biological treatment", "5.C.  Incineration and open",
    #             "5.D.  Wastewater treatment"],
    #     },
    #     "unit": "ktCO2eq",
    #     "cat_col": "GHGs",
    #     "rows_to_merge": [2, 3],
    #     "rows_to_drop": [0, 1],
    # },
}

table_defs_detail = {
    "Table_3-13_1": {  # energy detail 2024
        "tables": [5],
        "rows_to_fix": {
            2: ["1.A.1.c Manufacture of Solid Fuels & Other Energy"],
        },
        "time": "2024",
        "units": ["kt", "kt", "kt", "ktCO2eq"],
        "cat_col": "Categories",
        "rows_to_merge": [0, 1],
        "rows_to_drop": [2],
    },
    "Table_3-13_2": {  # energy detail 2024 2
        "tables": [6],
        "rows_to_fix": {
            -1: ["Categories"],
            3: ["1.A.3.d.i International water-borne navigation"],
        },
        # "unit": "ktCO2eq",
        "units": ["kt", "kt", "kt", "ktCO2eq"],
        "cat_col": "Categories",
        "rows_to_merge": [0, 1],
        "rows_to_drop": [2],
    },
    "Table3_17": {  # IPPU detail 2024
        "tables": [7],
        "rows_to_fix": {
            -1: ["GHG Source Categories"],
            2: ["2.A.4 Other Process Uses of Carbonates (include"],
        },
        "time": "2024",
        "units": ["kt", "kt", "kt", "kt", "ktCO2eq"],
        "cat_col": "GHG Source Categories",
        "rows_to_merge": [0, 1],
        "rows_to_drop": [2],
    },
    "Table_3-21_1": {  # Agriculture detail 2024 1
        "tables": [8],
        "rows_to_fix": {
            3: [
                "3.D.1.  Direct N2O emissions from",
                "3.D.1.c. Urine and dung deposited",
                "3.D.1.e. Mineralization/",
                "3.D.1.f. Cultivation of organic soils",
                "3.D.2.   Indirect N2O Emissions",
            ],
        },
        "time": "2024",
        "units": ["kt", "kt", "kt", "kt", "kt", "kt", "kt", "ktCO2eq"],
        "cat_col": "Greenhouse Gas Source and Sink Categories",
        "rows_to_merge": [0, 1, 2, 3, 4],
        "rows_to_drop": [5, 6],
    },
    "Table_3-21_2": {  # Agriculture detail 2024 2
        "tables": [9],
        "rows_to_fix": {
            3: [
                "3.E. Prescribed burning of",
                "3.F. Field burning of agricultural",
                "3.I. Other carbon-containing",
                "Other sources from agriculture (non-",
            ],
        },
        "units": ["kt", "kt", "kt", "kt", "kt", "kt", "kt", "ktCO2eq"],
        "cat_col": "Greenhouse Gas Source and Sink Categories",
        "rows_to_merge": [0, 1, 2, 3, 4],
        "rows_to_drop": [5, 6],
    },
    "Table_3-26": {  # LULUCF detail 2024
        "tables": [10],
        "rows_to_fix": {
            2: ["4.F.1. Other land use remaining other land"],
            3: [
                "N2O emission from aquaculture",
                "Other emissions from LULUCF",
                "Emissions and removals from natural",
            ],
        },
        "units": ["kt", "kt", "kt", "kt", "kt", "kt", "ktCO2eq"],
        "cat_col": "Greenhouse Gas Source and Sink Categories",
        "rows_to_merge": [0, 1, 2, 3, 4],
        "rows_to_drop": [5],
    },
    "Table_3-30": {  # waste detail 2024
        "tables": [11],
        "rows_to_fix": {
            2: ["4.F.1. Other land use remaining other land"],
            3: [
                "5.A.1 - Managed Waste Disposal",
                "5.A.2 - Unmanaged Waste",
                "5.A.3 - Uncategorized Waste",
                "5.B - Biological Treatment of Solid",
                "Anaerobic digestion at biogas",
                "5.C - Incineration and Open",
                "5.D - Wastewater Treatment and",
                "5.D.1 - Domestic Wastewater",
                "5.D.2 - Industrial Wastewater",
            ],
        },
        "units": ["kt", "kt", "kt", "kt", "kt", "kt", "kt", "ktCO2eq"],
        "cat_col": "Categories",
        "rows_to_merge": [1, 2],
        "rows_to_drop": [0],
    },
    # TODO: waste detail timeseries
}

cat_codes_manual = {
    "Total": "0",
    "PFCs": "0",
}
cat_code_regexp = r"^(?P<code>[a-zA-Z0-9\.]{1,6})\..*"
cat_code_regexp_2024 = r"^(?P<code>[a-zA-Z0-9\.]{1,11})\s.*"

header_long = ["category", "entity", "unit", "time", "data"]

# primap2 format conversion
coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

coords_terminologies = {
    "area": "ISO3",
    "category": "CRT",
    "scenario": "PRIMAP",
}
terminology_proc = "IPCC2006_PRIMAP"


coords_defaults = {
    "source": "IDN-GHG-Inventory",
    "provenance": "measured",
    "area": "IDN",
    "scenario": "NC4",
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    # "category": "PRIMAP1",
    # "entity": {
    #     "CO2 (séquestré)": "CO2 removals",
    #     "CO2 (émis)": "CO2 emissions",
    # },
}

filter_remove = {}
filter_keep = {}

meta_data = {
    "references": "https://unfccc.int/documents/659994",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Indonesia. National Communication (NC). NC 4.",
    "comment": "Read fom pdf by Johannes Gütschow",
    "institution": "UNFCCC",
}


# ###
# for processing
# ###
# aggregate categories
country_processing_step1 = {
    "move_ts": {
        "pfcs": {
            "dim": f"category ({coords_terminologies['category']})",
            "from": "0",
            "to": "2",
            "entities": [f"PFCS ({gwp_to_use})"],
            "sel": {"area": ["IDN"]},
        },
        "agri_CO2": {
            "dim": f"category ({coords_terminologies['category']})",
            "from": "3",
            "to": "M.3.GH",
            "entities": ["CO2"],
            "sel": {"area": ["IDN"]},
        },
    },
    "aggregate_coords": {
        f"category ({coords_terminologies['category']})": {
            "1.A": {
                "sources": ["1.A.1", "1.A.2", "1.A.3", "1.A.4", "1.A.5"],
                "sel": {
                    "entity": ["CO2", "CH4", "N2O"],
                },
            },
            "1": {
                "sources": ["1.A", "1.B"],
                "sel": {
                    "entity": ["CH4", "N2O", "CO2"],
                },
            },
            "2": {
                "sources": ["2.A", "2.B", "2.C", "2.D", "2.H"],
                "sel": {
                    "entity": ["CH4", "N2O", "CO2"],
                },
            },
            "3": {
                "sources": ["3.A", "3.B", "3.C", "3.D", "3.E", "3.F"],
                "sel": {
                    "entity": ["CH4", "N2O"],
                },
            },
            "4": {
                "sources": ["4.A", "4.B", "4.C", "4.D", "4.E", "4.F"],
                "sel": {
                    "entity": ["CO2"],
                },
            },
            "5": {
                "sources": ["5.A", "5.B", "5.C", "5.D", "5.E"],
                "sel": {
                    "entity": ["CH4", "N2O"],
                },
            },
        }
    },
    "basket_copy": {
        "GWPs_to_add": ["SARGWP100", "AR4GWP100", "AR6GWP100"],
        "entities": ["PFCS"],
        "source_GWP": gwp_to_use,
    },
}

cat_conversion = {
    "mapping": {
        "0": "0",
        "M.0.EL": "M.0.EL",
        "1": "1",
        "1.A": "1.A",
        "1.A.1": "1.A.1",
        "1.A.2": "1.A.2",
        "1.A.3": "1.A.3",
        "1.A.4": "1.A.4",
        "1.A.5": "1.A.5",
        "1.B": "1.B",
        "2": "2",
        "2.A": "2.A",
        "2.B": "2.B",
        "2.C": "2.C",
        "2.D": "2.D",
        "2.H": "2.H",
        "3": "M.AG",
        "3.A": "3.A.1",
        "3.B": "M.3.B.CRF",  # Manure Management including indirect emissions
        "3.C": "3.C.7",  # Rice Cultivation
        "3.D": "M.3.C.45.AG",  # Agricultural Soils
        "3.E": "M.3.C.1.SAV",  # Prescribed Burning of Savannahs
        "3.F": "3.C.1.b",  # Field burning of Agricultural Residues
        "M.3.GH": "M.3.C.23",  # urea, liming
        "4": "M.LULUCF",
        "4.A": "3.B.1",  # forest
        "4.B": "3.B.2",  # cropland
        "4.C": "3.B.3",  # grassland
        "4.D": "3.B.4",  # wetlands
        "4.E": "3.B.5",  # Settlements
        "4.F": "3.B.6",  # other land
        "5": "4",
        "5.A": "4.A",
        "5.B": "4.B",
        "5.C": "4.C",
        "5.D": "4.D",
        "5.E": "4.E",
        # "M.BK": "M.BK",
        # "M.BK.A": "M.BK.A",
        # "M.BK.M": "M.BM.M",
        # "M.BIO": "M.BIO",
    },
    "aggregate": {
        "3.A": {
            "sources": ["3.A.1", "M.3.B.CRF"],
            "sel": {
                "entity": ["CH4", "N2O"],
            },
        },
        "3.B": {
            "sources": ["3.B.1", "3.B.2", "3.B.3", "3.B.4", "3.B.5", "3.B.6"],
            "sel": {
                "entity": ["CO2", "CH4", "N2O"],
            },
        },
        "M.LULUCF": {
            "sources": ["3.B"],
            "sel": {
                "entity": ["CO2", "CH4", "N2O"],
            },
        },
        "M.3.C.1.AG": {
            "sources": ["3.C.1.b", "M.3.C.1.SAV"],
            "sel": {
                "entity": ["CH4", "N2O"],
            },
        },
        "3.C.1": {
            "sources": ["3.C.1.b", "M.3.C.1.SAV"],
            "sel": {
                "entity": ["CH4", "N2O"],
            },
        },
        "M.3.C.AG": {
            "sources": [
                "M.3.C.1.AG",
                "M.3.C.45.AG",
                "3.C.7",
                "M.3.C.23",
            ],
            "sel": {
                "entity": ["CH4", "N2O", "CO2"],
            },
        },
        "3.C": {
            "sources": [
                "M.3.C.1.AG",
                "M.3.C.45.AG",
                "3.C.7",
                "M.3.C.23",
            ],
            "sel": {
                "entity": ["CH4", "N2O", "CO2"],
            },
        },
        "M.AG.ELV": {
            "sources": ["M.3.C.AG"],
            "sel": {
                "entity": ["CH4", "N2O", "CO2"],
            },
        },
        "3": {
            "sources": ["M.AG", "M.LULUCF"],
            "sel": {
                "entity": ["CO2", "CH4", "N2O"],
            },
        },
        "4": {
            "sources": ["4.A", "4.B", "4.C", "4.D", "4.E"],
            "sel": {
                "entity": ["CO2", "CH4", "N2O"],
            },
        },
        "M.0.EL": {
            "sources": ["1", "2", "M.AG", "4"],
        },
        "0": {
            "sources": ["1", "2", "3", "4"],
        },
    },
}

gas_baskets = {
    "FGASES (SARGWP100)": ["PFCS (SARGWP100)"],
    "FGASES (AR4GWP100)": ["PFCS (AR4GWP100)"],
    "FGASES (AR5GWP100)": ["PFCS (AR5GWP100)"],
    "FGASES (AR6GWP100)": ["PFCS (AR6GWP100)"],
    "KYOTOGHG (SARGWP100)": ["CO2", "CH4", "N2O", "PFCS (SARGWP100)"],
    "KYOTOGHG (AR4GWP100)": ["CO2", "CH4", "N2O", "PFCS (AR4GWP100)"],
    "KYOTOGHG (AR5GWP100)": ["CO2", "CH4", "N2O", "PFCS (AR5GWP100)"],
    "KYOTOGHG (AR6GWP100)": ["CO2", "CH4", "N2O", "PFCS (AR6GWP100)"],
}
