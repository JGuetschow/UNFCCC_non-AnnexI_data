"""Config for China BUR3 and NC4

Configuration for reading the China's NC4 and BUR3 from pdf.
Full configuration is contained here including configuraton for conversions to
primap2 data format.

NOTE: GWPs are a mixture of AR4 and SAR values (SAR except for HFC-245fa and HFC-365mfc)
Thus the Kyoto GHG gas basket is not fully consistent with SAR GWPs and is
re-generated for the processed version of the data.
"""

## general config
gwp_to_use = "SARGWP100"  # see note above

coords_value_mapping = {
    "entity": {
        "CF4": "CF4",
        "CH4": "CH4",
        "CO2": "CO2",
        "HFC-125": "HFC125",
        "HFC-134a": "HFC134a",
        "HFC-143a": "HFC143a",
        "HFC-227ea": "HFC227ea",
        "HFC-23": "HFC23",
        "HFC-236fa": "HFC236fa",
        "HFC-245fa": "HFC245fa",
        "HFC-32": "HFC32",
        "HFC-365mfc": "HFC365MFC",
        "HFCs": f"HFCS ({gwp_to_use})",
        "HFCs HFC-134a": "HFC134a",
        "HFCs HFC-152a": "HFC152a",
        "N2O": "N2O",
        "PFCs": f"PFCS ({gwp_to_use})",
        "PFCs C2F6": "C2F6",
        "SF6": "SF6",
        "Total": f"KYOTOGHG ({gwp_to_use})",
        "合计": f"KYOTOGHG ({gwp_to_use})",
    },
    "category": {
        "1. Energy": "1",
        "2. Industrial Processes": "2",
        "2. Industrial processes": "2",
        "3. Agriculture": "3",
        "4. LULUCF": "4",
        "4. Land-use change and forestry (LUCF)": "4",
        "5. Waste": "4",
        "6. Memo Items": "IGNORE",
        "6. Memo items": "IGNORE",
        "Agricultural land": "4.B",
        "Agricultural soils": "3.D",
        "Agriculture": "3",
        "Biological treatment": "M.5.A.BIO",  #  HKG, 2006category 4.B
        "Biomass combustion": "M.BIO",
        "CO2 emissions from biomass": "M.BIO",
        "Cement production": "2.A.1",  # sum to 2.A, HKG
        "Changes in forest and other woody biomass stocks": "4.A.1",  # sum for HKG
        "Chemical industry": "2.B",
        "Consumption of halocarbons and SF6": "2.F",
        "Cropland": "4.B",
        "Energy": "1",
        "Energy industries": "1.A.1",
        "Energy industry": "1.A.1",
        "Enteric fermentation": "3.A",
        "Field burning of agricultural residues": "3.F",
        "Forest conversion": "M.DEF",
        "Forest land": "4.A",
        "Fuel combustion": "1.A",
        "Fugitive emission": "1.B",
        "Fugitive emissions": "1.B",
        "Grassland": "4.C",
        "Harvested wood products": "4.G.1",
        "Incineration": "5.C",
        "Industrial Processes": "2",
        "Industrial processes": "2",
        "International aviation": "M.1.A",
        "International marine": "M.1.B",
        "International navigation": "M.1.B",
        "LUCF": "4",
        "LULUCF": "4",
        "Land-UseChangeand Forestry (LUCF)": "4",
        "Landfill": "5.A",
        "Manufacturing and construction industries": "1.A.2",
        "Manufacturing industries and construction": "1.A.2",
        "Manure management": "3.B",
        "Memo Items": "IGNORE",
        "Metal industry": "2.C",
        "Metal production": "2.C",
        "Mineral industry": "2.A",
        "Mineral products": "2.A",
        "Non-energy products from fuels and solvent use": "2.D",  # mixture of 1996 and 2006 categories
        "Oil and natural gas": "1.B.2",
        "Oil and natural gas system": "1.B.2",
        "Other factors": "1.A.4",
        "Other land": "4.F",
        "Other sectors": "1.A.4",
        "Prescribed burning of savannas": "3.E",
        "Production of halocarbons and SF6": "2.E",
        "Rice cultivation": "3.C",
        "Settlements": "4.E",
        "Solid fuel": "1.B.1",
        "Solid fuels": "1.B.1",
        "Solid waste disposal": "5.A",
        "Special regional aviation": "M.SR.A",  # MAC only
        "Special regional marine": "M.SR.M",  # MAC only
        "Total": "0",
        "Total (with LUCF)": "0",
        "Total (with LULUCF)": "0",
        "Total (without LUCF)": "M.0.EL",
        "Total (without LULUCF)": "M.0.EL",
        "Total emissions": "0",
        "Transport": "1.A.3",
        "Waste": "5",
        "Wastewater handling": "5.B",
        "Wastewater treatment": "5.B",
        "Wetlands": "4.D",
    },
}


