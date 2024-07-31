"""
Configuration file to read Mongolia's BUR 2.
"""

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

inv_conf = {
    "entity_row": 0,
    "unit_row": 1,
    "index_cols": "Greenhouse gas source and sink categories",
    "header_long": ["orig_cat_name", "entity", "unit", "time", "data"],
    "cat_code_regexp": r"^(?P<code>[a-zA-Z0-9\.]{1,11})[\s\.].*",
    "cat_codes_manual": {
        # remove whitespace at start of line
        "2.G.2 -SF6 and PFCs from Other Product Uses": "2.G.2 - SF6 and PFCs from Other Product Uses",
        "2.G.3 -N2O from Product Uses": "2.G.3 - N2O from Product Uses",
        "1.C.1 -Transport of CO2": "1.C.1 - Transport of CO2",
        "3.C.1 -Emissions from biomass burning ": "3.C.1",
        "Memo Items (5)": "MEMO",
        "International Bunkers": "M.BK",
        "1.A.3.a.i - International Aviation (International Bunkers) (1)": "M.BK.A",
        "1.A.3.d.i - International water-borne navigation (International bunkers) (1)": "M.BK.M",
        "1.A.5.c - Multilateral Operations (1)(2)": "M.MULTIOP",
        "Total National Emissions and Removals": "0",
    },
    "header": [
        "Greenhouse gas source and sink categories",
        "CO2",
        "CH4",
        "N2O",
        "HFCs",
        "PFCs",
        "SF6",
        "other halogenated gases",
        "Other halogenated gases without CO2 equivalent conversion factors",
        "NOx",
        "CO",
        "NMVOCs",
        "SO2",
    ],
    "unit": [
        "-",
        "Gg",
        "Gg",
        "Gg",
        "GgCO2eq",
        "GgCO2eq",
        "GgCO2eq",
        "GgCO2eq",
        "Gg",
        "Gg",
        "Gg",
        "Gg",
        "Gg",
    ],
}

inv_conf_per_year = {
    "1990": {
        "pages_to_read": ["176", "177", "178", "179"],
        "rows_to_fix": {
            3: [
                "1.A.2 - Manufacturing Industries and",
                "2.B.4 - Caprolactam. Glyoxal and Glyoxylic Acid",
                "2.B.8 - Petrochemical and Carbon Black",
                "2.D - Non-Energy Products from Fuels and",
                "2.F - Product Uses as Substitutes for Ozone",
                "3.C - Aggregate sources and non-CO2 emissions",
                "3.C.4 - Direct N2O Emissions from managed",
                "3.C.5 - Indirect N2O Emissions from managed",
                "3.C.6 - Indirect N2O Emissions from manure",
                "5.A - Indirect N2O emissions from the atmospheric",
                "1.A.3.d.i - International water-borne navigation",
                "1.A.3.a.i - International Aviation (International",
            ],
            -2: ["3.C.1 - Emissions from biomass burning"],
            2: ["3.C.1 -Emissions from biomass burning"],
        },
        "page_defs": {
            "176": {
                "area": ["76,501,763,83"],
                "cols": ["265,320,360,396,433,471,503,564,624,658,694,741"],
            },
            "177": {
                "area": ["68,542,762,85"],
                "cols": ["280,329,374,410,449,482,546,604,637,679,725,751"],
            },
            "178": {
                "area": ["71,543,761,81"],
                "cols": ["265, 320,361,411,447,483,546,604,621,653,719,746"],
            },
            "179": {
                "area": ["70,542,761,346"],
                "cols": ["287,328,365,410,449,482,540,600,636,675,721,750"],
            },
        },
        "skip_rows": 11,
    },
    "2020": {
        "page_defs": {
            "180": {
                "area": ["70,436,769,86"],
                "cols": ["270, 322, 367, 405, 455, 488,550,607,637,669,727,753"],
            },
            "181": {
                "area": ["68,541,768,86"],
                "cols": ["288,343,379,405,460,490,559,600,650,683,729,755"],
            },
            "182": {
                "area": ["69, 539, 771, 86"],
                "cols": ["273,331,371,425,462,491,560,615,639,671,729,755"],
            },
            "183": {
                "area": ["69, 540, 769, 373"],
                "cols": ["288, 328,363,425,459,492,560,619,650,683,731,757"],
            },
        },
        "rows_to_fix": {
            -2: [
                "1.C.1 - Transport of CO2",
                "2.G.2 - SF6 and PFCs from Other Product Uses",
                "2.G.3 - N2O from Product Uses",
            ],
            2: [
                "2.B.8 - Petrochemical and Carbon Black",
                "2.D - Non-Energy Products from Fuels and",
                "2.F - Product Uses as Substitutes for Ozone",
                "3.C - Aggregate sources and non-CO2 emissions",
                "3.C.4 - Direct N2O Emissions from managed",
                "3.C.5 - Indirect N2O Emissions from managed",
                "3.C.6 - Indirect N2O Emissions from manure",
                "5.A - Indirect N2O emissions from the atmospheric",
                "1.A.3.d.i - International water-borne navigation",
                "1.A.3.a.i - International Aviation (International",
                "2.B.4 - Caprolactam. Glyoxal and Glyoxylic Acid",
            ],
        },
        "skip_rows": 0,
    },
}