catgory_conversion = {
    "mapping": {
        "0": "0",
        "1": "1",
        "1.A": "1.A",
        "1.A.1": "1.A.1",
        "1.A.2": "1.A.2",
        "1.A.3": "1.A.3",
        "1.A.4": "1.A.4",
        "1.B": "1.B",
        "1.B.1": "1.B.1",
        "1.B.2": "1.B.2",
        "2": "2",
        "2.A": "2.A",
        "2.A.1": "2.A.1",
        "2.B": "2.B",
        "2.C": "2.C",
        "2.D": "2.D",
        "2.E": "2.B.9",
        "2.F": "2.F",
        "3": "M.AG",
        "3.A": "3.A.1",
        "3.B": "3.A.2",
        "3.C": "3.C.7",
        "3.D": "M.3.AS",
        "3.E": "3.C.1.c",
        "3.F": "3.C.1.b",
        "4": "M.LULUCF",
        "4.A": "3.B.1",
        "4.A.1": "3.B.1.a",
        "4.B": "3.B.2",
        "4.C": "3.B.3",
        "4.D": "3.B.4",
        "4.E": "3.B.5",
        "4.F": "3.B.6",
        "4.G.1": "3.D.1",
        "5": "4",
        "5.A": "4.A",
        "5.B": "4.D",
        "5.C": "4.C",
        "M.0.EL": "M.0.EL",
        "M.1.A": "M.BK.A",
        "M.1.B": "M.BK.B",
        "M.5.A.BIO": "4.B",
        "M.BIO": "M.BIO",
        #'M.DEF': '', #
        #'M.SR.A': '',
        #'M.SR.M': '',
    },
    "aggregate": {"category": {}},
}

## NC4 specific config
config_nc4 = {
    "scenario": "NC4",
    "table_groups": {
        "overview": {
            "pages": {
                "CHN": [30],
                "MAC": [218],
                "HKG": [190],
            },
            "year": 2017,
            "unit": "kt / year",
        },
        "inventory": {
            "pages": {
                "CHN": [31, 32],
                "MAC": [219],
                "HKG": [191],
            },
            "year": 2017,
            "unit": "kt / year",
        },
        "fgas": {
            "pages": {
                "CHN": [33],
                "MAC": [],
                "HKG": [192],
            },
            "year": 2017,
            "unit": "kt / year",
        },
    },
    "page_defs": {
        "30": {  # CHN overview 2017
            "table_areas": ["77,756,520,582"],
            "split_text": True,
            "flavor": "stream",
        },
        "31": {  # CHN detail 2017
            "table_areas": ["73,451,518,74"],
            "columns": ["294,383,470"],
            "split_text": True,
            "flavor": "stream",
        },
        "32": {  # CHN detail 2017
            "table_areas": ["73,777,518,563"],
            "columns": ["290,379,468"],
            "split_text": True,
            "flavor": "stream",
        },
        "33": {  # CHN f-gases 2017
            "table_areas": ["74,508,766,235"],
            "columns": ["152,198,241,289,342,393,448,505,560,620,682,707,737"],
            "split_text": False,
            "flavor": "stream",
            "row_tol": 10,
            "rows_to_fix": {
                2: ["Industrial", "- Chemical"],
                3: ["- Consumption"],
                4: ["- Non-energy"],
            },
        },
        "190": {  # HKG overview 2017
            "table_areas": ["50,427,546,268"],
            "split_text": True,
            "flavor": "stream",
        },
        "191": {  # HKG detail 2017
            "table_areas": ["73,754,520,178"],
            "split_text": True,
            "flavor": "stream",
        },
        "192": {  # HKG f-gases 2017
            "table_areas": ["74,756,517,472"],
            "columns": ["181,237,282,332,384,440,480"],
            "split_text": True,
            "flavor": "stream",
            "rows_to_fix": {
                2: ["GHG source"],
            },
        },
        "218": {  # MAC overview 2017
            "table_areas": ["73,501,489,341"],
            "split_text": True,
            "flavor": "stream",
        },
        "219": {  # MAC detail 2017
            "table_areas": ["73,754,520,339"],
            "columns": ["291,393,458"],
            "split_text": True,
            "flavor": "stream",
        },
    },
}

## BUR3 specific config
config_bur3 = {
    "scenario": "BUR3",
    "table_groups": {
        "overview": {
            "pages": {
                "CHN": [11],
                "MAC": [63],
                "HKG": [43],
            },
            "year": 2018,
            "unit": "kt / year",
        },
        "inventory": {
            "pages": {
                "CHN": [13, 14],
                "MAC": [64],
                "HKG": [44],
            },
            "year": 2018,
            "unit": "kt / year",
        },
        "fgas": {
            "pages": {
                "CHN": [15],
                # "MAC": [],
                "HKG": [45],
            },
            "year": 2017,
            "unit": "kt / year",
        },
        "recalc": {
            "pages": {
                "CHN": [18],
                "MAC": [67],
                "HKG": [50],
            },
            "year": 2005,
            "unit": "kt / year",
        },
    },
    "page_def": {
        "11": {  # CHN overview 2018
            "table_areas": ["67,584,525,482"],
            "split_text": True,
            "flavor": "stream",
        },
        "13": {  # CHN detail 2018
            "table_areas": ["71,565,523,76"],
            "columns": ["325,389,453"],
            "split_text": False,
            "flavor": "stream",
            "row_tol": 10,
        },
        "14": {  # CHN detail 2018
            "table_areas": ["69,771,526,526"],
            "columns": ["331,388,453"],
            "split_text": False,
            "flavor": "stream",
        },
        "15": {  # CHN fgases 2018
            "table_areas": ["62,493,778,226"],
            "columns": ["133,180,226,276,334,384,442,502,560,620,687,712,752"],
            "split_text": False,
            "flavor": "stream",
            "row_tol": 10,
            "rows_to_fix": {
                2: ["Sources", "2. Industrial", "⎯ Mineral", "⎯ Chemical", "⎯ Metal"],
                3: ["⎯ Consumption"],
                4: ["⎯ Non-energy"],
            },
        },
        "18": {  # CHN overview 2005
            "table_areas": ["84,615,507,503"],
            "split_text": False,
            "flavor": "stream",
        },
        "43": {  # HKG overview 2018
            "table_areas": ["86,319,501,220"],
            "split_text": False,
            "flavor": "stream",
        },
        "44": {  # HKG detail 2018
            "table_areas": ["83,743,508,171"],
            "split_text": False,
            "flavor": "stream",
        },
        "45": {  # HKG f-gases 2018
            "table_areas": ["83,752,508,495"],
            "split_text": False,
            "flavor": "stream",
            "row_tol": 10,
            "rows_to_fix": {
                3: ["GHG source and sink"],
            },
        },
        "50": {  # HGK overview 2005
            "table_areas": ["84,753,499,651"],
            "split_text": False,
            "flavor": "stream",
        },
        "63": {  # MAC overview 2018
            "table_areas": ["67,336,514,168"],
            "columns": ["198,231,275,316,366,408,447"],
            "split_text": False,
            "flavor": "stream",
            "row_tol": 10,
            "strip_text": ".\n",
            "rows_to_fix": {
                2: ["Land-UseChangeand"],
            },
        },
        "64": {  # MAC detail 2018
            "table_areas": ["66,754,526,387"],
            "columns": ["308,389,458"],
            "split_text": False,
            "flavor": "stream",
        },
        "67": {  # MAC overview 2005
            "table_areas": ["65,549,520,438"],
            "split_text": False,
            "flavor": "stream",
        },
    },
}