inv_conf_per_entity = {
    "CO": {
        "page_defs": {
            "39": {
                "area": ["53,646,550,588"],
                "cols": ["279,328,364,400,440,478,520"],
            },
        },
        "cat_codes_manual": {"Total National Emissions": "0"},
        "category_column": "Categories",
        "columns_to_drop": ["Categories"],
        "years": ["1990", "1995", "2000", "2005", "2010", "2015", "2020"],
        "unit": "Gg",
    },
    "NOx": {
        "page_defs": {
            "38": {
                "area": ["53,120,538,93"],
                "cols": ["281,329,365,405,441,477,513"],
            },
            "39": {
                "area": ["51,772,539,740"],
                "cols": ["285,332,368,404,444,476,514"],
            },
        },
        "cat_codes_manual": {"Total National Emissions": "0"},
        "category_column": "Categories",
        "columns_to_drop": ["Categories"],
        "years": ["1990", "1995", "2000", "2005", "2010", "2015", "2020"],
        "unit": "Gg",
    },
    "HFCs": {
        "page_defs": {
            "38": {
                "area": ["55,469,534,364"],
                "cols": ["251,302,367,427,486"],
            },
        },
        "cat_codes_manual": {"Total National Emissions (Gg CO2e)": "0"},
        "category_column": "Categories",
        # 2007 will break gas basket consistency check
        "columns_to_drop": ["Share, %", "Categories", "2007"],
        "years": ["2010", "2015", "2020"],
        "unit": "Gg CO2e",
    },
    "N2O": {
        "page_defs": {
            "37": {
                "area": ["55,106,556,79"],
                "cols": ["170,258,305,347,394,440,476,512"],
            },
            "38": {
                "area": ["55,773,555,664"],
                "cols": ["215,264,306,353,395,439,476,513"],
            },
        },
        "rows_to_fix": {
            3: [
                "3 - Agriculture, Forestry, and Other",
                "3.C - Aggregate sources and non-",
                "4.D - Wastewater Treatment and",
            ]
        },
        "cat_codes_manual": {"Total National Emissions (Gg N2O)": "0"},
        "category_column": "Categories",
        "columns_to_drop": ["Share, %", "Categories"],
        "years": ["1990", "1995", "2000", "2005", "2010", "2015", "2020"],
        "unit": "Gg",
    },
    "CH4": {
        "page_defs": {
            "37": {
                "area": ["55,423,552,216"],
                "cols": ["186,250,296,326,383,427,467,507"],
            },
        },
        "rows_to_fix": {
            3: [
                "1.A - Fuel Combustion",
                "1.B - Fugitive emissions from",
                "3 - Agriculture, Forestry, and",
                "3.C - Aggregate sources and",
                "4.D - Wastewater Treatment",
                "Total National Emissions (Gg",
            ]
        },
        "cat_codes_manual": {"Total National Emissions (Gg CH4)": "0"},
        "category_column": "Categories",
        "columns_to_drop": ["Share, %", "Categories"],
        "years": ["1990", "1995", "2000", "2005", "2010", "2015", "2020"],
        "unit": "Gg",
        "del_value": [("1995", "4"), ("2005", "4")],
    },
    "CO2": {
        "page_defs": {
            "36": {
                "area": ["53,147,556,79"],
                "cols": ["150,204,254,306,352,406,459,513"],
            },
            "37": {
                "area": ["51,772,561,515"],
                "cols": ["151,202,252,305,357,404,463,517"],
            },
        },
        "rows_to_fix": {
            2: [
                "Categories",
                "Emissions and",
            ],
            3: [
                "1.A - Fuel",
                "1.B - Fugitive",
                "2 - Industrial Processes",
                "3 - Agriculture,",
                "Total National",
                "Total National",
            ],
            5: ["2.D - Non-Energy"],
            -2: [
                "Categories",
                "Emissions and Removals (Gg CO2)",
            ],
        },
        "rows_to_drop": [
            "Total National Emissions (Gg CO2)",
            "Total National Removals (Gg CO2)",
        ],
        "columns_to_drop": ["Share, %", "Categories"],
        "cat_codes_manual": {"Total National Emissions and Removals (Gg CO2)": "0"},
        "category_column": "Categories",
        "years": ["1990", "1995", "2000", "2005", "2010", "2015", "2020"],
        "unit": "Gg",
    },
}

inv_conf_harvested_wood_products = {
    "page": "151",
    "category_column": "Categories",
    "cat_codes_manual": {
        "GHG emission": "3.D.1",
    },
    "unit": "Gg",
    "entity": "CO2",
    # Table consists of three stacked parts
    "parts": {
        "part_1": {
            "page_defs": {
                "area": ["52,690,555,647"],
                "cols": ["101,149,196,231,268,310,351,398,433,476,514"],
            },
            "rows_to_fix": {
                3: [
                    "GHG",
                ],
            },
        },
        "part_2": {
            "page_defs": {
                "area": ["52,637,555,596"],
                "cols": ["99,150,197,239,281,326,372,425,469,516"],
            },
            "rows_to_fix": {
                3: [
                    "GHG",
                ],
            },
        },
        "part_3": {
            "page_defs": {
                "area": ["52,591,550,547"],
                "cols": ["106,156,197,239,281,326,372,420,465,509"],
            },
            "rows_to_fix": {
                3: [
                    "GHG",
                ],
            },
        },
    },
}

inv_conf_per_sector = {
    "total": {
        "page_defs": {
            "32": {
                "area": ["64,649,547,106"],
                "cols": ["106,182,237,294,345,403,480"],
            },
        },
        "entity": "KYOTOGHG (SARGWP100)",
        "unit": "Gg CO2e",
        "last_year": "2020",
        "rows_to_fix": {
            -3: [
                "Year",
            ],
        },
        "year_column": "Year",
        "cat_codes_manual": {
            "Energy": "1",
            "IPPU": "2",
            "Agriculture": "M.AG",
            "Waste": "4",
            "LULUCF": "M.LULUCF",
            "Total (excl. LULUCF)": "M.0.EL",
            "Total (incl. LULUCF)": "0",
        },
    },
    "energy": {
        "page_defs": {
            "43": {
                "area": ["59,478,544,79"],
                "cols": ["97,160,220,262,338,388,452,502"],
            },
            "44": {
                "area": ["60,773,546,582"],
                "cols": ["103,165,226,274,329,384,444,494"],
            },
        },
        "entity": "KYOTOGHG (SARGWP100)",
        "unit": "Gg CO2e",
        "last_year": "2020",
        "rows_to_fix": {
            11: [
                "Years",
            ],
        },
        "rows_to_drop": [0, 2],
        "year_column": "Years",
        "cat_codes_manual": {
            "1.A.1.a.i Electricity  generation": "1.A.1.a.i",
            "1.A.1.a.ii  Combined  heat and ipower peneration (CHP)": "1.A.1.a.ii",
            "1.A.1.c.ii  Other  energy ndustries": "1.A.1.c.ii",
            "Manufacturing industries and  construction": "1.A.2",
            "1.A.3.a 1 Civil  aviation t": "1.A.3.a",
            ".A.3.b Road  ransportation": "1.A.3.b",
            "1.A.3.c Railways": "1.A.3.c",
            "1.A.3.e.ii  Off-road": "1.A.3.e.ii",
        },
    },
    "energy cont": {
        "page_defs": {
            "44": {
                "area": ["59,552,553,84"],
                "cols": ["103,173,219,274,330,382,443,494"],
            },
        },
        "entity": "KYOTOGHG (SARGWP100)",
        "unit": "Gg CO2e",
        "last_year": "2020",
        "rows_to_fix": {
            8: [
                "Years",
            ],
        },
        "rows_to_drop": [0, 2],
        "year_column": "Years",
        "cat_codes_manual": {
            "Other sectors 1.A.4.a Commercial/ Institutional": "1.A.4.a",
            "1.A.4.b Residen-tial": "1.A.4.b",
            "1.A.4.c.i Agriculture -Stationary": "1.A.4.c.i",
            "1.A.4.c.ii Agriculture -Off-road vehicles and other machinery": "1.A.4.c.ii",
            "Non-specified 1.A.5.a Stationary": "1.A.5.a",
            "Fugitive emis 1.B.1.a Coal mining & handling (surface mining)": "1.B.1.a",
            "sions from fu 1.B.2.a.ii Oil -Flaring": "1.B.2.a.ii",
            "els 1.B.2.a.iii.2 Oil production and upgrading": "1.B.2.a.iii",
        },
    },
    "ippu": {
        "page_defs": {
            "74": {
                "area": ["68,701,544,313"],
                "cols": ["97,188,261,358,462"],
            },
        },
        "entity": "KYOTOGHG (SARGWP100)",
        "unit": "Gg CO2e",
        "last_year": "2020",
        "rows_to_fix": {
            3: [
                "Year",
            ],
        },
        "year_column": "Year",
        "cat_codes_manual": {
            "2.A-Mineral industry": "2.A",
            "2.C-Metal industry": "2.C",
            "2.D-Non-energy products from fuels and solvent use": "2.D",
            "2.F-Product uses as substitutes for ozone depleting substances": "2.F",
            "2. IPPU Total": "2",
        },
        "remove_duplicates": ["2"],
    },
    "livestock": {
        "page_defs": {
            "103": {
                "area": ["62,480,544,82"],
                "cols": ["97,182,259,326,403,474"],
            },
        },
        "unit": "Gg CO2e",
        "last_year": "2020",
        "rows_to_fix": {
            3: [
                "Year",
            ],
        },
        "rows_to_drop": [0, 1],
        "year_column": "Year",
        "cat_codes_manual": {
            "Fermentation Gg": "3.A.1",
            "Management CH4": "3.A.2",
            "(Total CH4)": "3.A",
            "Fermentation Gg C": "3.A.1",
            "Management O2e": "3.A.2",
            "(Gg CO2e)": "3.A",
        },
        "multi_entity": {
            "unit": ["Gg", "Gg", "Gg", "Gg CO2e", "Gg CO2e", "Gg CO2e"],
            "entity": [
                "CH4",
                "CH4",
                "CH4",
                "KYOTOGHG (SARGWP100)",
                "KYOTOGHG (SARGWP100)",
                "KYOTOGHG (SARGWP100)",
            ],
        },
    },
    "biomass_burning": {
        "page_defs": {
            "114": {
                "area": ["70,214,544,78"],
                "cols": ["116,185,239,304,365,426,491"],
            },
            "115": {
                "area": ["72,777,545,505"],
                "cols": ["123,190,250,313,374,438,495"],
            },
        },
        "last_year": "2020",
        "col_to_use": 5,
        "rows_to_fix": {
            7: [
                "3.C.1 - Emiss",
            ],
        },
        "year_column": "Year",
        # TODO: These categories are technically duplicate, just with a different unit
        "categories_to_drop": [
            "3.C.1 -Emiss  CH4 (Gg CO2e)",
            "ions from bioma (CO2e) N2O (Gg CO2e)",
            "ss burning  Total (Gg CO2e)",
        ],
        "cat_codes_manual": {
            "3.C.1  CH4 (Gg)": "3.C.1",
            "-Emissions fr  N2O (Gg)": "3.C.1",
            "om biomass bur  NOx (Gg)": "3.C.1",
            "ning  CO(Gg)": "3.C.1",
        },
        "multi_entity": {
            "unit": ["Gg", "Gg", "Gg", "Gg"],
            "entity": [
                "CH4",
                "N2O",
                "NOx",
                "CO",
            ],
        },
    },
    "managed_soils_direct": {
        "page_defs": {
            "119": {
                "area": ["70,600,541,173"],
                "cols": ["114,191,245,328,400,476"],
            },
        },
        "last_year": "2020",
        "col_to_use": 3,
        "rows_to_fix": {
            10: [
                "Urine and dung",
            ],
        },
        "year_column": "Year",
        # # TODO: technically duplicate, just with a different unit
        "categories_to_drop": [
            "3.C.4 -Direct N2O Emissions from managed soils (CO2e) Gg CO2e",
            "Inorganic N fertilizer application  N2O (Gg)",
            "Organic N applied as fertilizer (manure) N2O (Gg)",
            "Urine and dung N deposited on pasture, range and paddock by grazing animals N2O (Gg)",
            "N in crop residues  N2O (Gg)",
        ],
        "cat_codes_manual": {
            # TODO the next 4 categories are made up placeholders
            # "Inorganic N fertilizer application  N2O (Gg)": "3.C.4.i",
            # "Organic N applied as fertilizer (manure) N2O (Gg)": "3.C.4.ii",
            # "Urine and dung N deposited on pasture, range and paddock by grazing animals N2O (Gg)": "3.C.4.iii",
            # "N in crop residues  N2O (Gg)": "3.C.4.iiii",
            "3.C.4 -Direct N2O Emissions from managed soils N2O (Gg)": "3.C.4",
        },
        "entity": "N2O",
        "unit": "Gg",
        # "multi_entity": {
        #     "unit": ["Gg", "Gg", "Gg", "Gg", "Gg"],
        #     "entity": [
        #         "N2O",
        #         "N2O",
        #         "N2O",
        #         "N2O",
        #         "N2O",
        #     ],
        # },
    },
    "managed_soils_indirect": {
        "page_defs": {
            "125": {
                "area": ["74,214,539,83"],
                "cols": ["125,222,309,423"],
            },
            "126": {
                "area": ["72,775,539,369"],
                "cols": ["148,248,351,459"],
            },
        },
        "last_year": "2020",
        "col_to_use": 3,
        "rows_to_fix": {
            7: [
                "3.C.5 - Indirect N2O",
            ],
        },
        "year_column": "Year",
        # # TODO: technically duplicate, just with a different unit
        "categories_to_drop": [
            "3.C.5 -Indirect N2O emissions from managed  soils Gg CO2e",
            "Volatilization  pathway Gg N2O",
            "Leaching/runoff  pathway Gg N2O",
        ],
        "cat_codes_manual": {
            # TODO the next 2 categories are made up placeholders
            # "Volatilization  pathway Gg N2O": "3.C.5.i",
            # "Leaching/runoff  pathway Gg N2O": "3.C.5.ii",
            "3.C.5 -Indirect N2O emissions from managed  soils Gg N2O": "3.C.5",
        },
        "entity": "N2O",
        "unit": "Gg",
    },
    "bio_waste": {
        "page_defs": {
            "157": {
                "area": ["68,748,541,228"],
                "cols": ["108,176,222,283,332,387,429"],
            },
        },
        "last_year": "2020",
        "rows_to_fix": {
            2: [
                "Year",
            ],
        },
        "year_column": "Year",
        # # TODO: technically duplicate, just with a different unit
        "categories_to_drop": [
            "Total emissions from SWDS Gg CO2e",
            "Food",
            "Garden",
            "Paper Gg CH4",
            "Wood",
            "Textile",
        ],
        "cat_codes_manual": {
            # TODO the categories are made up placeholders
            # "Food": "4.A.1.food",
            # "Garden": "4.A.1.garden",
            # "Paper Gg CH4": "4.A.1.paper",
            # "Wood": "4.A.1.wood",
            # "Textile": "4.A.1.textile",
            "Total": "4.A.1.",
        },
        "entity": "CH4 ",
        "unit": "Gg",
    },
    "wastewater": {
        "page_defs": {
            "161": {
                "area": ["60,480,541,85"],
                "cols": ["98,165,226,281,340,408,465"],
            },
            "162": {
                "area": ["62,775,541,613"],
                "cols": ["110,176,229,288,349,414,486"],
            },
        },
        "last_year": "2020",
        "col_to_use": 7,
        "rows_to_fix": {
            10: [
                "Wastewater",
            ],
        },
        "year_column": "Year",
        # # TODO: technically duplicate, just with a different unit
        "categories_to_drop": [
            "Domestic wastewater  CH4 emissions",
            "Domestic wastewater  N2O emissions (Gg C",
            "Industrial wastewater  CH4 emissions O2 e)",
            "Wastewater treatment and discharge  Total emissions",
        ],
        "cat_codes_manual": {
            "Domestic wastewater  CH4 emissions (Gg CH4)": "4.D.1",
            "Domestic wastewater  N2O emissions (Gg N2O)": "4.D.1",
            "Industrial wastewater  CH4 emissions (Gg CH4)": "4.D.2",
        },
        "multi_entity": {
            "unit": ["Gg", "Gg", "Gg"],
            "entity": [
                "CH4",
                "N2O",
                "CH4",
            ],
        },
    },
}

# primap2 format conversion
coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

coords_defaults = {
    "source": "MNG-GHG-Inventory",
    "provenance": "measured",
    "area": "MNG",
    "scenario": "BUR2",
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

gwp_to_use = "SARGWP100"
coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        "HFCs": f"HFCS ({gwp_to_use})",
        "PFCs": f"PFCS ({gwp_to_use})",
        "SF6": f"SF6 ({gwp_to_use})",
        "other halogenated gases": f"other halogenated gases ({gwp_to_use})",
        "NMVOCs": "NMVOC",
    },
}

filter_remove = {
    "f_memo": {"category": "MEMO"},
    "f_empty": {"category": ""},
    "f2": {
        "entity": ["Other halogenated gases without CO2 equivalent conversion factors"],
    },
}

meta_data = {
    "references": "https://unfccc.int/documents/633382",
    "rights": "",  # unknown
    "contact": "daniel-busch@climate-resource.de",
    "title": "Mongolia. Biennial update report (BUR). BUR2",
    "comment": "Read fom pdf by Daniel Busch",
    "institution": "UNFCCC",
}

country_processing_step1 = {
    "tolerance": 0.01,
    "aggregate_cats": {
        "M.3.D.AG": {"sources": ["3.D.2"]},
        "M.3.C.AG": {
            "sources": ["3.C.1", "3.C.4", "3.C.5"],
        },
        "M.AG.ELV": {
            "sources": ["M.3.C.AG", "M.3.D.AG"],
        },
        # "3.A" : {"sources" : ["3.A.1", "3.A.2"]},
        # "3.C" : {"sources" : ["3.C.1",
        #                       "3.C.2",
        #                       "3.C.3",
        #                       "3.C.4",
        #                       "3.C.5",
        #                       "3.C.6",
        #                       "3.C.7",
        #                       "3.C.8", ]},
        # "3.D" : {"sources" : ["3.D.1", "3.D.2"]},
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
        "GWPs_to_add": ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
        "entities": ["HFCS", "PFCS"],
        "source_GWP": gwp_to_use,
    },
    "downscale": {
        "sectors": {
            "1.B_CH4": {
                "basket": "1.B",
                "basket_contents": ["1.B.1", "1.B.2"],
                "entities": ["CH4"],
                "dim": f"category ({coords_terminologies['category']})",
                # "tolerance": 0.05,  # some inconsistencies (rounding?)
            },
            "1.B_CO2": {
                "basket": "1.B",
                "basket_contents": ["1.B.1", "1.B.2"],
                "entities": ["CO2"],
                "dim": f"category ({coords_terminologies['category']})",
                "sel": {
                    "time": [
                        "2000",
                        "2005",
                        "2010",
                        "2015",
                        "2020",
                    ]
                },
            },
        }
    },
}

country_processing_gas_baskets = {"tolerance": 0.02}

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
